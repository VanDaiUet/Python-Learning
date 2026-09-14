# Sáu mốc dự án thực hành

> Đề P01–P06 đầy đủ để học tiếp. Trong lịch tăng tốc, dùng [phạm vi S1–S4](../LO_TRINH_4_TUAN.md) và [tiêu chí 4 tuần](../DANH_GIA.md); không cộng tất cả yêu cầu P01–P06 vào bốn tuần.

Đây là **đề để bạn tự xây**, không phải sáu ứng dụng đã được viết sẵn. Mỗi dự án tận dụng bài của những tuần trước; tuần cuối dành tích hợp và đánh giá. Tiêu chí chung và thang 100 điểm tham khảo tại [DANH_GIA.md](../DANH_GIA.md).

Lưu ở `bai_lam/du_an/P01/` đến `P06/`. Tên thư mục con có thể đặt theo sản phẩm. Dữ liệu giả lập hoặc công khai cần ghi nguồn và điều kiện sử dụng. Mọi lệnh trong tài liệu dự án là giao diện **đề nghị bạn triển khai**, không phải lệnh đã chạy được trong bộ khởi động.

## P01 — Nhật ký học tập bằng Python CLI

**Mốc:** tuần 12. **Chuẩn bị:** tuần 6–11 đã có hàm, file, test và cấu trúc module.

Ứng dụng giúp lưu từng buổi học, xem lại và tính thời gian theo chủ đề. Chỉ dùng thư viện chuẩn.

Schema JSON là list các object:

```json
[
  {
    "id": "session_001",
    "date": "2026-09-11",
    "topic": "python",
    "minutes": 45,
    "note": "Biến, phép tính và lời chào"
  }
]
```

Bốn lệnh yêu cầu, minh họa khi đứng trong thư mục P01 và đã chọn đúng Python:

```text
python main.py add --date 2026-09-11 --topic python --minutes 45 --note "Biến và phép tính"
python main.py list
python main.py summary
python main.py export --output report.csv
```

`add` tự sinh ID duy nhất. Quy định trước nơi lưu `sessions.json` và ghi trong README. Ngày phải đúng YYYY-MM-DD và tồn tại trên lịch; có thể parse bằng `date.fromisoformat` rồi đối chiếu `isoformat()` với chuỗi gốc. `topic.strip()` không rỗng, `minutes` là số nguyên dương; khi kiểm tra JSON phải loại cả bool khỏi trường số phút.

**Yêu cầu đạt:**

- Thêm hai buổi cùng chủ đề 30 và 45 phút cho tổng 75; thêm chủ đề khác không làm sai tổng.
- Đóng rồi mở chương trình vẫn đọc được dữ liệu.
- Tệp chưa tồn tại được xem là nhật ký rỗng; tệp hỏng phải báo lỗi, giữ nguyên dữ liệu.
- Có ít nhất 12 test có ý nghĩa, gồm ngày sai, ID trùng, phút âm/0/sai kiểu, dữ liệu rỗng, JSON hỏng và xuất CSV chứa dấu phẩy/tiếng Việt.
- README có cách chạy, dữ liệu mẫu tối thiểu 10 buổi và một giới hạn đã biết.

**Gợi ý cấu trúc:** `main.py` nhận lệnh, `service.py` xử lý nghiệp vụ, `storage.py` đọc/ghi, `tests/` kiểm thử. Bản đầu có thể nhỏ hơn rồi tách khi trách nhiệm đã rõ. Mở rộng tự chọn: lọc ngày và ghi file tạm trước khi thay file chính.

## P02 — Làm sạch dữ liệu và báo cáo bán hàng

**Mốc:** tuần 18. **Chuẩn bị:** xây dần từ tuần 14–17.

Dùng bộ **D1** đã ghi đầy đủ trong [giáo trình dữ liệu](../chuong_trinh/02_du_lieu_toan_ml.md): `customers.csv`, `products.csv`, `orders.csv`. Tự tạo các file theo khối CSV đó; bộ dữ liệu bán hàng chưa được lưu thành file trong bộ khởi động.

