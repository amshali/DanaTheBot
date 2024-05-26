from langchain.agents import AgentExecutor, create_openai_tools_agent


class ConversationManager:
    def __init__(self, loaded_tools, llm, prompt):
        self.user_conversation = {}
        self.user_history = {}
        self.loaded_tools = loaded_tools
        self.llm = llm
        self.prompt = prompt

    def get_user_agent(self, user_id):
        if user_id in self.user_conversation:
            return self.user_conversation[user_id]
        agent = create_openai_tools_agent(
            tools=self.loaded_tools, llm=self.llm, prompt=self.prompt
        )
        agent_executor = AgentExecutor(
            agent=agent, tools=self.loaded_tools, verbose=False, stream_runnable=False
        )
        self.user_conversation[user_id] = agent_executor
        return self.user_conversation[user_id]

    def get_user_history(self, user_id):
        if user_id in self.user_history:
            return self.user_history[user_id]
        self.user_history[user_id] = []
        return self.user_history[user_id]
