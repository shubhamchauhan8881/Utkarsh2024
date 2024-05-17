import asyncio
async def main():
    print('Hello ...1')
    await asyncio.sleep(1)
    print('... World!1')

async def main2():
    print('Hello ...2')
    await asyncio.sleep(1)
    print('... World!2')


asyncio.run(main())
asyncio.run(main2())