#include <Arduino.h>
#include "rscp.pb.h"          // Generated Protobuf header for RSCP messages
#include "pb_decode.h"        // Nanopb decoding functions
#include "cobs.h"             // COBS (Consistent Overhead Byte Stuffing) decoding
#include "request_monitor.h"  // Custom utility to print parsed request messages

// Input buffer for raw COBS-encoded data
uint8_t input_buffer[256];
// Buffer to hold decoded Protobuf message
uint8_t decoded_buffer[256];
// Current index into input_buffer
size_t input_index = 0;

void setup()
{
    // Initialize serial communication at 115200 baud
    Serial.begin(115200);
}

void loop()
{
    // Check if any bytes are available on the serial port
    while (Serial.available())
    {
        uint8_t b = Serial.read();

        // End of COBS packet (0x00 marks frame boundary)
        if (b == 0x00)
        {
            // Decode the COBS-encoded data
            size_t decoded_len = cobs_decode(decoded_buffer, input_buffer, input_index);

            // Initialize Protobuf message structure
            rscp_RequestEnvelope message = rscp_RequestEnvelope_init_zero;

            // Create a nanopb input stream from the decoded buffer
            pb_istream_t stream = pb_istream_from_buffer(decoded_buffer, decoded_len);

            // Attempt to decode the Protobuf message
            if (pb_decode(&stream, rscp_RequestEnvelope_fields, &message))
            {
                // If successful, print the message using custom utility
                print_RequestEnvelope(&message);
            }
            else
            {
                // Decoding failed; report error
                Serial.println("Failed to decode protobuf");
            }

            // Reset buffer index for next message
            input_index = 0;
        }
        else
        {
            // Add byte to buffer if space allows
            if (input_index < sizeof(input_buffer))
            {
                input_buffer[input_index++] = b;
            }
            else
            {
                // Input buffer overflow; reset and warn
                Serial.println("Warning: input_buffer overflow");
                input_index = 0;
                continue;
            }
        }
    }
}
