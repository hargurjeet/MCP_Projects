import arxiv
import json
import os
from typing import List
from dotenv import load_dotenv
import anthropic

load_dotenv()

PAPER_DIR = "/tmp/papers"
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for research papers from arXiv on a given topic and store their information in a local directory.

    Args:
        topic (str): The research topic to search for.
        max_results (int, optional): Maximum number of search results to return. Defaults to 5.

    Returns:
        List[str]: A list of short IDs of the retrieved papers.
    """
    client_arxiv = arxiv.Client()
    search = arxiv.Search(query=topic, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
    papers = client_arxiv.results(search)

    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "papers_info.json")

    try:
        with open(file_path, "r") as f:
            papers_info = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        papers_info[paper.get_short_id()] = {
            "title": paper.title,
            "authors": [a.name for a in paper.authors],
            "summary": paper.summary,
            "pdf_url": paper.pdf_url,
            "published": str(paper.published.date())
        }

    with open(file_path, "w") as f:
        json.dump(papers_info, f, indent=2)

    return paper_ids

def extract_info(paper_id: str) -> str:
    """
    Retrieve information about a paper with a given paper ID from locally saved topic directories.

    Args:
        paper_id (str): The short ID of the paper to look up.

    Returns:
        str: A formatted JSON string of the paper's information, or an error message if not found.
    """
    for topic_dir in os.listdir(PAPER_DIR):
        dir_path = os.path.join(PAPER_DIR, topic_dir)
        if os.path.isdir(dir_path):
            file_path = os.path.join(dir_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as f:
                        papers_info = json.load(f)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError):
                    continue
    return f"No saved info for paper ID: {paper_id}"


tools = [
    {
        "name": "search_papers",
        "description": "Search for papers on arXiv.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "extract_info",
        "description": "Get details about a specific paper ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "paper_id": {"type": "string"}
            },
            "required": ["paper_id"]
        }
    }
]

mapping_tool_function = {
    "search_papers": search_papers,
    "extract_info": extract_info
}

def execute_tool(tool_name, tool_args):
    """
    Execute a tool function by its name using provided arguments and return the result.

    Args:
        tool_name (str): Name of the tool to execute (must exist in mapping_tool_function).
        tool_args (dict): Arguments to pass to the tool function.

    Returns:
        str: Stringified result of the tool function execution.
    """
    result = mapping_tool_function[tool_name](**tool_args)
    if result is None:
        return "No results returned."
    if isinstance(result, list):
        return ', '.join(result)
    if isinstance(result, dict):
        return json.dumps(result, indent=2)
    return str(result)

def process_query(query):
    """
    Processes a user query using Claude 3 Sonnet and integrated tools, returning the assistant's final response.

    Args:
        query (str): The user input.

    Returns:
        str: Final assistant response as text.
    """
    messages = [{'role': 'user', 'content': query}]

    response = client.messages.create(
        max_tokens=2024,
        model='claude-3-7-sonnet-20250219', 
        tools=tools,
        messages=messages
    )

    process_query = True
    final_output = ""

    while process_query:
        assistant_content = []

        for content in response.content:
            if content.type == 'text':
                final_output = content.text
                assistant_content.append(content)

                # If only a simple reply, we’re done
                if len(response.content) == 1:
                    process_query = False

            elif content.type == 'tool_use':
                assistant_content.append(content)
                messages.append({'role': 'assistant', 'content': assistant_content})

                tool_id = content.id
                tool_args = content.input
                tool_name = content.name

                print(f"Calling tool {tool_name} with args {tool_args}")
                result = execute_tool(tool_name, tool_args)

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result
                        }
                    ]
                })

                response = client.messages.create(
                    max_tokens=2024,
                    model='claude-3-7-sonnet-20250219', 
                    tools=tools,
                    messages=messages
                )

                # If the assistant now only sends text, we're done
                if len(response.content) == 1 and response.content[0].type == "text":
                    final_output = response.content[0].text
                    process_query = False

    return final_output