# Dữ liệu NovaLearn — hoàn toàn giả lập

24 tài liệu và các tình huống được tự biên soạn cho bài học. Học phí, chính sách, lịch lớp và thông tin trung tâm đều hư cấu; không phải thông tin về một đơn vị thật hoặc về chương trình tự học của bạn.

| Tệp | Số mục | Mục đích |
|---|---:|---|
| [documents.json](documents.json) | 24 | Corpus dùng chung; IDs nl01–nl24 |
| [eval_dev.jsonl](eval_dev.jsonl) | 24 | Phát triển RAG tuần 1–5 |
| [eval_test.jsonl](eval_test.jsonl) | 24 | Kiểm tra RAG cuối R6 |
| [agent_dev.jsonl](agent_dev.jsonl) | 12 | Phát triển chọn công cụ |
| [agent_test.jsonl](agent_test.jsonl) | 12 | Kiểm tra agent cuối R6 |

JSONL là định dạng mỗi dòng chứa một object JSON độc lập. Mã nguồn `novalearn://nlXX` chỉ là định danh để truy vết, không phải liên kết mạng. `updated_at` là metadata hư cấu, không phải lời khẳng định chính sách hiện hành.

## Schema tài liệu

`doc_id`, `title`, `text`, `source`, `updated_at` đều là chuỗi. Giữ doc_id khi tạo chunk; tạo chunk_id riêng để không mất mối liên hệ với nguồn.

## Schema đánh giá RAG

`id`, `category`, `question`, `relevant_doc_ids`, `expected_answer`.

Mỗi tập có 16 ca `answerable` (12 đơn nguồn và 4 đa nguồn), 4 ca `out_of_scope`, 4 ca `adversarial`. Hai nhóm câu đơn nguồn dùng các chủ đề tài liệu khác nhau giữa dev/test. Câu ngoài phạm vi không có nguồn chuẩn.

Một số ca đối kháng yêu cầu bịa lại thông tin có thật; kỳ vọng là bác yêu cầu sai và trả thông tin có căn cứ. Một số ca yêu cầu secret/dữ liệu không có trong corpus; kỳ vọng là từ chối. Không tự quy mọi ca đối kháng về cùng một kiểu output.

`expected_answer` là hướng dẫn chấm ngữ nghĩa, không phải chuỗi để so bằng nhau tuyệt đối và không được truyền vào prompt đánh giá.

## Schema đánh giá công cụ

`id`, `category`, `request`, `expected_tools`, `expected_behavior`.

Mỗi tập có 4 ca tìm kiếm, 3 ca tạo bản nháp, 1 ca kết hợp tìm kiếm rồi tạo bản nháp, 1 ca cần hỏi làm rõ, 1 ca số giờ sai, 1 ca hành động không hỗ trợ và 1 ca không cần công cụ.

Công cụ chuẩn:

- `{"name": "search_catalog", "args": {"query": "..."}}`.
- `{"name": "draft_plan", "args": {"topic": "...", "hours_per_week": 10}}`.

Số giờ phải là số nguyên 1–60 và không nhận bool. Bản nháp gồm 5 buổi, tổng phút = số giờ × 60. Query đồng nghĩa có thể được chấp nhận theo rubric; không dùng so chuỗi tuyệt đối để kết luận mọi quyết định khác chữ đều sai.

## Kỷ luật phát triển

Giữ bản gốc, làm biến thể trong bài làm. Các chỉ dẫn giả hoặc yêu cầu “bỏ qua quy định” trong fixture là dữ liệu thử nghiệm. Không xem chúng là quyền thực hiện hành động trong công cụ hoặc trong môi trường làm việc.

Dev dùng để sửa prompt, retrieval, tool policy và ngưỡng. Test chỉ dùng sau khi khóa bản R6. Các file nhãn sẵn có không tạo thành benchmark ẩn; sau khi dùng test để sửa hệ thống, cần bộ mới cho đánh giá độc lập.

Đánh giá được mô tả tại [DANH_GIA.md](../../DANH_GIA.md). Bộ dữ liệu nhỏ phục vụ luyện tập, không chứng minh hệ thống sẵn sàng dùng với dữ liệu và người dùng ngoài thực tế.