Luồng công việc: lưu raw → xác thực schema/khóa → loại bản sao → cách ly dòng lỗi kèm lý do → ghép bảng → tính chỉ số bằng pandas và SQL → xuất báo cáo.

**Yêu cầu đạt:**

- Giải trình đủ 12 dòng: 1 bản sao loại bỏ, 5 dòng cách ly, 6 dòng sạch.
- Tổng sản phẩm 12; tổng doanh thu 1.300.000 VND; Bắc 500.000, Trung 600.000, Nam 200.000.
- Cùng dữ liệu cho kết quả SQL và pandas khớp nhau. Chạy quy trình hai lần không nhân đôi dữ liệu trong SQLite.
- Không sửa dữ liệu gốc; không tùy tiện thay missing bằng 0; kiểm tra cardinality của join.
- Báo cáo có bảng kiểm tra chất lượng, ít nhất hai biểu đồ có đơn vị và ba nhận xét có căn cứ. Dữ liệu 6 dòng không đủ cho kết luận thị trường.

**Bàn giao:** `prepare.py`, `queries.sql`, `report.md`, CSV sạch, CSV cách ly, SQLite, README và test đối chiếu. Mở rộng: tạo thêm dữ liệu giả có seed để thử tốc độ mà vẫn giữ bộ 12 dòng làm kiểm tra tính đúng.

## P03 — Bộ phân loại Wine có đánh giá đáng tin

**Mốc:** tuần 24. **Chuẩn bị:** dùng cùng split từ tuần 19.

Dữ liệu `sklearn.datasets.load_wine`: 178 mẫu, 13 đặc trưng và ba lớp, đã mô tả trong D3 của giáo trình. Mục tiêu là nhận dạng lớp dữ liệu, không phải đánh giá chất lượng đồ uống.

**Trình tự bắt buộc:**

1. Tách test 20%, sau đó validation bằng 25% phần còn lại; phân tầng và seed 42 theo D3. Lưu ID mẫu: 106 train, 36 validation, 36 test.
2. Đặt baseline Dummy; so sánh một mô hình tuyến tính và một mô hình cây trên train/CV/validation.
3. Gói preprocessing và estimator thành Pipeline. Mọi bước học tham số nằm trong phần fit của từng fold.
4. Viết `decision.md` chốt cấu hình và metric macro-F1 trước khi mở test. Refit toàn bộ Pipeline đã chọn trên train + validation theo quy trình P03 của giáo trình.
5. Đánh giá test sau quyết định; báo kết quả một cách trung thực. Không dùng test để tiếp tục chọn mô hình.

**Yêu cầu đạt:** tái lập được split, baseline và quy trình; có confusion matrix, support từng lớp và phân tích lỗi; save/load giữ cùng dự đoán; kiểm tra input thiếu/dư cột, thứ tự, kiểu số và batch rỗng. Những kiểm tra schema này là phần bàn giao dự án; nếu chưa làm bài mở rộng tuần 24, hoàn thiện trước khi đưa P03 vào API.

**Bàn giao:** `train.py`, `predict.py`, cấu hình, split, artifact do chính bạn tạo, schema, phiên bản thư viện, kết quả CV/validation/test tách riêng, model card và README. Mẫu schema ghi rõ đúng tên/thứ tự 13 đặc trưng. Không đòi một con số accuracy tùy ý; cần giải thích được kết quả so với baseline và giới hạn của bộ nhỏ.

**Tái sử dụng:** P06 có thể phục vụ chính artifact này, không huấn luyện lại mô hình trong mỗi request.

## P04 — Nhận dạng chữ số với PyTorch

**Mốc:** tuần 30. **Chuẩn bị:** tensor, train loop và CNN từ tuần 25–29.

