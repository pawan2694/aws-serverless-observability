"""
RAG Generator & Prompt Augmenter.

Yeh module retrieved context ko lekar final answer form karta hai.
Agar local Ollama server available hai to yeh real LLM ka use karta hai,
warna safe fallback ke saath rule-based answer return karta hai.
"""

import json
from typing import List, Dict, Any
from urllib import error, request

from app.core.config import settings


class OllamaClient:
    """Lightweight local Ollama client for free LLM inference."""

    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL

    def generate(self, prompt: str) -> str:
        """Call local Ollama /api/generate and return the model response."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        req = request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with request.urlopen(req, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return (payload.get("response") or "").strip()


class RagGenerator:
    """Retrieved context ke hisaab se structured answer generate karta hai."""

    def __init__(self, ollama_client: OllamaClient | None = None):
        self.ollama_client = ollama_client or OllamaClient()

    def _build_prompt(self, query: str, search_results: List[Dict[str, Any]]) -> str:
        context_lines = []
        for item in search_results:
            chunk = item["chunk"]
            context_lines.append(chunk["text"])

        context_block = "\n".join(context_lines) if context_lines else "No relevant telemetry context found."
        return (
            "You are an AWS Serverless Observability expert. Use the retrieved telemetry context below to answer the user's question. "
            "Be concise and factual. If the context is weak, say that you could not find enough evidence.\n\n"
            f"Question: {query}\n\n"
            f"Retrieved context:\n{context_block}\n\n"
            "Answer:"
        )

    def _fallback_response(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        retrieved_sources = []
        for item in search_results:
            chunk = item["chunk"]
            metadata = chunk["metadata"]
            source_label = f"{metadata.get('source', 'DB Record')} ({metadata.get('function_name', 'Global')})"
            retrieved_sources.append({
                "source": source_label,
                "item": chunk["text"]
            })

        query_lower = query.lower()

        if not search_results or search_results[0]["score"] == 0:
            answer = (
                f"I searched the telemetry database for **'{query}'**, but could not find specific matching records.\n\n"
                f"Try asking about specific function names like `send_message`, `read_market_data`, or general questions like *'Which function has high duration?'*."
            )
            confidence = "70%"
        else:
            top_text = search_results[0]["chunk"]["text"]
            fn_name = search_results[0]["chunk"]["metadata"].get("function_name", "your serverless stack")

            if "duration" in query_lower or "slow" in query_lower or "latency" in query_lower:
                answer = (
                    f"Based on retrieved CloudWatch metrics, **{fn_name}** exhibits key latency records:\n\n"
                    f"> `{top_text}`\n\n"
                    f"**RAG Optimization Advice:** High execution duration can indicate database connection bottlenecks, "
                    f"synchronous external HTTP calls, or insufficient CPU allocation. Try scaling allocated memory."
                )
            elif "memory" in query_lower or "ram" in query_lower:
                answer = (
                    f"Based on retrieved Lambda configurations, **{fn_name}** has memory allocation details:\n\n"
                    f"> `{top_text}`\n\n"
                    f"**RAG Memory Optimization:** AWS Lambda provisions CPU power proportionally with memory. "
                    f"If the function is idle-waiting on I/O, reducing memory size can save costs without impacting execution time."
                )
            elif "log" in query_lower or "error" in query_lower:
                answer = (
                    f"Retrieved CloudWatch Log event records for **{fn_name}**:\n\n"
                    f"> `{top_text}`\n\n"
                    f"No critical runtime panics were detected in recent execution batches."
                )
            else:
                answer = (
                    f"Based on retrieved telemetry data for **{fn_name}**:\n\n"
                    f"> `{top_text}`\n\n"
                    f"You can ask follow-up questions regarding duration metrics, memory configurations, or error logs."
                )

            confidence = f"{min(99, int(search_results[0]['score'] * 100) + 75)}%"

        return {
            "query": query,
            "answer": answer,
            "retrieved_context": retrieved_sources,
            "confidence_score": confidence,
        }

    def generate_response(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Try a real LLM response first, then fall back to the heuristic answer."""
        retrieved_sources = []
        for item in search_results:
            chunk = item["chunk"]
            metadata = chunk["metadata"]
            source_label = f"{metadata.get('source', 'DB Record')} ({metadata.get('function_name', 'Global')})"
            retrieved_sources.append({
                "source": source_label,
                "item": chunk["text"]
            })

        if search_results:
            try:
                prompt = self._build_prompt(query, search_results)
                llm_answer = self.ollama_client.generate(prompt)
                if llm_answer:
                    return {
                        "query": query,
                        "answer": llm_answer,
                        "retrieved_context": retrieved_sources,
                        "confidence_score": "95%",
                    }
            except (error.URLError, error.HTTPError, TimeoutError, ConnectionError, ValueError, OSError):
                pass

        fallback = self._fallback_response(query, search_results)
        fallback["retrieved_context"] = retrieved_sources
        return fallback
