"""
Environment Configuration Loader
Loads and validates environment variables with defaults
"""
import os
from typing import Any, Dict
from pathlib import Path


class EnvConfig:
    """Environment configuration with validation and defaults"""
    
    # API Keys
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    STABILITY_API_KEY: str = ""
    HUGGINGFACE_TOKEN: str = ""
    
    # GitHub Configuration
    GITHUB_TOKEN: str = ""
    GITHUB_USERNAME: str = ""
    GITHUB_DEFAULT_REPO: str = ""
    GIT_USER_NAME: str = ""
    GIT_USER_EMAIL: str = ""
    GIT_AUTO_COMMIT: bool = True
    GIT_AUTO_PUSH: bool = False
    GIT_BRANCH_PREFIX: str = "linguistic-bridges"
    GIT_COMMIT_MESSAGE_TEMPLATE: str = "[{agent}] {action}: {description}"
    
    # System Configuration
    MAX_PARALLEL_AGENTS: int = 10
    DEFAULT_MODEL: str = "claude-sonnet-4-5"
    WORKSPACE_PATH: str = ".claude/workspace"
    MAX_EVOLUTION_ITERATIONS: int = 3
    HYPOTHESIS_GENERATION_COUNT: int = 7
    MAX_TOKENS: int = 8000
    TEMPERATURE: float = 0.7
    HUMAN_APPROVAL_TIMEOUT: int = 3600
    DEBUG_MODE: bool = False
    PROGRESS_CHECK_INTERVAL: int = 300
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_FACTOR: int = 2
    VECTOR_DB_PATH: str = "./data/vector_db"
    GRACEFUL_DEGRADATION: bool = True
    
    def __init__(self):
        """Load configuration from environment variables"""
        self._load_from_env()
    
    def _load_from_env(self):
        """Load all configuration from environment variables"""
        # API Keys
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
        self.STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
        self.HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
        
        # GitHub Configuration
        self.GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
        self.GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
        self.GITHUB_DEFAULT_REPO = os.getenv("GITHUB_DEFAULT_REPO", "")
        self.GIT_USER_NAME = os.getenv("GIT_USER_NAME", "")
        self.GIT_USER_EMAIL = os.getenv("GIT_USER_EMAIL", "")
        self.GIT_AUTO_COMMIT = os.getenv("GIT_AUTO_COMMIT", "true").lower() == "true"
        self.GIT_AUTO_PUSH = os.getenv("GIT_AUTO_PUSH", "false").lower() == "true"
        self.GIT_BRANCH_PREFIX = os.getenv("GIT_BRANCH_PREFIX", "linguistic-bridges")
        self.GIT_COMMIT_MESSAGE_TEMPLATE = os.getenv(
            "GIT_COMMIT_MESSAGE_TEMPLATE",
            "[{agent}] {action}: {description}"
        )
        
        # System Configuration with type conversion
        self.MAX_PARALLEL_AGENTS = int(os.getenv("MAX_PARALLEL_AGENTS", "10"))
        self.DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-5")
        self.WORKSPACE_PATH = os.getenv("WORKSPACE_PATH", ".claude/workspace")
        self.MAX_EVOLUTION_ITERATIONS = int(os.getenv("MAX_EVOLUTION_ITERATIONS", "3"))
        self.HYPOTHESIS_GENERATION_COUNT = int(os.getenv("HYPOTHESIS_GENERATION_COUNT", "7"))
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8000"))
        self.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
        self.HUMAN_APPROVAL_TIMEOUT = int(os.getenv("HUMAN_APPROVAL_TIMEOUT", "3600"))
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.PROGRESS_CHECK_INTERVAL = int(os.getenv("PROGRESS_CHECK_INTERVAL", "300"))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
        self.RETRY_BACKOFF_FACTOR = int(os.getenv("RETRY_BACKOFF_FACTOR", "2"))
        self.VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
        self.GRACEFUL_DEGRADATION = os.getenv("GRACEFUL_DEGRADATION", "true").lower() == "true"
        
        # Validate and create directories
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration values"""
        # Validate model name
        valid_models = ["claude-sonnet-4-5", "claude-opus-4", "gemini-2.0-flash"]
        if self.DEFAULT_MODEL not in valid_models:
            print(f"Warning: Unknown model {self.DEFAULT_MODEL}, using claude-sonnet-4-5")
            self.DEFAULT_MODEL = "claude-sonnet-4-5"
        
        # Validate numeric ranges
        if self.MAX_PARALLEL_AGENTS < 1:
            self.MAX_PARALLEL_AGENTS = 1
        if self.MAX_PARALLEL_AGENTS > 50:
            print(f"Warning: MAX_PARALLEL_AGENTS={self.MAX_PARALLEL_AGENTS} is very high, consider reducing")
        
        if not (0.0 <= self.TEMPERATURE <= 2.0):
            print(f"Warning: TEMPERATURE={self.TEMPERATURE} out of range [0.0, 2.0], using 0.7")
            self.TEMPERATURE = 0.7
        
        if self.MAX_EVOLUTION_ITERATIONS < 1:
            self.MAX_EVOLUTION_ITERATIONS = 1
        
        if self.HYPOTHESIS_GENERATION_COUNT < 1:
            self.HYPOTHESIS_GENERATION_COUNT = 1
        
        # Create workspace directory
        Path(self.WORKSPACE_PATH).mkdir(parents=True, exist_ok=True)
        Path(self.VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get LLM model configuration"""
        # Map environment model names to actual API model identifiers
        model_mapping = {
            "claude-sonnet-4-5": "claude-sonnet-4-5-20250929",
            "claude-opus-4": "claude-opus-4-20250514",
            "gemini-2.0-flash": "gemini-2.0-flash-001"
        }
        
        return {
            "model": model_mapping.get(self.DEFAULT_MODEL, "claude-sonnet-4-5-20250929"),
            "max_tokens": self.MAX_TOKENS,
            "temperature": self.TEMPERATURE
        }
    
    def get_supervisor_config(self) -> Dict[str, Any]:
        """Get supervisor agent configuration"""
        return {
            "max_iterations": 100,
            "progress_check_interval": self.PROGRESS_CHECK_INTERVAL,
            "conflict_resolution_enabled": True,
            "max_parallel_agents": self.MAX_PARALLEL_AGENTS
        }
    
    def get_research_config(self) -> Dict[str, Any]:
        """Get research guild configuration"""
        return {
            "hypothesis": {
                "generation_batch_size": self.HYPOTHESIS_GENERATION_COUNT,
                "evolution_rounds": self.MAX_EVOLUTION_ITERATIONS,
                "ranking_method": "elo_tournament"
            },
            "meta_review": {
                "analysis_frequency": 10
            }
        }
    
    def get_failure_recovery_config(self) -> Dict[str, Any]:
        """Get failure recovery configuration"""
        return {
            "max_retries": self.MAX_RETRIES,
            "backoff_factor": self.RETRY_BACKOFF_FACTOR,
            "fallback_agents_enabled": True,
            "graceful_degradation": self.GRACEFUL_DEGRADATION
        }
    
    def get_human_approval_config(self) -> Dict[str, Any]:
        """Get human approval configuration"""
        return {
            "required_for": [
                "finalize_hypothesis",
                "deploy_experiment",
                "major_code_changes"
            ],
            "timeout": self.HUMAN_APPROVAL_TIMEOUT if self.HUMAN_APPROVAL_TIMEOUT > 0 else None
        }
    
    def get_github_config(self) -> Dict[str, Any]:
        """Get GitHub/Git configuration"""
        return {
            "github_token": self.GITHUB_TOKEN,
            "github_username": self.GITHUB_USERNAME,
            "github_default_repo": self.GITHUB_DEFAULT_REPO,
            "git_user_name": self.GIT_USER_NAME,
            "git_user_email": self.GIT_USER_EMAIL,
            "auto_commit": self.GIT_AUTO_COMMIT,
            "auto_push": self.GIT_AUTO_PUSH,
            "branch_prefix": self.GIT_BRANCH_PREFIX,
            "commit_message_template": self.GIT_COMMIT_MESSAGE_TEMPLATE
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "api_keys": {
                "anthropic": bool(self.ANTHROPIC_API_KEY),
                "google": bool(self.GOOGLE_API_KEY),
                "tavily": bool(self.TAVILY_API_KEY),
                "stability": bool(self.STABILITY_API_KEY),
                "huggingface": bool(self.HUGGINGFACE_TOKEN),
                "github": bool(self.GITHUB_TOKEN)
            },
            "github": {
                "username": self.GITHUB_USERNAME,
                "default_repo": self.GITHUB_DEFAULT_REPO,
                "auto_commit": self.GIT_AUTO_COMMIT,
                "auto_push": self.GIT_AUTO_PUSH,
                "branch_prefix": self.GIT_BRANCH_PREFIX
            },
            "system": {
                "max_parallel_agents": self.MAX_PARALLEL_AGENTS,
                "default_model": self.DEFAULT_MODEL,
                "workspace_path": self.WORKSPACE_PATH,
                "max_evolution_iterations": self.MAX_EVOLUTION_ITERATIONS,
                "hypothesis_generation_count": self.HYPOTHESIS_GENERATION_COUNT,
                "max_tokens": self.MAX_TOKENS,
                "temperature": self.TEMPERATURE,
                "debug_mode": self.DEBUG_MODE,
                "progress_check_interval": self.PROGRESS_CHECK_INTERVAL,
                "max_retries": self.MAX_RETRIES,
                "vector_db_path": self.VECTOR_DB_PATH,
                "graceful_degradation": self.GRACEFUL_DEGRADATION
            }
        }
    
    def __repr__(self) -> str:
        config_dict = self.to_dict()
        return f"EnvConfig({config_dict})"


# Global configuration instance
_config = None

def get_config() -> EnvConfig:
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = EnvConfig()
    return _config


def reload_config() -> EnvConfig:
    """Reload configuration from environment"""
    global _config
    _config = EnvConfig()
    return _config
