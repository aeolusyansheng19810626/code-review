import os

from groq import Groq

from langsmith import traceable, get_current_run_tree
from weekly_report.prompts import SYSTEM_PROMPT, USER_PROMPT


TIER_TOP = "openai/gpt-oss-120b"
TIER_UPPER_MID = "openai/gpt-oss-20b"
TIER_MID = "qwen/qwen3-32b"
TIER_LOW = "meta-llama/llama-4-scout-17b-16e-instruct"
TIER_FALLBACK = "llama-3.3-70b-versatile"
TIER_DEBUG = "llama-3.1-8b-instant"

QUALITY_CASCADE = [TIER_TOP, TIER_UPPER_MID, TIER_MID, TIER_LOW, TIER_FALLBACK, TIER_DEBUG]


@traceable
def generate_report(
    content: str,
    author: str = "",
    week: str = "",
    next_plan: str = "",
    model: str = TIER_TOP,
    return_model: bool = False,
) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable.")
    client = Groq(api_key=api_key)

    user_prompt = USER_PROMPT.format(
        author=author if author.strip() else "未填写",
        week=week if week.strip() else "本周",
        content=content,
        next_plan=next_plan if next_plan.strip() else "未填写",
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
            result = chat_completion.choices[0].message.content
            
            # LangSmith 上报 token
            run = get_current_run_tree()
            if run:
                usage = chat_completion.usage
                run.end(
                    outputs={"output": result},
                    metadata={
                        "input_tokens": usage.prompt_tokens,
                        "output_tokens": usage.completion_tokens,
                        "total_tokens": usage.total_tokens,
                        "model": model_name,
                    }
                )
            return (result, model_name) if return_model else result
        except Exception as e:
            last_error = str(e)
            continue

    result = f"周报生成失败：所有模型均不可用。最后错误：{last_error}"
    return (result, "") if return_model else result
