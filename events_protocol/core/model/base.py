import json
import typing
from dataclasses import dataclass

from pydantic import BaseModel as PydanticBaseModel


def _to_pascal(string: str) -> str:
    result = string.split('_')
    result[1:] = [word.capitalize() for word in result[1:]]
    return ''.join(result)


class BaseModel(PydanticBaseModel):
    def to_dict(self, *args, **kwargs) -> typing.Dict[str, typing.Any]:
        return self.dict(by_alias=True, *args, **kwargs)

    def to_json(self, *args, **kwargs) -> str:
        return self.json(by_alias=True)


class PascalPydanticMixin(BaseModel):
    class Config:
        alias_generator = _to_pascal

    def __init__(self, by_alias=True, **data: typing.Any) -> None:
        _data = dict()
        for key, value in data.items():
            if by_alias:
                key = self.Config.alias_generator(key)
            _data[key] = value
        super().__init__(**_data)