Bản CPU dùng `sklearn.datasets.load_digits`: ảnh xám 8×8 và 10 lớp. Đưa ảnh về `float32`, chia 16 để đưa thang pixel về [0,1], thêm chiều kênh để có `(N,1,8,8)` khi dùng CNN. Hệ số 16 là đặc tả dữ liệu, không phải thống kê học từ toàn bộ tập.

Chia train/validation/test một lần trước thí nghiệm; giữ nguyên split cho baseline và mạng. Làm MLP trước, rồi CNN nhỏ. Không cần tải ảnh ngoài hoặc huấn luyện mô hình lớn.

**Yêu cầu đạt:**

- Giải thích được shape từ input đến logits `(N,10)`, loss và bước cập nhật trọng số.
- Thử overfit một batch nhỏ để phát hiện lỗi trong đường huấn luyện.
- So sánh MLP và CNN với cùng split, lưu loss/metric theo epoch; chọn checkpoint bằng validation.
- Lúc đánh giá dùng chế độ eval và tắt ghi gradient; chỉ mở test sau khi chọn cấu hình.
- Checkpoint nạp lại chạy inference được; báo confusion matrix, ví dụ sai, thời gian, CPU/GPU và seed.
- Với thiết bị hoặc môi trường khác nhau, không hứa mọi phép tính lặp lại giống hệt từng bit.

**Bàn giao:** mã dataset/train/evaluate/predict, checkpoint, đường cong học, báo cáo thực nghiệm và README. Transfer learning ở tuần 28 dùng dữ liệu/kiến trúc phù hợp là bài riêng; không bắt buộc ép mô hình ảnh lớn vào ảnh 8×8 của dự án này.

## P05 — Trợ lý hỏi đáp tài liệu có trích dẫn

**Mốc:** tuần 36. **Chuẩn bị:** triển khai dần tuần 31–35.

Tự chọn **20–50 tài liệu ngắn** tự viết hoặc công khai có quyền sử dụng. Một lựa chọn đơn giản là các ghi chú học Python do bạn viết. Mỗi tài liệu có ID ổn định, tiêu đề, nguồn và nội dung. Không lấy chính đáp án của bộ đánh giá để nhét vào prompt mỗi câu.

Luồng: nhập tài liệu → chia đoạn → tạo chỉ mục → tìm top-k → đưa ngữ cảnh vào mô hình → kiểm tra định dạng → trả câu trả lời cùng ID nguồn. Có tìm kiếm từ khóa làm baseline; so sánh truy hồi theo embedding khi có tài nguyên.

**Tập đánh giá:** tự soạn tối thiểu 40 câu và đáp án/kỳ vọng: 20 câu có câu trả lời, 10 câu ngoài phạm vi, 10 câu kiểm tra gây nhiễu/trích dẫn sai/chỉ dẫn nằm trong tài liệu. Gán nhóm và ID nguồn đúng trước khi chạy. Chia dev/test từ đầu, chẳng hạn 20/20, phân bổ mỗi nhóm ở cả hai tập. Chỉ tối ưu trên dev; ghi kết quả test khi chốt.

**Yêu cầu đạt:**

- Đo retrieval Recall@k trên các câu có bằng chứng; ghi số câu và các ID tài liệu đúng cho từng câu.
- Đánh giá riêng tính đúng của câu trả lời, nguồn có thực sự hỗ trợ, và việc từ chối khi không đủ dữ liệu.
- Chấm tay một mẫu có tiêu chí rõ; nếu dùng LLM làm giám khảo, kiểm tra với nhãn tay và ghi bất đồng.
- Có giới hạn context, timeout, số lần thử lại và chi phí/số token nếu nhà cung cấp trả thông tin đó.
- Nội dung tài liệu được xử lý như dữ liệu. Các chỉ dẫn trong tài liệu không tự cấp quyền gọi công cụ hay thực hiện hành động.
- Với câu hỏi ngoài phạm vi, hệ thống có cách báo không đủ căn cứ thay vì tạo câu trả lời giả.

