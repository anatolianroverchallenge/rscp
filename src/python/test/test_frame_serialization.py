import unittest
from rscp.frame_parser import Frame
import struct


class TestFrameSerialization(unittest.TestCase):
    def test_regular_frame_serialization(self):
        frame = Frame.create(0x22, b"\x01\x02\x03")

        self.assertEqual(len(frame), 8)
        self.assertEqual(frame[:6], b"\x7E\x22\x03\x01\x02\x03")

        crc_value = struct.unpack(">H", frame[-2:])[0]
        self.assertEqual(crc_value, 29669)

    def test_empty_frame_serialization(self):
        frame = Frame.create(0xA0, b"")
        self.assertEqual(len(frame), 5)
        self.assertEqual(frame[:3], b"\x7E\xA0\x00")

        crc_value = struct.unpack(">H", frame[-2:])[0]
        self.assertEqual(crc_value, 56951)

    def test_max_length_frame_serialization(self):
        frame = Frame.create(0x00, bytes([100 for x in range(255)]))
        self.assertEqual(len(frame), 260)
        self.assertEqual(frame[:3], b"\x7E\x00\xFF")

        data = frame[3:-2]
        self.assertEqual(data, bytes([100 for x in range(255)]))

    def test_over_max_length_frame_serialization(self):
        with self.assertRaises(AssertionError):
            Frame.create(0x00, bytes([100 for x in range(256)]))
