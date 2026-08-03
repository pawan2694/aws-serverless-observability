/**
 * RAG (Retrieval-Augmented Generation) API Service
 * 
 * Communicates with the FastAPI backend RAG engine (/rag/query).
 */

import { API_BASE_URL } from '../config/config';

/**
 * Sends a user query to the FastAPI RAG endpoint
 * 
 * @param {string} userQuery - Natural language question typed by user in search bar
 * @returns {Promise<Object>} Object containing generated answer, retrieved context, and execution metadata
 */
export async function queryRagAssistant(userQuery) {
  try {
    const response = await fetch(`${API_BASE_URL}/rag/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: userQuery })
    });

    if (response.ok) {
      const data = await response.json();
      return {
        query: data.query,
        answer: data.answer,
        retrievedContext: data.retrieved_context || [],
        confidenceScore: data.confidence_score || '95%',
        timestamp: new Date().toLocaleTimeString()
      };
    }
  } catch (err) {
    console.error('Error contacting live RAG backend endpoint:', err);
  }

  // Fallback if backend is unreachable
  return {
    query: userQuery,
    answer: "Unable to connect to the FastAPI RAG backend service on port 8000.",
    retrievedContext: [],
    confidenceScore: "0%",
    timestamp: new Date().toLocaleTimeString()
  };
}
