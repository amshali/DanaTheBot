from chat import chat_with_retry
from conversation_manager import ConversationManager
from telegram import Message
from langchain_core.messages import SystemMessage


class Dana:
    def __init__(
        self,
        me_id: str,
        conv_manager: ConversationManager,
    ):
        self.me_id = me_id
        self.conv_manager = conv_manager

    async def process_message(
        self,
        message: Message,
    ) -> str:
        """Process a single incoming message."""
        print(f"Processing message: {message}")
        reply_context = None
        if message.reply_to_message and message.reply_to_message.text:
            reply_context = message.reply_to_message.text
        elif message.reply_to_message and message.reply_to_message.caption:
            reply_context = message.reply_to_message.caption
        elif message.quote and message.quote.text:
            reply_context = message.quote.text
        history = self.conv_manager.get_user_history(message.from_user.id)
        if reply_context:
            reply_to_input = f"QUOTED MESSAGE: {reply_context}"
            history.append(SystemMessage(content=reply_to_input))
        response, openai_cb = await chat_with_retry(
            self.conv_manager.get_user_agent(message.from_user.id),
            message.text,
            history,
        )
        return response
