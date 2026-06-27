"""
Report Agent — generates the final structured research report with citations.
"""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)


def run_report_agent(topic: str, verified_facts: dict, summaries: list[dict]) -> dict:
    """
    Generates a full markdown research report with citations.
    Returns: { markdown: str, citations: list[dict] }
    """
    client = get_groq_client()

    facts_text = "\n".join(f"- {f}" for f in verified_facts.get("verified_facts", []))
    uncertain_text = "\n".join(f"- {f}" for f in verified_facts.get("uncertain_claims", []))
    consensus = verified_facts.get("consensus", "")

    sources_text = ""
    for i, s in enumerate(summaries[:8], 1):
        sources_text += f"[{i}] {s['title']} — {s['url']}\n"

    prompt = f"""You are an expert research writer. Write a comprehensive, well-structured research report on: "{topic}"

Use the following verified information:

CONSENSUS:
{consensus}

VERIFIED FACTS:
{facts_text}

AREAS OF UNCERTAINTY:
{uncertain_text}

SOURCES AVAILABLE:
{sources_text}

Write a detailed report in Markdown format with these sections:
## Executive Summary
## Introduction
## Key Findings
## Detailed Analysis
## Areas of Uncertainty
## Conclusion

Rules:
- Use **bold** for important terms
- Add [N] citation markers where facts come from numbered sources
- Be thorough but clear — aim for 600-900 words
- Do NOT make up facts not present in the verified information
- Write in a professional, academic tone
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=3000,
    )

    markdown = response.choices[0].message.content

    # Build citations list from summaries
    citations = [
        {
            "title": s["title"],
            "url": s["url"],
            "snippet": s.get("snippet", "")[:200],
        }
        for s in summaries[:8]
    ]

    return {
        "markdown": markdown,
        "citations": citations,
    }
