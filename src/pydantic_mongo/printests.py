from datetime import datetime

from pydantic import BaseModel, Field

from src.pydantic_mongo.annotations import MongoList, MongoDT, MongoType
from src.pydantic_mongo.lib_mongo_path import MongoMeta
from src.pydantic_mongo import operators as mdb


class OrderMongoType(BaseModel, MongoType):
    a: int


class ValidationEmbedded(BaseModel, metaclass=MongoMeta):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    test_field: OrderMongoType = Field(validation_alias='_test')
    test_dt: MongoDT
    # test_union: MongoDT | None = None
    test_list: MongoList[MongoDT]


########## Features

print(ValidationEmbedded.test_field.validation_alias.a)
# print(ValidationEmbedded.test_dt)
# print(ValidationEmbedded.test_field.client)
# print(ValidationEmbedded.test_union[PydanticMongoDT].validation_alias)
# print(ValidationEmbedded.test_list.list_elem.validation_alias)
# print(ValidationEmbedded.test_dt.val_alias)
print(ValidationEmbedded(
    _test=OrderMongoType(a=2),
    test_dt=datetime(2022, 2, 2, 2),
    test_list=[],
).model_dump(exclude_none=True))
update = {mdb.set_: {ValidationEmbedded.test_field.validation_alias.a: 1}}
print(update)
