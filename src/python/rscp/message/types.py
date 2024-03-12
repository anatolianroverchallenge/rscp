from __future__ import annotations
import struct
from typing import List, Optional
from .base import MessageBase


class Acknowledge(MessageBase, msg_id=0x0):
    def serialize(self) -> bytes:
        return b""

    @staticmethod
    def deserialize(data: bytes) -> Acknowledge:
        assert len(data) == 0
        return Acknowledge()


class ArmDisarm(MessageBase, msg_id=0x1):
    def __init__(self, arm: bool):
        self.arm = arm

    def serialize(self) -> bytes:
        return struct.pack(">B", self.arm)

    @staticmethod
    def deserialize(data: bytes) -> ArmDisarm:
        assert len(data) == 1
        arm = struct.unpack(">B", data)[0]
        return ArmDisarm(arm)


class NavigateToGPS(MessageBase, msg_id=0x2):
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self) -> bytes:
        return struct.pack(">ff", self.latitude, self.longitude)

    @staticmethod
    def deserialize(data: bytes) -> NavigateToGPS:
        assert len(data) == 8
        latitude, longitude = struct.unpack(">ff", data)
        return NavigateToGPS(latitude, longitude)


class TaskFinished(MessageBase, msg_id=0x3):
    def serialize(self) -> bytes:
        return b""

    @staticmethod
    def deserialize(data: bytes) -> TaskFinished:
        assert len(data) == 0
        return TaskFinished()


class SetStage(MessageBase, msg_id=0x4):
    def __init__(self, stage_id: int):
        self.stage_id = stage_id

    def serialize(self) -> bytes:
        return struct.pack(">B", self.stage_id)

    @staticmethod
    def deserialize(data: bytes) -> SetStage:
        assert len(data) == 1
        stage_id = struct.unpack(">B", data)[0]
        return SetStage(stage_id)


class Text(MessageBase, msg_id=0x5):
    def __init__(self, text: str):
        self.text = text

    def serialize(self) -> bytes:
        return self.text.encode()

    @staticmethod
    def deserialize(data: bytes) -> Text:
        text = data.decode()
        return Text(text)


class LocateTag(MessageBase, msg_id=0x6):
    def __init__(self, tag_id: int):
        self.tag_id = tag_id

    def serialize(self) -> bytes:
        return struct.pack(">B", self.tag_id)

    @staticmethod
    def deserialize(data: bytes) -> LocateTag:
        assert len(data) == 1
        tag_id = struct.unpack(">B", data)[0]
        return LocateTag(tag_id)


class LocateMultipleTags(MessageBase, msg_id=0x7):
    def __init__(self, tag_ids: List[int]):
        self.tag_ids = tag_ids

    def serialize(self) -> bytes:
        return struct.pack(f">{len(self.tag_ids)}B", *self.tag_ids)

    @staticmethod
    def deserialize(data: bytes) -> LocateMultipleTags:
        tag_ids = struct.unpack(f">{len(data)}B", data)
        return LocateMultipleTags(list(tag_ids))


class Location3D(MessageBase, msg_id=0x8):
    def __init__(self, x: float, y: float, z: float, reference: Optional[str] = None):
        self.x = x
        self.y = y
        self.z = z
        self.reference = reference

    def serialize(self) -> bytes:
        return struct.pack(">fff", self.x, self.y, self.z) + (
            b"" if self.reference is None else self.reference.encode()
        )

    @staticmethod
    def deserialize(data: bytes) -> Location3D:
        assert len(data) >= 12

        x, y, z = struct.unpack(">fff", data[:12])

        if len(data) == 12:
            return Location3D(x, y, z, None)

        reference_str = data[12:].decode()
        return Location3D(x, y, z, reference=reference_str)


class Detection(MessageBase, msg_id=0x9):
    def __init__(self, tag_id: int, location: Optional[Location3D] = None):
        self.tag_id = tag_id
        self.location = location

    def serialize(self) -> bytes:
        return struct.pack(">B", self.tag_id) + (
            self.location.serialize() if self.location is not None else b""
        )

    @staticmethod
    def deserialize(data: bytes) -> Detection:
        assert len(data) >= 1
        tag_id = struct.unpack(">B", data[:1])[0]

        if len(data) == 1:
            return Detection(tag_id, None)

        assert len(data) >= 13

        location = Location3D.deserialize(data[1:])
        return Detection(tag_id, location)
