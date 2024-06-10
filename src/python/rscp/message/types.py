from __future__ import annotations
import struct
from typing import List, Optional
from .base import MessageBase
import yaml

FLOATING_POINT_TOLERANCE = 1e-6


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

    def __eq__(self, other) -> bool:
        if not isinstance(other, NavigateToGPS):
            return False
        return (
            abs(self.latitude - other.latitude) < FLOATING_POINT_TOLERANCE
            and abs(self.longitude - other.longitude) < FLOATING_POINT_TOLERANCE
        )


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


class ArucoTag(MessageBase, msg_id=0x6):
    def __init__(self, tag_id: int, dictionary: int):
        self.tag_id = tag_id
        self.dictionary = dictionary

    def serialize(self) -> bytes:
        return struct.pack(">IB", self.tag_id, self.dictionary)

    @staticmethod
    def deserialize(data: bytes) -> ArucoTag:
        assert len(data) == 5
        tag_id, dictionary = struct.unpack(">IB", data)
        return ArucoTag(tag_id, dictionary)


class LocateArucoTags(MessageBase, msg_id=0x7):
    def __init__(self, tag_list: List[ArucoTag]):
        self.tag_list = tag_list

    def serialize(self) -> bytes:
        return b"".join(tag.serialize() for tag in self.tag_list)

    @staticmethod
    def deserialize(data: bytes) -> LocateArucoTags:
        assert len(data) % 5 == 0
        tag_list = [
            ArucoTag.deserialize(data[i : i + 5]) for i in range(0, len(data), 5)
        ]

        return LocateArucoTags(tag_list)


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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Location3D):
            return False
        return (
            abs(self.x - other.x) < FLOATING_POINT_TOLERANCE
            and abs(self.y - other.y) < FLOATING_POINT_TOLERANCE
            and abs(self.z - other.z) < FLOATING_POINT_TOLERANCE
            and self.reference == other.reference
        )


class Detection(MessageBase, msg_id=0x9):
    def __init__(self, distance: float, description: str):
        self.distance = distance
        self.description = description

    def serialize(self) -> bytes:
        return struct.pack(">f", self.distance) + self.description.encode()

    @staticmethod
    def deserialize(data: bytes) -> Detection:
        assert len(data) >= 4

        distance = struct.unpack(">f", data[:4])[0]
        description = data[4:].decode()
        print(Detection(distance, description))
        return Detection(distance, description)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Detection):
            return False
        return (
            abs(self.distance - other.distance) < FLOATING_POINT_TOLERANCE
            and self.description == other.description
        )

class SetParameters(MessageBase, msg_id=0xA):
    def __init__(self, parameters: dict):
        self.parameters = parameters

    def serialize(self) -> bytes:
        yaml_str = yaml.dump(self.parameters, default_flow_style=False, sort_keys=False)
        return yaml_str.encode()

    @staticmethod
    def deserialize(data: bytes) -> SetParameters:
        parameters = yaml.safe_load(data)
        return SetParameters(parameters)
        
