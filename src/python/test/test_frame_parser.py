import unittest
from rscp.frame_parser import Frame, FrameParser


class TestFrameParser(unittest.TestCase):
    def test_parser(self):
        frame: bytes = Frame.create(0x22, b"\x01\x02\x03")

        n_fired = 0
        def on_update(frame):
            nonlocal n_fired
            n_fired += 1

        frame_parser = FrameParser(on_update)

        for byte in frame:
            frame_parser.process(byte)

        self.assertEqual(n_fired, 1)

    def test_parser_multiple_frames(self):
        n_fired = 0
        def on_update(frame):
            nonlocal n_fired
            n_fired += 1
        frame_parser = FrameParser(on_update)
        
        frame1: bytes = Frame.create(0x22, b"\x01\x02\x03")
        frame2: bytes = Frame.create(0x23, b"\x04\x05\x06")
        frame3: bytes = Frame.create(1, b"")
        
        frame = frame1 + frame2 + frame3
        for byte in frame:
            frame_parser.process(byte)

        self.assertEqual(n_fired, 3)

    def test_parser_crc_error(self):
        # replace crc with 0x0000
        frame = Frame.create(0x22, b"\x01\x02\x03")[:-2] + b"\x00\x00"

        def on_update(_):
            self.fail("on_update should not be called due to crc error")

        frame_parser = FrameParser(on_update)
        for byte in frame:
            frame_parser.process(byte)
