# Kết quả rà soát phần hướng dẫn học

Ngày rà soát: 12/09/2026. Phạm vi: giáo trình B01–B80, chuyên sâu L01–L36 và tài liệu bắt đầu/thực hành đi kèm.

## Nhận xét và phần đã bổ sung

Tài liệu trước đây đã có mục tiêu, đề thực hành và tiêu chí đạt, nhưng nhiều bài chỉ giải thích khái niệm trong một đoạn ngắn. Người mới dễ biết phải làm gì mà chưa hiểu vì sao làm như vậy, đặc biệt ở các chủ đề có nhiều kiến thức phụ thuộc.

Đã thêm bốn tài liệu kiến thức, có mục tiên quyết, cơ chế, ví dụ tính tay hoặc mã kèm kết quả, liên hệ bài học, lỗi thường gặp và câu hỏi có đáp án gợi ý. Từng bài B/L đã được nối tới mục cần đọc; README, hướng dẫn bắt đầu, lịch 4 tuần và hai bộ thực hành cũng có đường vào.

| Nhóm | Phần làm rõ |
|---|---|
| Python | Interpreter/terminal, kiểu và chuyển kiểu, điều kiện, vòng lặp, tham chiếu và sao chép, return/print, hợp đồng, CSV/JSON, ngoại lệ, test, môi trường, Git, OOP/generator/CLI |
| Dữ liệu và toán/ML | Shape/axis/broadcasting, dữ liệu thiếu và join, EDA, vector/ma trận, đạo hàm/gradient, thống kê, SQL/transaction, chia tập/leakage, metric, Pipeline, PCA và lưu mô hình |
| LLM/RAG | Token khác từ, context, provider/HTTP/schema, provenance, chunking/overlap, TF-IDF/BM25, embedding/cosine, RRF/reranker, bằng chứng/từ chối, Recall/MRR/nDCG, ablation và LoRA |
| Deep Learning/hệ thống/agent | Forward/backward/optimizer, batch/epoch, MLP/CNN/attention, API/async, hợp đồng tool, state/trace, timeout/retry/idempotency, phân quyền, test/eval, Docker/CI, latency/drift |

Các hợp đồng liên quan được đối chiếu với bài tập: trung bình rỗng của bộ 6 báo lỗi còn bộ 8 trả None; từ chối trong starter RAG có citations rỗng; starter agent dùng action `tool`/`final` và giới hạn bước không ngắt được một lời gọi đồng bộ đang treo.

## Bằng chứng kiểm tra

| Tài liệu | Mục kiến thức | Ví dụ Python đã chạy bằng thư viện chuẩn | Ví dụ chỉ kiểm cú pháp, cần thư viện ngoài |
|---|---:|---:|---:|
| [Python](01_python.md) | 10 | 21 | 0 |
| [Dữ liệu, toán và ML](02_du_lieu_toan_ml.md) | 10 | 7 | 3 |
| [LLM và RAG](03_llm_rag.md) | 12 | 14 | 0 |
| [Deep Learning, hệ thống và agent](04_deep_learning_he_thong_agent.md) | 12 | 13 | 1 |
| **Tổng** | **44** | **55** | **4** |

- Chạy độc lập 55 khối `# RUN: stdlib` bằng Python của `.venv`, với chế độ UTF-8; tất cả kết thúc thành công. Đối chiếu đầu ra với phần giải thích và các assertion có trong ví dụ.
- Phân tích cú pháp cả 59 khối Python. Bốn khối `# NEEDS` cần NumPy, pandas, scikit-learn hoặc PyTorch; các gói này chưa có trong môi trường kiểm tra nên chưa xác nhận kết quả chạy thực của chúng.
- Kiểm đủ 80 bài B và 36 lab L, mỗi bài có đúng một dòng đọc kiến thức đặt ngay sau tiêu đề; kiểm đường dẫn tệp và anchor nội bộ trong tài liệu Markdown.
- Rà công thức/số minh họa và đối chiếu dữ liệu D1, cách chia D3, hợp đồng starter và corpus NovaLearn; không dùng nhãn test cuối kỳ để xây ví dụ tối ưu mô hình.

## Phạm vi của kết quả

Kiểm chứng trên xác nhận các ví dụ thư viện chuẩn và cấu trúc dẫn đường của tài liệu. Nó chưa là phép đánh giá hiệu quả học tập với học viên thực, cũng không chứng minh model, embedding, API, GPU hay Docker đã được huấn luyện/chạy/nghiệm thu.

Thời lượng giữ nguyên: nền tảng 4 tuần, chuyên sâu 6 tuần tiếp theo; mỗi tuần 43 giờ với 30 giờ thực hành. Phần giải thích dùng quỹ kiến thức có sẵn, đọc theo bài thay vì đọc hết cùng lúc. Các phần nâng cao giữ phạm vi mở rộng hoặc học tiếp đã quy định trong lịch.

Điểm bắt đầu: [mục lục kiến thức](README.md), rồi theo dòng **Đọc để hiểu bài** của bài đang học.
