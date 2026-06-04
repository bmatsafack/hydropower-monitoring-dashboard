#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import socket
import time
import pandas as pd
from datetime import datetime

channel_id = 3375067
read_key = "ZYIZ9MMDKAQV7Q39"

labview_host = "10.211.55.9"

labview_ports = {
    1: 71,  # isa
    2: 72,  # isb
    3: 73,  # isc
    4: 74,  # va
    5: 94,  # vb
    6: 93,  # vc
    7: 92,  # pm
    8: 91,  # wm
}

field_names = {
    1: "isa",
    2: "isb",
    3: "isc",
    4: "va",
    5: "vb",
    6: "vc",
    7: "pm",
    8: "wm",
}

url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
params = {
    "api_key": read_key,
    "results": 1
}

interval = 15
rows = []

while True:
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "feeds" in data and len(data["feeds"]) > 0:
            latest_feed = data["feeds"][-1]

            timestamp = datetime.now()
            values = []

            for field, port in labview_ports.items():
                field_key = f"field{field}"
                field_value = latest_feed.get(field_key)

                if field_value is not None:
                    try:
                        value = float(field_value)
                        values.append(value)

                        value_str = f"{value:.8f}"

                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                            s.sendto(value_str.encode("utf-8"), (labview_host, port))

                        print(
                            f"{field_names[field]} from Field{field} "
                            f"sent to LabVIEW Port {port}: {value_str}"
                        )

                    except ValueError:
                        print(f"Invalid value for Field{field}: {field_value}")
                        values.append(None)

                else:
                    print(f"Field{field} ({field_names[field]}) is missing.")
                    values.append(None)

            rows.append([timestamp] + values)

        else:
            print("No data retrieved from ThingSpeak.")

        time.sleep(interval)

    except KeyboardInterrupt:
        print("Stopping the program...")
        break

    except requests.exceptions.RequestException as e:
        print(f"ThingSpeak request error: {e}")
        time.sleep(interval)

    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(interval)

df = pd.DataFrame(rows, columns=[
    "time", "isa", "isb", "isc", "va", "vb", "vc", "pm", "wm"
])

df.to_excel("data_pythonLabview.xlsx", index=False)

print("Data saved to data_pythonLabview.xlsx")