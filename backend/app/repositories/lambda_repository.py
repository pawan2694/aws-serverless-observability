from sqlalchemy.orm import Session

from app.models.cloudwatch_log import CloudWatchLog
from app.models.cloudwatch_metric import CloudWatchMetric
from app.models.lambda_function import LambdaFunction


class LambdaRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, lambda_function: LambdaFunction) -> LambdaFunction:
        self.db.add(lambda_function)
        self.db.commit()
        self.db.refresh(lambda_function)
        return lambda_function

    def bulk_create(
        self,
        lambda_functions: list[LambdaFunction],
    ) -> None:
        self.db.query(CloudWatchMetric).delete(synchronize_session=False)
        self.db.query(CloudWatchLog).delete(synchronize_session=False)
        self.db.query(LambdaFunction).delete(synchronize_session=False)
        self.db.add_all(lambda_functions)
        self.db.commit()