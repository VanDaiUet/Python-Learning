# Đánh giá hướng LLM/RAG/AI Agent

Áp dụng cho R1–R6 trong [chương trình 6 tuần](README.md). Chấm riêng tính đúng phần mềm, chất lượng mô hình và việc vận hành.

## Tiêu chí chung

| Hạng mục | Điểm |
|---|---:|
| Đúng phạm vi, schema và chức năng | 20 |
| Hiểu và tự sửa được mã | 20 |
| Đánh giá có dữ liệu, baseline và phân tích lỗi | 25 |
| Kiểm thử, giới hạn và khả năng chạy lại | 25 |
| README, cấu hình và demo | 10 |

Đạt từ **75/100**, đồng thời đủ các điều kiện bắt buộc của mốc. Output fake, số đo chưa chạy hoặc nguồn không hỗ trợ không được tính là bằng chứng chất lượng mô hình.

| Mốc | Điều kiện bắt buộc | Cách ghi kết quả |
|---|---|---|
| R1 | Hợp đồng output/provider, kiểm tra schema, xử lý lỗi và ngân sách theo L01–L06 | Tách test fake và lượt gọi thật; ghi lỗi và phần chưa có model |
| R2 | Baseline từ khóa, dense/hybrid/reranking thực theo L07–L12; metric truy hồi trên dev | Mục tiêu giảng dạy macro Recall@5 ≥ 0,80; đủ nguồn ≥ 3/4 câu đa nguồn |
| R3 | Generation thật trên 24 ca dev, trích dẫn truy vết, cấu hình tái lập | Mục tiêu đúng có căn cứ ≥ 12/16 câu có đáp án; đa nguồn ≥ 3/4; ngoài phạm vi ≥ 3/4; đối kháng 4/4 |
| R4 | Mô hình chọn tool thật; allowlist/schema/bounds/cache/phiên độc lập có test | Tool correctness và task success đều hướng tới ≥ 10/12 ca agent dev; không có hành động cấm được thực thi |
| R5 | So workflow và agent trên cùng 24 RAG dev + 12 agent dev, giữ model/ngân sách tương đương | 72 kết quả hoặc lỗi được giữ; chọn phương án bằng bằng chứng, không mặc định agent tốt hơn |
| R6 | Bản cuối chạy API/Docker/kiểm tra tự động, rollback và 36 ca test thật qua service | Chốt trước khi mở test: các mục tiêu chất lượng R3/R4 áp dụng tương ứng cho test; công bố đạt/chưa đạt từng mục |

Các ngưỡng là **mục tiêu của bài tập nhỏ**, không phải chuẩn ngành hoặc số đo đã đạt. Nếu chưa đạt sau lượt test cuối, giữ nguyên báo cáo; sửa trên dev và dùng tập đánh giá mới cho vòng độc lập tiếp theo. Không thử lại nhiều cấu hình trên cùng test rồi chọn điểm đẹp.

## Chia dữ liệu

- `eval_dev.jsonl`: 24 ca = 16 có đáp án (12 đơn nguồn, 4 đa nguồn) + 4 ngoài phạm vi + 4 đối kháng.
- `eval_test.jsonl`: 24 ca có cùng cơ cấu, chỉ dùng ở R6.
- `agent_dev.jsonl` và `agent_test.jsonl`: mỗi tập 12 ca chọn công cụ, bao gồm tìm kiếm, lập kế hoạch, kết hợp, hỏi làm rõ, đầu vào sai, hành động không hỗ trợ và không cần công cụ.
- Corpus 24 tài liệu dùng chung cho lập chỉ mục; việc lập chỉ mục tài liệu nguồn không phải đưa nhãn test vào mô hình.
- Không chuyển `expected_answer`, `relevant_doc_ids`, `expected_tools` hoặc `expected_behavior` từ bộ chấm sang request của hệ thống.
- Tập test nằm sẵn trong bộ học để tự chấm, không được bảo mật khỏi người học; vai trò giữ kín phụ thuộc kỷ luật phát triển.

Lưu cấu hình, model/provider/version, prompt, chunking, retrieval, tool policy, seed nếu áp dụng và dấu nhận diện dữ liệu trước lượt test. Ghi cả lỗi, timeout và lần retry; không xóa ca thất bại khỏi báo cáo.

## Chấm truy hồi

Với mỗi câu có đáp án, loại ID trùng trước khi lấy k tài liệu đầu:

`Recall@k = số ID liên quan tìm được trong top-k / số ID liên quan chuẩn`.

