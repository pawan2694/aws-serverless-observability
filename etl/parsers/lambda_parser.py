import json
from pathlib import Path

from app.models.lambda_function import LambdaFunction


class LambdaParser:

    def parse(self, file_path: str) -> list[LambdaFunction]:
        file_path = Path(file_path)

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        functions = data.get("Functions", [])

        lambda_functions = []

        for item in functions:
            handler = ""

            command = (
                item.get("ImageConfigResponse", {})
                .get("ImageConfig", {})
                .get("Command", [])
            )

            if command:
                handler = command[0]

            architecture = ""
            architectures = item.get("Architectures", [])
            if architectures:
                architecture = architectures[0]

            log_group = (
                item.get("LoggingConfig", {})
                .get("LogGroup", "")
            )

            lambda_function = LambdaFunction(
                function_name=item.get("FunctionName", ""),
                function_arn=item.get("FunctionArn", ""),
                runtime=item.get("Runtime", ""),
                handler=handler,
                role="",
                description=item.get("Description", ""),
                timeout=item.get("Timeout", 0),
                memory_size=item.get("MemorySize", 0),
                code_size=item.get("CodeSize", 0),
                version=item.get("Version", ""),
                package_type=item.get("PackageType", ""),
                architecture=architecture,
                last_modified=item.get("LastModified", ""),
                log_group=log_group,
                revision_id=item.get("RevisionId", ""),
            )

            lambda_functions.append(lambda_function)

        return lambda_functions