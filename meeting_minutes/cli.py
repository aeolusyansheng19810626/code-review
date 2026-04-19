import argparse
import sys

from dotenv import load_dotenv


load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser(description="会议纪要生成工具")
    parser.add_argument("file", help="会议记录文件路径（.txt）")
    parser.add_argument(
        "--mode",
        choices=["brief", "full"],
        default="full",
        help="输出模式：brief 要点摘要 / full 完整纪要",
    )
    parser.add_argument("--model", default="openai/gpt-oss-120b", help="使用的 Groq 模型")
    parser.add_argument("--output", "-o", help="输出文件路径（默认打印到终端）")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        transcript = f.read()

    if not transcript.strip():
        print("错误：文件内容为空。")
        sys.exit(1)

    print(f"正在生成{'要点摘要' if args.mode == 'brief' else '完整纪要'}...")
    from meeting_minutes.summarizer import summarize

    result = summarize(transcript, mode=args.mode, model=args.model)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"纪要已保存至：{args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
