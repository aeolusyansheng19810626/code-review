ADVISOR_SYSTEM_PROMPT = "你是一个资深软件架构师，擅长技术决策分析和架构设计。"

GENERATE_SOLUTIONS_PROMPT = """
用户描述了一个技术需求，请生成3个可行的技术方案并对比，输出纯 JSON，不要包含任何 Markdown 格式：
{
  "requirement": "需求摘要",
  "solutions": [
    {
      "id": 1,
      "name": "方案名称",
      "description": "方案描述",
      "tech_stack": ["技术1", "技术2"],
      "pros": ["优点1", "优点2"],
      "cons": ["缺点1", "缺点2"],
      "complexity": "低|中|高",
      "cost": "低|中|高",
      "timeline": "预估工期",
      "best_for": "适合什么场景"
    }
  ],
  "recommendation": 1,
  "recommendation_reasoning": "推荐理由"
}

待处理需求：
{requirement}
"""

EVALUATE_SOLUTION_PROMPT = """
用户提供了一个技术方案，请从多维度深度评估，输出纯 JSON，不要包含任何 Markdown 格式：
{
  "solution_name": "方案名称",
  "overall_score": 0.0,
  "dimensions": [
    {
      "name": "可扩展性|性能|安全性|可维护性|成本|团队匹配度",
      "score": 0-10,
      "analysis": "分析说明",
      "risks": ["风险1"],
      "suggestions": ["建议1"]
    }
  ],
  "decision": "推荐采用|谨慎采用|不推荐",
  "decision_reasoning": "决策理由",
  "alternatives": ["可替代方案1"]
}

待评估方案：
{solution}
"""

def get_generate_prompt(requirement: str) -> str:
    return GENERATE_SOLUTIONS_PROMPT.format(requirement=requirement)

def get_evaluate_prompt(solution: str) -> str:
    return EVALUATE_SOLUTION_PROMPT.format(solution=solution)
