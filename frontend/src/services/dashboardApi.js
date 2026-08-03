/**
 * Dashboard API Service
 * 
 * Provides asynchronous functions to fetch telemetry data from the FastAPI endpoints.
 * Handles HTTP requests, JSON parsing, and error checking.
 */

import { API_BASE_URL } from '../config/config';

/**
 * Fetches overall metrics summary (total lambdas, total metrics, total logs)
 * Endpoint: GET /dashboard/summary
 * 
 * @returns {Promise<Object>} Summary object { total_lambdas, total_metrics, total_logs }
 */
export async function fetchDashboardSummary() {
  const response = await fetch(`${API_BASE_URL}/dashboard/summary`);
  if (!response.ok) {
    throw new Error(`Failed to fetch summary data (Status: ${response.status})`);
  }
  return await response.json();
}

/**
 * Fetches top Lambda functions with the highest average execution duration
 * Endpoint: GET /dashboard/high-duration
 * 
 * @returns {Promise<Array>} List of functions [{ function_name, avg_duration, memory_size, timeout }]
 */
export async function fetchHighDurationFunctions() {
  const response = await fetch(`${API_BASE_URL}/dashboard/high-duration`);
  if (!response.ok) {
    throw new Error(`Failed to fetch high-duration functions (Status: ${response.status})`);
  }
  return await response.json();
}

/**
 * Fetches top Lambda functions configured with the highest RAM memory allocation
 * Endpoint: GET /dashboard/high-memory
 * 
 * @returns {Promise<Array>} List of functions [{ function_name, memory_size, timeout }]
 */
export async function fetchHighMemoryFunctions() {
  const response = await fetch(`${API_BASE_URL}/dashboard/high-memory`);
  if (!response.ok) {
    throw new Error(`Failed to fetch high-memory functions (Status: ${response.status})`);
  }
  return await response.json();
}

/**
 * Convenience function to fetch all dashboard datasets concurrently using Promise.all
 * 
 * @returns {Promise<Object>} Combined object { summary, highDuration, highMemory }
 */
export async function fetchAllDashboardData() {
  const [summary, highDuration, highMemory] = await Promise.all([
    fetchDashboardSummary(),
    fetchHighDurationFunctions(),
    fetchHighMemoryFunctions()
  ]);

  return { summary, highDuration, highMemory };
}
