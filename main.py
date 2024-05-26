import os
import argparse
from dotenv import load_dotenv
import logging
from langchain_openai import ChatOpenAI
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from langchain.agents import load_tools

from conversation_manager import ConversationManager
from dana import Dana
from prompts import answer_prompt
import time

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class DanaTheBot:
    def __init__(self):
        loaded_tools = []
        if os.getenv("OPENWEATHERMAP_API_KEY") is not None:
            loaded_tools.extend(load_tools(["openweathermap-api"]))
        if os.getenv("GOOGLE_API_KEY") is not None:
            loaded_tools.extend(load_tools(["google-search"]))

        llm = ChatOpenAI(model=os.getenv("OPEN_AI_MODEL_NAME"), temperature=0.2)
        conv_manager = ConversationManager(
            loaded_tools,
            llm,
            answer_prompt,
        )
        token = os.getenv("BOT_TOKEN")
        self.dana = Dana(
            int(token.split(":")[0]),
            conv_manager,
        )
        self.application = ApplicationBuilder().token(token).build()
        start_handler = CommandHandler(
            "start",
            self.start,
            filters=filters.User(username=os.getenv("ALLOWED_USERS").split(",")),
        )
        self.application.add_handler(start_handler)
        answer_handler = MessageHandler(
            filters.TEXT
            & (~filters.COMMAND)
            & filters.User(username=os.getenv("ALLOWED_USERS").split(",")),
            self.answer,
        )
        self.application.add_handler(answer_handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"""
I'm a Dana, your personal assitant. I can tell you about the weather, news, or
provide you with information or opinion about pretty much any subject you want.

Have fun!
--
Soy Dana, tu asistente personal. Puedo informarte sobre el clima, las noticias o proporcionarte información u opinión sobre prácticamente cualquier tema que desees.

¡Diviértete!
--
من دانا هستم، دستیار شخصی شما. می‌توانم در مورد آب و هوا، اخبار، یا ارائه اطلاعات یا نظر در مورد تقریباً هر موضوعی که بخواهید به شما بگویم.

خوش بگذره!
    """,
        )

    async def answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_to_process = update.edited_message
        if update.message:
            message_to_process = update.message
        else:
            message_to_process = update.edited_message
        print("Message from user", message_to_process.from_user)
        response = await self.dana.process_message(message_to_process)
        if response is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=response
            )

    def run(self):
        self.application.run_polling()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dana The Bot")
    # Add arguments
    parser.add_argument("--env-path", type=str, required=True)

    # Parse the command-line arguments
    args = parser.parse_args()
    # Load environment variables from .env file
    load_dotenv(dotenv_path=args.env_path)
    bot = DanaTheBot()

    bot.run()
