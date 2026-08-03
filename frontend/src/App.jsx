import React, { useState, useEffect } from 'react';
import { Clock, HardDrive, Sparkles, BarChart2 } from 'lucide-react';

// Import API Services
import { fetchAllDashboardData } from './services/dashboardApi';
import { queryRagAssistant } from './services/ragApi';

// Import Common UI Components
import Header from './components/common/Header';
import ErrorBanner from './components/common/ErrorBanner';

// Import Telemetry Dashboard Components
import SummaryCards from './components/dashboard/SummaryCards';
import HighDurationTable from './components/dashboard/HighDurationTable';
import HighMemoryTable from './components/dashboard/HighMemoryTable';

// Import RAG AI Assistant Components
import RagExplanationCard from './components/rag/RagExplanationCard';
import RagSearchBar from './components/rag/RagSearchBar';
import RagChatWindow from './components/rag/RagChatWindow';

/**
 * Main App Component
 * 
 * Manages central application state:
 * - mainView: Active main navigation view ('dashboard' | 'rag')
 * - summary, highDuration, highMemory: Telemetry metrics state
 * - ragMessages: Array of chat conversation history
 * - ragLoading: Boolean indicating AI query execution state
 */
export default function App() {
  // --- MAIN NAVIGATION VIEW STATE ---
  const [mainView, setMainView] = useState('dashboard'); // 'dashboard' or 'rag'

  // --- TELEMETRY DASHBOARD STATE ---
  const [summary, setSummary] = useState(null);
  const [highDuration, setHighDuration] = useState([]);
  const [highMemory, setHighMemory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastRefreshed, setLastRefreshed] = useState(null);
  const [activeTab, setActiveTab] = useState('duration');

  // --- RAG CHAT ASSISTANT STATE ---
  const [ragMessages, setRagMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: "Hello! I am your **AWS Serverless RAG Assistant**. Ask me anything about your Lambda execution durations, memory configurations, or CloudWatch logs!",
      context: [
        { source: 'PostgreSQL DB', item: 'Connected to AWS Observability Telemetry Store' }
      ],
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [ragLoading, setRagLoading] = useState(false);

  /**
   * Fetches all telemetry metrics concurrently from FastAPI backend
   */
  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const { summary, highDuration, highMemory } = await fetchAllDashboardData();
      setSummary(summary);
      setHighDuration(highDuration);
      setHighMemory(highMemory);
      setLastRefreshed(new Date().toLocaleTimeString());
    } catch (err) {
      console.error('Telemetry fetch error:', err);
      setError(err.message || 'Unable to connect to backend server.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handles user submission in ChatGPT-style RAG search bar
   * 1. Adds user query to chat history
   * 2. Calls RAG service (Retrieval -> Augmentation -> Generation)
   * 3. Appends AI response & retrieved DB context badge to chat log
   */
  const handleRagQuery = async (userQueryText) => {
    if (!userQueryText.trim()) return;

    // Add User message to chat history
    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: userQueryText,
      timestamp: new Date().toLocaleTimeString()
    };
    setRagMessages(prev => [...prev, userMsg]);
    setRagLoading(true);

    try {
      // Execute RAG Pipeline (Retrieval + Prompt Augmentation + LLM Response)
      const ragResult = await queryRagAssistant(userQueryText);

      // Append AI response with retrieved ground-truth database context
      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: ragResult.answer,
        context: ragResult.retrievedContext,
        timestamp: ragResult.timestamp
      };
      setRagMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error('RAG Query Error:', err);
      const errorMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: "I encountered an error executing the RAG retrieval pipeline. Please check backend connection.",
        context: [],
        timestamp: new Date().toLocaleTimeString()
      };
      setRagMessages(prev => [...prev, errorMsg]);
    } finally {
      setRagLoading(false);
    }
  };

  // Fetch telemetry metrics once when component mounts
  useEffect(() => {
    loadDashboardData();
  }, []);

  return (
    <div style={{ padding: '2rem', maxWidth: '1280px', margin: '0 auto', width: '100%' }}>
      {/* 1. Header Navigation Bar */}
      <Header
        loading={loading}
        lastRefreshed={lastRefreshed}
        onRefresh={loadDashboardData}
      />

      {/* 2. Top View Switcher Tabs (Dashboard vs RAG Assistant) */}
      <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <button
          onClick={() => setMainView('dashboard')}
          style={{
            background: mainView === 'dashboard' ? 'var(--accent-gradient)' : 'rgba(31, 41, 55, 0.6)',
            color: mainView === 'dashboard' ? '#ffffff' : 'var(--text-muted)',
            border: '1px solid ' + (mainView === 'dashboard' ? 'transparent' : 'var(--border-color)'),
            padding: '0.65rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
            fontSize: '0.9rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            transition: 'var(--transition)'
          }}
        >
          <BarChart2 size={18} /> Observability Dashboard
        </button>

        <button
          onClick={() => setMainView('rag')}
          style={{
            background: mainView === 'rag' ? 'var(--accent-gradient)' : 'rgba(31, 41, 55, 0.6)',
            color: mainView === 'rag' ? '#ffffff' : 'var(--text-muted)',
            border: '1px solid ' + (mainView === 'rag' ? 'transparent' : 'var(--border-color)'),
            padding: '0.65rem 1.25rem',
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
            fontSize: '0.9rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            transition: 'var(--transition)'
          }}
        >
          <Sparkles size={18} color={mainView === 'rag' ? '#fff' : 'var(--accent-primary)'} /> RAG AI Assistant
        </button>
      </div>

      {/* Error Alert Banner */}
      <ErrorBanner error={error} />

      {/* =================================================================== */}
      {/* VIEW 1: OBSERVABILITY TELEMETRY DASHBOARD                          */}
      {/* =================================================================== */}
      {mainView === 'dashboard' && (
        <>
          {/* KPI Summary Cards */}
          <SummaryCards summary={summary} loading={loading} />

          {/* Metric Tables Container */}
          <section className="glass-card" style={{ padding: '1.5rem' }}>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '1.5rem',
              borderBottom: '1px solid var(--border-color)',
              paddingBottom: '1rem'
            }}>
              <div style={{ display: 'flex', gap: '1rem' }}>
                <button
                  onClick={() => setActiveTab('duration')}
                  style={{
                    background: activeTab === 'duration' ? 'var(--accent-gradient)' : 'transparent',
                    color: activeTab === 'duration' ? '#fff' : 'var(--text-muted)',
                    border: 'none',
                    padding: '0.5rem 1rem',
                    borderRadius: 'var(--radius-sm)',
                    cursor: 'pointer',
                    fontWeight: 500,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    transition: 'var(--transition)'
                  }}
                >
                  <Clock size={16} /> Top Duration Functions
                </button>

                <button
                  onClick={() => setActiveTab('memory')}
                  style={{
                    background: activeTab === 'memory' ? 'var(--accent-gradient)' : 'transparent',
                    color: activeTab === 'memory' ? '#fff' : 'var(--text-muted)',
                    border: 'none',
                    padding: '0.5rem 1rem',
                    borderRadius: 'var(--radius-sm)',
                    cursor: 'pointer',
                    fontWeight: 500,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    transition: 'var(--transition)'
                  }}
                >
                  <HardDrive size={16} /> Highest Memory Configured
                </button>
              </div>
            </div>

            {activeTab === 'duration' && (
              <HighDurationTable functions={highDuration} loading={loading} />
            )}

            {activeTab === 'memory' && (
              <HighMemoryTable functions={highMemory} loading={loading} />
            )}
          </section>
        </>
      )}

      {/* =================================================================== */}
      {/* VIEW 2: CHATGPT-STYLE RAG AI ASSISTANT                             */}
      {/* =================================================================== */}
      {mainView === 'rag' && (
        <div>
          {/* Educational RAG Step-by-Step Flow Card */}
          <RagExplanationCard />

          {/* ChatGPT-Style Search Bar & Sample Prompts */}
          <RagSearchBar
            onSubmit={handleRagQuery}
            loading={ragLoading}
          />

          {/* Interactive Chat Window & Context Visualizer */}
          <RagChatWindow
            messages={ragMessages}
            loading={ragLoading}
          />
        </div>
      )}
    </div>
  );
}
