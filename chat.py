from langchain_core.messages import AIMessage, HumanMessage
import asyncio
from langchain_community.callbacks import get_openai_callback
from langchain.agents import AgentExecutor


async def chat_with_retry(agent_executor: AgentExecutor, message: str, chat_history):
    retries = 3
    while retries > 0:
        try:
            with get_openai_callback() as cb:
                response = agent_executor.invoke(
                    {"input": message, "chat_history": chat_history}
                )
                chat_history.append(HumanMessage(content=message))
                chat_history.append(AIMessage(content=response["output"]))
                if len(chat_history) > 30:
                    chat_history.pop(0)
                    chat_history.pop(0)
                return response["output"], cb
        except Exception as e:
            print(f"An exception occurred: {e}")
            retries -= 1
            print(f"Retrying... (Remaining retries: {retries})")
            await asyncio.sleep(1)
    return None, None
