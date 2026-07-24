from sqlalchemy.orm import Session

from app.models.lambda_function import LambdaFunction
from app.repositories.lambda_repository import LambdaRepository


class LambdaLoader:

    def __init__(self, db: Session):
        self.repository = LambdaRepository(db)

    def load(
        self,
        lambda_functions: list[LambdaFunction],
    ) -> None:

        self.repository.bulk_create(lambda_functions)