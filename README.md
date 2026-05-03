# Rover Satellite Communications Protocol
Rover Satellite Communications Protocol is a protocol for communicating with a rover over a serial connection. This project is designed for [Anatolian Rover Challenge (ARC)](www.anatolianrover.space/).

<h2>If you are a competitor in <strong>ARC'26</strong>, please watch this repository to get notified about the updates.</h2>

**Also check out [Discussions](https://github.com/anatolianroverchallenge/rscp/discussions) for updates and questions.**

# Issue Tracking
Please use the [GitHub issue tracker](https://github.com/anatolianroverchallenge/rscp/issues) to report issues or request features.
https://github.com/anatolianroverchallenge/rscp/releases

# Releases
The latest release can be found on the [GitHub releases page](https://github.com/anatolianroverchallenge/rscp/releases). If you cannot see any releases, hold tight! We are working hard.

# Table of Contents
- [Rover Satellite Communications Protocol](#rover-satellite-communications-protocol)
- [Issue Tracking](#issue-tracking)
- [Releases](#releases)
- [Table of Contents](#table-of-contents)
- [Details](#details)
  - [Frame Format](#frame-format)
  - [Communication Sequence](#communication-sequence)
    - [Stage 1 Antenna Installation](#stage-1-antenna-installation)
    - [Stage 2 Shackleton Crater](#stage-2-shackleton-crater)
    - [Stage 3 Lava Tube](#stage-3-lava-tube)
    - [Stage 4 Return to Airlock](#stage-4-return-to-airlock)
- [Getting Started](#getting-started)
  - [Installation of python package](#installation-of-python-package)
  - [Examples](#examples)
- [License](#license)
- [Authors](#authors)
- [Acknowledgements](#acknowledgements)

# Details
RSCP now uses [Google Protocol Buffers](https://developers.google.com/protocol-buffers) for serialization and deserialization of messages. This means you don't have to manually serialize/deserialize RSCP messages. 

You can use the provided `.proto` files under [proto](proto) directory to generate the necessary classes for your language. Refer to the [official documentation](https://protobuf.dev/getting-started/) for more information. You can use the official `protoc` compiler to generate the necessary classes for your language, or you can use the pre-generated classes provided in this repository, which can be found in the [releases](https://github.com/anatolianroverchallenge/rscp/releases). Always use the latest release for the most up-to-date classes.

The releases will have [c.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/c.zip) [cpp.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/cpp.zip) [rscp_protobuf.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/rscp_protobuf.zip) [nanopb.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/nanopb.zip) [index.html](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/index.html) files which contain the necessary classes for the respective languages, generated using the `.proto` files in the [proto](proto) directory using the `protoc` compiler.

| Language      | File                                                                                                            | Description                                         |
| ------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| C             | [c.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/c.zip)                         | C source files                                      |
| C++           | [cpp.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/cpp.zip)                     | C++ source files                                    |
| rscp_protobuf | [rscp_protobuf.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/rscp_protobuf.zip) | Python source files (pip3 install <url> to install) |
| nanopb        | [nanopb.zip](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/nanopb.zip)               | C source and header files for nanopb library        |
| docs          | [index.html](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/index.html)               | Documentation for the protocol                      |

You may use `rscp_protobuf.zip` under the [releases](https://github.com/anatolianroverchallenge/rscp/releases) to install the python package using `pip3 install https://github.com/anatolianroverchallenge/rscp/releases/latest/download/rscp_protobuf.zip`

The `nanopb` library is used to generate the C/C++ source and header files that can be used in embedded systems. Refer to the [official documentation](https://jpa.kapsi.fi/nanopb/) and [nanopb examples](https://github.com/nanopb/nanopb/tree/master/examples) for more information.

You may find the latest Protobuf documentation of the protocol [here](https://github.com/anatolianroverchallenge/rscp/releases/latest/download/index.html)

## Frame Format

To communicate with the RSCP module, all you need to do is:

- Create a `rscp.ResponseEnvelope` object
- Fill out the appropriate fields
- Serialize the object using the `SerializeToString` method
- Encode it with `cobs` encoding. For python you can use the `cobs` package.
- Send the encoded message to the rover over serial

To receive an instruction from the RSCP module, you need to:
- Receive the message from the serial port and accumulate it over a buffer
- If `0x00` is received, decode the message using `cobs` decoding
- Parse the message using the `rscp.RequestEnvelope` object
- Use `request.WhichOneof('request')` to determine the type of the message
- Use the appropriate method to handle the data

## Communication Sequence

RSCP client module will be sending host messages to the rovers in `rscp.RequestEnvelope` format. The rovers will be sending responses to the host in `rscp.ResponseEnvelope` format.

### Stage 1 Antenna Installation

| Message Type               | Direction        | Description                                         | light           |
| -------------------------- | ---------------- | --------------------------------------------------- | --------------- |
| SetStage(1)                | HM -> CM         | --                                                  | :heart:         |
| SetStage(1)                | **CM -> Rover**  | Rover sets the stage to 1                           | :heart:         |
| Acknowledge                | **Rover -> CM**  | Rover acknowledges the stage setting                | :heart:         |
| Acknowledge                | CM -> HM         | --                                                  | :heart:         |
| ArmDisarm(arm=True)        | HM -> CM         | --                                                  | :heart:         |
| ArmDisarm(arm=True)        | **CM -> Rover**  | Rover arms itself                                   | :green_heart:   |
| Acknowledge                | **Rover -> CM**  | Rover acknowledges the arming request               | :green_heart:   |
| Acknowledge                | CM -> HM         | --                                                  | :green_heart:   |
| SearchArea(lat1,lon1,rad1) | HM -> CM         | --                                                  | :green_heart:   |
| SearchArea(lat1,lon1,rad1) | **CM -> Rover**  | Rover starts receives area coordinates              | :green_heart:   |
| Acknowledge                | **Rover -> CM**  | Rover acknowledges and starts navigation and search | :yellow_heart:  |
| Acknowledge                | CM -> HM         | --                                                  | :yellow_heart:  |
| no message sent            | --               | finished navigating and searching                   | :yellow_heart:  |
| no message sent            | --               | install antenna                                     | :yellow_heart:  |
| GPSCoordinate(lat2,lon2)   | **Rover -> CM**  | Rover sends coordinates of the peak                 | :yellow_heart:  |
| GPSCoordinate(lat2,lon2)   | CM -> HM         | --                                                  | :yellow_heart:  |
| TaskCompleted              | **Rover -> CM**  | rover reports navigation finished                   | :green_heart:   |
| TaskCompleted              | CM -> HM         | --                                                  | :green_heart:   |

  
  
### Stage 2 Shackleton Crater

| Message Type               | Direction        | Description                                         | light           |
| -------------------------- | ---------------- | --------------------------------------------------- | --------------- |
| SetStage(2)                | HM -> CM         | --                                                  | :green_heart:   |
| SetStage(2)                | **CM -> Rover**  | Rover sets the stage to 2                           | :green_heart:   |
| Acknowledge                | **Rover -> CM**  | Rover acknowledges the stage setting                | :green_heart:   |
| Acknowledge                | CM -> HM         | --                                                  | :green_heart:   |
| SearchArea(lat3,lon3,rad3) | HM -> CM         | --                                                  | :green_heart:   |
| SearchArea(lat3,lon3,rad3) | **CM -> Rover**  | Rover starts receives area coordinates              | :green_heart:   |
| Acknowledge                | **Rover -> CM**  | Rover acknowledges and starts navigation and search | :yellow_heart:  |
| Acknowledge                | CM -> HM         | --                                                  | :yellow_heart:  |
| no message sent            | --               | finished navigating and searching                   | :yellow_heart:  |
| GPSCoordinate(lat4,lon4)   | **Rover -> CM**  | Rover sends coordinates of the dark-colored Ilmenite-Rich basalt     | :yellow_heart:  |
| GPSCoordinate(lat4,lon4)   | CM -> HM         | --                                                  | :yellow_heart:  |
| TaskCompleted              | **Rover -> CM**  | rover reports navigation finished                   | :green_heart:   |
| TaskCompleted              | CM -> HM         | --                                                  | :green_heart:   |

  
### Stage 3 Lava Tube

| Message Type             | Direction       | Description                                           | light          |
| ------------------------ | --------------- | ----------------------------------------------------- | -------------- |
| SetStage(3)              | HM -> CM        | --                                                    | :green_heart:  |
| SetStage(3)              | **CM -> Rover** | Rover sets the stage to 3                             | :green_heart:  |
| Acknowledge              | **Rover -> CM** | Rover acknowledges the stage setting                  | :green_heart:  |
| Acknowledge              | CM -> HM        | --                                                    | :green_heart:  |
| NavigateToGPS(lat5,lon5) | HM -> CM        | --                                                    | :green_heart:  |
| NavigateToGPS(lat5,lon5) | **CM -> Rover** | Rover starts receives lava tube enterance coordinates | :green_heart:  |
| Acknowledge              | **Rover -> CM** | Rover acknowledges and starts navigation              | :yellow_heart:  |
| Acknowledge              | CM -> HM        | --                                                    | :yellow_heart: |
| no message sent          | --              | finished navigating                                   | :yellow_heart: |
| TaskCompleted            | **Rover -> CM** | rover reports navigation finished                     | :green_heart:  |
| TaskCompleted            | CM -> HM        |                     | :green_heart:  |
| no message sent          | --              | Rover locates tag i (lava tube enterance)             | :green_heart:  |
| StartExploration            | HM -> CM        | --                                                    | :green_heart:  |
| StartExploration           | **CM -> Rover** | Rover starts to exploring                             | :green_heart:  |
| Acknowledge              | **Rover -> CM** | Rover acknowledges the message receiving              | :yellow_heart:  |
| Acknowledge              | CM -> HM        | --                                                    | :yellow_heart: |
| no message sent          | --              | continue exploring                                    | :yellow_heart: |
| no message sent          | --              | Rover measures the length of covered section          | :yellow_heart: |
| distance                 | **Rover -> CM** | Rover sends the measured distance                     | :yellow_heart: |
| distance                 | CM -> HM        | --                                                    | :yellow_heart: |
| no message sent          | --              | continue exploring                                    | :yellow_heart: |
| no message sent          | --              | Rover locates tag j (lava tube exit) and exits        | :yellow_heart: |
| TaskCompleted            | **Rover -> CM** | rover reports mission completed                       | :green_heart:  |
| TaskCompleted            | CM -> HM        | --                                                    | :green_heart:  |



### Stage 4 Return to Airlock
| Message Type             | Direction       | Description                                     | light          |
| ------------------------ | --------------- | ----------------------------------------------- | -------------- |
| SetStage(4)              | HM -> CM        | --                                              | :green_heart:  |
| SetStage(4)              | **CM -> Rover** | Rover sets the stage to 3                       | :green_heart:  |
| Acknowledge              | **Rover -> CM** | Rover acknowledges the stage setting            | :green_heart:  |
| Acknowledge              | CM -> HM        | --                                              | :green_heart:  |
| NavigateToGPS(lat6,lon6) | HM -> CM        | --                                              | :green_heart:  |
| NavigateToGPS(lat6,lon6) | **CM -> Rover** | Rover starts receives GPS coordinates           | :green_heart:  |
| Acknowledge              | **Rover -> CM** | Rover acknowledges and starts navigation        | :yellow_heart: |
| Acknowledge              | CM -> HM        | --                                              | :yellow_heart: |
| no message sent          | --              | finished navigating                             | :yellow_heart: |
| TaskCompleted            | **Rover -> CM** | rover reports navigation finished               | :green_heart:  |
| TaskCompleted            | CM -> HM        |              | :green_heart:  |
| no message sent          | --              | Rover locates tag k (airlock enterance)         | :yellow_heart: |
| no message sent          | --              | Rover docks to the airlock                      | :yellow_heart: |
| ArmDisarm(arm=False)     | HM -> CM        | --                                              | :yellow_heart:  |
| ArmDisarm(arm=False)     | **CM -> Rover** | Rover disarms itself, light turns yellow to red | :heart:        |
| Acknowledge              | **Rover -> CM** | Rover acknowledges the arming request           | :heart:        |
| Acknowledge              | CM -> HM        | mission completed.                              | :heart:        |




# Getting Started

## Installation of python package

```bash
python3 -m pip install https://github.com/anatolianroverchallenge/rscp/releases/latest/download/rscp_protobuf.zip

# To test the installation
python3 -c "import rscp_protobuf"
```

## Examples
- [aruco_detection_example.py](examples/aruco_detection_example.py) is an example code to detect the Aruco markers which will be placed in the competition area.

- Check out the [examples/python](examples/python) directory for more examples of the protocol using Python.



# License
This project is licensed under the terms of the [BSD 3-Clause License](LICENSE).

# Authors
* **Sencer Yazici** - [Sencer Yazici](mailto:senceryazici@gmail.com)
* **Yavuz Hanege** - [Yavuz Hanege](mailto:hanegeyavuz@gmail.com)

# Acknowledgements
This project is developed for [Anatolian Rover Challenge (ARC)](https://www.anatolianrover.space/)
