#ifndef COBS_H
#define COBS_H

#include <vector>
#include <cstdint>
#include <cstddef>

/**
 * @brief Decodes data encoded with Consistent Overhead Byte Stuffing (COBS).
 * 
 * This function takes a buffer of bytes that has been encoded using the COBS
 * algorithm and reconstructs the original data by removing the added overhead
 * bytes and restoring zero delimiters.
 *
 * @param input  Pointer to the COBS-encoded byte buffer.
 * @param length Length of the input buffer.
 * @return std::vector<uint8_t> Decoded byte buffer.
 *
 * @note If the encoded input is malformed (e.g., code byte is 0 or exceeds bounds),
 *       decoding will stop prematurely.
 */
std::vector<uint8_t> cobs_decode(const uint8_t* input, size_t length) {
    std::vector<uint8_t> output;
    output.reserve(length);  // Reserve enough space for the decoded data

    size_t index = 0;
    while (index < length) {
        uint8_t code = input[index];

        // Stop decoding on invalid code byte or if bounds are exceeded
        if (code == 0 || index + code > length + 1)
            break;

        // Copy the next (code - 1) bytes as literal data
        for (uint8_t i = 1; i < code; ++i) {
            output.push_back(input[index + i]);
        }

        // Append a zero byte if the code is not 0xFF (which means no zero was encoded)
        if (code != 0xFF && index + code < length) {
            output.push_back(0);
        }

        index += code;
    }

    return output;
}

#endif // COBS_H
