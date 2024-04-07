import asyncio

from bot_app import *
from web_app import *

async def main():
    await bot.start_bot()
    await app.run()
    
if __name__ == '__main__':
    asyncio.run(main())