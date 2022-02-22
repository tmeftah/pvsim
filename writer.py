import csv
import os


class Writer:
    def __init__(self, path: str, filename: str, mode: str = "a") -> None:

        self.file_path = os.path.join(path, filename)
        self.path = path
        self.mode: str = mode

    def addrow(self, data):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.file_path, self.mode) as write_obj:
            writer = csv.writer(write_obj, delimiter=";")
            writer.writerow(data)
