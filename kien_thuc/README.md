# Kiến thức cốt lõi để hiểu và làm được bài học

Đây là phần giải thích đi cùng giáo trình: **44 mục kiến thức trong bốn tài liệu**, được nối tới **80 bài B01–B80 và 36 lab L01–L36**. Các bài B/L giữ đề bài và tiêu chí đạt; các mục P/D/R/H dưới đây giải thích cơ chế và kiến thức liên quan để làm bài.

P01 ở đây là mục kiến thức Python; **khác dự án P01** trong `du_an/DE_BAI.md`. Tương tự, R01 là mục giải thích, còn **R1–R6** là các mốc sản phẩm chuyên sâu.

## Cách học mỗi ngày

1. Mở [lịch N01–N28](../LO_TRINH_4_TUAN.md), hoặc lab hiện tại của [hướng 1](../chuyen_sau/huong_01/README.md).
2. Ở bài B/L, theo dòng **Đọc để hiểu bài**. Nếu mục yêu cầu kiến thức chưa vững, quay về phần tiên quyết được nêu.
3. Đọc định nghĩa và cơ chế; tự diễn giải bằng lời của mình. Tính tay hoặc ghi trạng thái từng bước của ví dụ.
4. Dự đoán đầu ra trước khi chạy; sau đó thay một đầu vào và giải thích điều thay đổi.
5. Che đáp án gợi ý, trả lời câu hỏi cuối mục rồi quay lại đề thực hành.

Khối kiến thức **1,5 giờ/ngày** đã có trong lịch: có thể dành khoảng 45 phút đọc, 30 phút phân tích ví dụ, 15 phút tự kiểm. Việc mở máy chạy và sửa các biến thể tiếp tục trong **5 giờ thực hành/ngày**. Tổng vẫn là **43 giờ/tuần, trong đó 30 giờ thực hành**.

Một mục có thể dùng cho nhiều bài: lần đầu đọc phần cần thiết, lần sau ôn và đọc sâu đoạn mới liên quan. Không cần đọc hết bốn tài liệu trước khi làm bài đầu tiên. Các phần mở rộng như CNN, LoRA hoặc Docker theo đúng phạm vi lịch; không tự thêm tất cả vào bốn tuần.

## Mỗi mục giúp bạn trả lời gì?

- Khái niệm này là gì, đầu vào/đầu ra có ý nghĩa gì?
- Nó hoạt động từng bước thế nào; công thức và ký hiệu đại diện cho gì?
- Ví dụ nhỏ cho kết quả nào, vì sao?
- Kiến thức liên quan nào cần để dùng nó trong Python/AI?
- Lỗi nào dễ xảy ra và kiểm tra nguyên nhân thế nào?
- Bạn có tự trả lời câu hỏi và làm một biến thể được không?

Mức đọc hiểu đạt khi giải thích được cơ chế và kết quả ví dụ mà không chép lại. Mức thực hành đạt theo test, sản phẩm và bằng chứng của bài B/L; đọc xong tài liệu không tự đánh dấu hoàn thành dự án.

## Bắt đầu theo chặng

