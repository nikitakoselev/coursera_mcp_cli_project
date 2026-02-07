from pydantic import Field  
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and return it as a string.",
)
def read_document(
    doc_id: str = Field(description="The ID of the document to read. For example, 'report.pdf'.")
):
    if doc_id not in docs:
        raise ValueError(f"Error: Document with ID '{doc_id}' not found.")
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edits the contents of a document by replaceing a string in the document with a new string.",
)
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit. For example, 'report.pdf'."),
    old_str: str = Field(description="The string in the document to replace. Must match exactly, including whitespace and punctuation."),
    new_str: str = Field(description="The new string to replace the target string with."),
):
    if doc_id not in docs:
        raise ValueError(f"Error: Document with ID '{doc_id}' not found.")
    if old_str not in docs[doc_id]:
        raise ValueError(f"Error: Target string '{old_str}' not found in document '{doc_id}'.")
    
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Document '{doc_id}' updated successfully."

# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
