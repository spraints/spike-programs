from hub import port
import runloop
import color_sensor
import motor_pair

async def main():
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
    mid = 0 # change this to be halfway between white and black.
    for i in range(100):
        # You may need to change the C to match the port that your light sensor is connected to.
        lightness = color_sensor.reflection(port.C)
        if lightness < mid:
            # ‘return’ stops the current function (main) test edit 3
            return
        else:
            print("keep going!")
        await motor_pair.move_for_degrees(motor_pair.PAIR_1, 45, 0, velocity = 30)

runloop.run(main())
