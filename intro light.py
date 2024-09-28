from hub import light_matrix, port, sound
import color_sensor
import runloop

async def main():
    sound.beep(duration=500)
    for i in range(100):
        lightness = color_sensor.reflection(port.B)
        light_matrix.show([lightness] * 25)
        print(lightness)
        await runloop.sleep_ms(100)
    sound.beep(duration=500)
    light_matrix.show_image(light_matrix.IMAGE_ASLEEP)

runloop.run(main())
