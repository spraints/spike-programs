from hub import port
import color_sensor
import motor_pair
import runloop

async def main():
    left_motor_port = port.B
    right_motor_port = port.A
    light_sensor_port = port.C
    drive_pair = motor_pair.PAIR_1

    dark_color = 30
    light_color = 100

    drive_duration = 15000 # milliseconds
    interval = 50 # milliseconds

    motor_pair.pair(drive_pair, left_motor_port, right_motor_port)

    steps = int(drive_duration / interval)
    mid = int((dark_color + light_color) / 2)

    for i in range(steps):
        lightness = color_sensor.reflection(light_sensor_port)
        steering = lightness - mid
        motor_pair.move(drive_pair, steering, velocity = 90)
        await runloop.sleep_ms(interval)

    motor_pair.stop(drive_pair)

runloop.run(main())
