import re
import uuid
from typing import Dict
from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:  # return value annotation for float
        """
        Really basic beautiful soup and requests combo to get the price of the item provided.
        :return: self.price as a float
        """
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        price = element.text.strip()

        self.price = float(re.compile(r'(\d*)').search(price).group(1))  # search for number in string
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }
