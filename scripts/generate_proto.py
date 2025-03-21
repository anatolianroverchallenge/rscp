#!/usr/bin/env python3
import os
import subprocess
import sys

# Paths configuration:
# - PROTO_DIR: Directory where your protocol.proto file resides.
# - OUTPUT_DIR: Directory inside your Python package for the generated code.
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PROTO_DIR = os.path.join(BASE_DIR, "proto")
OUTPUT_DIR = os.path.join(BASE_DIR, "src", "python", "proto")


def main():
    # Ensure the output directory exists.
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Define the proto file to compile.
    proto_file = os.path.join(PROTO_DIR, "rscp.proto")

    # Construct the protoc command.
    protoc_cmd = [
        "/usr/local/bin/protoc",
        f"--proto_path={PROTO_DIR}",
        f"--python_out={OUTPUT_DIR}",
        f"--cpp_out={OUTPUT_DIR}",
        f"--rust_out={OUTPUT_DIR}",
        f"--doc_out={OUTPUT_DIR}",
        proto_file,
    ]

    print("Running protoc command:")
    print(" ".join(protoc_cmd))

    try:
        subprocess.run(protoc_cmd, check=True)
        print("Protocol Buffers generated successfully.")
    except subprocess.CalledProcessError as err:
        print("Error generating Protocol Buffers code.", file=sys.stderr)
        sys.exit(err.returncode)


if __name__ == "__main__":
    main()
