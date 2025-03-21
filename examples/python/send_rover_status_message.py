import cobs
import cobs.cobs
import rscp_protobuf
import io
import serial

def create_status_message() -> rscp_protobuf.RoverStatus:
    status = rscp_protobuf.RoverStatus()
    status.state = rscp_protobuf.RoverState.DISARMED
    status.battery_state.voltage = 12.3
    status.battery_state.current = 0.5
    status.battery_state.state_of_charge = 0.95
    status.coordinate.latitude = 1.234
    status.coordinate.longitude = 5.678
    status.coordinate.altitude = 0.98765
    return status

def send_response_over_serial(response: rscp_protobuf.ResponseEnvelope, serial_port: io.BytesIO):
    response_bytes = response.SerializeToString()
    cobs_encoded = cobs.cobs.encode(response_bytes)
    to_send_over_serial = cobs_encoded + b"\x00"

    serial_port.write(to_send_over_serial)
    print(f"Message sent over serial: {to_send_over_serial}")

response = rscp_protobuf.ResponseEnvelope()
response.rover_status.CopyFrom(create_status_message())

with serial.Serial("/dev/ttyUSB0", 115200, timeout=1) as ser:
    send_response_over_serial(response, ser)
