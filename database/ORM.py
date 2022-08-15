import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

class Mongo_ORM:

    def __init__(self, server: str) -> None:

        self.server = server

    # -- establish connection -- #

    def connect(self, db: str, collection: str) -> None:

        self.client = pymongo.MongoClient(self.server)
        self.database = self.client[f"{db}"]
        self.collection = self.database[f"{collection}"]

    # -- collection -- #
    
    def insert_many(self, data: list) -> None:

        self.collection.insert_many(data)

    def insert(self, data: dict) -> None:

        self.collection.insert_one(data)

    def find_all(self) -> list:

        return [data for data in self.collection.find()]

    def find_one(self) -> dict:

        return self.collection.find_one()

    def find_by(self, query: dict) -> list:

        return [data for data in self.collection.find(query)]

    def collection_size(self) -> int:

        return self.collection.count_documents({})

    # -- database -- #

    def list_collections(self) -> list:

        return self.database.collection_names(include_system_collections=False)

    # -- client -- #

    def delete_database(self, database: str) -> None:

        self.client.drop_database(database)



class Database(Mongo_ORM):

    server = os.getenv("MONGO_SERVER")

    def __init__(self, database: str, collection: str) -> None:

        super().__init__(server=Database.server)
        self.connect(db=database, collection=collection)
