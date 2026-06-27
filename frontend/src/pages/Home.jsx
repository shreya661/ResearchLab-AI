import { useState } from 'react'

const EXAMPLES = [
  'Climate change and renewable energy',
  'CRISPR gene editing breakthroughs',
  'Artificial Intelligence in healthcare',
  'Quantum computing applications',
  'Mental health and social media',
  'SpaceX Mars mission progress',
]

const AGENT_FLOW = [
  { icon: '🔍', label: 'Search' },
  { icon: '📖', label: 'Research' },
  { icon: '✅', label: 'Fact-Check' },
  { icon: '📝', label: 'Report' },
]

export default function HomePage({ onSearch }) {
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!topic.trim() || loading) return
    setLoading(true)
    await onSearch(topic.trim())
    setLoading(false)
  }

  return (
    <div className="home-page">
      {/* Background orbs */}
      <div className="home-bg-orb orb1" />
      <div className="home-bg-orb orb2" />

      <div className="home-hero fade-in">
        {/* Badge */}
        <div className="hero-badge">
          <span>●</span> Powered by Groq + Tavily + LangGraph
        </div>

        {/* Title */}
        <h1 className="home-title">
          Research anything with<br />
          <span className="gradient-text">AI Agents</span>
        </h1>

        {/* Subtitle */}
        <p className="home-subtitle">
          Enter any topic and our multi-agent system will search the web,
          analyze sources, verify facts, and generate a complete research report — automatically.
        </p>

        {/* Search */}
        <form className="search-container" onSubmit={handleSubmit}>
          <input
            id="research-topic-input"
            className="search-input"
            type="text"
            placeholder="e.g. Impact of AI on job markets..."
            value={topic}
            onChange={e => setTopic(e.target.value)}
            disabled={loading}
            autoFocus
          />
          <button
            id="start-research-btn"
            className="search-btn"
            type="submit"
            disabled={!topic.trim() || loading}
          >
            {loading ? <span className="spinner" /> : '→'}
            {loading ? 'Starting...' : 'Research'}
          </button>
        </form>

        {/* Example topics */}
        <div className="example-topics">
          {EXAMPLES.map(ex => (
            <button
              key={ex}
              className="example-chip"
              onClick={() => setTopic(ex)}
            >
              {ex}
            </button>
          ))}
        </div>

        {/* Agent flow preview */}
        <div className="agent-flow-preview">
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginRight: 4 }}>Your question</span>
          <span className="flow-arrow">→</span>
          {AGENT_FLOW.map((node, i) => (
            <div key={node.label} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <div className="flow-node">
                {node.icon} {node.label}
              </div>
              {i < AGENT_FLOW.length - 1 && <span className="flow-arrow">→</span>}
            </div>
          ))}
          <span className="flow-arrow">→</span>
          <span style={{ fontSize: '0.78rem', color: 'var(--accent-green)' }}>📄 Report</span>
        </div>
      </div>
    </div>
  )
}
