import cobs
import cobs.cobs
import rscp_protobuf
import io
import serial

def on_receive(data: bytes):
    cobs_decoded = cobs.cobs.decode(data)
    response = rscp_protobuf.ResponseEnvelope()
    response.ParseFromString(cobs_decoded)
    print(f"Received message: {response}")

with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
    buffer = b""
    while True:
        data = ser.read(1)
        if data == b"\x00":
            on_receive(buffer)
            buffer = b""
        else:
            buffer += data
        
