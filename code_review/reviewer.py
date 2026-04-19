import os
import json
from importlib import import_module
from groq import Groq
from dotenv import load_dotenv

try:
    from code_review.prompts import REVIEW_SYSTEM_PROMPT, get_review_prompt
except ImportError:
    prompts = import_module("prompts")
    REVIEW_SYSTEM_PROMPT = prompts.REVIEW_SYSTEM_PROMPT
    get_review_prompt = prompts.get_review_prompt

load_dotenv()

# ── 5-tier 模型配置 ───────────────────────────────────────────────────────────
TIER_TOP       = "openai/gpt-oss-120b"
TIER_UPPER_MID = "openai/gpt-oss-20b"
TIER_MID       = "qwen/qwen3-32b"
TIER_LOW       = "meta-llama/llama-4-scout-17b-16e-instruct"
TIER_DEBUG     = "llama-3.1-8b-instant"

QUALITY_CASCADE = [TIER_TOP, TIER_UPPER_MID, TIER_MID, TIER_LOW, TIER_DEBUG]

class CodeReviewer:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=api_key)

    def review_code(self, code: str) -> dict:
        """Review code string and return JSON result with fallback logic."""
        last_error = None
        for model in QUALITY_CASCADE:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
                        {"role": "user", "content": get_review_prompt(code)},
                    ],
                    model=model,
                    response_format={"type": "json_object"},
                )
                result = chat_completion.choices[0].message.content
                return json.loads(result)
            except Exception as e:
                last_error = str(e)
                # 如果是 404/400 (模型不存在) 或 429 (额度限制)，尝试下一个
                continue
        
        return {"error": f"All models failed. Last error: {last_error}"}

    def review_file(self, file_path: str) -> dict:
        """Review code from a file and return JSON result."""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return self.review_code(code)
