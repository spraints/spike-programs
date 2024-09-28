from hub import port
import motor_pair
import runloop

async def main():
    velocity = 50 # Secret number 1
    steering = 0 # Secret number 2
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, steering, velocity = velocity)

runloop.run(main())
