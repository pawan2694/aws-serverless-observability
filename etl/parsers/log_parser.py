import json
import re
from datetime import datetime
from pathlib import Path

from app.models.cloudwatch_log import CloudWatchLog


class LogParser:

    REQUEST_ID_PATTERN = re.compile(
        r"RequestId:\s([a-f0-9\-]+)"
    )

    def parse(
        self,
        file_path: str,
        lambda_id: int,
    ) -> list[CloudWatchLog]:

        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        logs = []

        for item in data.get("events", []):

            message = item.get("message", "")

            request_id = None

            match = self.REQUEST_ID_PATTERN.search(message)

            if match:
                request_id = match.group(1)

            log = CloudWatchLog(
                lambda_id=lambda_id,
                request_id=request_id,
                event_id=item.get("eventId"),
                log_stream_name=item.get("logStreamName"),
                message=message,
                log_timestamp=datetime.fromtimestamp(
                    item.get("timestamp") / 1000
                ),
                ingestion_time=datetime.fromtimestamp(
                    item.get("ingestionTime") / 1000
                ),
            )

            logs.append(log)

        return logs