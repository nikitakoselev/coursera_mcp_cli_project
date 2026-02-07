# core/local_llm.py
import asyncio
from gpt4all import GPT4All
from types import SimpleNamespace

class LocalLLM:
    def __init__(self, model_path="Meta-Llama-3-8B-Instruct.Q4_0.gguf"):
        self.model = GPT4All(model_path)

    async def complete(self, prompt, max_tokens=512):
        # Run blocking GPT4All.generate in a separate thread
        return await asyncio.to_thread(self.model.generate, prompt, max_tokens=max_tokens)

    async def chat(self, messages=None, tools=None, max_tokens=512, **kwargs):
        # Convert messages to prompt
        if messages:
            prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        else:
            prompt = ""

        completion_text = await self.complete(prompt, max_tokens=max_tokens)

        # Return object compatible with MCP
        return SimpleNamespace(
            completion=completion_text,
            stop_reason="stop"
        )

    @staticmethod
    def add_assistant_message(messages, message):
        messages.append({"role": "assistant", "content": message})

    @staticmethod
    def add_user_message(messages, message):
        messages.append({"role": "user", "content": message})

    @property
    def model_name(self):
        return "local_gpt4all"
    
    def text_from_message(self, message: SimpleNamespace) -> str:
        """
        Drop-in replacement for Claude.text_from_message().
        Extracts the text/completion from the message object.
        """
        return getattr(message, "completion", "")
