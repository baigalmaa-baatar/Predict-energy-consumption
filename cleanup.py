import os
import sys
import json
import datetime as dt

def to_csv(zip_code, hourly_data):
    date = dt.datetime.fromtimestamp(hourly_data["time"] + 8 * 3600) # 8 * 3600 is a cheap hack to solve TZ
    columns = [
        zip_code,
        date.strftime("%Y-%m-%d %H:%M:%S"),
    ]

    for header in headers[2:]:
        columns.append(str(hourly_data[header] if header in hourly_data else 0))

    return ",".join(columns)

headers = [
    "zip_code",
    "time",
    "temperature",
    "apparentTemperature",
    "precipIntensity",
    "precipProbability",
    "dewPoint",
    "humidity",
    "pressure",
    "windSpeed",
    "windGust",
    "windBearing",
    "uvIndex",
    "cloudCover",
    "visibility",
]
print("\t".join(headers))

zip_codes = next(os.walk('../../Documents/0 Final project'))[1]

for zip_code in zip_codes:
    file_names = os.listdir(zip_code)
    file_names = filter(lambda f: f.endswith(".txt"), file_names)
    file_names.sort()

    if len(file_names) < 1096:
        # folder is not ready, we will skip
        sys.stderr.write("skipping {}, because it's not ready\n".format(zip_code))
        sys.stderr.flush()

        continue

    for file_name in file_names:
        file_name = "{}/{}".format(zip_code, file_name)

        with open(file_name, "r") as f:
            lines = f.read().split("\n")
            lines = map(lambda line: line.strip(), lines)
            try:
                data = json.loads(filter(lambda line: line.startswith("var hours = "), lines)[0][12:-1])
            except:
                sys.stderr.write("error on {}\n".format(file_name))
                sys.stderr.flush()

            for hourly_data in data:
                print(to_csv(zip_code, hourly_data))
                hourly_data["time"] += 1800 # a hack to create 30 minutes of data
                print(to_csv(zip_code, hourly_data))
