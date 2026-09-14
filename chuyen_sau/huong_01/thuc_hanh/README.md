# Bộ thực hành Python cho LLM/RAG/agent

Có **9 bài hàm** bổ trợ cho 36 lab dự án. Làm trong thời gian thực hành của lab tương ứng; không cộng thêm một khóa riêng.

Đọc kiến thức trước khi điền hàm: bài 1 → [R05: chuẩn hóa và nguồn gốc](../../../kien_thuc/03_llm_rag.md#r05), bài 2 → [R06: chunking](../../../kien_thuc/03_llm_rag.md#r06), bài 3 → [R07: lexical](../../../kien_thuc/03_llm_rag.md#r07), bài 4 → [R12: Recall@k](../../../kien_thuc/03_llm_rag.md#r12), bài 5 → [R09: RRF](../../../kien_thuc/03_llm_rag.md#r09), bài 6 → [R03: schema](../../../kien_thuc/03_llm_rag.md#r03), bài 7 → [H06: tool](../../../kien_thuc/04_deep_learning_he_thong_agent.md#h06), bài 8 → [H08: cache/idempotency](../../../kien_thuc/04_deep_learning_he_thong_agent.md#h08), bài 9 → [H07: vòng agent](../../../kien_thuc/04_deep_learning_he_thong_agent.md#h07). Các ví dụ giải thích cơ chế; docstring của bài tập vẫn là hợp đồng cần thực hiện.

| Bài | Hàm cần viết | Kỹ năng và trường hợp cần tự thử |
|---|---|---|
| 1 | `normalize_text` | Chữ thường và khoảng trắng; giữ tiếng Việt có dấu, chuỗi rỗng |
| 2 | `chunk_words` | Chia văn bản theo số từ, overlap, không tạo đoạn cuối chỉ lặp overlap |
| 3 | `lexical_search` | Tìm theo từ khóa; top-k, điểm bằng nhau, truy vấn rỗng, không sửa corpus |
| 4 | `recall_at_k` | Tính đủ nguồn liên quan; bỏ trùng, nhiều nguồn, trường hợp không có nhãn nguồn |
| 5 | `reciprocal_rank_fusion` | Gộp hai hay nhiều danh sách xếp hạng; bỏ trùng và phá hòa ổn định |
| 6 | `validate_answer` | Kiểm tra schema, ID nguồn hợp lệ và từ chối; phân biệt schema với độ đúng |
| 7 | `validate_tool_call` | Tên/args theo allowlist, chuỗi rỗng, số giờ sai và bool giả làm số |
| 8 | `deduplicate_calls` | Nhận ra cùng lời gọi dù thứ tự khóa JSON khác nhau |
| 9 | `run_agent` | State/trace, giới hạn bước, cache trong một lượt chạy và xử lý lỗi |

Đọc toàn bộ docstring của mỗi hàm trong [bai_tap.py](bai_tap.py). Bộ chấm dùng đúng hợp đồng đó. Các kiểm thử chọn trường hợp có ý nghĩa nhưng không chứng minh mọi đầu vào đều an toàn hoặc mọi đáp án đều đúng.

## Lệnh chạy

Từ `F:\Python Learning`:

```powershell
.\.venv\Scripts\python.exe chuyen_sau\huong_01\thuc_hanh\demo.py
.\.venv\Scripts\python.exe chuyen_sau\huong_01\thuc_hanh\kiem_tra.py --bai 1
.\.venv\Scripts\python.exe chuyen_sau\huong_01\thuc_hanh\kiem_tra.py
```

Sửa thân hàm còn `NotImplementedError` trong `bai_tap.py`. Lệnh không có `--bai` chấm cả 9 bài. Bài chưa điền báo chưa hoàn thành hoặc lỗi; không sửa test để biến kết quả sai thành đúng.

Sau khi đã tự thử, có thể xem [dap_an.py](dap_an.py) và chạy bản tham khảo:

```powershell
.\.venv\Scripts\python.exe chuyen_sau\huong_01\thuc_hanh\kiem_tra.py --dap-an
```

**Cờ `--dap-an` kiểm tra bản tham khảo, không chấm năng lực hay bài làm của bạn.** Demo cũng gọi bản tham khảo để luôn minh họa được luồng ban đầu.

## Ranh giới của bộ mẫu

`lexical_search` dùng tỷ lệ các từ truy vấn khác nhau xuất hiện trong tiêu đề/nội dung. Đây là baseline trùng từ; nó không phải BM25, TF-IDF hay mô hình embedding. Chỉ các kết quả có điểm dương được trả về.

`recall_at_k` nhận một câu: loại trùng ID trước khi lấy k nguồn đầu, chia số nguồn đúng tìm được cho số nguồn liên quan chuẩn. Không có nguồn chuẩn thì trả `None`; đừng biến thành số 0 rồi cộng vào trung bình các câu có đáp án.

`validate_answer` chỉ kiểm tra các khóa `answer`, `citations`, `abstain`, kiểu dữ liệu và việc ID thuộc danh sách cho phép. Một câu trả lời sai dữ kiện vẫn có thể qua hàm này; kiểm tra căn cứ phải đọc nguồn và chấm riêng.

`run_agent` là bộ điều phối **đồng bộ** với giới hạn số lần gọi policy. Giới hạn bước không ngắt được một provider hoặc công cụ đang treo; khi ghép thật, phải đặt timeout ở tầng HTTP/tool và có cơ chế hủy phù hợp. Cache chỉ có hiệu lực trong một lượt chạy, không phải cơ chế bảo đảm “chỉ thực hiện một lần” cho thao tác bên ngoài.

Policy của demo là hàm đã lập trình sẵn. Nó không dùng LLM để chọn hành động. `draft_plan` chỉ trả dữ liệu tính toán; các bài này không gửi email, ghi đăng ký hoặc gọi dịch vụ thật.

## Bài đầu tiên gợi ý

1. Chạy demo và chỉ ra đâu là query, tài liệu, điểm và trace.
2. Hoàn thành `normalize_text`; tự thử `"  HỌC   Python  "` và chuỗi chỉ có khoảng trắng.
3. Chạy chấm bài 1, sau đó viết thêm một test cho tab/xuống dòng.
4. Đóng đáp án, giải thích vì sao giữ dấu tiếng Việt và khi nào phải đổi chiến lược chuẩn hóa.

Dữ liệu ở [du_lieu/README.md](du_lieu/README.md). Bộ kiểm thử dùng fixture kỹ thuật nhỏ; không dùng các nhãn test cuối kỳ để tối ưu câu trả lời.
