from typing import TypeVar, Type, List, Dict, Union
from abc import ABCMeta, abstractmethod
from common.database import Database

T = TypeVar('T', bound='Model')  # bound means that T must be a Model or subclass of Model


class Model(metaclass=ABCMeta):
    """
    This is the model superclass- like a template for all other classes used by the app
    "Abstract" in Python means that what you're using exists but is not defined yet
    This abstract model class is a definition of what our classes should be (it's not an actual class)
    New models in the application (item, alert, store) should fit this abstract model class
    """
    collection: str # reminder to set class level mongodb collection variable applicable to all
    _id: str  # these work as both class properties and instance properties

    def __init__(self, *args, **kwargs):
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())  # self.json() returns the dictionary to insert

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)
        # same as: return cls(**Database.find_one(cls.collection, {"_id": _id}))

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError  # required for saving to mongodb

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})  # sub classes will define collection properties
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: str) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]
