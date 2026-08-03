"""
RAG Text Chunker Module

Extremely important component of the RAG pipeline.
It extracts raw telemetry data from PostgreSQL database tables and transforms them
into semantic, metadata-rich text chunks suitable for vector embedding and retrieval.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.lambda_function import LambdaFunction
from app.models.cloudwatch_metric import CloudWatchMetric
from app.models.cloudwatch_log import CloudWatchLog


class TelemetryChunker:
    """
    Handles extracting database records and creating chunk objects.
    Each chunk contains:
    - text: The readable text describing the serverless event or metric.
    - metadata: Key-value dictionary storing function name, metric name, source table, etc.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_chunks(self) -> List[Dict[str, Any]]:
        chunks = []

        # --- 1. CHUNK LAMBDA FUNCTIONS ---
        functions = self.db.query(LambdaFunction).all()
        for fn in functions:
            chunk_text = (
                f"AWS Lambda Function Config: Name='{fn.function_name}', "
                f"Memory Size={fn.memory_size} MB, Timeout={fn.timeout}s, "
                f"Runtime='{fn.runtime or 'python3.11'}', Handler='{fn.handler or 'index.handler'}'."
            )
            chunks.append({
                "id": f"fn_{fn.id}",
                "text": chunk_text,
                "metadata": {
                    "source": "Lambda Functions Table",
                    "function_name": fn.function_name,
                    "memory_size": fn.memory_size,
                    "timeout": fn.timeout,
                    "type": "configuration"
                }
            })

        # --- 2. CHUNK CLOUDWATCH METRICS ---
        metrics = self.db.query(CloudWatchMetric).limit(300).all()
        for m in metrics:
            fn_name = m.lambda_function.function_name if m.lambda_function else "Unknown"
            chunk_text = (
                f"CloudWatch Metric: Function='{fn_name}', "
                f"MetricName='{m.metric_name}', Value={m.metric_value} {m.unit or 'ms'}, "
                f"Timestamp='{m.timestamp}'."
            )
            chunks.append({
                "id": f"metric_{m.id}",
                "text": chunk_text,
                "metadata": {
                    "source": "CloudWatch Metrics",
                    "function_name": fn_name,
                    "metric_name": m.metric_name,
                    "metric_value": m.metric_value,
                    "type": "metric"
                }
            })

        # --- 3. CHUNK CLOUDWATCH LOGS ---
        logs = self.db.query(CloudWatchLog).limit(300).all()
        for log in logs:
            fn_name = log.lambda_function.function_name if log.lambda_function else "Unknown"
            # Clean up newlines in log message
            msg_clean = (log.message or "").replace("\n", " ").strip()
            if not msg_clean:
                continue

            chunk_text = (
                f"CloudWatch Log Event: Function='{fn_name}', "
                f"RequestID='{log.request_id or 'N/A'}', Message='{msg_clean[:200]}'."
            )
            chunks.append({
                "id": f"log_{log.id}",
                "text": chunk_text,
                "metadata": {
                    "source": "CloudWatch Logs",
                    "function_name": fn_name,
                    "request_id": log.request_id,
                    "type": "log"
                }
            })

        return chunks
