import os
import logging
from typing import Union
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


class LLMManager:
    """Handles LLM initialization and configuration."""

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)

    def initialize_llm(self) -> Union[ChatOpenAI, ChatAnthropic]:
        """Initialize the language model based on configuration."""
        model_config = self.config_manager.get_model_config()
        provider = model_config.get("provider", "openai")

        if provider == "openai":
            return self._initialize_openai_llm(model_config)
        elif provider == "anthropic":
            return self._initialize_anthropic_llm(model_config)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _initialize_openai_llm(self, model_config: dict) -> ChatOpenAI:
        """Initialize OpenAI LLM with configuration."""
        # Use environment variable or passed key
        api_key = model_config.get("api_key") or os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not found in config or environment variables")

        llm = ChatOpenAI(
            model=model_config.get("name", "gpt-4o"),
            temperature=model_config.get("temperature", 0.2),
            api_key=api_key,
        )
        
        self.logger.info(f"Initialized OpenAI LLM: {model_config.get('name', 'gpt-4o')}")
        return llm

    def _initialize_anthropic_llm(self, model_config: dict) -> ChatAnthropic:
        """Initialize Anthropic LLM with configuration."""
        api_key = model_config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            raise ValueError("Anthropic API key not found in config or environment variables")

        llm = ChatAnthropic(
            model=model_config.get("name", "claude-3.5-sonnet-latest"),
            temperature=model_config.get("temperature", 0.2),
            api_key=api_key,
            timeout=model_config.get("timeout", 60.0),
        )
        
        self.logger.info(f"Initialized Anthropic LLM: {model_config.get('name', 'claude-3.5-sonnet-latest')}")
        return llm