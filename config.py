import os


class MQTT:
    HOST = os.environ.get("MQTT_HOST") or "localhost"
    QUEUE_NAME = os.environ.get("QUEUE_NAME") or "meter"


class MeterConfig(MQTT):
    pass


class SimPvConfig(MQTT):
    # Writer
    FILENAME = os.environ.get("FILENAME") or "meter.csv"
    FILE_PATH = os.environ.get("FILE_PATH") or "./out"

    # SunPos
    LATITUDE = os.environ.get("LATITUDE") or 33.6
    LONGITUDE = os.environ.get("LONGITUDE") or 10.8
    TIMEZONE = os.environ.get("TIMEZONE") or 1
    LOCATION = (float(LATITUDE), float(LONGITUDE))
    TIMEZONE = int(TIMEZONE)
