from typing import Callable, Optional
import queue
import io
import logging
from ..frame_parser import FrameParser
from .base import MessageBase
from .parser import MessageParser


LOGGER = logging.getLogger(__name__)


class Broker:
    def __init__(
        self,
        on_receive: Optional[Callable[[MessageBase], None]] = None,
        on_send: Optional[Callable[[MessageBase], None]] = None,
        max_send_queue_size: int = -1,
    ):
        self._message_parser = MessageParser(self._internal_on_receive)
        self._frame_parser = FrameParser(self._message_parser.process)
        self._message_queue = queue.Queue(max_send_queue_size)
        self.on_send = on_send
        self.on_receive = on_receive

    def _internal_on_send(self, message: MessageBase):
        LOGGER.info("Sending message: %s", message)

        if not self.on_send:
            return

        self.on_send(message)

    def _internal_on_receive(self, message: MessageBase):
        LOGGER.info("Received message: %s", message)

        if not self.on_receive:
            return

        self.on_receive(message)

    def dispatch(self, message: MessageBase):
        while self._message_queue.full():
            self._message_queue.get()

        self._message_queue.put(message)

    def process(self, stream: io.BytesIO):
        # handle received messages
        # if stream has in_waiting attribute, use it, otherwise use len(stream.getvalue())
        if hasattr(stream, "in_waiting"):
            read_bytes = stream.read(stream.in_waiting)
        else:
            read_bytes = stream.getvalue()
        self._frame_parser.process(read_bytes)

        if self._message_queue.empty():
            return

        # handle messages to send
        message = self._message_queue.get()
        frame = message.create_frame()
        stream.write(frame)
        stream.flush()

        self._internal_on_send(message)
