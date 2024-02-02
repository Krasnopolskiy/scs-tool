import asyncio

from dotenv import load_dotenv

from cli.executors import execute

load_dotenv()

if __name__ == "__main__":
    asyncio.run(execute())
