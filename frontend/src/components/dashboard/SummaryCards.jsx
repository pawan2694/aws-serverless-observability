import React from 'react';
import { Server, Cpu, Database, CheckCircle2 } from 'lucide-react';

/**
 * SummaryCards Component
 * 
 * Displays key performance indicator (KPI) metric cards for total Lambdas,
 * total metrics, and total CloudWatch logs.
 * 
 * @param {Object} props
 * @param {Object|null} props.summary - Summary data object { total_lambdas, total_metrics, total_logs }
 * @param {boolean} props.loading - Loading state flag
 */
export default function SummaryCards({ summary, loading }) {
  return (
    <section style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
      gap: '1.25rem',
      marginBottom: '2.5rem'
    }}>
      {/* Card 1: Total Lambda Functions */}
      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', fontWeight: 500 }}>
            Lambda Functions
          </span>
          <div style={{ padding: '0.5rem', borderRadius: '8px', background: 'rgba(99, 102, 241, 0.15)' }}>
            <Server color="var(--accent-primary)" size={22} />
          </div>
        </div>
        <h2 style={{ fontSize: '2.25rem', fontWeight: 700, color: '#fff' }}>
          {loading ? '...' : (summary?.total_lambdas ?? 0)}
        </h2>
        <span style={{ fontSize: '0.8rem', color: 'var(--success)', display: 'inline-flex', alignItems: 'center', gap: '0.25rem', marginTop: '0.5rem' }}>
          <CheckCircle2 size={14} /> Active Functions Tracked
        </span>
      </div>

      {/* Card 2: Total CloudWatch Metrics */}
      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', fontWeight: 500 }}>
            CloudWatch Metrics
          </span>
          <div style={{ padding: '0.5rem', borderRadius: '8px', background: 'rgba(6, 182, 212, 0.15)' }}>
            <Cpu color="var(--info)" size={22} />
          </div>
        </div>
        <h2 style={{ fontSize: '2.25rem', fontWeight: 700, color: '#fff' }}>
          {loading ? '...' : (summary?.total_metrics?.toLocaleString() ?? 0)}
        </h2>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '0.5rem', display: 'block' }}>
          Duration & Invocations Metrics
        </span>
      </div>

      {/* Card 3: Total CloudWatch Logs */}
      <div className="glass-card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.875rem', fontWeight: 500 }}>
            CloudWatch Logs
          </span>
          <div style={{ padding: '0.5rem', borderRadius: '8px', background: 'rgba(16, 185, 129, 0.15)' }}>
            <Database color="var(--success)" size={22} />
          </div>
        </div>
        <h2 style={{ fontSize: '2.25rem', fontWeight: 700, color: '#fff' }}>
          {loading ? '...' : (summary?.total_logs?.toLocaleString() ?? 0)}
        </h2>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '0.5rem', display: 'block' }}>
          Ingested Log Records
        </span>
      </div>
    </section>
  );
}
