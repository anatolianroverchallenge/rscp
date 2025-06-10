#include <iostream>
#include <fstream>
#include <vector>
#include "rscp.pb.h"      // Generated protobuf header
#include "Include\cobs.h" // COBS (Consistent Overhead Byte Stuffing) encoding/decoding

/**
 * @brief Callback function to handle and decode incoming COBS-encoded protobuf messages.
 *
 * This function takes a byte buffer representing a COBS-encoded Protocol Buffers message,
 * decodes it using the COBS algorithm, and attempts to deserialize it into a
 * `rscp::RequestEnvelope` object. If successful, it prints out the request type and
 * a full debug string of the message contents.
 *
 * @param buffer A reference to a vector of bytes representing the received data frame.
 *
 * @note If decoding or parsing fails, an error message is printed to stderr.
 */
void on_receive(const std::vector<uint8_t> &buffer)
{
    // Decode the received buffer using COBS
    auto decoded = cobs_decode(buffer.data(), buffer.size());

    // Deserialize the protobuf message into a RequestEnvelope object
    rscp::RequestEnvelope request;
    if (!request.ParseFromArray(decoded.data(), decoded.size()))
    {
        std::cerr << "Failed to parse cmakprotobuf message.\n";
        return;
    }

    // Log the received request type and full debug output
    std::cout << "Received Request type: " << request.request_case() << std::endl;
    std::cout << request.DebugString() << std::endl;
}

/**
 * main function
 */
int main()
{
    rscp::RequestEnvelope request;

    // Simulated raw COBS-encoded data stream (might represent multiple frames)
    std::vector<uint8_t> simulated_data = {
        0x05, 0x0A, 0x02, 0x08, 0x01, 0x00, 0x05, 0x12, 0x02, 0x08, 0x03, 0x00, 0x1C, 0x1A, 0x19, 0x0A, 0x17,
        0x09, 0x58, 0x39, 0xB4, 0xC8, 0x76, 0xBE, 0xF3, 0x3F, 0x11, 0x83, 0xC0, 0xCA, 0xA1, 0x45, 0xB6, 0x16,
        0x40, 0x1D, 0xA1, 0xD6, 0x7C, 0x3F, 0x00, 0x18, 0x22, 0x19, 0x0A, 0x12, 0x09, 0x58, 0x39, 0xB4, 0xC8,
        0x76, 0xBE, 0xF3, 0x3F, 0x11, 0x83, 0xC0, 0xCA, 0xA1, 0x45, 0xB6, 0x16, 0x40, 0x15, 0x01, 0x03, 0xC8,
        0x42, 0x00};

    std::vector<uint8_t> buffer;

    // Split the stream into frames using 0x00 as a frame delimiter
    for (auto byte : simulated_data)
    {
        if (byte == 0x00)
        {
            // Process the complete frame
            on_receive(buffer);
            buffer.clear();
        }
        else
        {
            // Accumulate bytes into the current frame
            buffer.push_back(byte);
        }
    }

    return 0;
}
