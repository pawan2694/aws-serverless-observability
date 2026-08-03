import React, { useRef, useEffect } from 'react';
import { Bot, User, Sparkles, Loader2 } from 'lucide-react';
import RagContextBadge from './RagContextBadge';

/**
 * RagChatWindow Component
 * 
 * Renders the conversation message stream between the User and the RAG AI Assistant.
 * Formats Markdown bolding and embeds the retrieved ground-truth context badge.
 * 
 * @param {Object} props
 * @param {Array} props.messages - Array of chat message objects [{ id, sender, text, context, timestamp }]
 * @param {boolean} props.loading - Indicates if AI is currently generating a response
 */
export default function RagChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  // Auto-scroll to bottom of chat whenever messages update
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  /**
   * Simple helper to format basic Markdown bolding (**text**) into <strong> tags
   */
  const formatMarkdown = (text) => {
    if (!text) return '';
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} style={{ color: '#ffffff' }}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <div className="glass-card" style={{
      minHeight: '380px',
      maxHeight: '520px',
      overflowY: 'auto',
      padding: '1.25rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem'
    }}>
      {/* Empty State message */}
      {messages.length === 0 && !loading && (
        <div style={{
          margin: 'auto',
          textAlign: 'center',
          color: 'var(--text-dim)',
          padding: '2rem'
        }}>
          <Bot size={40} color="var(--accent-primary)" style={{ opacity: 0.8, marginBottom: '0.75rem' }} />
          <h3 style={{ fontSize: '1.1rem', color: 'var(--text-main)', marginBottom: '0.25rem' }}>
            RAG AI Observability Assistant
          </h3>
          <p style={{ fontSize: '0.85rem', maxWidth: '420px', margin: '0 auto', color: 'var(--text-muted)' }}>
            Ask any question above! RAG retrieves your live PostgreSQL Lambda telemetry and generates context-aware answers.
          </p>
        </div>
      )}

      {/* Message Stream */}
      {messages.map((msg) => (
        <div
          key={msg.id}
          style={{
            display: 'flex',
            gap: '0.75rem',
            alignItems: 'flex-start',
            flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row'
          }}
        >
          {/* Avatar Icon */}
          <div style={{
            padding: '0.5rem',
            borderRadius: '50%',
            background: msg.sender === 'user' ? 'var(--accent-gradient)' : 'rgba(16, 185, 129, 0.2)',
            color: '#ffffff',
            flexShrink: 0
          }}>
            {msg.sender === 'user' ? <User size={16} /> : <Sparkles size={16} color="var(--success)" />}
          </div>

          {/* Message Bubble */}
          <div style={{
            maxWidth: '82%',
            padding: '0.875rem 1.1rem',
            borderRadius: 'var(--radius-md)',
            background: msg.sender === 'user' ? 'rgba(99, 102, 241, 0.25)' : 'rgba(31, 41, 55, 0.8)',
            border: '1px solid ' + (msg.sender === 'user' ? 'rgba(99, 102, 241, 0.4)' : 'var(--border-color)'),
            color: 'var(--text-main)',
            fontSize: '0.9rem',
            lineHeight: '1.5',
            whiteSpace: 'pre-wrap'
          }}>
            {/* Sender Label & Timestamp */}
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-dim)', marginBottom: '0.35rem' }}>
              <strong>{msg.sender === 'user' ? 'You' : 'RAG AI Assistant'}</strong>
              <span>{msg.timestamp}</span>
            </div>

            {/* Formatted Text */}
            <div>{formatMarkdown(msg.text)}</div>

            {/* Retrieved Context Badge (Shown for AI responses) */}
            {msg.sender === 'ai' && (
              <RagContextBadge contextItems={msg.context} />
            )}
          </div>
        </div>
      ))}

      {/* Loading Indicator */}
      {loading && (
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <div style={{ padding: '0.5rem', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.2)' }}>
            <Sparkles size={16} color="var(--success)" />
          </div>
          <div style={{
            padding: '0.75rem 1rem',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(31, 41, 55, 0.8)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-muted)',
            fontSize: '0.85rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Loader2 size={16} className="spin" color="var(--accent-primary)" />
            Retrieving vector context & generating response...
          </div>
        </div>
      )}

      {/* Auto-scroll anchor */}
      <div ref={bottomRef} />
    </div>
  );
}
