#!/usr/bin/env python3
import argparse
import datetime
import dotenv
import json
import logging
import os.path
import pytz
import requests
import sys

FORMAT = "%(asctime)-15s %(levelname)7s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(os.path.splitext(os.path.split(__file__)[-1])[0])
logger.setLevel(logging.INFO)


def convert_single_solve(solve, newer_than):
    fi_tz = pytz.timezone(os.getenv("SOLVE_TIMEZONE"))
    solve_date_time = fi_tz.localize(datetime.datetime.fromtimestamp(solve[3]))
    solve_object = {
        "modifier": solve[0][0],
        "duration": solve[0][1],
        "scramble": '"{}"'.format(solve[1]),
        "comment": '"{}"'.format(solve[2]),
        "solve_date_time": solve_date_time.isoformat().split("+")[0],
    }
    if newer_than and solve_date_time <= newer_than:
        return
    doc_id = "{}@{:07}".format(solve_object["solve_date_time"], solve_object["duration"])
    solve_object["duration"] /= 1000
    r = requests.put(
        "{}/{}/_create/{}".format(os.getenv("ELASTICSEARCH_HOST"), os.getenv("INDEX_NAME"), doc_id), json=solve_object
    )
    if r.status_code >= 400:
        try:
            payload = r.json()
            logger.info("{}".format(payload["error"]["reason"]))
        except:
            logger.error("[{}] Failed due to '{}'".format(doc_id, r.json()))
    elif r.status_code >= 200 and r.status_code < 300:
        logger.info("[{}] Stored successfully.".format(r.json()["_id"]))
    else:
        logger.error("[{}] Unexpected result: status code = {}, result = {}".format(doc_id, r.status_code, r.json()))


def convert_solves(cstimer_export, newer_than):
    with open(cstimer_export, "r") as input_file:
        payload = json.load(input_file)
        for key in payload.keys():
            if key.startswith("session"):
                solves = payload[key]
                if len(solves) > 0:
                    for solve in solves:
                        convert_single_solve(solve, newer_than)


if __name__ == "__main__":
    dotenv.load_dotenv(verbose=True)
    parser = argparse.ArgumentParser(
        description="A CSTimer data importer to Elasticsearch. Set up ELASTICSEARCH_HOST environment variable prior running."
    )
    parser.add_argument(
        "-t",
        "--newer-than",
        metavar="date-time",
        type=str,
        help="process only solves newer than the given ISO-8601 date & time",
    )
    parser.add_argument("cstimer_export", metavar="FILE", type=str, nargs="+", help="the file to process")
    args = parser.parse_args()
    # Create an index to elasticsearch.
    r = requests.put("{}/{}".format(os.getenv("ELASTICSEARCH_HOST"), os.getenv("INDEX_NAME")))
    if r.status_code >= 400:
        try:
            payload = r.json()
            logger.info("{}".format(payload["error"]["reason"]))
        except:
            logger.error("... Failed due to '{}'".format(r.json()))
    elif r.status_code >= 200 and r.status_code < 300:
        logger.info("Index created with result {}".format(r.json()))
    else:
        logger.error("... Unexpected result: status code = {}, result = {}".format(r.status_code, r.json()))
    fi_tz = pytz.timezone(os.getenv("SOLVE_TIMEZONE"))
    for cstimer_export in args.cstimer_export:
        if args.newer_than:
            newer_than = fi_tz.localize(datetime.datetime.fromisoformat(args.newer_than))
        else:
            newer_than = None
        convert_solves(cstimer_export, newer_than)
