import unittest
from unittest.mock import patch

from shared.llm_factory import (
    _normalize_openai_v1_base_url,
    _parse_truthy_env_flag,
    create_llm_service,
)


class NormalizeOpenAiV1BaseUrlTests(unittest.TestCase):
    def test_appends_v1_by_default(self):
        self.assertEqual(
            _normalize_openai_v1_base_url("https://host"),
            "https://host/v1",
        )

    def test_skips_append_when_disabled(self):
        self.assertEqual(
            _normalize_openai_v1_base_url("https://host/api", append_v1=False),
            "https://host/api",
        )

    def test_preserves_existing_v1_suffix(self):
        self.assertEqual(
            _normalize_openai_v1_base_url("https://host/v1"),
            "https://host/v1",
        )


class ParseTruthyEnvFlagTests(unittest.TestCase):
    def test_false_string(self):
        self.assertFalse(_parse_truthy_env_flag("false", default=True))

    def test_none_uses_default(self):
        self.assertTrue(_parse_truthy_env_flag(None, default=True))
        self.assertFalse(_parse_truthy_env_flag(None, default=False))


class CustomLlmProviderTests(unittest.TestCase):
    def test_requires_base_url(self):
        with self.assertRaises(ValueError) as ctx:
            create_llm_service(
                {
                    "llm_provider": "openai_compatible",
                    "custom_llm_base_url": "",
                    "custom_llm_model": "m",
                }
            )
        self.assertIn("CUSTOM_LLM_BASE_URL", str(ctx.exception))

    @patch("shared.llm_factory.OpenAILlmService")
    def test_append_v1_false_from_string_env_vars(self, mock_openai_llm):
        mock_openai_llm.return_value = object()
        create_llm_service(
            {
                "llm_provider": "custom",
                "custom_llm_base_url": "https://host/api",
                "custom_llm_api_key": "key",
                "custom_llm_model": "m",
                "custom_llm_append_v1": "false",
            }
        )
        _, kwargs = mock_openai_llm.call_args
        self.assertEqual(kwargs["base_url"], "https://host/api")

    def test_creates_openai_llm_service(self):
        svc = create_llm_service(
            {
                "llm_provider": "custom_llm",
                "custom_llm_base_url": "http://localhost:8000",
                "custom_llm_api_key": "key",
                "custom_llm_model": "llama",
            }
        )
        self.assertEqual(type(svc).__name__, "OpenAILlmService")


if __name__ == "__main__":
    unittest.main()