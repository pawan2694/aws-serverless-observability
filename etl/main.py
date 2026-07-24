from pathlib import Path

from app.db.base import Base
from app.db.database import engine
from app.db.session import SessionLocal
from app.models.cloudwatch_log import CloudWatchLog
from app.models.cloudwatch_metric import CloudWatchMetric
from app.models.lambda_function import LambdaFunction
from etl.loaders.lambda_loader import LambdaLoader
from etl.loaders.log_loader import LogLoader
from etl.loaders.metric_loader import MetricLoader
from etl.parsers.lambda_parser import LambdaParser
from etl.parsers.log_parser import LogParser
from etl.parsers.metric_parser import MetricParser

ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"
METRICS_DIR = RAW_DIR / "metrics"
SKIP_FILES = {
    "lambda-functions.json",
    "lambda-metrics.json",
    "s3-buckets.json",
    "sns-topics.json",
    "sqs-queues.json",
}


def _handler_suffix(handler: str) -> str:
    if not handler:
        return ""
    return handler.rsplit(".", 1)[-1].strip().lower()


def _lookup_lambda_id(db: SessionLocal, raw_name: str) -> int | None:
    normalized = raw_name.strip().lower()

    if not normalized:
        return None

    lambda_functions = db.query(LambdaFunction).all()
    for lambda_function in lambda_functions:
        function_name = (lambda_function.function_name or "").lower()
        handler_suffix = _handler_suffix(lambda_function.handler)

        if normalized == function_name:
            return lambda_function.id
        if normalized == handler_suffix:
            return lambda_function.id

    return None


def _resolve_lambda_id_from_metric_file(db: SessionLocal, file_name: str) -> int | None:
    stem = Path(file_name).stem
    if "_" not in stem:
        return None

    metric_name = stem.rsplit("_", 1)[-1]
    if metric_name not in {"Duration", "Errors", "Invocations", "Throttles"}:
        return None

    lambda_name = stem.rsplit("_", 1)[0]
    return _lookup_lambda_id(db, lambda_name)


def _resolve_lambda_id_from_log_file(db: SessionLocal, file_name: str) -> int | None:
    stem = Path(file_name).stem
    if stem.endswith("_page1") or stem.endswith("_page2"):
        stem = stem.rsplit("_page", 1)[0]

    return _lookup_lambda_id(db, stem)


def main() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        lambda_parser = LambdaParser()
        lambda_functions = lambda_parser.parse(str(RAW_DIR / "lambda-functions.json"))

        lambda_loader = LambdaLoader(db)
        lambda_loader.load(lambda_functions)

        metric_parser = MetricParser()
        log_parser = LogParser()

        loaded_metrics: list[CloudWatchMetric] = []
        loaded_logs: list[CloudWatchLog] = []

        for metric_file in sorted(METRICS_DIR.glob("*.json")):
            lambda_id = _resolve_lambda_id_from_metric_file(db, metric_file.name)
            if lambda_id is None:
                continue

            loaded_metrics.extend(metric_parser.parse(str(metric_file), lambda_id))

        for raw_file in sorted(RAW_DIR.glob("*.json")):
            if raw_file.name in SKIP_FILES:
                continue
            if raw_file.name.startswith("lambda-"):
                continue
            if raw_file.is_dir():
                continue

            lambda_id = _resolve_lambda_id_from_log_file(db, raw_file.name)
            if lambda_id is None:
                continue

            parsed_logs = log_parser.parse(str(raw_file), lambda_id)
            if parsed_logs:
                loaded_logs.extend(parsed_logs)

        if loaded_metrics:
            MetricLoader(db).load(loaded_metrics)

        if loaded_logs:
            LogLoader(db).load(loaded_logs)

        print(f"{len(lambda_functions)} Lambda Functions Imported Successfully.")
        print(f"{len(loaded_metrics)} CloudWatch Metrics Imported Successfully.")
        print(f"{len(loaded_logs)} CloudWatch Logs Imported Successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()