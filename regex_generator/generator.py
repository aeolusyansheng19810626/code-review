import os

from groq import Groq

from regex_generator.prompts import SYSTEM_PROMPT, USER_PROMPT


TIER_TOP = "openai/gpt-oss-120b"
TIER_UPPER_MID = "openai/gpt-oss-20b"
TIER_MID = "qwen/qwen3-32b"
TIER_LOW = "meta-llama/llama-4-scout-17b-16e-instruct"
TIER_FALLBACK = "llama-3.3-70b-versatile"
TIER_DEBUG = "llama-3.1-8b-instant"

QUALITY_CASCADE = [TIER_TOP, TIER_UPPER_MID, TIER_MID, TIER_LOW, TIER_FALLBACK, TIER_DEBUG]


def generate_regex(description: str, language: str = "Python", samples: str = "", model: str = TIER_TOP) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
    client = Groq(api_key=api_key)

    user_prompt = USER_PROMPT.format(
        language=language,
        description=description,
        samples=samples if samples.strip() else "未提供",
    )

    models = [model] if model else QUALITY_CASCADE
    if model in QUALITY_CASCADE:
        models = [model] + [fallback for fallback in QUALITY_CASCADE if fallback != model]

    last_error = None
    for model_name in models:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                model=model_name,
                max_tokens=2048,
                temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            last_error = str(e)
            continue

    return f"正则生成失败：所有模型均不可用。最后错误：{last_error}"
