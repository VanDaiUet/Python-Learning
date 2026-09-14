"""Demo tìm kiếm từ khóa và agent giả lập; dùng đáp án, không sửa bài tập.

Chạy: python demo.py
Dữ liệu: du_lieu/documents.json nằm cùng thư mục với script này.
Không gọi LLM, embedding/dense retrieval, mạng, shell hay tool bên ngoài.
"""

import json
from pathlib import Path
import sys

from dap_an import lexical_search, run_agent


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    data_path = Path(__file__).resolve().parent / "du_lieu" / "documents.json"
    try:
        documents = json.loads(data_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"Chưa đọc được du_lieu/documents.json: {type(error).__name__}")
        return 1
    fields = {"doc_id", "title", "text", "source", "updated_at"}
    if (not isinstance(documents, list)
            or not all(isinstance(doc, dict) and fields <= set(doc)
                       and all(isinstance(doc[key], str) for key in fields) for doc in documents)):
        print("Dữ liệu cần là list document có doc_id, title, text, source, updated_at dạng str.")
        return 1

    query = "Học phí khóa Python nền tảng"
    print("DEMO THAM KHẢO — lexical retrieval + policy/agent GIẢ LẬP")
    print("Không gọi LLM; không có embedding/dense retrieval hoặc công cụ bên ngoài.")
    print(f"Đã đọc {len(documents)} tài liệu. Câu hỏi: {query}")
    print("\nTop-3 theo từ khóa (điểm không phải xác suất câu trả lời đúng):")
    for row in lexical_search(query, documents, k=3):
        print(f"- {row['doc_id']} | score={row['score']:.3f} | nguồn={row['source']}")
        print(f"  {row['text']}")

    search = {"name": "search_catalog", "args": {"query": query}}

    def fake_policy(history):
        # Lần hai cố ý đề xuất cùng tool để minh họa cache. Final được
        # lập trình sẵn, KHÔNG phải câu trả lời do một mô hình sinh ra.
        if len(history) < 2:
            return {"type": "tool", "call": search}
        if len(history) == 2:
            return {"type": "tool", "call": {
                "name": "draft_plan", "args": {"topic": "Python", "hours_per_week": 10}}}
        return {"type": "final", "answer":
                "[GIẢ LẬP] Đã lấy kết quả tìm kiếm và tạo bản nháp kế hoạch. Hãy đọc tài liệu nguồn; "
                "đây không phải câu trả lời đã được LLM sinh và đánh giá."}

    def local_executor(call):
        if call["name"] == "search_catalog":
            return lexical_search(call["args"]["query"], documents, k=3)
        if call["name"] == "draft_plan":
            hours = call["args"]["hours_per_week"]
            return {"topic": call["args"]["topic"], "hours_per_week": hours,
                    "total_minutes": hours * 60,
                    "sessions": [{"session": i, "minutes": hours * 12}
                                 for i in range(1, 6)]}
        raise ValueError("Công cụ ngoài danh sách")

    result = run_agent(fake_policy, local_executor, max_steps=4)
    print("\nTrace agent giả lập (bước 2 phải dùng cached=true):")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\nDemo chỉ chứng minh luồng phần mềm và tìm từ khóa; chưa đánh giá năng lực LLM.")
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
