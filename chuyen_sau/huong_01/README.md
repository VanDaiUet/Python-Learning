# Hướng 1 — Thực hành LLM, RAG và AI Agent

Chương trình này học **sau phần nền tảng 4 tuần**. Bạn xây một trợ lý hỗ trợ học viên của trung tâm **NovaLearn giả lập**, từ xử lý tài liệu đến RAG, agent dùng công cụ và dịch vụ API.

**6 tuần bổ sung × 43 giờ = 258 giờ**, trong đó **180 giờ thực hành**. Nếu học liên tục sau nền tảng, toàn bộ hai chặng là 10 tuần, 430 giờ. Thời lượng là kế hoạch; đạt mốc dựa trên sản phẩm và khả năng giải thích.

## Lịch và sản phẩm

| Tuần chuyên sâu | Tuần tính cả nền tảng | Lab | Trọng tâm | Mốc đầu ra |
|---|---|---|---|---|
| 1 | 5 | L01–L06 | Prompt, hợp đồng, provider, schema, ngân sách và lỗi | R1: lớp gọi mô hình có kiểm thử |
| 2 | 6 | L07–L12 | Nhập tài liệu, chunking, từ khóa, embedding, hybrid, reranking | R2: công cụ truy hồi có so sánh |
| 3 | 7 | L13–L18 | RAG, nguồn, từ chối, đánh giá từng tầng và ablation | R3: RAG được đánh giá bằng mô hình thật |
| 4 | 8 | L19–L24 | Công cụ, trạng thái, giới hạn bước, cache và kiểm soát agent | R4: agent có giới hạn và trace |
| 5 | 9 | L25–L30 | Câu nhiều bước, làm rõ, phục hồi lỗi, so workflow với agent | R5: báo cáo so sánh trên dev |
| 6 | 10 | L31–L36 | API, đồng thời, Docker, CI, giám sát và nghiệm thu | R6: dịch vụ NovaLearn chạy localhost |

Có **36 lab dự án**, mỗi lab gồm 1,5 giờ kiến thức + 5 giờ thực hành + 0,5 giờ ôn. Mỗi tuần làm 6 lab và ôn nhẹ 1 giờ ngày thứ bảy: 9 giờ kiến thức + 30 giờ thực hành + 4 giờ ôn. Nghỉ giải lao không nằm trong giờ học. Phần mở rộng thay thế thời gian còn dư trong lab, không cộng thêm giờ.

