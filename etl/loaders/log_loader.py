from sqlalchemy.orm import Session

from app.models.cloudwatch_log import CloudWatchLog


class LogLoader:

    def __init__(self, db: Session):
        self.db = db

    def load(
        self,
        logs: list[CloudWatchLog],
    ) -> None:
        self.db.query(CloudWatchLog).delete(synchronize_session=False)
        self.db.add_all(logs)
        self.db.commit()