import unittest

from app.rag.generator import RagGenerator


class DummyOllamaClient:
    def __init__(self, response: str | None = None, error: Exception | None = None):
        self.response = response
        self.error = error

    def generate(self, prompt: str) -> str:
        if self.error:
            raise self.error
        return self.response or ""


class RagGeneratorTests(unittest.TestCase):
    def test_uses_llm_answer_when_available(self):
        generator = RagGenerator(ollama_client=DummyOllamaClient(response="Local Llama answer"))
        result = generator.generate_response(
            "Show memory usage",
            [{
                "chunk": {
                    "text": "Memory Size 1024 MB",
                    "metadata": {"source": "CloudWatch Logs", "function_name": "demo"},
                },
                "score": 0.9,
            }],
        )
        self.assertEqual(result["answer"], "Local Llama answer")
        self.assertEqual(result["confidence_score"], "95%")

    def test_falls_back_to_rule_based_response_when_llm_fails(self):
        generator = RagGenerator(ollama_client=DummyOllamaClient(error=ConnectionError("offline")))
        result = generator.generate_response(
            "Show memory usage",
            [{
                "chunk": {
                    "text": "Memory Size 1024 MB",
                    "metadata": {"source": "CloudWatch Logs", "function_name": "demo"},
                },
                "score": 0.9,
            }],
        )
        self.assertIn("Based on retrieved Lambda configurations", result["answer"])
        self.assertIn("demo", result["answer"])


if __name__ == "__main__":
    unittest.main()
