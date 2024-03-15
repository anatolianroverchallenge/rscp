import unittest
import rscp.message.types as message_types
from rscp.message.broker import Broker
import io
import logging

LOGGER = logging.getLogger(__name__)


class VirtualIO(io.BytesIO):
    def __init__(self):
        self.tx_buffer = bytearray()
        self.rx_buffer = bytearray()

    def write(self, data):
        self.tx_buffer.extend(data)

    def read(self, size):
        data = self.rx_buffer[:size]
        self.rx_buffer = self.rx_buffer[size:]
        return bytes(data)

    def getvalue(self):
        return self.read(len(self.rx_buffer))


class ConnectedIO:
    def __init__(self):
        self.endpoint1 = VirtualIO()
        self.endpoint2 = VirtualIO()

    def handle(self):
        # Transfer data between host and client
        self.endpoint1.rx_buffer.extend(self.endpoint2.tx_buffer)
        self.endpoint2.rx_buffer.extend(self.endpoint1.tx_buffer)

        # clear tx buffers
        self.endpoint1.tx_buffer.clear()
        self.endpoint2.tx_buffer.clear()


class TestBroker(unittest.TestCase):
    def test_two_way_communication(self):
        tx_queue = [
            message_types.Acknowledge(),
            message_types.ArmDisarm(1),
            message_types.TaskFinished(),
            message_types.SetStage(2),
            message_types.Text("Test::String"),
            message_types.LocateTag(5),
            message_types.LocateMultipleTags([3, 4]),
            message_types.Location3D(
                1.100000023841858,
                2.0999999046325684,
                3.0999999046325684,
                "reference::origin",
            ),
            message_types.Detection(
                10,
                message_types.Location3D(
                    1.100000023841858,
                    2.0999999046325684,
                    3.0999999046325684,
                    "reference::world",
                ),
            ),
        ]
        n_messages = len(tx_queue)
        list_id = 0

        n_fired = 0

        def host_on_receive(message):
            nonlocal n_fired
            n_fired += 1
            list_id_trunc = (list_id - 1) % n_messages
            self.assertAlmostEqual(message, tx_queue[list_id_trunc])

        def host_on_send(message):
            nonlocal n_fired
            n_fired += 1
            list_id_trunc = (list_id) % n_messages
            self.assertAlmostEqual(message, tx_queue[list_id_trunc])

        host_broker = Broker(on_receive=host_on_receive, on_send=host_on_send)
        connected_io = ConnectedIO()

        def client_on_receive(message):
            nonlocal n_fired
            n_fired += 1
            list_id_trunc = (list_id - 1) % n_messages
            self.assertAlmostEqual(message, tx_queue[list_id_trunc])

        def client_on_send(message):
            nonlocal n_fired
            n_fired += 1
            list_id_trunc = (list_id) % n_messages
            self.assertAlmostEqual(message, tx_queue[list_id_trunc])

        client_broker = Broker(on_receive=client_on_receive, on_send=client_on_send)

        n_loop_iteration = 50
        for i in range(n_loop_iteration):
            list_id = i % n_messages
            host_broker.dispatch(tx_queue[list_id])
            client_broker.dispatch(tx_queue[list_id])

            host_broker.process(connected_io.endpoint1)
            client_broker.process(connected_io.endpoint2)

            connected_io.handle()

        self.assertEqual(n_fired, 4 * n_loop_iteration - 2)
