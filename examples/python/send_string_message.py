import cobs
import cobs.cobs
import rscp_protobuf
import io
import serial

def send_response_over_serial(response: rscp_protobuf.ResponseEnvelope, serial_port: io.BytesIO):
    response_bytes = response.SerializeToString()
    cobs_encoded = cobs.cobs.encode(response_bytes)
    to_send_over_serial = cobs_encoded + b"\x00"

    print(f"Sending message over serial: {to_send_over_serial}")
    serial_port.write(to_send_over_serial)

response = rscp_protobuf.ResponseEnvelope()
response.message = "Hello from rover!!"

with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
    send_response_over_serial(response, ser)
