from typing import Any, Callable, Generic, TypeVar
from bson import ObjectId


def documentize(d: dict, nominal: str) -> dict:
    ''' Transforms a `dict` to a suitable MongoDB document.

    The function modifies the given object by removing the `nominal` field, and assigning its value to the `_id` field.

    Parameters:
      d (dict): The dictionary to transform
      nominal (str): The name of the field to use as the `_id`

    Returns:
      dict: The transformed dictionary
    '''
    d['_id'] = d.pop(nominal)
    return d


def pythonize(d: dict, nominal: str) -> dict:
    ''' Transforms a `dict` obtained from a MongoDB document into a `dict` represenation expected in python

    The function modifies the given MongoDB document `dict` by removing the `_id` field, and assigning its value to the `nominal` field.

    Parameters:
      d (dict): The MongoDB document as a dict
      nominal (str): The name of the field to use instead of `_id`

    Returns:
      dict: The transformed dictionary
    '''
    d[nominal] = d.pop('_id')
    return d


M = TypeVar('M')
D = TypeVar('D')


class MongoIdHandler(Generic[M, D]):
    def __init__(self, id_field_name: str,
                 default_factory: Callable[[], M],
                 to_model_type: Callable[[D], M],
                 from_model_type: Callable[[M], D],
                 ) -> None:
        """ 
        Handles marshaling an id between the model stated type to the 'mongo' storage type.
        The 'mongo' type is actually some python type, which pymongo will then convert according to its own
        codec conventions.
        """
        self.id_field_name = id_field_name
        self.default_factory = default_factory
        self.to_model_type = to_model_type
        self.from_model_type = from_model_type

    def to_mongo_dict(self, d: dict):
        if d.has_key(self.id_field_name):
            d['_id'] = self.from_model_type(d.pop(self.id_field_name))
        else:
            d['_id'] = self.default_factory()
        return d

    def from_mongo_dict(self, d: dict):
        d[self.id_field_name] = self.to_model_type(d.pop('_id'))
        return d


class TransparentIdHandler(MongoIdHandler):
    def __init__(self, id_field_name: str, default_factory: Callable[[], Any]) -> None:
        super().__init__(id_field_name, default_factory, lambda d: d, lambda m: m)


class StringAsObjectIdHandler(MongoIdHandler):
    def __init__(self, id_field_name: str) -> None:
        """
        :param default_factory: A no-arguments callable that creates a new [Tmodel] value if none is supplied
        :param to_model_type: A [Tmodel] argument callable that converts the type from the one used in the document storage to the one the model expects
        :param from_model_type: A [Tdoc] the type from the one used the model exposes to the one the document should store
        """
        super().__init__(
            id_field_name=id_field_name,
            default_factory=lambda: str(ObjectId()),
            to_model_type=lambda oid: str(oid),
            from_model_type=lambda s: ObjectId(s)
        )
