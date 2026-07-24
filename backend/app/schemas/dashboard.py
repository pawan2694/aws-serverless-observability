from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_lambdas: int
    total_metrics: int
    total_logs: int

class HighDurationResponse(BaseModel):
    function_name: str
    avg_duration: float
    memory_size: int
    timeout: int