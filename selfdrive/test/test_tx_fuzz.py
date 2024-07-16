
from selfdrive.car.body.interface import CarInterface
from selfdrive.test.helpers import with_processes

@with_processes
def tx_fuzz_test(car_brand):
    """
    Fuzz the transmitted CAN messages and assert that panda accepts them.
    """
    car_interface = CarInterface.get_car_interface_from_brand(car_brand)

    for _ in range(100):
        # Generate a random CarControl message
        cc = car_interface.create_fake_carcontrol()

        # Transmit the CAN messages using the safety_tx_hook
        for msg in cc.canMonoTxPackets:
            assert car_interface.safety_tx_hook(msg), "Panda should accept TX messages"

            # Check if controls are allowed
            if not car_interface.CP.controlsAllowed:
                assert msg.tx == False, "TX should be False when controls are not allowed"