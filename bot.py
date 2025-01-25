import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject

from pybook import PyBook

from config import BOT_TOKEN


bot = Bot(BOT_TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def hello(message: Message):
    await message.answer("Hello, I am need for work with marimo")


@dp.message(Command("marimo"))
async def marimo(message: Message, command: CommandObject):
    args = command.args

    if not args:
        await message.answer("You must use this command with args")

    elif args == "stop":
        PyBook.stop_marimo(message.from_user.id)
        await message.answer("You session closed")

    else:
        args_split = args.split()

        if len(args_split) > 2:
            await message.answer("To many args")
            return

        url = PyBook.start_marimo(message.from_user.id, args_split[0], args_split[1])
        await message.answer(f"Marimo started. Your URL: {url}")


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
