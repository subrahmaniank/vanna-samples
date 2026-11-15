import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger("LlmFactory")

try:
    from vanna.integrations.openai import OpenAILlmService
except ImportError:
    OpenAILlmService = None

try:
    from vanna.integrations.azureopenai.llm import AzureOpenAILlmService
except ImportError:
    AzureOpenAILlmService = None


def create_llm_service(env_vars: Optional[Dict[str, Any]] = None) -> Any:
    """
    Factory creating an LLM service based on environment configuration.
    Supports:
      1. 'openrouter' / 'open_router':
         OpenRouter unified API endpoint (https://openrouter.ai/api/v1)
      2. 'bedrock_mantle' / 'bedrock' / 'aws_bedrock':
         AWS Bedrock Mantle native OpenAI-compatible inference endpoint
         (e.g. https://bedrock-mantle.<region>.api.aws/v1)
      3. 'azure_openai' / 'azure':
         Azure OpenAI service endpoint
      4. 'openai':
         Standard OpenAI platform
    """
    if env_vars is None:
        env_vars = {}

    provider = env_vars.get("llm_provider") or os.getenv("LLM_PROVIDER", "").strip().lower()

    # OpenRouter configuration
    openrouter_key = (
        env_vars.get("openrouter_api_key")
        or os.getenv("OPENROUTER_API_KEY")
        or ""
    ).strip()
    openrouter_model = (
        env_vars.get("openrouter_model")
        or os.getenv("OPENROUTER_MODEL")
        or "anthropic/claude-3.5-sonnet"
    ).strip()
    openrouter_base_url = (
        env_vars.get("openrouter_base_url")
        or os.getenv("OPENROUTER_BASE_URL")
        or "https://openrouter.ai/api/v1"
    ).strip()
    openrouter_site_url = (
        env_vars.get("openrouter_site_url")
        or os.getenv("OPENROUTER_SITE_URL")
        or os.getenv("OR_SITE_URL")
        or ""
    ).strip()
    openrouter_app_name = (
        env_vars.get("openrouter_app_name")
        or os.getenv("OPENROUTER_APP_NAME")
        or os.getenv("OR_APP_NAME")
        or "Vanna 2.0 SQL Agent"
    ).strip()

    # Bedrock Mantle configuration
    bedrock_endpoint = (
        env_vars.get("bedrock_mantle_endpoint")
        or os.getenv("BEDROCK_MANTLE_ENDPOINT")
        or os.getenv("AWS_BEDROCK_MANTLE_ENDPOINT")
        or ""
    ).strip()
    bedrock_key = (
        env_vars.get("bedrock_mantle_api_key")
        or os.getenv("BEDROCK_MANTLE_API_KEY")
        or os.getenv("AWS_BEDROCK_API_KEY")
        or os.getenv("AWS_BEARER_TOKEN_BEDROCK")
        or ""
    ).strip()
    bedrock_model = (
        env_vars.get("bedrock_mantle_model")
        or os.getenv("BEDROCK_MANTLE_MODEL")
        or os.getenv("AWS_BEDROCK_MODEL")
        or "anthropic.claude-3-5-sonnet-20241022-v2:0"
    ).strip()
    bedrock_region = (
        env_vars.get("bedrock_region")
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1"
    ).strip()
    bedrock_project_id = (
        env_vars.get("bedrock_mantle_project_id")
        or os.getenv("BEDROCK_MANTLE_PROJECT_ID")
        or ""
    ).strip()

    # Azure OpenAI configuration
    azure_endpoint = (
        env_vars.get("azure_openai_endpoint")
        or os.getenv("AZURE_OPENAI_ENDPOINT")
        or ""
    ).strip()
    azure_key = (
        env_vars.get("azure_openai_key")
        or os.getenv("AZURE_OPENAI_API_KEY")
        or ""
    ).strip()
    azure_model = (
        env_vars.get("azure_openai_model")
        or os.getenv("AZURE_OPENAI_MODEL")
        or "gpt-4o-mini"
    ).strip()
    azure_api_version = (
        env_vars.get("azure_openai_api_version")
        or os.getenv("AZURE_OPENAI_API_VERSION")
        or "2024-12-01-preview"
    ).strip()

    # Auto-detect provider if not explicitly given
    if not provider:
        if openrouter_key or os.getenv("OPENROUTER_API_KEY"):
            provider = "openrouter"
        elif bedrock_endpoint or bedrock_key or os.getenv("AWS_BEDROCK_MANTLE_ENDPOINT"):
            provider = "bedrock_mantle"
        elif azure_endpoint:
            provider = "azure_openai"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        else:
            provider = "openrouter" if openrouter_key else "bedrock_mantle"

    logger.info(f"Creating LLM service with provider: {provider}")

    if provider in ("openrouter", "open_router"):
        if not OpenAILlmService:
            raise ImportError(
                "OpenAILlmService is required for OpenRouter. Install with: pip install 'vanna[openai]'"
            )

        base_url = openrouter_base_url or "https://openrouter.ai/api/v1"
        cleaned_base_url = base_url.rstrip("/")
        if not cleaned_base_url.endswith("/v1") and "/v1" not in cleaned_base_url:
            cleaned_base_url = f"{cleaned_base_url}/v1"

        extra_headers: Dict[str, str] = {}
        if openrouter_site_url:
            extra_headers["HTTP-Referer"] = openrouter_site_url
        if openrouter_app_name:
            extra_headers["X-Title"] = openrouter_app_name

        extra_kwargs: Dict[str, Any] = {}
        if extra_headers:
            extra_kwargs["default_headers"] = extra_headers

        logger.info(
            f"Using OpenRouter at: {cleaned_base_url} with model: {openrouter_model}"
        )
        return OpenAILlmService(
            model=openrouter_model,
            api_key=openrouter_key or "dummy-key",
            base_url=cleaned_base_url,
            **extra_kwargs
        )

    elif provider in ("bedrock_mantle", "bedrock", "aws_bedrock", "mantle"):
        if not OpenAILlmService:
            raise ImportError(
                "OpenAILlmService is required for Bedrock Mantle. Install with: pip install 'vanna[openai]'"
            )

        endpoint = bedrock_endpoint
        if not endpoint:
            endpoint = f"https://bedrock-mantle.{bedrock_region}.api.aws/v1"

        # Normalize URL: ensure /v1 path is present if standard Mantle host
        cleaned_endpoint = endpoint.rstrip("/")
        if not cleaned_endpoint.endswith("/v1") and "/v1" not in cleaned_endpoint:
            cleaned_endpoint = f"{cleaned_endpoint}/v1"

        extra_kwargs = {}
        if bedrock_project_id:
            extra_kwargs["default_headers"] = {"OpenAI-Project": bedrock_project_id}

        logger.info(
            f"Using AWS Bedrock Mantle at: {cleaned_endpoint} with model: {bedrock_model}"
        )
        return OpenAILlmService(
            model=bedrock_model,
            api_key=bedrock_key or "dummy-key",
            base_url=cleaned_endpoint,
            **extra_kwargs
        )

    elif provider in ("azure_openai", "azure"):
        if AzureOpenAILlmService and azure_endpoint:
            cleaned_endpoint = azure_endpoint.rstrip("/") + "/"
            logger.info(f"Using AzureOpenAILlmService at: {cleaned_endpoint} with model: {azure_model}")
            return AzureOpenAILlmService(
                model=azure_model,
                api_key=azure_key or "dummy-key",
                azure_endpoint=cleaned_endpoint,
                api_version=azure_api_version
            )
        elif OpenAILlmService:
            cleaned_endpoint = azure_endpoint.rstrip("/") + "/" if azure_endpoint else None
            logger.info(f"Using OpenAILlmService for Azure at: {cleaned_endpoint}")
            return OpenAILlmService(
                model=azure_model,
                api_key=azure_key or "dummy-key",
                base_url=cleaned_endpoint
            )
        else:
            raise ImportError("AzureOpenAILlmService or OpenAILlmService is required.")

    elif provider == "openai":
        if not OpenAILlmService:
            raise ImportError("OpenAILlmService is required. Install with: pip install 'vanna[openai]'")
        openai_key = os.getenv("OPENAI_API_KEY", "").strip() or None
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
        logger.info(f"Using standard OpenAI with model: {openai_model}")
        return OpenAILlmService(
            model=openai_model,
            api_key=openai_key
        )

    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER '{provider}'. Supported options: 'openrouter', 'bedrock_mantle', 'azure_openai', 'openai'"
        )
