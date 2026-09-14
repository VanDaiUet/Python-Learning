"""Chín bài tập Python chuẩn; tự cài đặt các hàm rồi chạy kiem_tra.py.

Không cần cài thư viện ngoài. Không nhập đáp án vào file này để làm test xanh.
Gợi ý: re, json, set, sorted và vòng lặp thường đã đủ cho các bài.
"""


def normalize_text(text: str) -> str:
    """Bài 1: chuyển chữ thường, gộp mọi khoảng trắng, bỏ trắng hai đầu.

    Giữ dấu tiếng Việt và dấu câu. Ví dụ '  HỌC\tPython ' -> 'học python'.
    Đầu vào không phải str: raise TypeError. Không thay dấu bằng ASCII.
    """
    raise NotImplementedError("Bài 1: hãy cài đặt normalize_text")


def chunk_words(text: str, max_words: int, overlap: int) -> list[str]:
    """Bài 2: chia theo text.split(), giữ nguyên chữ hoa/thường và dấu câu.

    max_words phải là int > 0; overlap là int với 0 <= overlap < max_words.
    Loại bool ở cả hai tham số; tham số số sai phải raise ValueError.
    Văn bản rỗng -> []; không sinh chunk cuối chỉ lặp lại phần overlap.
    Ví dụ ('a b c d e', 3, 1) -> ['a b c', 'c d e']; không sửa đầu vào.
    """
    raise NotImplementedError("Bài 2: hãy cài đặt chunk_words")


def lexical_search(query: str, documents: list[dict], k: int = 3) -> list[dict]:
    r"""Bài 3: tìm từ khóa bằng token Unicode re.findall(r'\w+', text.lower()).

    Document có doc_id, title, text, source, updated_at. Điểm = số token
    query KHÁC NHAU có trong title hoặc text / tổng token query khác nhau.
    Bỏ điểm 0, xếp score giảm/doc_id tăng, lấy k. Trả mỗi dòng đúng bốn
    trường doc_id, score, text, source. Không sửa tài liệu. Query không có
    token -> []; k phải là int dương, loại bool, sai -> ValueError.
    """
    raise NotImplementedError("Bài 3: hãy cài đặt lexical_search")


def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int):
    """Bài 4: loại ID truy xuất trùng, giữ thứ tự, rồi mới lấy k đầu.

    Recall = số ID liên quan tìm được / số ID liên quan KHÁC NHAU.
    relevant_ids rỗng -> None (không áp dụng), không coi là 0 hay 1.
    k phải là int dương, loại bool; sai -> ValueError kể cả dữ liệu rỗng.
    """
    raise NotImplementedError("Bài 4: hãy cài đặt recall_at_k")


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 3,
                           rank_constant: int = 60) -> list[dict]:
    """Bài 5: mỗi ranking loại trùng trước khi đánh số rank từ 1.

    Điểm một ID = tổng 1/(rank_constant + rank) ở các ranking chứa nó.
    Trả {doc_id, score}, score giảm/doc_id tăng, tối đa k dòng.
    Cho phép ranking rỗng; k và rank_constant là int dương, loại bool;
    giá trị không hợp lệ -> ValueError. Không sửa danh sách đầu vào.
    """
    raise NotImplementedError("Bài 5: hãy cài đặt reciprocal_rank_fusion")


def validate_answer(answer, allowed_ids) -> bool:
    """Bài 6: chỉ nhận dict có CHÍNH XÁC answer, citations và abstain.

    answer là str không rỗng sau strip; citations là list[str]; abstain
    có type bool. Nếu abstain=True: citations phải rỗng. Nếu False:
    citations không rỗng, không trùng, tất cả nằm trong allowed_ids.
    Trả False cho schema sai, không ném lỗi. Chỉ kiểm schema/ID, chưa
    kiểm tra bằng chứng có hỗ trợ nội dung trả lời hay không.
    """
    raise NotImplementedError("Bài 6: hãy cài đặt validate_answer")


def validate_tool_call(call) -> bool:
    """Bài 7: call là dict đúng {name, args}, không nhận trường thừa.

    search_catalog: args đúng {query: str không rỗng sau strip}.
    draft_plan: args đúng {topic: str không rỗng, hours_per_week: int 1..60}.
    Loại bool khỏi hours_per_week. Tool lạ/schema sai -> False.
    Kiểm schema không cấp quyền cho một công cụ có tác động bên ngoài.
    """
    raise NotImplementedError("Bài 7: hãy cài đặt validate_tool_call")


def deduplicate_calls(calls: list[dict]) -> list[dict]:
    """Bài 8: giữ lần đầu mỗi call bằng khóa JSON có sort_keys=True.

    calls gồm object JSON hợp lệ. Thứ tự khóa không ảnh hưởng so sánh,
    kể cả khóa lồng nhau; thứ tự phần tử list vẫn có ý nghĩa. Giữ thứ tự
    các call xuất hiện lần đầu; không sửa đầu vào, không gộp khác đối số.
    """
    raise NotImplementedError("Bài 8: hãy cài đặt deduplicate_calls")


def run_agent(policy, tool_executor, max_steps: int = 4) -> dict:
    """Bài 9: agent ĐỒNG BỘ, mỗi lần gọi policy(history) tính một bước.

    max_steps là int dương, loại bool; sai -> ValueError. history là bản
    sao trace trước bước hiện tại. Action chỉ được có đúng một trong:
    {'type': 'tool', 'call': tool_call} hoặc {'type': 'final', 'answer':
    str không rỗng}. Tool call phải qua validate_tool_call trước executor.
    Gọi tool_executor(call); call trùng trong cùng run dùng cache và đánh
    dấu cached=True, vẫn tính bước. Cache dùng khóa như bài 8.
    Luôn trả đúng {status, answer, trace}; answer='' khi chưa hoàn thành.
    Status: completed / invalid_action / step_limit / error. Final cũng
    được ghi trace. Lỗi policy/executor -> error, chỉ ghi tên loại ngoại
    lệ vào error_type, KHÔNG ghi thông điệp hoặc traceback có thể lộ khóa.
    Trace tool: {step,type,call,cached,result}; final: {step,type};
    invalid: {step,type='invalid_action'}; error: {step,type='error',error_type}.
    Giới hạn bước KHÔNG phải timeout: callable đồng bộ bị treo vẫn bị treo.
    Bài này không chạy shell, mạng hay hành động ngoài workspace.
    """
    raise NotImplementedError("Bài 9: hãy cài đặt run_agent")
