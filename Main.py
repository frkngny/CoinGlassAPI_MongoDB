import time
from coinglassApi import CoinGlassAPI
import json
from threading import Thread


def load_io_params():
    with open('io_params.json') as json_file:
        return json.load(json_file)


class Main:
    def __init__(self):
        self.io_params = load_io_params()
        self.disabled = [""]  # list to disable to get data for (e.g. "open_interest")

        self.CGApi = CoinGlassAPI(self.io_params, self.disabled)
        self.db_manager = self.CGApi.DBManager
        self.my_db = self.db_manager.my_db

        self.collections = list(self.io_params.keys())
        self.time_interval = 5

    def collect_data_and_store(self):
        while True:
            start_time = time.perf_counter()

            self.CGApi.common_market()  # collect from api and write into db

            end_time = time.perf_counter()
            if (start_time - end_time) > self.time_interval:
                time.sleep(self.time_interval)
            else:
                wait = self.time_interval - (start_time - end_time)
                time.sleep(wait)

    def runner(self):
        col_store = Thread(target=self.collect_data_and_store)
        col_store.start()


main = Main()
main.runner()
