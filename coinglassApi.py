import time
import requests
import json
from DatabaseManager import DatabaseManager


class CoinGlassAPI:
    def __init__(self, ioparams: dict, disabled: list):
        self.base_url = "https://open-api.coinglass.com/public/v2/"
        self.DBManager = DatabaseManager()
        self.io_params = ioparams
        self.disabled = disabled

    def write_into_collection(self, collection_name: str, item: dict):
        self.DBManager.write_into_collection(name=collection_name, item=item)

    def write_many_into_collection(self, collection_name: str, items: list):
        self.DBManager.write_many_into_collection(name=collection_name, items=items)

    def get_data(self, segment: str, params: dict):
        try:
            symbol = params["symbol"]
        except KeyError:
            symbol = None

        try:
            time_type = params["time_type"]
        except KeyError:
            time_type = None

        if time_type is not None:
            url = f"{self.base_url}/{segment}?time_type={time_type}&symbol={symbol}"
        else:
            url = f"{self.base_url}/{segment}?symbol={symbol}"

        return json.loads(requests.get(url, headers={"accept": "application/json"}).text)["data"]

    def create_and_write(self, returned_data: list, params: list, segment: str):
        try:
            list_params: list = self.io_params[segment]["list"]
            for key in params:
                if not key.startswith("--"):
                    list_params.append(key)
        except KeyError:
            list_params = list()
            pass

        data_to_write = list()
        for data in returned_data:
            item = dict()
            for key in params:
                key = key.removeprefix("--")
                try:
                    item[key] = data[key]
                except KeyError as kErr:
                    if kErr.args[0] == "updateTime":
                        item[key] = round(time.time()*1000)
            try:
                if len(list_params) != 0:
                    data_list = data["list"]
                    exchange_list = list()
                    for exchange in data_list:
                        list_item = dict()
                        for key in list_params:
                            list_item[key] = exchange[key]
                        exchange_list.append(list_item)
                    item["list"] = exchange_list
            except:
                pass
            data_to_write.append(item)
        self.write_many_into_collection(segment, data_to_write)

    def common_market(self):
        for segment, market_class in self.io_params.items():
            if segment not in self.disabled:
                url_params = market_class["url_params"]
                symbol = url_params["symbol"].upper()
                params = market_class["params"]

                if segment == "perpetual_market":
                    returned_data = self.get_data(segment, url_params)[symbol]
                elif segment == "long_short":
                    returned_data = self.get_data(segment, url_params)  # [0]["list"]
                elif segment == "open_interest":
                    returned_data = self.get_data(segment, url_params)
                elif segment == "option":
                    returned_data = self.get_data(segment, url_params)
                elif segment == "liquidation_history":
                    returned_data = self.get_data(segment, url_params)  # [0]["list"]
                else:
                    return
                self.create_and_write(returned_data, params, segment)
