import os
import json
from groq import Groq
from dotenv import load_dotenv
from prompts import ADVISOR_SYSTEM_PROMPT, get_generate_prompt, get_evaluate_prompt

load_dotenv()

# ── 5-tier 模型配置 ───────────────────────────────────────────────────────────
TIER_TOP       = "openai/gpt-oss-120b"
TIER_UPPER_MID = "openai/gpt-oss-20b"
TIER_MID       = "qwen/qwen3-32b"
TIER_LOW       = "meta-llama/llama-4-scout-17b-16e-instruct"
TIER_DEBUG     = "llama-3.1-8b-instant"
TIER_FALLBACK  = "llama-3.3-70b-versatile" # 增加一个肯定存在的官方 ID

QUALITY_CASCADE = [TIER_TOP, TIER_UPPER_MID, TIER_MID, TIER_LOW, TIER_FALLBACK, TIER_DEBUG]

class TechAdvisor:
    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Groq API key is required. Please provide it in the input field or .env file.")
        self.client = Groq(api_key=api_key)

    def _call_ai(self, user_prompt: str) -> dict:
        last_error = None
        for model in QUALITY_CASCADE:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": ADVISOR_SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    model=model,
                    response_format={"type": "json_object"},
                    temperature=0.2
                )
                result = chat_completion.choices[0].message.content
                return json.loads(result)
            except Exception as e:
                last_error = str(e)
                continue
        return {"error": f"All models failed. Last error: {last_error}"}

    def generate_solutions(self, requirement: str) -> dict:
        return self._call_ai(get_generate_prompt(requirement))

    def evaluate_solution(self, solution: str) -> dict:
        return self._call_ai(get_evaluate_prompt(solution))
