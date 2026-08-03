import React, { useState } from 'react';
import { Database, ChevronDown, ChevronUp } from 'lucide-react';

/**
 * RagContextBadge Component
 * 
 * Collapsible UI badge attached to AI responses displaying the exact database records
 * and metric logs retrieved during the RAG Retrieval step.
 * 
 * @param {Object} props
 * @param {Array} props.contextItems - Array of retrieved context objects { source, item }
 */
export default function RagContextBadge({ contextItems }) {
  const [expanded, setExpanded] = useState(false);

  if (!contextItems || contextItems.length === 0) return null;

  return (
    <div style={{ marginTop: '0.75rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', paddingTop: '0.5rem' }}>
      {/* Toggle Button */}
      <button
        onClick={() => setExpanded(!expanded)}
        style={{
          background: 'rgba(99, 102, 241, 0.1)',
          border: '1px solid rgba(99, 102, 241, 0.25)',
          color: 'var(--accent-primary)',
          padding: '0.3rem 0.6rem',
          borderRadius: 'var(--radius-sm)',
          fontSize: '0.75rem',
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.35rem',
          fontWeight: 500
        }}
      >
        <Database size={13} />
        {contextItems.length} Retrieved RAG Context Items
        {expanded ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
      </button>

      {/* Expanded Context List */}
      {expanded && (
        <div style={{
          marginTop: '0.5rem',
          padding: '0.75rem',
          borderRadius: 'var(--radius-sm)',
          background: 'rgba(0, 0, 0, 0.3)',
          border: '1px solid var(--border-color)',
          fontSize: '0.8rem',
          color: 'var(--text-muted)'
        }}>
          <strong style={{ color: 'var(--text-main)', display: 'block', marginBottom: '0.35rem' }}>
            Ground Truth Database Telemetry Retrieved:
          </strong>
          <ul style={{ paddingLeft: '1.2rem', margin: 0 }}>
            {contextItems.map((ctx, idx) => (
              <li key={idx} style={{ marginBottom: '0.25rem' }}>
                <span style={{ color: 'var(--info)', fontWeight: 500 }}>[{ctx.source}]</span>: {ctx.item}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
