from typing import Callable, Optional
import logging
import construct
from .base import Registry, MessageBase

# pylint: disable=wildcard-import, unused-wildcard-import
# This is necessary to import all message types, so they can be registered in the Registry
from .types import *

LOGGER = logging.getLogger(__name__)


class MessageParser:
    def __init__(self, on_message_callback: Callable[[MessageBase], None]):
        self.on_message_callback = on_message_callback

    @staticmethod
    def parse_message(frame: construct.Container) -> Optional[MessageBase]:
        msg_id = frame["msg_id"]
        if not Registry.has_id(msg_id):
            LOGGER.error("Unknown message id: %d", msg_id)
            return None

        msg_cls: MessageBase = Registry.get_class_by_id(msg_id)
        return msg_cls.deserialize(frame["data"])

    def process(self, frame: construct.Container):
        LOGGER.debug("Received frame: %s", frame)

        msg = MessageParser.parse_message(frame)
        self.on_message_callback(msg)
