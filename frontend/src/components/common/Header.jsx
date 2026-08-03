import React from 'react';
import { RefreshCw } from 'lucide-react';

/**
 * Header Component
 * 
 * Renders the dashboard top header section, including page title, subtitle,
 * last updated timestamp, and the interactive refresh button.
 * 
 * @param {Object} props
 * @param {boolean} props.loading - Indicates if data is currently being fetched
 * @param {string|null} props.lastRefreshed - Timestamp string of the last successful data fetch
 * @param {Function} props.onRefresh - Callback function to trigger a fresh data reload
 */
export default function Header({ loading, lastRefreshed, onRefresh }) {
  return (
    <header style={{
      marginBottom: '2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      flexWrap: 'wrap',
      gap: '1rem'
    }}>
      {/* Title & Subtitle Section */}
      <div>
        <h1 style={{
          fontSize: '2rem',
          fontWeight: 700,
          background: 'linear-gradient(90deg, #ffffff, #9ca3af)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          AWS Serverless Observability
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', marginTop: '0.25rem' }}>
          Real-time telemetry, execution metrics, & serverless performance insights
        </p>
      </div>

      {/* Timestamp & Refresh Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {/* Displays the last updated time if available */}
        {lastRefreshed && (
          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
            Updated: {lastRefreshed}
          </span>
        )}

        {/* Refresh Data Button */}
        <button
          className="btn btn-primary"
          onClick={onRefresh}
          disabled={loading}
          title="Click to reload metric data from backend"
        >
          {/* Animated spinning icon when loading is true */}
          <RefreshCw size={16} className={loading ? 'spin' : ''} />
          {loading ? 'Refreshing...' : 'Refresh Data'}
        </button>
      </div>
    </header>
  );
}
