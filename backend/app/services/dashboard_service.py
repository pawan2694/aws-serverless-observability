from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):
        self.repository = DashboardRepository(db)

    def get_summary(self):
        return self.repository.get_summary()

    def get_high_duration(self):
        return self.repository.get_high_duration()