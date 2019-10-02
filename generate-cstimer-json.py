#!/usr/bin/env python3
import csv
import datetime
import json

if __name__ == "__main__":
    result = {"session1": []}
    with open("chaotimer.csv", "r") as chaotimes:
        rows = csv.DictReader(chaotimes)
        for row in rows:
            solve_date_time = datetime.datetime.fromisoformat(row["solve_date_time"])
            best_time = datetime.time.fromisoformat(row["best_time"])
            average = datetime.time.fromisoformat(row["average"])
            try:
                worst_time = datetime.time.fromisoformat(row["worst_time"])
                generated = ""
                td = datetime.timedelta(
                    hours=worst_time.hour,
                    minutes=worst_time.minute,
                    seconds=worst_time.second,
                    microseconds=worst_time.microsecond,
                )
                worst_time = td
            except:
                generated = "Imported from Chaotimer. Duration is generated."
                td = datetime.timedelta(
                    hours=average.hour, minutes=average.minute, seconds=average.second, microseconds=average.microsecond
                )
                worst_time = 2 * td
                td = datetime.timedelta(
                    hours=best_time.hour,
                    minutes=best_time.minute,
                    seconds=best_time.second,
                    microseconds=best_time.microsecond,
                )
                worst_time -= td
            td = datetime.timedelta(
                hours=best_time.hour,
                minutes=best_time.minute,
                seconds=best_time.second,
                microseconds=best_time.microsecond,
            )
            best_time = int(1000 * td.total_seconds())
            scramble_na = "Scramble is not known."
            result["session1"].append([[0, best_time], scramble_na, "", int(solve_date_time.timestamp())])
            worst_time = int(1000 * worst_time.total_seconds())
            result["session1"].append(
                [[0, worst_time], scramble_na, generated, int(solve_date_time.replace(minute=1).timestamp())]
            )
    print(json.dumps(result))
    # [0, 132550], "L' F2 R B2 U2 F2 D2 F2 R' D2 L R2 U' R' F' D2 L D' U2 L2 U2", "", 1568037867
