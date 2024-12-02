import runloop
import math
import motor_pair, motor
from hub import port, device_uuid, motion_sensor

LARGE_BLUE_WHEEL = 8.7 # mm

async def main():
    ace = AdvancedBase()
    ace.debug()
    await runloop.sleep_ms(1000)
    ace.debug()

    # draw an H
    await ace.drive_forward(80)
    await ace.show_state()
    await ace.drive_backward(40)
    await ace.turn_right(90)
    await ace.drive_forward(40)
    await ace.turn_left(90)
    await ace.drive_forward(40)
    await ace.drive_backward(80)

    await runloop.sleep_ms(1000)
    ace.debug()

class AdvancedBase:
    def __init__(self, leftmotor=port.A, rightmotor=port.B, motorpair=motor_pair.PAIR_1, wheeldiameter_cm=LARGE_BLUE_WHEEL):
        self.mp = motor_pair.pair(motorpair, leftmotor, rightmotor)
        self.lm = leftmotor
        self.wd = wheeldiameter_cm
        self.angle_goal = 0
        motion_sensor.reset_yaw(0)

    async def drive_forward(self, cm):
        goal_position = motor.relative_position(self.lm) + self.degrees(cm)
        # while goal_position < motor.relative_position(self.lm):
        #     print("todo")
        print("todo: drive forward {} cm".format(cm))

    async def drive_backward(self, cm):
        print("todo: drive backward {} cm".format(cm))

    async def turn_left(self, degrees):
        print("todo: turn left {} degrees".format(degrees))

    async def turn_right(self, degrees):
        print("todo: turn right {} degrees".format(degrees))

    def debug(self):
        print("[{}] current angle: {}, goal: {}".format(device_uuid(), self.angle_goal, self.get_yaw()))

    def get_yaw(self):
        return motion_sensor.tilt_angles()[0] / 10

    def degrees(self, cm):
        return cm * 360 / (math.pi * self.wd)

runloop.run(main())
