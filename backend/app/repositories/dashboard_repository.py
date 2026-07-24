from sqlalchemy import Numeric, cast, func
from sqlalchemy.orm import Session

from app.models.lambda_function import LambdaFunction
from app.models.cloudwatch_metric import CloudWatchMetric
from app.models.cloudwatch_log import CloudWatchLog


class DashboardRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_summary(self):

        return {
            "total_lambdas":
                self.db.query(func.count(LambdaFunction.id)).scalar(),

            "total_metrics":
                self.db.query(func.count(CloudWatchMetric.id)).scalar(),

            "total_logs":
                self.db.query(func.count(CloudWatchLog.id)).scalar(),
        }


    def get_high_duration(self):

        result = (
            self.db.query(
                LambdaFunction.function_name,
                func.round(
                    cast(
                        func.avg(CloudWatchMetric.metric_value),
                        Numeric,
                    ),
                    2,
                ).label("avg_duration"),
                LambdaFunction.memory_size,
                LambdaFunction.timeout,
            )
            .join(
                CloudWatchMetric,
                LambdaFunction.id == CloudWatchMetric.lambda_id,
            )
            .filter(
                CloudWatchMetric.metric_name == "Duration"
            )
            .group_by(
                LambdaFunction.id,
                LambdaFunction.function_name,
                LambdaFunction.memory_size,
                LambdaFunction.timeout,
            )
            .order_by(
                func.avg(CloudWatchMetric.metric_value).desc()
            )
            .limit(10)
            .all()
        )

        return result