from typing import Callable
import logging
import crc
import construct

LOGGER = logging.getLogger(__name__)


class Frame:
    @staticmethod
    def format() -> construct.Struct:
        return construct.Struct(
            "start_byte" / construct.Const(b"\x7E"),
            "msg_id" / construct.Byte,
            "length" / construct.Byte,
            "data" / construct.Bytes(lambda this: this.length),
            "checksum"
            / construct.Checksum(
                construct.Int16ub,
                lambda data: crc.Calculator(crc.Crc16.CCITT.value).checksum(data),
                lambda this: this.start_byte
                + bytes([this.msg_id, this.length])
                + this.data,
            ),
        )

    @staticmethod
    def create(msg_id: int, data: bytes) -> bytes:
        assert len(data) <= 255

        LOGGER.debug("Creating frame with msg_id: %d, data: %s", msg_id, data)
        return Frame.format().build(
            {"msg_id": msg_id, "length": len(data), "data": data}
        )


class FrameParser:
    def __init__(self, on_frame_callback: Callable[[construct.Container], None]):
        self.on_frame_callback = on_frame_callback
        self.buffer = bytearray()

    def _strip_buffer_start(self, buffer: bytes) -> bytes:
        start_index = buffer.find(b"\x7E")
        if start_index == -1:
            return buffer, b""
        return buffer[start_index:], buffer[:start_index]

    def process(self, read_bytes: bytes):
        if read_bytes is None:
            return

        if not isinstance(read_bytes, bytes):
            read_bytes = bytes([read_bytes])

        if len(self.buffer) == 0 and len(read_bytes) == 0:
            return

        self.buffer.extend(read_bytes)
        # Frame.format().start_byte
        if not self.buffer.startswith(b"\x7E"):
            read_bytes, stripped = self._strip_buffer_start(read_bytes)
            LOGGER.warning(
                "Buffer contains invalid start condition, dropping bytes: %s", stripped
            )

        try:
            frame = Frame.format().parse(self.buffer)
            self.on_frame_callback(frame)
            length = len(Frame.format().build(frame))
            self.buffer = self.buffer[length:]
        except construct.ChecksumError as e:
            LOGGER.error("Checksum error %s, dropping bytes: %s", e, self.buffer)
        except construct.ConstructError as e:
            LOGGER.debug("Parsing error %s, dropping bytes: %s", e, self.buffer)
