from __future__ import annotations
from typing import Dict, Type
from ..frame_parser import Frame


class Registry:
    _id_to_class: Dict[int, Type] = {}
    _class_to_id: Dict[Type, int] = {}

    @staticmethod
    def has_id(msg_id):
        return msg_id in Registry._id_to_class

    @staticmethod
    def has_class(class_type):
        return class_type in Registry._class_to_id

    @staticmethod
    def register(msg_id):
        def decorator(class_type):
            Registry._id_to_class[msg_id] = class_type
            Registry._class_to_id[class_type] = msg_id

        return decorator

    @staticmethod
    def get_class_by_id(msg_id):
        assert Registry.has_id(msg_id)

        return Registry._id_to_class[msg_id]

    @staticmethod
    def get_id_by_class(class_type):
        assert Registry.has_class(class_type)

        return Registry._class_to_id[class_type]


class MessageBase:
    def __init_subclass__(cls, msg_id, **kwargs):
        super().__init_subclass__(**kwargs)
        Registry.register(int(msg_id))(cls)

    def serialize(self) -> bytes:
        raise NotImplementedError()

    @staticmethod
    def deserialize(data: bytes) -> MessageBase:
        raise NotImplementedError()

    def create_frame(self) -> bytes:
        body = self.serialize()
        assert len(body) <= 255

        _id = Registry.get_id_by_class(type(self))
        return Frame.create(_id, body)

    def __str__(self):
        attributes = ", ".join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"{self.__class__.__name__}({attributes})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self)
