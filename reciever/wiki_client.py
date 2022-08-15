
import random
from mediawiki import MediaWiki, DisambiguationError


class Wiki:
    """
    * functionality wrapper for 'MediaWiki' object

    > object contains methods to access and collect topic text from wiki
    > object has two containers

        + container one: collection
            - collection holds topic keys
            - topic values:
                - summary
                - section names
                - section -> section keys
                    section values:
                        - content

        + container two: associated search
            - associated search holds search topic keys
            - serch topic values:
                - array of associated topics that returned in search

    > object contains one item of automation
        - pull associated search topics

    > object contains items of conditional automation
        - parse topics upon instantiation

    """
    def __init__(
        
        self,
        topic: str | list,
        hops: int = 1,
        auto_parse: bool = False
        
        ) -> None:
        # init
        self.__topic = topic
        self.__hops = hops
        # client
        self.__client = MediaWiki()
        # continers
        self.__collection = {}
        self.__associated_search = {}
        # automation
        self.get_associated_searches()
        # conditional automation
        if auto_parse:
            self.parse_topics()


    @property
    def topic(self) -> str | list:
        return self.__topic

    @property
    def hops(self) -> int:
        return self.__hops

    @property
    def client(self) -> MediaWiki:
        return self.__client

    @property
    def collection(self) -> dict:
        return self.__collection

    @collection.setter
    def collection(self, collection: dict) -> None:
        self.__collection = collection

    @property
    def associated_search(self) -> list:
        return self.__associated_search


    @staticmethod
    def _parse_single_topic(
        
        collection: dict, 
        client: MediaWiki, 
        topic: str | list
        
        ) -> dict:

        """
        function to get data on a single topic

        if the 'Wiki' object is initialized
        with a topic list, then this function will
        use the first topic in the list
        """
        loop = True
        while loop:

            try:
                if isinstance(topic, str):
                    top = client.page(topic)
                    loop = False

                if isinstance(topic, list):
                    top = client.page(topic[0])
                    loop = False

            except DisambiguationError as err:

                topic = err.options[0]
    

        if top.title not in collection.keys():

            collection[top.title] = {
                
                'title': top.title,
                'summary': top.summary,
                'section_name': top.sections,
                'sections': {}
            }

            for section in top.sections:
                if section not in [
                    'See also',
                    'References', 
                    'Further reading', 
                    'External links'
                    ]:

                    collection[top.title]['sections'][section] = {
                        'content': top.section(section_title=section)
                    }

        return collection


    @staticmethod
    def _parse_multiple_topics(

        collection: dict,
        client: MediaWiki,
        topic: str | list
        
        ) -> dict:

        """
        function to get data on multiple topics
        """

        if isinstance(topic, list):

            for top in topic:

                collection = Wiki._parse_single_topic(

                    collection=collection,
                    client=client,
                    topic=top
                )

        return collection

    @staticmethod
    def _search_associated_topics(
        
        collection: dict, 
        client: bool, 
        topic: str,
        associated_search: dict
        
        ) -> dict:

        return Wiki._parse_multiple_topics(
            
            collection=collection,
            client=client,
            topic=associated_search[topic]
        )
    
        
    def parse_single_topic(self) -> None:
        """
        method to parse a Wiki object that has
        been instantiated with a single topic
        """
        self.collection = Wiki._parse_single_topic(

            collection=self.collection, 
            client=self.client, 
            topic=self.topic
        )

    def parse_multiple_topics(self) -> None:
        """
        method to parse Wiki object that has been
        instantiated with multiple topics
        """

        self.collection = Wiki._parse_multiple_topics(

            collection=self.collection,
            client=self.client,
            topic=self.topic
        )
        
    def parse_topics(self) -> None:

        """
        method to distinguish between number of topics
        and call appropiate method
        """

        if isinstance(self.topic, str):
            self.parse_single_topic()

        if isinstance(self.topic, list):
            self.parse_multiple_topics()


    def pull_associated_searches(self, topic: str, top: int = 5) -> None:
        """
        method to set search results for a given topic
        """
        self.associated_search[topic] = self.client.search(topic)[0:top]


    def get_associated_searches(self) -> None:
        """
        method to receive all associated searches
        """
        if isinstance(self.topic, list):

            for topic in self.topic:
                self.pull_associated_searches(topic=topic)

        if isinstance(self.topic, str):

            self.pull_associated_searches(topic=self.topic)


    def fetch_associations(self) -> None:
        """
        method to recieve all associated searches
        """
        if isinstance(self.topic, str):

            self.collection = Wiki._search_associated_topics(
                collection=self.collection,
                client=self.client,
                topic=self.topic,
                associated_search=self.associated_search
            )

        if isinstance(self.topic, list):

            for topic in self.topic:
                self.collection = Wiki._search_associated_topics(

                    collection=self.collection,
                    client=self.client,
                    topic=self.topic,
                    associated_search=self.associated_search
                )

    
    def process_associated_searches(self, topic: str) -> None:
        """
        method
        """
        if topic not in list(self.associated_search.keys()):

            self.pull_associated_searches(topic=topic)
        
        self.collection = Wiki._parse_multiple_topics(

            collection=self.collection, 
            client=self.client, 
            topic=self.associated_search[topic]
        )


    def hop_search(self, search_topics: list, hop: int) -> None:

        h = 0
        while h <= hop:

            for topic in search_topics:
                self.process_associated_searches(topic=topic)


            h += 1
            if h == hop:
                continue

            else:

                tmp = []
                for topic in search_topics:
                    tmp.extend(self.associated_search[topic])

                search_topics = tmp


    def fetch_multiple_hops(self) -> None:

        if isinstance(self.topic, str):

            self.hop_search(
                
                search_topics=self.associated_search[self.topic], 
                hop=self.hops
                
            )

        if isinstance(self.topic, list):

            for topic in self.topic:

                if topic not in list(self.associated_search.keys()):

                    self.pull_associated_searches(topic=topic)

                self.hop_search(

                    search_topics=self.associated_search[topic], 
                    hop=self.hops
                )