import asyncio
import os
import sys

import httpx
from dotenv import load_dotenv
from dto import ServerInfo
from httpx._transports import default
from settings import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:  # Ensure the update contains a message
        if context.args:
            parameter = context.args[0]  # The first argument after /start
            await update.message.reply_text(
                f"Received parameter: {parameter}"
            )  # Create buttons
        keyboard = [
            [InlineKeyboardButton("Authorization", callback_data="authorize")],
            [InlineKeyboardButton("Cancel", callback_data="cancel")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send message with buttons
        await update.message.reply_text(
            f"Hi {update.message.from_user.username}! Please choose an option:",
            reply_markup=reply_markup,
        )


# Define a callback query handler for button clicks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        print("No callback query found in update!")
        return
    await query.answer()  # Acknowledge the callback query
    # Handle button clicks
    if query.data == "authorize":
        await query.edit_message_text("You chose Authorization!")
    elif query.data == "cancel":
        await query.edit_message_text("You canceled the operation.")


def get_proxy(proxy_url_get: str, default: str) -> str:
    response = httpx.get(proxy_url_get)
    data = response.json()
    proxy_url = ""
    if len(data) != 0:
        proxy_url = ServerInfo.model_validate(data[0]).get_link()
    return proxy_url if proxy_url else default


# Define the /start command handler
def main():
    """
    Handles the initial launch of the program (entry point).
    """
    proxy_url = "socks5://5.182.37.30:1080"
    proxy_url = get_proxy(settings.get_proxy_url, default=proxy_url)
    print(proxy_url)
    application = (
        Application.builder()
        .token(settings.tg_token)
        .concurrent_updates(True)
        # .read_timeout(30)
        .proxy(proxy_url)
        .get_updates_proxy(proxy_url)
        # .write_timeout(30)
        .build()
    )
    print("Telegram Bot started!", flush=True)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()


if __name__ == "__main__":
    main()
