import json
import os
import sys
from datetime import datetime

from config import SimPvConfig
from mqtt import Listner
from sunpos import SunPos
from writer import Writer


class PvSim(Listner):
    def __init__(self, qm: int = 1) -> None:
        configuration = SimPvConfig()
        self.queue_name = configuration.QUEUE_NAME
        super().__init__(host=configuration.HOST)
        self.qm = qm
        self.sunpos = SunPos(location=configuration.LOCATION, timezone=configuration.TIMEZONE)
        self.writer = Writer(configuration.FILE_PATH, configuration.FILENAME)

    def run(self):
        self.listen(self.queue_name)

    def stop(self):
        self.close()

    # override simulation function on the Listner
    def sim(self, body):
        data = json.loads(body)

        meter_kW = data["value"]
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        self.sunpos.time = timestamp.time()
        self.sunpos.date = timestamp.date()

        # Get the Sun's apparent location in the sky
        azimuth, elevation = self.sunpos.getpos()

        # get the air mass
        airmass = self.sunpos.amcalc(elevation)

        # Get the solar intensity
        solar_intensity = round(self.sunpos.solint(airmass) * self.qm, 2)

        # Get the sum of meter and pvsim
        sumpower = round(solar_intensity + meter_kW, 2)

        self.writer.addrow([timestamp, meter_kW, solar_intensity, sumpower])


if __name__ == "__main__":

    try:
        mypvsim = PvSim(qm=5)
        mypvsim.run()
    except KeyboardInterrupt:
        mypvsim.stop()
        print("PvSim stoped.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