Lấy trung bình trên **16 câu answerable**; không cộng nhóm ngoài phạm vi vào trung bình này. Báo riêng **x/4 câu đa nguồn tìm đủ mọi nguồn cần thiết**, vì Recall trung bình có thể che việc thiếu một nửa bằng chứng ở câu nhiều nguồn.

Ví dụ nguồn chuẩn là `[nl01, nl02]`, top-k chỉ có `[nl01]`: Recall bằng 0,5, nhưng câu đó chưa tìm đủ nguồn. ID trùng không làm điểm tăng. k tính theo tài liệu, không phải số chunk; ghi rõ quy tắc quy đổi chunk về doc_id.

## Chấm generation

Chấm bằng tay từng output, có thể nhờ bộ chấm tự động hỗ trợ nhưng phải đối chiếu một mẫu có nhãn tay.

- **Đúng nội dung:** đủ các dữ kiện và điều kiện cần trả lời; số tiền/thời gian/đơn vị chính xác theo corpus.
- **Có căn cứ:** nguồn trích thực sự hỗ trợ phát biểu; không chỉ kiểm tra mã nguồn tồn tại.
- **Đủ nguồn:** câu đa nguồn có đủ bằng chứng; không lấy một tài liệu để chứng minh dữ kiện của tài liệu khác.
- **Từ chối phù hợp:** câu ngoài phạm vi được báo thiếu thông tin; ca đối kháng có thông tin thật vẫn có thể trả lời đúng dữ kiện và bác yêu cầu bịa.
- **Schema:** ghi đúng kiểu, khóa và quy tắc `abstain`; sai schema là lỗi phần mềm riêng.

Trên 16 câu có đáp án, **đúng có căn cứ** chỉ đạt khi vừa đúng nội dung vừa có nguồn hỗ trợ. Báo riêng các nhóm 16/4/4, không chỉ một tỷ lệ gộp. Một câu trả lời từ chối mọi câu sẽ không đạt nhóm có đáp án.

## Chấm agent

`Tool correctness = số ca có chuỗi công cụ được chấp nhận / 12`.

Đối chiếu tên, thứ tự phụ thuộc, schema và ý nghĩa args với `expected_tools`. Chuỗi query có thể khác chữ nhưng cùng mục đích tìm kiếm; ghi lý do chấp nhận bằng tay. Với draft, chủ đề tương đương và số giờ đúng là bắt buộc. Các ca đúng là không gọi tool cũng nằm trong mẫu số.

`Task success = số ca đạt toàn bộ expected_behavior / 12`.

Một trace chọn đúng tool nhưng không dùng kết quả đúng có thể đạt tool correctness và trượt task success. Nhãn `expected_tools` mô tả một trace được chấp nhận; nếu cho phép cách khác, phải ghi quy tắc trước lượt test và giữ nhất quán.

Báo số ca có đề xuất công cụ cấm, số đề xuất bị chặn và số hành động cấm thực sự qua kiểm soát/thực thi. Với tập sẵn có, ghi riêng nhóm 4 ca RAG đối kháng và các ca agent bị chặn; các ca mock bổ sung là một bảng khác. Yêu cầu **0 hành động cấm được cho phép/thực thi trên các ca đã chạy**. Không suy ra an toàn cho mọi đầu vào từ con số này.

## Độ trễ, chi phí và vận hành

Báo số request, cấu hình, concurrency, warm-up, cách tính p50/p95 và tỷ lệ lỗi. Nhãn `fake` và `real` phải tách riêng; fake nhanh không chứng minh backend thật đạt tốc độ đó.

Chỉ tính tiền khi có usage thực và đơn giá đã xác minh tại thời điểm chạy. Nếu không có thông tin, ghi `unknown` hoặc `not_applicable` cùng lý do; không tự đặt chi phí bằng 0. Mô hình cục bộ vẫn dùng tài nguyên máy.

R6 cần lệnh cài/chạy/test, image Docker chạy thật, cấu hình mẫu không bí mật, log phù hợp, phiên bản artifact và diễn tập rollback. CI có thể là pipeline kiểm tra tự động chạy cục bộ; CI trên dịch vụ ngoài là mở rộng.

## Mẫu báo cáo kết quả

Sao chép [mau_bao_cao.md](mau_bao_cao.md) vào bài làm. Không điền sẵn tỷ lệ đạt. Với mỗi mốc, ghi `hoan_thanh`, `can_sua` hoặc `chua_co_tai_nguyen` và dẫn bằng chứng.

Bộ mẫu đi kèm chỉ chạy kỹ thuật bằng thư viện chuẩn. Việc kiểm thử đáp án tham khảo đạt không đồng nghĩa các mốc R2–R6 đã hoàn thành.
