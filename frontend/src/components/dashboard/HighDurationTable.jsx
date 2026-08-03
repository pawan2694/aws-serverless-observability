import React from 'react';

/**
 * HighDurationTable Component
 * 
 * Renders a styled tabular view listing the top Lambda functions ordered by
 * highest average duration (ms).
 * 
 * @param {Object} props
 * @param {Array} props.functions - List of high duration function objects
 * @param {boolean} props.loading - Indicates if fetching data is in progress
 */
export default function HighDurationTable({ functions, loading }) {
  return (
    <div>
      {/* Section Header */}
      <div style={{ marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>
          Top 10 High Duration Lambda Functions
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
          Functions with highest average execution duration (ms)
        </p>
      </div>

      {/* Table Container with Horizontal Scroll fallback */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '0.75rem 1rem' }}>#</th>
              <th style={{ padding: '0.75rem 1rem' }}>Function Name</th>
              <th style={{ padding: '0.75rem 1rem' }}>Avg Duration (ms)</th>
              <th style={{ padding: '0.75rem 1rem' }}>Memory Size</th>
              <th style={{ padding: '0.75rem 1rem' }}>Timeout</th>
            </tr>
          </thead>
          <tbody>
            {/* Map over the high-duration array to render table rows */}
            {functions.map((fn, idx) => (
              <tr key={fn.function_name || idx} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-dim)' }}>{idx + 1}</td>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 600, color: '#e5e7eb' }}>
                  <code>{fn.function_name}</code>
                </td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--warning)', fontWeight: 600 }}>
                  {fn.avg_duration} ms
                </td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-muted)' }}>
                  {fn.memory_size} MB
                </td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-muted)' }}>
                  {fn.timeout} s
                </td>
              </tr>
            ))}

            {/* Empty state message if array is empty and not loading */}
            {functions.length === 0 && !loading && (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-dim)' }}>
                  No high duration metric data available.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
