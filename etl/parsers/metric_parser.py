import json
from datetime import datetime
from pathlib import Path

from app.models.cloudwatch_metric import CloudWatchMetric


class MetricParser:

    def parse(self, file_path: str, lambda_id: int) -> list[CloudWatchMetric]:
        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        metric_name = data.get("Label", "")

        metrics = []

        for item in data.get("Datapoints", []):
            timestamp = item.get("Timestamp")
            parsed_timestamp = None
            if timestamp:
                try:
                    parsed_timestamp = datetime.fromisoformat(timestamp)
                except ValueError:
                    parsed_timestamp = None

            metric = CloudWatchMetric(
                lambda_id=lambda_id,
                metric_name=metric_name,
                metric_value=item.get("Average", 0.0),
                unit=item.get("Unit", ""),
                metric_timestamp=parsed_timestamp,
            )

            metrics.append(metric)

        return metrics