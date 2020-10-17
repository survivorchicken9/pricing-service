import uuid
from typing import Dict
from dataclasses import dataclass, field
from models.item import Item
from models.model import Model
from models.user import User
from libs.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)  # executes after dataclass init
        self.email = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "user_email": self.user_email
        }

    def load_item_price(self):
        self.item.load_price()  # finds price on site and assigns to self.price
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"The item ({self.item} has reached a price below the limit ({self.price_limit}).\n"
                  f"The latest price is: {self.item.price}")
            Mailgun.send_mail(
                [self.user_email],
                f"Notification for {self.name}",
                f"This alert has reached a price under {self.price_limit}. "
                f"The current price is {self.item.price}."
                f"Check the current price at this url: {self.item.url}",
                f"<p>This alert has reached a price under {self.price_limit}.</p>"
                f"<p>The current price is {self.item.price}.</p>"
                f"<p>Click <a href='{self.item.url}'>here</a> to view your item in the browser.</p>",
            )
