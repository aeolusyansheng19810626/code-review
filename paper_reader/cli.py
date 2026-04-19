import argparse
import os
import sys

from dotenv import load_dotenv


load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser(description="论文精读工具")
    parser.add_argument("file", help="论文文件路径（.txt 或 .pdf）")
    parser.add_argument("--model", default="openai/gpt-oss-120b", help="使用的 Groq 模型")
    parser.add_argument("--output", "-o", help="输出文件路径（默认打印到终端）")
    args = parser.parse_args()

    # 读取文件
    if args.file.endswith(".pdf"):
        try:
            import pdfplumber

            with pdfplumber.open(args.file) as pdf:
                paper_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except ImportError:
            print("请安装 pdfplumber：pip install pdfplumber")
            sys.exit(1)
    else:
        with open(args.file, "r", encoding="utf-8") as f:
            paper_text = f.read()

    if not paper_text.strip():
        print("错误：文件内容为空或无法提取文字。")
        sys.exit(1)

    print(f"正在分析论文：{os.path.basename(args.file)}...")
    from paper_reader.reader import read_paper

    result, used_model = read_paper(paper_text, model=args.model, return_model=True)
    if used_model:
        print(f"使用模型：{used_model}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"分析报告已保存至：{args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
