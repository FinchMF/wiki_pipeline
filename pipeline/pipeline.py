
from mediawiki import MediaWiki
from pymongo import MongoClient

class Pipeline:

    def __init__(
        
        self, 
        wiki: MediaWiki, 
        orm: MongoClient,
        hops: bool = False

        ) -> None:

        self.wiki = wiki
        self.orm = orm
        self.hops = hops


    def fetch(self) -> None:

        self.wiki.parse_topics()
        self.wiki.get_associated_searched()
        self.wiki.fetch_associations()

        if self.hops:
            
            self.fetch_multiple_hops()

    def store(self) -> None:

        for topic in self.wiki.collection.keys():
            self.orm.insert(self.wiki.collection[topic])


    def run(self) -> None:

        self.fetch()
        self.store()

