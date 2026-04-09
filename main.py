import asyncio
import bot1
import bot2

async def main():
    await asyncio.gather(
        bot1.start_bot(),
        bot2.start_bot()
    )

asyncio.run(main())