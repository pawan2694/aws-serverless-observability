import React from 'react';
import { AlertCircle } from 'lucide-react';

/**
 * ErrorBanner Component
 * 
 * Displays a styled alert notification banner when an error occurs (e.g. backend server down).
 * 
 * @param {Object} props
 * @param {string} props.error - The error message text to display
 */
export default function ErrorBanner({ error }) {
  // If there is no error message, do not render anything
  if (!error) return null;

  return (
    <div style={{
      padding: '1rem 1.25rem',
      borderRadius: 'var(--radius-md)',
      background: 'rgba(239, 68, 68, 0.15)',
      border: '1px solid rgba(239, 68, 68, 0.3)',
      color: '#fca5a5',
      marginBottom: '1.5rem',
      display: 'flex',
      alignItems: 'center',
      gap: '0.75rem'
    }}>
      {/* Alert icon from lucide-react */}
      <AlertCircle size={20} color="#ef4444" />
      
      <div>
        <strong>Backend Connection Error:</strong> {error}. Ensure FastAPI backend is active on <code>http://localhost:8000</code>.
      </div>
    </div>
  );
}