- [Bài tập L01–L18: LLM và RAG](01_llm_rag.md).
- [Bài tập L19–L36: agent và triển khai](02_agent_trien_khai.md).
- [Giải thích kiến thức LLM/RAG](../../kien_thuc/03_llm_rag.md) và [agent, API, triển khai](../../kien_thuc/04_deep_learning_he_thong_agent.md#h06): mỗi lab dẫn tới đúng mục qua dòng **Đọc để hiểu bài**. Đọc phần tiên quyết, phân tích ví dụ, trả lời câu hỏi có gợi ý trong 1,5 giờ kiến thức của lab.
- [Tiến độ 42 ngày](TIEN_DO.csv), có liên hệ với ngày 29–70 nếu nối tiếp lịch nền tảng.
- [Tiêu chí đánh giá R1–R6](DANH_GIA.md).
- [Bộ mã thực hành: 9 bài có đáp án và kiểm thử](thuc_hanh/README.md).
- [Dữ liệu, nhãn và quy tắc đánh giá](thuc_hanh/du_lieu/README.md).

## Điều kiện bắt đầu

Bạn cần tự viết được hàm Python, đọc JSON, xử lý ngoại lệ, thêm test và chạy chương trình trong môi trường riêng. Cần hiểu HTTP request/response, train/validation/test và làm được API nhỏ theo nền tảng. Nếu những phần này còn yếu, sửa trước khi bắt đầu các lab phụ thuộc.

Không yêu cầu đã fine-tune mô hình hoặc học huấn luyện phân tán. Bắt đầu với Python và hàm rõ ràng; chỉ chọn một framework agent sau khi tự mô tả được state, tool, observation và điều kiện dừng.

## Dự án NovaLearn

Trợ lý có hai nhóm công việc: trả lời quy định có bằng chứng và tạo **bản nháp** kế hoạch học. Hai công cụ được phép trong bài mẫu:

- `search_catalog(query)`: tìm trong tài liệu giả lập, trả đoạn và ID nguồn.
- `draft_plan(topic, hours_per_week)`: tính bản nháp 5 buổi có tổng phút bằng số giờ × 60; không lưu, không gửi và không đăng ký khóa học.

Tất cả học phí, thời khóa biểu và chính sách trong corpus là **nội dung hư cấu để thử chương trình**, không phải học phí hoặc lịch của bộ tự học này. Các chuỗi `novalearn://nl01` là mã nguồn giả lập, không phải địa chỉ web.

Dữ liệu có 24 tài liệu, 48 câu đánh giá RAG và 24 tình huống chọn công cụ. Mỗi nhóm có tập dev/test riêng. Dùng dev trong tuần 1–5; chỉ mở test khi chốt R6. Nhãn có sẵn để tự chấm nên đây là bài đánh giá có kỷ luật, không phải benchmark ẩn độc lập.

## Chạy phần khởi động hôm nay

Từ thư mục gốc:

```powershell
Set-Location -LiteralPath 'F:\Python Learning'
.\.venv\Scripts\python.exe chuyen_sau\huong_01\thuc_hanh\demo.py
.\.venv\Scripts\python.exe chuyen_sau\huong_01\thuc_hanh\kiem_tra.py --bai 1
```

Demo dùng đáp án tham khảo, tìm kiếm từ khóa và policy giả lập. Nó giúp nhìn luồng dữ liệu; **chưa gọi LLM, chưa tạo embedding và chưa chứng minh chất lượng agent dùng mô hình thật**. Lệnh chấm bài sẽ báo chưa hoàn thành cho đến khi bạn điền hàm trong `bai_tap.py`.

Bộ khởi động chỉ dùng thư viện chuẩn. Khi học dense retrieval, reranking và generation, chọn mô hình/phần mềm phù hợp máy theo tài liệu chính thức, tạo môi trường riêng và lưu phiên bản sau khi chạy được. Không có bước tự động tải mô hình, cài GPU hoặc gọi API trả phí trong bộ khởi động.

Lưu bài mới tại `bai_lam/huong_01/novalearn/` tính từ gốc kho học. Mỗi lab ghi mã, cấu hình, dữ liệu/phiên bản, kết quả thật và lỗi đã gặp; các lab phát triển tiếp cùng dự án.

## Mức hoàn thành phải ghi rõ

- Kiểm thử fake chứng minh các tình huống phần mềm đã được mô phỏng.
- R2 đầy đủ cần thí nghiệm truy hồi/reranking bằng mô hình thật theo lab; phép trùng từ trong demo là baseline riêng.
- R3 cần generation thật; R4–R6 cần bằng chứng mô hình quyết định công cụ và được kiểm soát bằng mã.
- R6 cần API, Docker và kiểm tra tự động chạy thật; chỉ viết Dockerfile chưa đủ nghiệm thu container.
- Nếu thiếu tài nguyên hoặc chưa chạy một phần, ghi `chua_hoan_thanh` cho phần đó rồi tiếp tục việc độc lập. Không dùng output dựng sẵn để điền điểm chất lượng.

## Nguồn học

Nội dung bài tập và NovaLearn do bộ học này thiết kế. Đối chiếu kỹ thuật với [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction), [Sentence Transformers: Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html), [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/), [FastAPI về đồng thời](https://fastapi.tiangolo.com/async/) và [Docker Get Started](https://docs.docker.com/get-started/). Các nguồn này phục vụ tra cứu; không yêu cầu đăng ký khóa ngoài hoặc công bố bài làm.
