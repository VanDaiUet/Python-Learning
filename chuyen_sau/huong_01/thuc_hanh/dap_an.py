"""Đáp án tham khảo dùng thư viện chuẩn cho chín bài RAG/agent.

Đọc sau khi đã thử bài tập. Đây là baseline từ khóa và bộ điều phối đồng
bộ, không phải mô hình embedding, LLM hay hệ thống agent production.
"""

import copy
import json
import re


def _positive_int(value, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} phải là số nguyên dương, không phải bool")


def _canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)


def normalize_text(text: str) -> str:
    """Chữ thường + gộp khoảng trắng, giữ dấu; text khác str -> TypeError."""
    if not isinstance(text, str):
        raise TypeError("text phải là chuỗi")
    return " ".join(text.lower().split())


def chunk_words(text: str, max_words: int, overlap: int) -> list[str]:
    """Chia theo khoảng trắng; bỏ chunk chỉ còn overlap ở cuối.

    max_words int > 0; overlap int từ 0 đến max_words-1; bool bị loại.
    Tham số số sai -> ValueError. Văn bản rỗng -> []; giữ chữ hoa/dấu câu.
    """
    _positive_int(max_words, "max_words")
    if (isinstance(overlap, bool) or not isinstance(overlap, int)
            or not 0 <= overlap < max_words):
        raise ValueError("overlap phải là int với 0 <= overlap < max_words")
    if not isinstance(text, str):
        raise TypeError("text phải là chuỗi")
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"\w+", normalize_text(text)))


def lexical_search(query: str, documents: list[dict], k: int = 3) -> list[dict]:
    r"""Tìm token Unicode \w+; điểm là tỉ lệ token query khác nhau khớp.

    Document hợp lệ có doc_id/title/text/source/updated_at. Không sửa
    dữ liệu; trả doc_id/score/text/source, điểm > 0, score giảm/ID tăng.
    k phải int dương loại bool, sai -> ValueError; query rỗng -> [].
    """
    _positive_int(k, "k")
    query_tokens = _tokens(query)
    if not query_tokens:
        return []
    results = []
    for doc in documents:
        document_tokens = _tokens(doc["title"]) | _tokens(doc["text"])
        score = len(query_tokens & document_tokens) / len(query_tokens)
        if score > 0:
            results.append({"doc_id": doc["doc_id"], "score": score,
                            "text": doc["text"], "source": doc["source"]})
    return sorted(results, key=lambda row: (-row["score"], row["doc_id"]))[:k]


