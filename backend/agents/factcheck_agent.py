"""
Fact-Check Agent — verifies and filters information from the research summaries.
Removes contradictions, flags uncertain claims, and consolidates verified facts.
"""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=api_key)


def run_factcheck_agent(topic: str, summaries: list[dict]) -> dict:
    """
    Takes research summaries and returns verified facts + flagged uncertainties.
    Returns: { verified_facts: [...], uncertain_claims: [...], consensus: str }
    """
    client = get_groq_client()

    combined = ""
    for i, s in enumerate(summaries, 1):
        combined += f"\n[Source {i}] {s['title']}\n{s['llm_analysis']}\n"

    prompt = f"""You are a fact-checking expert. The research topic is: "{topic}"

Below are summaries and analyses from multiple web sources. Your job is to:
1. Identify facts that appear in MULTIPLE sources (high confidence)
2. Identify claims that appear in only ONE source (uncertain/unverified)
3. Identify any contradictions between sources
4. Write a brief consensus statement about what is most reliably known

RESEARCH SUMMARIES:
{combined}

Respond in this EXACT format:

VERIFIED FACTS:
- [fact supported by multiple sources]
- [fact supported by multiple sources]

UNCERTAIN CLAIMS:
- [claim from only one source]

CONTRADICTIONS:
- [contradiction if any, or "None found"]

CONSENSUS:
[2-3 sentence statement of what is reliably established about this topic]
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content
    return _parse_factcheck(raw)


def _parse_factcheck(raw: str) -> dict:
    """Parse the structured fact-check response."""
    result = {
        "verified_facts": [],
        "uncertain_claims": [],
        "contradictions": [],
        "consensus": "",
    }

    section = None
    for line in raw.split("\n"):
        line = line.strip()
        if line.startswith("VERIFIED FACTS:"):
            section = "verified"
        elif line.startswith("UNCERTAIN CLAIMS:"):
            section = "uncertain"
        elif line.startswith("CONTRADICTIONS:"):
            section = "contradictions"
        elif line.startswith("CONSENSUS:"):
            section = "consensus"
        elif line.startswith("- ") and section in ("verified", "uncertain", "contradictions"):
            result[{
                "verified": "verified_facts",
                "uncertain": "uncertain_claims",
                "contradictions": "contradictions"
            }[section]].append(line[2:])
        elif section == "consensus" and line:
            result["consensus"] += line + " "

    result["consensus"] = result["consensus"].strip()
    return result
