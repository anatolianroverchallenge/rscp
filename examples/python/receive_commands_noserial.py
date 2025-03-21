import cobs
import cobs.cobs
import rscp_protobuf
import io
import time

# This simulated buffer contains 
# raw bytes that represent a message 
# that was receiver over serial module
# to simulate RSCP Host -> Rover communication
simulated_buffer = io.BytesIO(b'\x05\n\x02\x08\x01\x00\x05\x12\x02\x08\x03\x00\x1c\x1a\x19\n\x17\tX9\xb4\xc8v\xbe\xf3?\x11\x83\xc0\xca\xa1E\xb6\x16@\x1d\xa1\xd6|?\x00\x18"\x19\n\x12\tX9\xb4\xc8v\xbe\xf3?\x11\x83\xc0\xca\xa1E\xb6\x16@\x15\x01\x03\xc8B\x00')

def on_receive(data: bytes):
    # first step is to COBS decode the data
    cobs_decoded = cobs.cobs.decode(data)
    
    request = rscp_protobuf.RequestEnvelope()
    # next step is to decode(parse) the protobuf message
    request.ParseFromString(cobs_decoded)
    
    print(f"Received new message at: {time.time()}")
    print(f"Received Request type: {request.WhichOneof('request')}")
    print(request)

if __name__ == "__main__":
    buffer = b""
    while True:
        # instead of this, you may use serial.read() to read from serial port
        # see receive_commands.py for serial example
        data = simulated_buffer.read(1)
        if data == b"\x00":
            on_receive(buffer)
            buffer = b""
        else:
            buffer += data
        
