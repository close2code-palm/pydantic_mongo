import copy
import datetime
import typing
from contextlib import suppress
from enum import Enum
from typing import Type, get_args, Iterable, Any

from pydantic import BaseModel
from pydantic._internal._generics import PydanticGenericMetadata
from pydantic._internal._model_construction import ModelMetaclass
from sotrans_models.utils.type_checks import is_list_type, is_union


class MongoStr(str):
    pass


def get_field_from_args(args: Iterable):
    for arg in args:
        if arg is not None:
            return arg


def propagate_model(model, mongo_path, prefix):
    for field_name in model.model_fields:
        info = model.model_fields[field_name]
        field_type = info.annotation

        new_prefix = f"{prefix}." if prefix else ""

        field = MongoStr(f"{new_prefix}{field_name}")

        if is_union(field_type):
            args = get_args(field_type)
            field_type = get_field_from_args(args)

        if is_list_type(field_type):
            args = get_args(field_type)
            field_type = get_field_from_args(args)
            field = [field]  # type: ignore[assignment]

        with suppress(TypeError):
            if field_type and issubclass(field_type, BaseModel):
                generate_mongo_path_class(
                    field,
                    field_type,
                    prefix=f"{new_prefix}{field_name}",
                    alias=info.alias,
                    val_alias=info.validation_alias,
                    ser_alias=info.serialization_alias,
                )
        try:
            mongo_path.__dict__.update({field_name: field})  # type: ignore[attr-defined]
            # setattr(mongo_path, field_name, field)
        except AttributeError:
            # setattr(mongo_path[0], field_name, field)
            mongo_path[0].__dict__.update({field_name: field})  # type: ignore[index]


def generate_mongo_path_class(
    mongo_path: typing.Callable | MongoStr,
    model: Type[BaseModel],
    prefix: str = None,
    alias="",
    val_alias: str = None,
    ser_alias="",
):
    is_bm = issubclass(model, BaseModel)
    # new_prefix = f"{prefix}." if prefix else ""
    if is_bm:
        propagate_model(model, mongo_path, prefix)
    # if ser_alias:
    #     mongo_path.__dict__.update(ser_alias=ser_alias)

    # if alias:
        #     mongo_path.__dict__.update(alias=alias)

    if val_alias:
        # named_embed = mongo_path.replace(mongo_path, val_alias)
        prefs = prefix.split('.')
        after_validation_prefix = '.'.join(prefs[:-1]) or ''
        if after_validation_prefix:
            val_alias_with_prefix = f'{after_validation_prefix}.{val_alias}'
        else:
            val_alias_with_prefix = val_alias
        named_embed = MongoStr(val_alias_with_prefix)
        # field_copy = copy.deepcopy(mongo_path)
        generate_mongo_path_class(named_embed, model, val_alias_with_prefix)
        mongo_path.__dict__.update(validation_alias=named_embed)


def settable():
    return


def create_fields_from_model(model: Type[BaseModel]) -> typing.Callable:
    o = settable
    generate_mongo_path_class(o, model)
    return o


class MongoMeta(ModelMetaclass):
    def __new__(
        cls,
        name,
        bases,
        attrs,
        __pydantic_generic_metadata__: PydanticGenericMetadata | None = None,
        __pydantic_reset_parent_namespace__: bool = True,
        **kwargs: Any,
    ):
        super_class = super().__new__(
            cls,
            name,
            bases,
            attrs,
            __pydantic_generic_metadata__,
            __pydantic_reset_parent_namespace__,
            **kwargs,
        )
        o = create_fields_from_model(super_class)
        for k in o.__dict__:
            setattr(super_class, k, o.__dict__[k])
        return super_class


##########
# class DriverFields(DriverCreateModel, metaclass=MongoMeta):
#     pass


# class OrderFields(OrderCreateModel, metaclass=MongoMeta):
#     pass

# print(MongoStr(123))
# print(DriverFields.)
# print(DriverFields.verification)

# print(DriverFields.passport.number)
# print(type(DriverFields.passport))
# print(DriverFields.drivers_license.country)
# print(DriverFields.id.__str__(FieldAlias.validation))
##########

# a = MongoStr(123)
# a = a.replace(a, '23')
# print(a)
