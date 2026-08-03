import React from 'react';
import { Database, Cpu, Sparkles, ArrowRight, HelpCircle } from 'lucide-react';

/**
 * RagExplanationCard Component
 * 
 * An educational visual guide explaining how RAG (Retrieval-Augmented Generation) works:
 * Step 1: Retrieval from Database / Vector Store
 * Step 2: Prompt Augmentation with context
 * Step 3: LLM Generation for accurate answers
 */
export default function RagExplanationCard() {
  return (
    <div className="glass-card" style={{ padding: '1.25rem', marginBottom: '1.5rem', background: 'rgba(15, 23, 42, 0.6)' }}>
      {/* Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
        <Sparkles size={18} color="var(--accent-primary)" />
        <h4 style={{ fontSize: '1rem', fontWeight: 600 }}>How RAG Works in This Project</h4>
        <span style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem', background: 'rgba(99, 102, 241, 0.2)', color: 'var(--accent-primary)', borderRadius: '4px', marginLeft: 'auto' }}>
          Educational Workflow
        </span>
      </div>

      {/* 3-Step Flow Diagram */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        alignItems: 'center',
        fontSize: '0.85rem'
      }}>
        {/* Step 1: User Question & Retrieval */}
        <div style={{ padding: '0.875rem', borderRadius: '8px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem', color: 'var(--info)', fontWeight: 600 }}>
            <Database size={16} /> 1. RETRIEVAL
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: '1.4' }}>
            User types a question. The system searches PostgreSQL & CloudWatch logs for matching metrics.
          </p>
        </div>

        {/* Step 2: Augmentation */}
        <div style={{ padding: '0.875rem', borderRadius: '8px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem', color: 'var(--warning)', fontWeight: 600 }}>
            <Cpu size={16} /> 2. AUGMENTATION
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: '1.4' }}>
            The retrieved metrics & log entries are injected into the LLM prompt as ground-truth context.
          </p>
        </div>

        {/* Step 3: Generation */}
        <div style={{ padding: '0.875rem', borderRadius: '8px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem', color: 'var(--success)', fontWeight: 600 }}>
            <Sparkles size={16} /> 3. GENERATION
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: '1.4' }}>
            The LLM reads your exact data and generates an accurate, hallucination-free answer!
          </p>
        </div>
      </div>
    </div>
  );
}