Fake provider dùng để kiểm tra schema, timeout và luồng phần mềm. **Nghiệm thu P05 đầy đủ cần đo chất lượng đầu ra trên một mô hình thật**: mô hình nhỏ chạy cục bộ hoặc môi trường/API bạn chọn. Nếu chưa đủ tài nguyên, hoàn thành phần tìm kiếm/tích hợp và ghi phần đánh giá sinh là chưa xong. Không cần trả phí để làm các phần đầu.

**Bàn giao:** dữ liệu có nguồn, bộ đánh giá và cách chia, cấu hình chunk/top-k, mã lập chỉ mục/truy vấn, báo cáo dev/test, phiên bản mô hình và prompt, README/demo. Fine-tuning và agent có nhiều công cụ là phần mở rộng; không phải điều kiện của một RAG cơ bản tốt.

## P06 — Đưa một dự án thành dịch vụ AI

**Mốc:** tuần 40. **Chuẩn bị:** phát triển từng phần từ tuần 37.

Chọn **P03 hoặc P05**, giữ phạm vi một dịch vụ. Đích triển khai bắt buộc là localhost; đưa lên cloud là phần mở rộng sau khi đã hiểu chi phí và cấu hình.

**Hợp đồng tối thiểu:**

- `GET /health`: báo trạng thái sẵn sàng của dịch vụ; phân biệt tiến trình đang chạy và mô hình đã nạp.
- `POST /predict` cho P03 hoặc `POST /ask` cho P05: schema vào/ra rõ, báo lỗi đầu vào và lỗi phụ thuộc có cấu trúc.
- Nạp artifact/chỉ mục khi khởi động; cấu hình qua môi trường; không hard-code secret.
- Mỗi request có ID, thời gian xử lý, trạng thái và phiên bản mô hình trong log phù hợp; tránh ghi dữ liệu nhạy cảm không cần thiết.

**Yêu cầu đạt:**

1. Test đơn vị cho logic và test tích hợp cho API: yêu cầu hợp lệ, thiếu trường, sai kiểu, batch rỗng/quá lớn và phụ thuộc lỗi.
2. Docker image chạy được theo README; lưu phiên bản dependency sau khi cài thành công; CI thực hiện kiểm tra tự động.
3. Đo latency p50/p95, throughput và lỗi với tải nhỏ có mô tả số request, concurrency, warm-up và môi trường. Chọn mục tiêu đo trước rồi giải thích kết quả, không đặt một ngưỡng chung cho mọi máy.
4. Theo dõi input drift và chất lượng khi có nhãn/phản hồi; hiểu drift không tự chứng minh accuracy giảm.
5. Thử chuyển sang artifact/chỉ mục phiên bản trước bằng cấu hình; chứng minh rollback hoạt động.
6. Một người theo README có thể cài, khởi động, gọi API mẫu và chạy test.

**Bàn giao:** source, Dockerfile, cấu hình mẫu, CI, test, báo cáo tải, hướng dẫn xử lý sự cố/rollback, sơ đồ thành phần và demo 5–7 phút. Nếu chưa có Docker chạy được trên máy, thử API localhost và đánh dấu phần container chưa hoàn thành; không tự coi tài liệu thiết kế là bằng chứng đã chạy.

## Mẫu README cho mỗi dự án

```markdown
# Tên dự án
Mục tiêu, ai dùng, và ví dụ đầu vào → đầu ra.

## Dữ liệu
Nguồn, schema, đơn vị, giới hạn và cách tái tạo.

## Chạy từ đầu
Phiên bản Python, cài dependency, lệnh chuẩn bị/train/run/test.

## Kết quả
Baseline hoặc cách đối chiếu, metric, tập đánh giá, môi trường.

## Quyết định
Vì sao chọn giải pháp này, phương án đã đo và đánh đổi.

## Giới hạn
Những trường hợp chưa xử lý và việc cần làm tiếp.
```
