from sqlalchemy.orm import Session

from app.models.cloudwatch_metric import CloudWatchMetric


class MetricLoader:

    def __init__(self, db: Session):
        self.db = db

    def load(
        self,
        metrics: list[CloudWatchMetric],
    ) -> None:
        self.db.query(CloudWatchMetric).delete(synchronize_session=False)
        self.db.add_all(metrics)
        self.db.commit()