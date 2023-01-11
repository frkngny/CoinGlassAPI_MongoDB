from DatabaseManager import DatabaseManager
import time
import json


def load_io_params():
    with open('io_params.json') as json_file:
        return json.load(json_file)


class LocalSaver:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.collections = list(load_io_params().keys())

    def save_local(self):
        for collection_name in self.collections:
            collection = self.db_manager.get_collection(name=collection_name)
            output = dict()
            index = 0
            for item in collection:
                id = item.pop("_id")
                output[index] = item
                index += 1

            timestamp = time.time()
            with open(f"{collection_name}-{timestamp}.json", "w") as outfile:
                json.dump(output, outfile)


lc = LocalSaver()
lc.save_local()