| Chặng hiện tại | Điểm vào |
|---|---|
| Ngày 1, mới học lập trình | [P01 — Chạy mã và biến](01_python.md#p01), [P02 — Điều kiện](01_python.md#p02), rồi [Bắt đầu](../BAT_DAU.md) |
| Tuần 1, đang làm tám bộ bài Python | [P03–P10 trong tài liệu Python](01_python.md#p03); theo bảng ở [bộ bài tập](../thuc_hanh/README.md) |
| Tuần 2, dữ liệu và ML | [D01 — Shape và broadcasting](02_du_lieu_toan_ml.md#d01), rồi các mục D tương ứng bài |
| Tuần 3, PyTorch và tìm kiếm | [H01–H03](04_deep_learning_he_thong_agent.md#h01), [R01](03_llm_rag.md#r01), [R07–R08](03_llm_rag.md#r07) |
| Tuần 4, API và đánh giá | [H04–H05](04_deep_learning_he_thong_agent.md#h04), [H10–H12](04_deep_learning_he_thong_agent.md#h10), [R12](03_llm_rag.md#r12) |
| Chuyên sâu L01–L18 | [LLM và RAG](03_llm_rag.md), kèm phần H được gắn ở từng lab |
| Chuyên sâu L19–L36 | [H06–H12: agent và hệ thống](04_deep_learning_he_thong_agent.md#h06), quay về R khi cải thiện retrieval/RAG |

## Tra cứu 44 mục

| Mã | Kiến thức |
|---|---|
| P01 | [Chạy mã, biến và kiểu](01_python.md#p01) |
| P02 | [Biểu thức và điều kiện](01_python.md#p02) |
| P03 | [Vòng lặp và điều kiện dừng](01_python.md#p03) |
| P04 | [Chuỗi và cấu trúc dữ liệu](01_python.md#p04) |
| P05 | [Hàm và hợp đồng](01_python.md#p05) |
| P06 | [Tệp, CSV và JSON](01_python.md#p06) |
| P07 | [Ngoại lệ và debug](01_python.md#p07) |
| P08 | [Kiểm thử](01_python.md#p08) |
| P09 | [Module, môi trường và Git](01_python.md#p09) |
| P10 | [OOP, generator và CLI](01_python.md#p10) |
| D01 | [Shape, axis và broadcasting](02_du_lieu_toan_ml.md#d01) |
| D02 | [Bảng dữ liệu và join](02_du_lieu_toan_ml.md#d02) |
| D03 | [EDA và biểu đồ](02_du_lieu_toan_ml.md#d03) |
| D04 | [Vector, ma trận và thang đo](02_du_lieu_toan_ml.md#d04) |
| D05 | [Đạo hàm và gradient descent](02_du_lieu_toan_ml.md#d05) |
| D06 | [Xác suất và thống kê](02_du_lieu_toan_ml.md#d06) |
| D07 | [SQL và transaction](02_du_lieu_toan_ml.md#d07) |
| D08 | [Chia tập, baseline và leakage](02_du_lieu_toan_ml.md#d08) |
| D09 | [Mô hình tuyến tính và metric](02_du_lieu_toan_ml.md#d09) |
| D10 | [Cây, Pipeline, PCA và artifact](02_du_lieu_toan_ml.md#d10) |
| R01 | [LLM và tokenization](03_llm_rag.md#r01) |
| R02 | [Prompt và ranh giới dữ liệu](03_llm_rag.md#r02) |
| R03 | [Provider, HTTP và schema](03_llm_rag.md#r03) |
| R04 | [Ngân sách context/token](03_llm_rag.md#r04) |
| R05 | [Ingestion và nguồn gốc](03_llm_rag.md#r05) |
| R06 | [Chunking và overlap](03_llm_rag.md#r06) |
| R07 | [Lexical, TF-IDF và BM25](03_llm_rag.md#r07) |
| R08 | [Embedding và cosine](03_llm_rag.md#r08) |
| R09 | [Hybrid và RRF](03_llm_rag.md#r09) |
| R10 | [Reranker](03_llm_rag.md#r10) |
| R11 | [RAG và kiểm bằng chứng](03_llm_rag.md#r11) |
| R12 | [Đánh giá, ablation và LoRA](03_llm_rag.md#r12) |
| H01 | [Tensor và autograd](04_deep_learning_he_thong_agent.md#h01) |
| H02 | [Batch, train/eval và checkpoint](04_deep_learning_he_thong_agent.md#h02) |
| H03 | [MLP, CNN và attention](04_deep_learning_he_thong_agent.md#h03) |
| H04 | [API và vòng đời model](04_deep_learning_he_thong_agent.md#h04) |
| H05 | [Async và giới hạn đồng thời](04_deep_learning_he_thong_agent.md#h05) |
| H06 | [Hợp đồng và thực thi tool](04_deep_learning_he_thong_agent.md#h06) |
| H07 | [Workflow, agent và state](04_deep_learning_he_thong_agent.md#h07) |
| H08 | [Timeout, retry và idempotency](04_deep_learning_he_thong_agent.md#h08) |
| H09 | [Phân quyền và prompt injection](04_deep_learning_he_thong_agent.md#h09) |
| H10 | [Test, đánh giá và trace](04_deep_learning_he_thong_agent.md#h10) |
| H11 | [Artifact, Docker và CI](04_deep_learning_he_thong_agent.md#h11) |
| H12 | [Latency, chi phí và drift](04_deep_learning_he_thong_agent.md#h12) |

## Đọc nhãn ví dụ và kết quả

`# RUN: stdlib` là khối Python độc lập chỉ cần thư viện chuẩn. Ví dụ đầu ra và các phép tính được dùng để học cơ chế; ranking giả, fake provider hoặc vector tự tạo không phải kết quả mô hình thật.

`# NEEDS: ...` là ví dụ cần thư viện ghi ở dòng đầu. Trong đợt rà soát này, các khối đó chỉ được kiểm tra cú pháp, chưa được chạy với thư viện tương ứng. Chỉ cài/chạy khi đến bài cần chúng theo [hướng dẫn môi trường](../BAT_DAU.md).

Nguồn chính thức được đặt cạnh phần kỹ thuật cần tra cứu. Tài liệu của thư viện có thể cập nhật; khi thực hành ghi phiên bản đã cài và xem tài liệu tương ứng. Nội dung giải thích và số liệu minh họa không thay cho bằng chứng chạy dự án.

Xem [kết quả rà soát và phạm vi kiểm chứng](KIEM_TRA_TAI_LIEU.md).

