from pymongo import MongoClient

# replace connection string to connect MongoDB cluster, you can get it from cluster's connection
# define db_name


class DatabaseManager:
    def __init__(self):
        self.connection_string = "mongodb+srv://<user>:<pw>@<clustername.clusterid>.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.connection_string)
        self.db_name = "<dbname>"
        self.my_db = self.client[self.db_name]

    def write_into_collection(self, name: str, item: dict):
        """
        Write an item into collection
        :param name: Collection name
        :param item: Dict item
        """
        collection = self.my_db[name]
        collection.insert_one(item)

    def write_many_into_collection(self, name: str, items: list):
        """
        Write many items into collection
        :param name: Collection name
        :param items: Dict items list
        """
        collection = self.my_db[name]
        collection.insert_many(items)

    def get_collection(self, name: str):
        """
        Get items in collection
        :param name: Collection name
        :return: Collection as DataFrame
        """
        collection = self.my_db[name]
        return collection.find()

    def search_in_collection(self, name: str, query: dict):
        """
        Filter for collection
        :param name: Collection name
        :param query: Query (e.g. {"symbol": "BTC"})
        :return: Search result
        """
        collection = self.my_db[name]
        return collection.find(query)
