"""
Search Agent — uses Tavily to find relevant web sources for the research topic.
"""
from tools.web_search import search_web

def run_search_agent(topic: str, num_queries: int = 3) -> list[dict]:
    """
    Generates multiple search queries for the topic and collects results.
    Returns a deduplicated list of search result dicts.
    """
    queries = _generate_queries(topic)
    seen_urls = set()
    all_results = []

    for query in queries[:num_queries]:
        results = search_web(query, max_results=5)
        for r in results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                all_results.append(r)

    # Sort by relevance score
    all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return all_results[:12]  # top 12 unique sources


def _generate_queries(topic: str) -> list[str]:
    """Create multiple search angles for a topic."""
    return [
        topic,
        f"{topic} latest research 2024",
        f"{topic} key findings and insights",
        f"{topic} overview and analysis",
    ]
