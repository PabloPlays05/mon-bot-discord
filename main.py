import asyncio
import bot1
import bot2

RUN_BOT1 = True
RUN_BOT2 = True

async def main():
    print("🚀 START MAIN")

    tasks = []

    if RUN_BOT1:
        tasks.append(bot1.start_bot())

    if RUN_BOT2:
        tasks.append(bot2.start_bot())

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())