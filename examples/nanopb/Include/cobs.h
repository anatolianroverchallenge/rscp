
#ifndef COBS_H
#define COBS_H

size_t cobs_decode(uint8_t *out_buf, const uint8_t *in_buf, size_t len) {
    size_t out_idx = 0, in_idx = 0;
    while (in_idx < len) {
        uint8_t code = in_buf[in_idx++];
        for (int i = 1; i < code; i++) {
            out_buf[out_idx++] = in_buf[in_idx++];
        }
        if (code != 0xFF && in_idx < len) {
            out_buf[out_idx++] = 0;
        }
    }
    return out_idx;
}

#endif