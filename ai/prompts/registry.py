import logging
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger(__name__)

_PROMPT_DIR = Path(__file__).parent


@lru_cache(maxsize=10)
def load_prompt(name: str) -> str:
    prompt_file = _PROMPT_DIR / f"{name}.md"
    if not prompt_file.exists():
        logger.warning(f"Prompt file not found: {prompt_file}")
        return ""
    return prompt_file.read_text(encoding="utf-8")


def list_prompts() -> list[str]:
    return [f.stem for f in _PROMPT_DIR.glob("*.md")]
