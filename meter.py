import datetime
import json
import os
import random
import sys
import time

from config import MeterConfig
from mqtt import Emitter


class Meter(Emitter):
    def __init__(self) -> None:
        configuration = MeterConfig()
        self.queue = configuration.QUEUE_NAME
        super().__init__(host=configuration.HOST)

    def run(self):
        self.declare_queue(queue_name=self.queue)

        now_ = datetime.datetime.combine(
            datetime.date.today(), datetime.datetime.min.time()
        )  # today at 00:00:00

        for i in range(86400):
            body = json.dumps(
                {
                    "timestamp": now_.strftime("%Y-%m-%d %H:%M:%S"),
                    "value": random.randint(0, 9000),
                }
            )

            self.publish(body, self.queue)
            now_ = now_ + datetime.timedelta(seconds=1)
            time.sleep(0)  # how fast schould send meter value

        self.close()


if __name__ == "__main__":
    try:
        mypmeter = Meter()
        mypmeter.run()
    except KeyboardInterrupt:
        mypmeter.close()
        print("Meter stoped.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
