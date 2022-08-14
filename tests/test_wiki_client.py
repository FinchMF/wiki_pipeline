import sys
import unittest
import pickle as pkl
sys.path.append('../')

from reciever.wiki_client import Wiki


def set_single_data() -> dict:
    
    with open('./tests/test_data/chess_object.pkl', 'rb') as f:
        chess_object = pkl.load(f)

    return chess_object

def set_multiple_data() -> list:

    with open('./tests/test_data/tax_object.pkl', 'rb') as f:
        tax_object = pkl.load(f)

    with open('./tests/test_data/chess_object.pkl', 'rb') as f:
        chess_object = pkl.load(f)

    return tax_object, chess_object


class TestWiki(unittest.TestCase):

    def test_parse_single_topic(self) -> None:

        client = Wiki(topic='Chess')
        client.parse_single_topic()

        chess_object = set_single_data()
        self.assertEqual(client.collection['Chess']['summary'], chess_object['summary'])

    
    def test_parse_multiple_topics(self) -> None:

        client = Wiki(topic=['Taxes', 'Chess'])
        client.parse_multiple_topics()

        tax_object, chess_object = set_multiple_data()

        self.assertEqual(client.collection['Tax']['summary'], tax_object['summary'])
        self.assertEqual(client.collection['Chess']['summary'], chess_object['summary'])



if __name__ == '__main__':

    unittest.main()