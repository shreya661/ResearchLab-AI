# 🔬 ResearchLab AI

> **A multi-agent AI system that transforms a single research query into a verified, citation-rich research report — automatically.**

![Multi-Agent](https://img.shields.io/badge/AI-Multi--Agent-6C63FF?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama3--70b-orange?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-blueviolet?style=for-the-badge)

---

## 🚀 Problem Statement
Conducting reliable online research is tedious and time-consuming. Users typically have to:
* Query multiple search engines and filter through irrelevant links.
* Read dense articles to extract key facts while avoiding cognitive overload.
* Cross-verify claims across different publications to filter out misinformation and AI hallucinations.
* Manually compile findings, insert formatted citations, and export clean PDF reports.

This process is prone to analytical fatigue and consumes hours of manual effort.

---

## 🧠 Solution Design & Value
ResearchLab AI addresses these problems using a state-of-the-art **Reasoning Agent Workflow** orchestrated via LangGraph:
* **Dynamic Information Gathering**: The pipeline executes multiple queries across the web to secure comprehensive, fresh data instead of relying on static databases.
* **Autonomous Cross-Verification**: A dedicated fact-checker agent cross-references findings from different sources to separate established consensus from isolated/uncertain claims.
* **Transparent Execution**: Instead of a "black-box" loading spinner, WebSocket connection streams the step-by-step progress of each agent live to the React user interface.
* **Professional Export**: Generates beautifully styled PDF or Markdown reports complete with an index of numbered citations mapping claims directly back to their source URLs.

---

## 🏗️ Technical Architecture & LangGraph Workflow

### 1. State Schema (`ResearchState`)
The agent pipeline utilizes a global, shared memory state defined in [coordinator.py](file:///c:/Users/patha/OneDrive/Desktop/capstone/backend/agents/coordinator.py):
* `topic` *(str)*: The target query or question to research.
* `search_results` *(list[dict])*: Extracted and deduplicated search results from Tavily API.
* `summaries` *(list[dict])*: LLM-summarized analysis of each individual source page.
* `verified_facts` *(dict)*: Structured fact-check details (verified facts, contradictions, uncertain claims, and consensus).
* `report_markdown` *(str)*: Compiled research report formatted in Markdown.
* `citations` *(list[dict])*: Formatted citations map mapping URL sources to numbered references.
* `error` *(str)*: Exception message if any step in the pipeline fails.
* `current_agent` *(str)*: The ID of the currently active agent.

### 2. Functional Nodes
The system runs 4 specialized agent nodes:
1. **Search Agent (`search`)**: Generates 3 query variations for the topic, fetches results via Tavily, deduplicates URLs, and retains the top 12 most relevant sources based on score.
2. **Research Agent (`research`)**: Summarizes the content of each deduplicated source using Groq's `llama3-70b-8192` model.
3. **Fact-Check Agent (`factcheck`)**: Performs cross-source correlation to flag contradictions and compile verified consensus.
4. **Report Agent (`report`)**: Integrates facts and citations into a final markdown-formatted research document.

### 3. Graph Routing Layout

```mermaid
graph TD
    START([Start Pipeline]) --> search[Search Agent: Query & Deduplicate]
    search --> cond_search{Check State}
    cond_search -- "Error" --> END([End Pipeline])
    cond_search -- "Success" --> research[Research Agent: Extract & Summarize]
    
    research --> cond_research{Check State}
    cond_research -- "Error" --> END
    cond_research -- "Success" --> factcheck[Fact-Check Agent: Cross-Verify Facts]
    
    factcheck --> cond_factcheck{Check State}
    cond_factcheck -- "Error" --> END
    cond_factcheck -- "Success" --> report[Report Agent: Compile Markdown & Citations]
    
    report --> END
```

---

## 📂 Project Structure

```
capstone/
├── backend/                      # FastAPI Backend
│   ├── main.py                   # FastAPI app entry point and lifespan DB init
│   ├── requirements.txt          # Python packages
│   ├── .env.example              # Environment variables template
│   ├── agents/                   # LangGraph Orchestration & Nodes
│   │   ├── coordinator.py        # Pipeline setup & State Schema
│   │   ├── search_agent.py       # Tavily querying & URL deduplication
│   │   ├── research_agent.py     # Groq LLM page summarization
│   │   ├── factcheck_agent.py    # Fact verification & contradiction identification
│   │   └── report_agent.py       # Final report generation agent
│   ├── tools/                    # Core Utilities
│   │   ├── web_search.py         # Tavily API HTTP client
│   │   └── pdf_generator.py      # ReportLab PDF compiled layout
│   ├── api/                      # Routing & Controller layer
│   │   ├── research.py           # Start, check status, WebSocket, and PDF export routes
│   │   └── history.py            # Session storage & delete endpoints
│   ├── db/                       # SQL Database config
│   │   ├── database.py           # Async engine & sessionmaker setup
│   │   └── models.py             # ResearchSession database model schema
│   └── models/                   # Pydantic schemas
│       └── schemas.py            # Request/Response & WebSocket schemas
│
└── frontend/                     # React Frontend
    ├── index.html                # HTML entry point
    └── src/
        ├── App.jsx               # Navigation, routing, and main styles
        ├── index.css             # Glassmorphism global theme custom rules
        ├── pages/                
        │   ├── Home.jsx          # Start page with search input and history list
        │   └── Research.jsx      # Live websocket progress viewer & report renderer
        └── components/           
            ├── AgentTracker.jsx  # Live agent state indicators
            ├── ReportViewer.jsx  # Markdown-to-HTML parser
            └── CitationList.jsx  # Toggleable citation details panel
```

---

## 🔒 Safety & Verification Features

* **Deny-by-Default Query Filters**: Input queries are sanitized to ensure API safety before triggering external search pipelines.
* **Strict Source Deduplication**: The search agent tracks visited URLs via a strict uniqueness filter, preventing duplicate hits from skewing summaries.
* **Automated Fact Categorization**: Rather than accepting LLM output verbatim, the fact-check agent separates claims into distinct keys:
  * *Verified Facts*: Assertions supported by multiple source URLs.
  * *Uncertain Claims*: Statements appearing in only a single source.
  * *Contradictions*: Outright contradictions flagged for user awareness.
* **PDF Flow Safeguards**: The PDF engine in [pdf_generator.py](file:///c:/Users/patha/OneDrive/Desktop/capstone/backend/tools/pdf_generator.py) sanitizes layout markup to prevent formatting breaks or buffer overflow crashes during compilation.

---

## 💻 Setup & Installation Instructions

### Prerequisites
Ensure the following are installed locally:
* **Python**: Version 3.13+
* **Node.js**: Version 18+
* **PostgreSQL**: Version 14+
* **Groq API Key**: Free API access key from [console.groq.com](https://console.groq.com)
* **Tavily API Key**: Free Search API key from [app.tavily.com](https://app.tavily.com)

---

### 1. Backend Setup & Configuration

1. **Activate Virtual Environment**:
   Navigate to the backend directory and set up a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows (Command Prompt/PowerShell):
   .\venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy the example environment template to create your config:
   ```bash
   # On Windows:
   copy .env.example .env

   # On Mac/Linux:
   cp .env.example .env
   ```
   Open the `.env` file and insert your API keys and PostgreSQL credentials:
   ```env
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
   TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx
   DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/researchlab
   ```

4. **Initialize Database**:
   Log into your PostgreSQL database client (e.g., `psql` or pgAdmin) and create the database:
   ```sql
   CREATE DATABASE researchlab;
   ```
   > [!NOTE]
   > You do not need to run manual table migrations. The SQLAlchemy initialization logic inside the FastAPI lifespan handler will automatically set up all database tables on application startup.

5. **Start Backend Server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   * Interactive Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
   * API root: [http://localhost:8000/](http://localhost:8000/)

---

### 2. Frontend Setup & Run

1. **Navigate & Install Dependencies**:
   Open a separate terminal window, go to the frontend directory, and install npm packages:
   ```bash
   cd frontend
   npm install
   ```

2. **Run React Web App**:
   ```bash
   npm run dev
   ```
   * Open your browser and navigate to: [http://localhost:5173](http://localhost:5173)

---

## 📡 API & Payload Reference

### Endpoints Table

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/research/start` | Initiates a new research session in the background |
| `GET` | `/api/research/{session_id}/status` | Fetches current research status and report details |
| `WS` | `/api/research/ws/{session_id}` | Live WebSockets stream of active agent progress |
| `GET` | `/api/research/{session_id}/pdf` | Downloads the generated research document as a PDF |
| `GET` | `/api/history` | Lists all historical research sessions |
| `DELETE` | `/api/history/{session_id}` | Deletes a session from database history |

### API Payload Examples

#### Start Research (`POST /api/research/start`)
* **Request Body**:
  ```json
  {
    "topic": "AI in healthcare and patient diagnosis accuracy"
  }
  ```
* **Response**:
  ```json
  {
    "session_id": "99fbc502-b2d9-4f96-8eb5-1ad899fb58d2",
    "topic": "AI in healthcare and patient diagnosis accuracy",
    "status": "running"
  }
  ```

#### WebSocket Event Stream (`WS /api/research/ws/{session_id}`)
The WebSocket connection sends text frames matching the Pydantic schema in [schemas.py](file:///c:/Users/patha/OneDrive/Desktop/capstone/backend/models/schemas.py):
```json
{
  "session_id": "99fbc502-b2d9-4f96-8eb5-1ad899fb58d2",
  "agent": "research",
  "status": "running",
  "message": "📖 Reading and summarizing sources...",
  "data": null
}
```

---

## 📈 Production & Deployment

### 1. Build the Frontend
To compile optimized static assets for production deployment:
```bash
cd frontend
npm run build
```
This generates a production bundle in the `frontend/dist/` directory, which can be served statically by Nginx, Vercel, or Netlify.

### 2. Run Backend in Production
In production, do not run Uvicorn with `--reload`. Instead, run FastAPI behind an ASGI server like Gunicorn using Uvicorn worker threads to manage traffic:
```bash
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 👤 Author & License
Built by **shreya661** as a Capstone project submission. All rights reserved.
For inquiries, connect via GitHub: [github.com/shreya661](https://github.com/shreya661).
