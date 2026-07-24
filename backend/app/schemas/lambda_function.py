from pydantic import BaseModel, ConfigDict


class LambdaFunctionIngestion(BaseModel):
    function_name: str
    runtime: str
    handler: str
    role: str
    memory_size: int
    timeout: int
    last_modified: str
    code_size: int
    architecture: str


class LambdaFunctionResponse(BaseModel):
    id: int
    function_name: str
    runtime: str
    handler: str
    role: str
    memory_size: int
    timeout: int
    last_modified: str
    code_size: int
    architecture: str

    model_config = ConfigDict(
        from_attributes=True
    )