import React, { useState } from 'react';
import { Send, Sparkles, HelpCircle } from 'lucide-react';

/**
 * RagSearchBar Component
 * 
 * ChatGPT-style search input bar for asking natural language questions about AWS Serverless metrics.
 * Includes sample question chips for quick testing.
 * 
 * @param {Object} props
 * @param {Function} props.onSubmit - Function called when user submits a query
 * @param {boolean} props.loading - Indicates if query processing is in progress
 */
export default function RagSearchBar({ onSubmit, loading }) {
  const [query, setQuery] = useState('');

  // Sample ChatGPT-style suggested questions for instant testing
  const samplePrompts = [
    "Which Lambda function has high duration?",
    "Show functions with highest memory allocation",
    "Analyze recent CloudWatch log errors"
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    onSubmit(query);
    setQuery('');
  };

  const handleChipClick = (promptText) => {
    if (loading) return;
    onSubmit(promptText);
  };

  return (
    <div style={{ marginBottom: '1.5rem' }}>
      {/* ChatGPT-Style Form Input */}
      <form onSubmit={handleSubmit} style={{ position: 'relative', width: '100%' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask AI Assistant about your AWS Lambda metrics, memory, or logs..."
          disabled={loading}
          style={{
            width: '100%',
            padding: '1rem 3.5rem 1rem 1.25rem',
            borderRadius: 'var(--radius-lg)',
            background: 'rgba(31, 41, 55, 0.7)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            color: '#ffffff',
            fontSize: '0.95rem',
            outline: 'none',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.25)',
            transition: 'var(--transition)'
          }}
        />

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!query.trim() || loading}
          style={{
            position: 'absolute',
            right: '0.6rem',
            top: '50%',
            transform: 'translateY(-50%)',
            background: query.trim() && !loading ? 'var(--accent-gradient)' : 'rgba(255, 255, 255, 0.1)',
            color: '#ffffff',
            border: 'none',
            borderRadius: 'var(--radius-md)',
            padding: '0.55rem',
            cursor: query.trim() && !loading ? 'pointer' : 'not-allowed',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'var(--transition)'
          }}
          title="Send query to RAG Assistant"
        >
          <Send size={18} />
        </button>
      </form>

      {/* Suggested Query Chips */}
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.75rem', alignItems: 'center' }}>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <Sparkles size={12} color="var(--accent-primary)" /> Try asking:
        </span>
        {samplePrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleChipClick(prompt)}
            disabled={loading}
            style={{
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-muted)',
              fontSize: '0.78rem',
              padding: '0.3rem 0.65rem',
              borderRadius: '16px',
              cursor: 'pointer',
              transition: 'var(--transition)'
            }}
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
