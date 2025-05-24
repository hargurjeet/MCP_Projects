# ResearchGPT: An Intelligent Research Paper Discovery Assistant

ResearchGPT is a Streamlit-based chatbot application that helps users explore and understand research papers from arXiv. The application leverages the Claude 3 Sonnet language model to provide intelligent paper search, summarization, and analysis capabilities through a user-friendly chat interface.

The application enables users to search for papers on specific topics, retrieve detailed information about individual papers, and engage in natural language conversations about research content. It integrates directly with the arXiv API for real-time paper searches and uses advanced language processing to provide meaningful insights and summaries. The interactive chat interface makes academic research exploration more accessible and efficient.

## Repository Structure
```
MCP_Projects/
├── Dockerfile              # Container configuration for deployment
├── requirements.txt        # Python package dependencies
└── src/                   # Application source code
    ├── streamlit_app.py   # Main Streamlit application entry point
    └── utils/
        └── paper_tools.py # Core paper search and processing utilities
```

## Usage Instructions
### Prerequisites
- Python 3.9 or higher
- Docker (optional, for containerized deployment)
- Anthropic API key for Claude 3 Sonnet access

Required Python packages:
- streamlit
- arxiv
- python-dotenv
- anthropic

### Installation

#### Local Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd MCP_Projects
```

2. Create and activate a virtual environment:
```bash
# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

#### Docker Installation
1. Build the Docker image:
```bash
docker build -t researchgpt .
```

2. Run the container:
```bash
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your_api_key_here researchgpt
```

### Quick Start
1. Start the application:
```bash
streamlit run src/streamlit_app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter queries in the chat interface, such as:
- "Search papers on large language models"
- "Summarize paper 2403.00001"
- "Find research on agentic AI"

### More Detailed Examples
1. Searching for papers:
```python
# Example query
"Find recent papers about transformer architectures in deep learning"
```

2. Getting paper details:
```python
# Example query
"Tell me more about paper 2403.00001"
```

### Troubleshooting

Common Issues:
1. API Key Issues
   - Error: "ANTHROPIC_API_KEY not found"
   - Solution: Ensure the API key is properly set in the .env file or environment variables
   - Debug: `echo $ANTHROPIC_API_KEY` to verify the key is set

2. Paper Storage Issues
   - Error: "Permission denied: '/tmp/papers'"
   - Solution: Ensure the /tmp directory has proper write permissions
   - Debug: `chmod 777 /tmp` in the container or local environment

3. Streamlit Connection Issues
   - Error: "Could not connect to Streamlit server"
   - Solution: Check if port 8501 is available
   - Debug: `netstat -ano | grep 8501` to check port usage

## Data Flow
ResearchGPT processes user queries through a pipeline that connects arXiv paper search, local storage, and natural language processing using Claude 3 Sonnet.

```ascii
User Query → Streamlit UI → Claude 3 Sonnet → arXiv API
                ↑                   ↓
                ↑    Local Storage  ↓
                ←←←←←←←←←←←←←←←←←←←←
```

Component Interactions:
1. User submits query through Streamlit interface
2. Query is processed by Claude 3 Sonnet to determine intent
3. Paper search requests are sent to arXiv API when needed
4. Paper information is cached in local storage (/tmp/papers)
5. Claude 3 Sonnet processes paper information and generates responses
6. Responses are formatted and displayed in the Streamlit UI
7. Chat history is maintained in Streamlit session state