def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str],
                k: int) -> float | None:
    """Dedup retrieved rồi mới cắt k; relevant cũng tính theo tập ID.

    relevant rỗng -> None. k sai/không dương/bool -> ValueError.
    """
    _positive_int(k, "k")
    relevant = set(relevant_ids)
    if not relevant:
        return None
    retrieved = set(list(dict.fromkeys(retrieved_ids))[:k])
    return len(retrieved & relevant) / len(relevant)


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 3,
                           rank_constant: int = 60) -> list[dict]:
    """RRF sum 1/(constant+rank); mỗi list dedup trước rank 1-based.

    Cho phép list rỗng; score giảm/ID tăng. k và constant int dương,
    bool bị loại; sai -> ValueError. Không sửa các ranking đầu vào.
    """
    _positive_int(k, "k")
    _positive_int(rank_constant, "rank_constant")
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(dict.fromkeys(ranking), start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1 / (rank_constant + rank)
    rows = [{"doc_id": doc_id, "score": score} for doc_id, score in scores.items()]
    return sorted(rows, key=lambda row: (-row["score"], row["doc_id"]))[:k]


def validate_answer(answer, allowed_ids) -> bool:
    """Kiểm schema đúng ba khóa; không kiểm nội dung có căn cứ hay không.

    answer str không trắng; citations list[str]; abstain bool thật.
    Abstain -> citations rỗng; trả lời -> citations không rỗng, duy nhất,
    tất cả thuộc allowed_ids. Input schema sai -> False.
    """
    if not isinstance(answer, dict) or set(answer) != {"answer", "citations", "abstain"}:
        return False
    if not isinstance(answer["answer"], str) or not answer["answer"].strip():
        return False
    citations = answer["citations"]
    if (not isinstance(citations, list)
            or not all(isinstance(item, str) for item in citations)
            or type(answer["abstain"]) is not bool):
        return False
    if answer["abstain"]:
        return citations == []
    return (bool(citations) and len(set(citations)) == len(citations)
            and all(item in allowed_ids for item in citations))


def validate_tool_call(call) -> bool:
    """Chỉ search_catalog(query) hoặc draft_plan(topic,hours_per_week).

    Exact keys, chuỗi không trắng; hours int 1..60, không bool.
    Schema sai/tool lạ -> False; không cấp quyền thực hiện side effect.
    """
    if not isinstance(call, dict) or set(call) != {"name", "args"}:
        return False
    name, args = call["name"], call["args"]
    if not isinstance(name, str) or not isinstance(args, dict):
        return False
    if name == "search_catalog":
        return (set(args) == {"query"} and isinstance(args["query"], str)
                and bool(args["query"].strip()))
    if name == "draft_plan":
        return (set(args) == {"topic", "hours_per_week"}
                and isinstance(args["topic"], str) and bool(args["topic"].strip())
                and isinstance(args["hours_per_week"], int)
                and not isinstance(args["hours_per_week"], bool)
                and 1 <= args["hours_per_week"] <= 60)
    return False


def deduplicate_calls(calls: list[dict]) -> list[dict]:
    """Giữ call đầu tiên theo canonical JSON, không quan tâm thứ tự khóa.

    Đầu vào JSON hợp lệ; thứ tự list có nghĩa, không sửa đầu vào.
    """
    seen = set()
    result = []
    for call in calls:
        key = _canonical_json(call)
        if key not in seen:
            seen.add(key)
            result.append(call)
    return result


def run_agent(policy, tool_executor, max_steps: int = 4) -> dict:
    """Agent đồng bộ; hợp đồng action/trace chi tiết ở bai_tap.run_agent.

    Mỗi policy(history) tính một bước, gồm cả cache hit và final.
    Exact action keys; tool phải validate; history/call/cache được sao
    chép để tránh sửa ngầm. Trả đúng status/answer/trace. Error chỉ ghi
    tên kiểu ngoại lệ. max_steps sai -> ValueError. KHÔNG có timeout
    cưỡng bức; callable đồng bộ treo không được giải quyết bởi giới hạn bước.
    """
    _positive_int(max_steps, "max_steps")
    trace = []
    cache = {}

    def result(status, answer=""):
        return {"status": status, "answer": answer, "trace": trace}

    for step in range(1, max_steps + 1):
        try:
            action = policy(copy.deepcopy(trace))
            if isinstance(action, dict):
                if (set(action) == {"type", "answer"} and action["type"] == "final"
                        and isinstance(action["answer"], str) and action["answer"].strip()):
                    trace.append({"step": step, "type": "final"})
                    return result("completed", action["answer"])
                if (set(action) == {"type", "call"} and action["type"] == "tool"
                        and validate_tool_call(action["call"])):
                    call = copy.deepcopy(action["call"])
                    key = _canonical_json(call)
                    cached = key in cache
                    if not cached:
                        cache[key] = copy.deepcopy(tool_executor(copy.deepcopy(call)))
                    trace.append({"step": step, "type": "tool", "call": call,
                                  "cached": cached, "result": copy.deepcopy(cache[key])})
                    continue
            trace.append({"step": step, "type": "invalid_action"})
            return result("invalid_action")
        except Exception as error:
            trace.append({"step": step, "type": "error", "error_type": type(error).__name__})
            return result("error")
    return result("step_limit")
