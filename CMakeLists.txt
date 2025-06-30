cmake_minimum_required(VERSION 3.15)
project(rscp_cpp_example)

set(CMAKE_CXX_STANDARD 17)

# Protobuf Settings
find_package(Protobuf REQUIRED)
find_package(absl CONFIG REQUIRED)

# Uncomment only if necessary (for Dynamic Linking Errors)
#set(Protobuf_LIBRARIES "<libprotobuf.lib-path>")


include_directories(
    ${Protobuf_INCLUDE_DIR}
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/examples/Cpp
    ${CMAKE_SOURCE_DIR}/examples/Cpp/Include
    ${CMAKE_SOURCE_DIR}/examples/Cpp/proto
)

add_executable(receive_commands_noserial
    examples/Cpp/receive_commands_noserial.cpp
    examples/Cpp/proto/rscp.pb.cc
)

target_compile_definitions(receive_commands_noserial PRIVATE blurb)


target_link_libraries(receive_commands_noserial
    ${Protobuf_LIBRARIES}
    absl::base
    absl::log_internal_check_op
    absl::log_severity
    absl::strings
)
# Protobuf Lib Path Debug
message(STATUS "Protobuf libs: ${Protobuf_LIBRARIES}")

