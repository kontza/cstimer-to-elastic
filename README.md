# Introduction
This Python script converts cstimer.net's session JSON output into format that can be imported into Elasticsearch.

Input is of the form:
```
"session1": [
    [
        [0, 69256], "D F' U R L2 F' D' L F D2 L2 D2 F U2 B L2 U2 L2 D2 F2 R", "", 1568037867
    ],
    ...
```

Converted output is of the form:
```
{
    "_id": "2019-09-09T14:04:27@0069256",
    "modifier": 0,
    "duration": 69.256,
    "scramble": "\"D F' U R L2 F' D' L F D2 L2 D2 F U2 B L2 U2 L2 D2 F2 R\"",
    "comment": "\"\"",
    "solve_date_time": "2019-09-09T14:04:27"
}
```

# Environment
Setup a `.env` file with the following properties:

Variable name       | Description
--------------------|-----------------
ELASTICSEARCH_HOST  | The URL of your Elasticsearch instance (a Bonsai.io authorized URL).
INDEX_NAME          | The name of the index in Elasticsearch where to push solve data.
SOLVE_TIMEZONE      | Your current timezone, e.g. 'Europe/London'.
