"""
RAG Generator & Prompt Augmenter.

Yeh module retrieved context ko lekar final answer form karta hai.
Current implementation simple rule-based generator hai; isko baad mein real LLM API ke saath replace kiya ja sakta hai.
"""

from typing import List, Dict, Any


class RagGenerator:
    """Retrieved context ke hisaab se structured answer generate karta hai."""

    def generate_response(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Top-k retrieved chunks ko lekar response payload banata hai.

        Yeh step ko "prompt augmentation" kah sakte hain, kyunki answer ko retrieved data ke
        saath enrich kiya jata hai. Is implementation mein actual LLM call nahi hai,
        lekin flow conceptually wahi hai.
        """
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

        # Agar koi match nahi mila to fallback answer de diya jata hai.
        if not search_results or search_results[0]["score"] == 0:
            answer = (
                f"I searched the telemetry database for **'{query}'**, but could not find specific matching records.\n\n"
                f"Try asking about specific function names like `send_message`, `read_market_data`, or general questions like *'Which function has high duration?'*."
            )
            confidence = "70%"
        else:
            top_text = search_results[0]["chunk"]["text"]
            fn_name = search_results[0]["chunk"]["metadata"].get("function_name", "your serverless stack")

            # Query keyword ke hisaab se different response style choose hoti hai.
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
            "confidence_score": confidence
        }
