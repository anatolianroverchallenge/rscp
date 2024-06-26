import unittest
from rscp.message.types import (
    MessageBase,
    Acknowledge,
    ArmDisarm,
    TaskFinished,
    NavigateToGPS,
    Text,
    SetStage,
    ArucoTag,
    LocateArucoTags,
    Location3D,
    Detection,
    SetParameters,
)
from typing import List, Type


class TestMessageSerialization(unittest.TestCase):
    def _test_message_serialization(
        self, msg_cls: Type[MessageBase], expected_str: bytes, *args, **kwargs
    ):
        msg = msg_cls(*args, **kwargs)
        serialized = msg.serialize()
        self.assertEqual(serialized, expected_str)

        msg_constructed = msg_cls.deserialize(expected_str)

        self.assertEqual(msg_constructed, msg)

    def test_ack(self):
        self._test_message_serialization(Acknowledge, b"")

    def test_arm_disarm(self):
        self._test_message_serialization(ArmDisarm, b"\x01", True)
        self._test_message_serialization(ArmDisarm, b"\x00", False)

    def test_task_finished(self):
        self._test_message_serialization(TaskFinished, b"")

    def test_navigation_to_gps(self):
        self._test_message_serialization(
            NavigateToGPS, b"?\x80\x00\x00@\x00\x00\x00", 1.0, 2.0
        )

    def test_text(self):
        self._test_message_serialization(Text, b"Hello World", "Hello World")

    def test_set_stage(self):
        self._test_message_serialization(SetStage, b"\x01", 1)

    def test_locate_tag(self):
        self._test_message_serialization(ArucoTag, b"\x00\x00\x00\x01\x01", 1, 1)

    def test_locate_multiple_tags(self):
        tag1 = ArucoTag(1, 1)
        tag2 = ArucoTag(2, 2)
        self._test_message_serialization(
            LocateArucoTags, b"\x00\x00\x00\x01\x01\x00\x00\x00\x02\x02", [tag1, tag2]
        )

    def test_location_3d(self):
        self._test_message_serialization(
            Location3D, b"@@\x00\x00@\xa0\x00\x00A\x10\x00\x00world", 3, 5, 9, "world"
        )
        self._test_message_serialization(
            Location3D, b"@@\x00\x00@\xa0\x00\x00A\x10\x00\x00", 3, 5, 9, None
        )

    def test_detection(self):
        self._test_message_serialization(
            Detection,
            b"@I\x0eVgreen",
            3.1415,
            "green",
        )

    def test_set_parameters(self):
        params = {
            "param1": 1,
            "latitude": 10.0,
            "longitude": 20.0,
            "text": "hello",
            "array": [1, 2],
        }

        self._test_message_serialization(
            SetParameters,
            b"param1: 1\nlatitude: 10.0\nlongitude: 20.0\ntext: hello\narray:\n- 1\n- 2\n",
            params,
        )
