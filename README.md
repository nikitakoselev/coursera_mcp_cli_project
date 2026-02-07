# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models. Originally designed to work with the Anthropic API, this version has been extended to support locally running LLMs for experimentation and offline usage. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture. This exercise is based on code from the Coursera course [Introduction to Model Context Protocol](https://www.coursera.org/learn/introduction-to-model-context-protocol/).

---

To set up the project, first ensure you have Python 3.9+ installed. Optionally, you may need Node.js and npm if you are using the `uv` package on Mac or Windows. Create or edit a `.env` file in the project root to include your Anthropic API key if you plan to use it:

```
ANTHROPIC_API_KEY=""
```

Next, install dependencies. You can use `uv`, which is a fast Python package installer and resolver. Install it with `pip install uv`. Then create and activate a virtual environment with `uv venv` and `source .venv/bin/activate` (on Windows: `.venv\Scripts\activate`). Install all dependencies with `uv pip install -e .` and run the project using `uv run main.py`. If `uv run` complains about `npx` missing, install Node.js and npm and restart your terminal. Alternatively, you can set up without `uv` by creating and activating a virtual environment (`python -m venv .venv` and `source .venv/bin/activate`), installing dependencies manually with `pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0" gpt4all`, and running the project with `python main.py`.

This project now supports using a local LLM via GPT4All. Place your model (e.g., `Meta-Llama-3-8B-Instruct.Q4_0.gguf`) in the project folder and ensure `core/local_llm.py` points to the correct model path. The chat interface works without requiring an Anthropic API key. Run it with `uv run main.py` or `python main.py`.

Once running, simply type your message and press Enter to chat with the model. You can stop the session at any time by typing `exit`, `quit`, or `stop`, which will terminate the session gracefully. You can include document content in your queries by using the `@` symbol followed by a document ID, for example: `> Tell me about @deposition.md`. Commands are executed with a `/` prefix, for example: `> /summarize deposition.md`. Commands and document IDs support auto-completion with the Tab key.

To add new documents, edit the `mcp_server.py` file and add them to the `docs` dictionary, for example:

```python
docs = {
    "report.pdf": "Contents of the report...",
    "deposition.md": "Contents of the deposition..."
}
```

You can implement new MCP tools using the `@mcp.tool` decorator. For example:

```python
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and returns it as a string."
)
def read_document(
    doc_id: str = Field(description="The ID of the document, e.g., 'report.pdf'")
):
    if doc_id not in docs:
        raise ValueError(f"Document '{doc_id}' not found.")
    return docs[doc_id]
```

The `Field` function is used to provide metadata about the expected input, such as descriptions, which is used by the interface and auto-completion, while the actual input will be a string provided by the user.

For development, complete any TODOs in `mcp_server.py` and implement missing functionality in `mcp_client.py`. Linting and type checks are not implemented by default, but you can optionally add `flake8` or `mypy` for static analysis: `pip install flake8 mypy` followed by `flake8 .` and `mypy .`.

To preserve your work and push it to GitHub, initialize a Git repository with `git init`, add files with `git add .`, and commit with `git commit -m "Initial commit with local LLM support"`. Create a repository on GitHub (via web or `gh repo create my-mcp-chat --public`) and push your changes: `git branch -M main`, `git remote add origin git@github.com:YOUR_USERNAME/my-mcp-chat.git`, and `git push -u origin main`.

This project enables experimenting with AI interactions both online via Anthropic and offline with local models, supports document retrieval, command execution, and tool extensions, and provides a foundation for further MCP development.
