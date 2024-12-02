from hub import light_matrix, port, motion_sensor
import runloop, motor, motor_pair, math, time

left_motor = port.E
right_motor = port.A

front_motor = port.C
back_motor = port.D
mp = motor_pair.PAIR_1

async def main():
    motor_pair.pair(mp, left_motor, right_motor)

    # await test_motors()
    # await drive_each_direction()

    c = Controller()
    # await c.figure_out_yaw()
    await c.drive_p()
    await c.drive_p(cm=10)
    await c.drive_p(angle_goal_change=100)

    #return await motor_pair.move_for_degrees(mp, 360, 0)

class Controller:
    def __init__(self):
        wheel_diameter = 8.7
        self.cm_per_deg = 8.7 * math.pi / 360

        motion_sensor.reset_yaw(0)
        self.last_yaw = 0
        self.wraps = 0
        self.angle_goal = self.angle()

        motor.reset_relative_position(left_motor, 0)
        motor.reset_relative_position(right_motor, 0)
        self.position_goal = self.position()

    def degrees(self, cm):
        return cm / self.cm_per_deg

    def cm(self, deg):
        return deg * self.cm_per_deg

    # Returns degrees turned overall since the start.
    # Positive is left, negative is right.
    # This assumes that it's been called with less than ~160 degrees of movement since the last call.
    def angle(self):
        yaw, _, _ = motion_sensor.tilt_angles()
        if yaw > 1000 and self.last_yaw < -1000:
            self.wraps -= 1
        if yaw < -1000 and self.last_yaw > 1000:
            self.wraps += 1
        self.last_yaw = yaw
        return 360 * self.wraps + (yaw / 10)

    # Gets the total amount moved so far, in cm.
    def position(self):
        lp = motor.relative_position(left_motor)
        rp = motor.relative_position(right_motor)
        return self.cm((lp + rp) / 2)

    # Figure out what the yaw is like.
    # It starts at 0.
    # Turning left makes yaw go higher, until it gets to 1800, then it switches to negative.
    # Don't actually use this, though.
    async def figure_out_yaw(self):
        for i in range(20):
            if i > 5 and i < 15:
                dir = 100
            else:
                dir = -100
            await motor_pair.move_for_time(mp, 200, dir)
            yaw, _, _ = motion_sensor.tilt_angles()
            print("{}: yaw={} angle={} position={}".format(i, yaw, self.angle(), self.position()))

    # Drive a little bit using a proportional gyro move.
    # Velocity is cm per second. (spike takes degrees per second.)
    # Note: Spike velocity for large motors can be up to 1050 deg / sec.
    # Angle_goal is in degrees. Positive is left, negative is right.
    # Checking relative position is fast (about 30,000 per second).
    async def drive_p(self, cm = 0, velocity = 1, angle_goal_change = 0):
        self.position_goal += cm
        self.angle_goal += angle_goal_change
        print("new goal: pos={} vs {}, angle={} vs {}".format(self.position_goal, self.position(), self.angle_goal, self.angle()))

# Drive a little bit in each direction.
async def drive_each_direction():
    # 100 spins in place, one wheel forwards, the other backwards.
    # 50 spins one wheel and leaves the other in place.
    # 0 is straight.
    dirs = [-100, -75, -50, -25, 0, 25, 50, 75, 100]
    for d in dirs:
        light_matrix.write("{}".format(d))
        await motor_pair.move_for_degrees(mp, 180, d, velocity = 50)

# Spin each motor a little.
async def test_motors():
    motor_ports = [
        ("front", front_motor),
        ("back", back_motor),
        ("left", left_motor),
        ("right", right_motor)
    ]
    for l, p in motor_ports:
        light_matrix.write(l)
        await motor.run_for_time(p, 3000, 50)

runloop.run(main())
