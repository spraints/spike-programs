from hub import light_matrix
import runloop

async def main():
    # write your code here
    await light_matrix.write("Hi boom!")

runloop.run(main())
