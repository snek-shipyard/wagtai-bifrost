from example.tests.test_bifrost import BaseBifrostTest
from home.factories import (
    AdvertFactory
)

class AdvertTest(BaseBifrostTest):
    def setUp(self):
        super().setUp()
        # Create advert
        self.advert = AdvertFactory()

    def test_advert_query(self):
        query = """
        {
           adverts {
                id
                url
                text
            }
        }
        """
        executed = self.client.execute(query)
        advert = executed["data"]["adverts"][0]

        # Check all the fields
        self.assertTrue(isinstance(advert["id"], str))
        self.assertTrue(isinstance(advert["url"], str))
        self.assertTrue(isinstance(advert["text"], str))
