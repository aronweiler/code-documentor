import os
import yaml
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from .models import PipelineConfig


class ConfigManager:
    """Manages configuration loading and environment variables."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        load_dotenv()
        self._config = None
    
    def load_config(self) -> PipelineConfig:
        """Load configuration from YAML file."""
        if self._config is None:
            with open(self.config_path, 'r') as file:
                config_dict = yaml.safe_load(file)
            self._config = PipelineConfig(**config_dict)
        return self._config
    
    def get_api_key(self, provider: str) -> str:
        """Get API key for the specified provider."""
        key_mapping = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "azure_openai": "AZURE_OPENAI_API_KEY"
        }
        
        key_name = key_mapping.get(provider)
        if not key_name:
            raise ValueError(f"Unknown provider: {provider}")
        
        api_key = os.getenv(key_name)
        if not api_key:
            raise ValueError(f"API key not found for {provider}. Please set {key_name} in your .env file.")
        
        return api_key
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration including API keys."""
        config = self.load_config()
        model_config = config.model.copy()
        
        provider = model_config.get("provider", "openai")
        model_config["api_key"] = self.get_api_key(provider)
        
        # Add Azure-specific configuration if needed
        if provider == "azure_openai":
            model_config.update({
                "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")
            })
        
        return model_config
