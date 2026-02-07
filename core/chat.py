# core/chat.py
from core.claude import Claude
from mcp_client import MCPClient
from core.tools import ToolManager
from anthropic.types import MessageParam


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(self, query: str) -> str:
        """
        Run a single chat turn.
        Returns the assistant response as a string.
        Supports 'exit', 'quit', 'stop' to immediately end the conversation.
        """
        # --- Early exit ---
        if query.strip().lower() in ("exit", "quit", "stop"):
            print("Goodbye!")
            return None  # signal to CLI that conversation should stop

        await self._process_query(query)

        while True:
            # Await response from LLM (Claude or LocalLLM)
            response = await self.claude_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            # Add assistant response to history if available
            if hasattr(self.claude_service, "add_assistant_message"):
                self.claude_service.add_assistant_message(self.messages, response)

            # Determine stop reason safely
            stop_reason = getattr(response, "stop_reason", None)

            if stop_reason == "tool_use":
                # Assistant wants to use a tool
                print(self.claude_service.text_from_message(response))
                tool_results = await ToolManager.execute_tool_requests(
                    self.clients, response
                )
                if hasattr(self.claude_service, "add_user_message"):
                    self.claude_service.add_user_message(self.messages, tool_results)
            else:
                # Normal completion
                final_text = self.claude_service.text_from_message(response)
                return final_text
