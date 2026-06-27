from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

# ── Request Models ──────────────────────────────────────────────
class ResearchRequest(BaseModel):
    topic: str

# ── Citation ────────────────────────────────────────────────────
class Citation(BaseModel):
    title: str
    url: str
    snippet: str

# ── Agent Progress Event (sent via WebSocket) ───────────────────
class AgentEvent(BaseModel):
    session_id: str
    agent: str          # coordinator | search | research | factcheck | report
    status: str         # started | running | done | error
    message: str
    data: Optional[Any] = None

# ── Session Response ────────────────────────────────────────────
class SessionStartResponse(BaseModel):
    session_id: str
    topic: str
    status: str

class SessionStatusResponse(BaseModel):
    session_id: str
    topic: str
    status: str
    current_agent: Optional[str]
    report_markdown: Optional[str]
    citations: Optional[List[Citation]]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

class HistoryItem(BaseModel):
    session_id: str
    topic: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
