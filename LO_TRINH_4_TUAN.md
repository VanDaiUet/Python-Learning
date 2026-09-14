# Lộ trình tăng tốc 4 tuần — Python cho AI Engineer

**Lịch đang áp dụng: 43 giờ/tuần, tổng 172 giờ.** Mỗi tuần có 30 giờ thực hành trực tiếp, 9 giờ học kiến thức và 4 giờ ôn/tự đánh giá. Dành 6 ngày học chính và một ngày chỉ ôn nhẹ 1 giờ; thời gian nghỉ không tính vào giờ học.

Mục tiêu sau 4 tuần: tự viết chương trình Python nhỏ, xử lý dữ liệu, xây một mô hình ML có đánh giá đúng, thực hành PyTorch cơ bản và đưa mô hình thành API chạy localhost. Bạn cũng làm tìm kiếm tài liệu và tiếp cận RAG; nghiệm thu phần sinh câu trả lời cần chạy mô hình thật.

172 giờ ngắn hơn khối lượng 320–400 giờ của lịch cũ. Chương trình chọn phần cốt lõi và giảm độ sâu; không coi việc đọc đủ tên chủ đề là đã thành thạo nâng cao. Toàn bộ 80 bài vẫn nằm trong thư viện để học tiếp.

## Nhịp học mỗi ngày

| Khối | Giờ | Cách làm |
|---|---:|---|
| Kiến thức | 1,5 | Đọc đúng phần được chỉ định; dự đoán kết quả trước khi chạy ví dụ |
| Bài tập nhỏ | 2 | Tự viết, thử nhiều đầu vào; dùng gợi ý khi đã tự thử |
| Dự án/lab | 3 | Ghép kỹ năng thành sản phẩm; tính cả thời gian debug và viết test |
| Ôn và nhật ký | 0,5 | Đóng tài liệu, giải thích hoặc viết lại một phần; ghi điểm vướng |
| **Một ngày chính** | **7** | Sáu ngày = 42 giờ |
| Ngày thứ bảy | **1** | Ôn nhẹ và cập nhật tiến độ; phần còn lại nghỉ |

Như vậy mỗi tuần có **9 giờ kiến thức + 30 giờ thực hành + 4 giờ ôn = 43 giờ**. Bài kiểm tra viết mã trong ngày chính nằm trong quỹ thực hành; không cộng lần nữa vào giờ ôn.

## Cách sử dụng giáo trình có sẵn

- [Phần giải thích kiến thức cốt lõi](kien_thuc/README.md): mở bài B theo lịch, theo dòng **Đọc để hiểu bài**, đọc cơ chế và ví dụ rồi làm nhiệm vụ đã chọn. Một mục dùng cho nhiều bài chỉ cần ôn phần đã biết; không cộng thêm thời gian đọc ngoài lịch.
- [Python B01–B24](chuong_trinh/01_python_nen_tang.md).
- [Dữ liệu, toán và ML B25–B48](chuong_trinh/02_du_lieu_toan_ml.md).
- [Deep Learning, LLM và triển khai B49–B80](chuong_trinh/03_deep_learning_llm_trien_khai.md).
- [24 bài tập có mã khởi đầu](thuc_hanh/README.md).

**Bxx là mã bài tham khảo; các số “tuần” trong ba tài liệu dài thuộc bản 40 tuần.** Với chương trình hiện tại, theo ngày N01–N28 bên dưới. Chỉ làm phần được chọn trong cột thực hành; không cộng toàn bộ nhiệm vụ của lịch 40 tuần vào ngày đó.

Các file `tuan_01.py` đến `tuan_08.py` giữ nguyên tên để công cụ kiểm tra hoạt động; trong lịch mới bạn hoàn thành cả tám bộ này trong ngày 1–4. Cờ `--tuan 8` có nghĩa kiểm tra **bộ bài số 8**, không phải đợi đến tuần 8.

Lưu bài mới tại `bai_lam/4_tuan/ngay_01/` đến `ngay_28/`; sản phẩm tại `bai_lam/4_tuan/S1/` đến `S4/`. Dùng [TIEN_DO.csv](TIEN_DO.csv) để ghi giờ thực tế hằng ngày.

## Tuần 1 — Python dùng được ngay

**Đầu ra S1:** ứng dụng dòng lệnh ghi nhật ký học, lưu JSON; ba thao tác thêm, liệt kê và thống kê. Thực hành 30 giờ.

| Ngày | Giờ | Kiến thức cần đọc | Thực hành và sản phẩm trong 5 giờ |
|---|---:|---|---|
| N01 | 7 | B01–B04: chạy file, biến, kiểu, input, phép tính, if | Chạy demo; làm bộ 1–2; tự viết chương trình tính thời gian học và phân loại kết quả theo điểm. Dự đoán đầu ra trước khi chạy. |
| N02 | 7 | B05–B08: vòng lặp, điều kiện dừng, chuỗi, list | Làm bộ 3–4; xử lý list thời lượng, đếm buổi đạt mục tiêu, chuẩn hóa văn bản; thử rỗng, số 0 và phần tử trùng. |
| N03 | 7 | B09–B12: set, dict, hàm, tham số, return, type hint | Làm bộ 5–6; tách ba hàm tổng hợp nhật ký. Phân biệt return với print; kiểm tra trung bình có phần thập phân. |
| N04 | 7 | B13–B16: pathlib, CSV/JSON, ngoại lệ và unittest | Làm bộ 7–8; đọc dữ liệu mẫu, xuất kết quả; tự thêm ít nhất hai test. Chạy cả tám bộ trên bài làm của mình. |
| N05 | 7 | B17–B20 chọn phần module, Git, class/instance và dataclass đơn giản | Tách logic, lưu trữ và CLI; tạo Git repo cho bài làm, ghi một commit; viết một dataclass để hiểu đối tượng, không bắt buộc đưa class vào mọi chức năng. |
| N06 | 7 | B23–B24 chọn luồng CLI, xác thực và README | Tích hợp S1 với ít nhất 6 test; thử đóng/mở lại; dành 60 phút tự làm một biến thể không xem đáp án. |
| N07 | 1 | Ôn nhẹ | Giải thích list/dict/hàm/ngoại lệ bằng lời; cập nhật điểm và ba lỗi cần nhớ. Không giao thêm lab. |

**S1 tối thiểu:** mỗi bản ghi có `date`, `topic`, `minutes`; ngày hợp lệ, chủ đề không rỗng, phút nguyên dương. Thêm hai buổi 30 và 45 phút phải cho tổng 75. Thiếu file thì bắt đầu rỗng; JSON hỏng phải báo lỗi và không ghi đè. Có dữ liệu giả, lệnh chạy và README.

**Qua tuần 1 khi:** tám bộ bài tập đạt kiểm tra, tự giải thích được cách làm, S1 giữ dữ liệu qua lần chạy và có test cho rỗng, đầu vào sai, tổng hợp, ghi/đọc. S1 là phạm vi rút gọn; chưa đồng nghĩa hoàn thành toàn bộ P01 của lịch dài.

## Tuần 2 — Dữ liệu, toán thực dụng và Machine Learning

**Đầu ra S2:** một báo cáo dữ liệu nhỏ và Pipeline phân loại Wine có thể lưu/nạp. Thực hành 30 giờ.

Tạo môi trường ML theo [BAT_DAU.md](BAT_DAU.md) ở đầu ngày 8. Thời gian cài đặt và debug môi trường nằm trong khối thực hành của ngày, không tính thêm.

| Ngày | Giờ | Kiến thức cần đọc | Thực hành và sản phẩm trong 5 giờ |
|---|---:|---|---|
| N08 | 7 | B25–B26: NumPy, shape, axis, broadcasting | Tạo mảng, lấy lát cắt; tính trung bình theo cột; chuẩn hóa có cột hằng; đối chiếu một phép tính bằng vòng lặp và NumPy. |
| N09 | 7 | B27–B28: pandas, missing, duplicate, join | Tạo ba CSV D1 từ giáo trình; giữ raw, tách dòng lỗi và ghép bảng có kiểm tra khóa. Giải trình mọi dòng. |
| N10 | 7 | B29–B30 và B35 chọn SELECT, JOIN, GROUP BY | Tính doanh thu bằng pandas và SQLite; đối chiếu tổng; vẽ hai biểu đồ có đơn vị; viết báo cáo một trang. |
| N11 | 7 | B31–B34 chọn dot product, đạo hàm, MSE, trung bình/phương sai, lấy mẫu | Tính tay một dự đoán tuyến tính; tự viết gradient descent cho `y=3x+2`; vẽ loss. Mô phỏng lấy mẫu để thấy trung bình mẫu biến động. Chưa làm kiểm định chuyên sâu. |
| N12 | 7 | B37–B40 và B43 chọn split, baseline, macro-F1, logistic và Pipeline | Dùng D3 Wine; lưu split 106/36/36 theo giáo trình. Fit Dummy và Pipeline scaler/logistic chỉ trên train; so trên validation; giữ kín test. |
| N13 | 7 | B41–B42, B44, B47–B48 chọn cây nhỏ, CV và bàn giao | So thêm một cây với logistic; nếu đủ thời gian, CV 3 fold trên train với cả Pipeline. Chốt cấu hình, refit train+validation rồi đánh giá test; lưu artifact, schema, metric và README. |
| N14 | 1 | Ôn nhẹ | Giải thích vì sao không fit scaler trên test; phân biệt baseline, validation và test; cập nhật tiến độ. |

**Phần dữ liệu:** D1 có 12 dòng = 1 bản sao + 5 dòng cách ly + 6 dòng sạch; tổng 1.300.000 VND. SQL và pandas phải khớp. D1 phục vụ học làm sạch, D3 phục vụ học mô hình; đây là hai bộ riêng.

**Phần mô hình:** dùng đúng D3 trong giáo trình. Không đổi cấu hình theo kết quả test. Dự đoán trước/sau lưu nạp phải khớp trên một batch kỹ thuật lấy từ train. Báo macro-F1, confusion matrix, số mẫu và so baseline; không đặt một ngưỡng accuracy chung để chạy đi chạy lại test.

**Qua tuần 2 khi:** báo cáo dữ liệu có thể tái tạo, Pipeline chạy từ file Python và bạn giải thích được cách tránh rò rỉ dữ liệu. Đưa cùng artifact S2 vào API tuần 4.

## Tuần 3 — PyTorch và nền tảng ứng dụng LLM

**Đầu ra S3:** một MLP nhỏ trên digits, cùng công cụ tìm kiếm ghi chú có ID nguồn. Thực hành 30 giờ.

Đầu ngày 15 cài PyTorch bản CPU phù hợp môi trường theo hướng dẫn chính thức đã dẫn trong BAT_DAU. Chọn dữ liệu nhỏ; ngày 18 có thể dùng để sửa nền tảng thay cho CNN.

| Ngày | Giờ | Kiến thức cần đọc | Thực hành và sản phẩm trong 5 giờ |
|---|---:|---|---|
| N15 | 7 | B49–B50: tensor, dtype, autograd, optimizer | Đối chiếu phép nhân với NumPy; tính gradient bằng tay; học `y=3x+2` bằng PyTorch và giải thích zero_grad/backward/step. |
| N16 | 7 | B51–B52: Dataset, DataLoader, train/eval, checkpoint | Dùng load_digits; chia tập một lần, pixel /16; viết vòng train/evaluate cho mạng nhỏ; lưu split và checkpoint. |
| N17 | 7 | B53–B54: MLP, overfitting và validation | Thử học thuộc một batch nhỏ; huấn luyện MLP; lưu đường cong train/validation và chọn checkpoint bằng validation. |
| N18 | 7 | B55 và B59–B60 chọn shape CNN, đánh giá và lưu nạp | Hoàn thiện MLP; nếu nền tảng đã đạt, thử thêm CNN nhỏ trên train/validation với cùng split. Chốt mô hình bằng validation rồi mới mở test, xuất confusion matrix và dự đoán mẫu; nếu chưa vững, bỏ CNN để sửa train loop/kiểm thử. |
| N19 | 7 | B57–B58, B61–B62 chọn token, embedding, attention khái niệm, prompt và schema | Soạn prompt cho ba nhiệm vụ; viết giao diện provider và kiểm tra JSON/timeout bằng fake. Dành tối đa 2 giờ thử một mô hình thật phù hợp máy nếu có; ghi rõ kết quả thực và phần chưa chạy. |
| N20 | 7 | B63–B64: TF-IDF, cosine, chunk và nguồn | Gom 20 ghi chú ngắn đã viết; gán ID; dựng tìm kiếm TF-IDF top-3; trả đoạn và ID nguồn. Thử năm truy vấn phát triển rồi ghi lỗi. |
| N21 | 1 | Ôn nhẹ | Giải thích train/eval, gradient, token và retrieval; ghi giới hạn của mô hình và máy đang dùng. |

**S3 đạt phần Deep Learning khi:** có một MLP thật đã huấn luyện, loss/metric được ghi, split rõ, chọn mô hình bằng validation và checkpoint nạp lại được. CNN là phần mở rộng trong quỹ ngày 18. Không bắt buộc transfer learning hoặc GPU.

**S3 đạt phần tìm kiếm khi:** mỗi kết quả truy về đúng đoạn và ID nguồn; TF-IDF chạy CPU không cần LLM. Fake provider chỉ kiểm tra phần mềm. Kết quả giả lập không được dùng để báo chất lượng sinh câu trả lời.

## Tuần 4 — Đánh giá truy hồi và triển khai ứng dụng AI

**Đầu ra S4 bắt buộc:** API phục vụ mô hình Wine từ S2, có kiểm thử, README và số đo latency. Đồng thời có báo cáo đánh giá tìm kiếm; RAG sinh và Docker là phần mở rộng có điều kiện trong lịch tăng tốc.

| Ngày | Giờ | Kiến thức cần đọc | Thực hành và sản phẩm trong 5 giờ |
|---|---:|---|---|
| N22 | 7 | B65–B66: tập đánh giá, câu ngoài phạm vi và chỉ dẫn trong tài liệu | Soạn 20 câu: 12 có đáp án, 4 ngoài phạm vi, 4 gây nhiễu. Lưu dev/test 10/10, mỗi phần gồm 6/2/2; phát triển trên dev. Các truy vấn đã thử ở N20 chỉ vào dev hoặc nằm ngoài bộ này, không vào test. Chuẩn bị môi trường API; kiểm tra Docker sẵn dùng nếu định làm phần mở rộng. |
| N23 | 7 | B71–B72 chọn tích hợp truy hồi, nguồn và báo cáo | Chốt tìm kiếm rồi đo Recall@3 trên 6 câu test có bằng chứng; báo cả tử/mẫu. Nếu model thật đã chạy được, ghép RAG và chấm 10 đầu ra test. Nếu chưa, hoàn thiện tìm kiếm và dùng thời gian còn lại sửa S2/schema/test. |
| N24 | 7 | B73–B74: FastAPI, schema, model lifecycle, lỗi và timeout | Xây /health và /predict cho Wine; nạp model lúc khởi động; kiểm tra hợp lệ, thiếu trường, sai kiểu, batch rỗng/quá lớn và lỗi nội bộ. /ask là mở rộng sau khi /predict đã đạt. |
| N25 | 7 | B75–B76 chọn cấu hình, logging, tái lập; Docker khi có môi trường | Bắt buộc chạy API từ môi trường ảo sạch, có cấu hình mẫu và script kiểm tra. Nếu Docker sẵn, build/run container localhost; nếu không, ghi chưa thực hành Docker và dùng thời gian hoàn thiện khả năng cài/chạy lại. |
| N26 | 7 | B77–B78 chọn log, latency, giới hạn đồng thời và rollback | Gửi 50 request ở mức đồng thời 1 rồi 3; ghi p50/p95, lỗi và môi trường. Lưu phiên bản artifact; mô phỏng đổi cấu hình lỗi và khôi phục bản tốt. |
| N27 | 7 | B79–B80 chọn README, demo và phản biện | Chạy S4 từ hướng dẫn; demo 5–7 phút; kiểm tra 90 phút tự sửa một yêu cầu Python/API. Viết báo cáo kết quả thật và danh sách kỹ năng chưa đạt. |
| N28 | 1 | Tổng kết | Chấm bốn mốc S1–S4, điền tiến độ và chọn hai nội dung học tiếp. Phần còn lại nghỉ. |

**Đánh giá RAG:** bộ 20 câu là bài tập nhỏ, không đủ để kết luận chất lượng sản phẩm ngoài thực tế. Đo retrieval và generation riêng. Chỉ được ghi “đã thực hành RAG sinh” khi chạy mô hình thật và chấm câu trả lời về tính đúng, căn cứ và từ chối. Chưa có model thật thì ghi `generation_chua_hoan_thanh`; không ảnh hưởng việc hoàn thành API Wine.

**S4 bắt buộc:** sáu trường hợp API nêu ở N24 có test, nạp lại artifact cho dự đoán nhất quán, request ID/phiên bản/thời gian có trong log, có số đo tải nhỏ và README chạy theo được. Triển khai localhost đủ. S4 là mốc tăng tốc, không tự động tương đương P06 đầy đủ với Docker/CI của lịch dài.

## Bốn mốc tự đánh giá

Dùng [DANH_GIA.md](DANH_GIA.md) để chấm điểm và ghi bằng chứng. Mỗi mốc đạt từ 75/100 và phải thỏa các điều kiện bắt buộc tương ứng.

| Mốc | Bằng chứng bắt buộc | Phần mở rộng ghi riêng |
|---|---|---|
| S1 | 24 bài khởi động; CLI lưu JSON; ít nhất 6 test; tự sửa được yêu cầu | Xuất CSV, ID duy nhất, ghi file nguyên tử |
| S2 | Đối chiếu dữ liệu; Wine Pipeline; split/baseline/metric; save/load | CV và tìm kiếm tham số sâu, thêm ensemble |
| S3 | MLP digits thật; checkpoint; công cụ TF-IDF có nguồn | CNN, model ngôn ngữ thật chạy thử |
| S4 | API Wine; 6 ca test; môi trường tái lập; latency; báo cáo retrieval test | RAG sinh được đánh giá thật, Docker, CI trên dịch vụ |

Nếu cuối tuần 1 còn chưa tự viết được hàm hoặc xử lý file, dùng phần mở rộng của N18/N23 để củng cố; vẫn giữ lịch bốn tuần và ghi chính xác phần chưa hoàn thành. Không tăng giờ vô hạn để bù bài còn hổng, không đánh dấu đạt chỉ vì đã chạy được đáp án.

## Nội dung học tiếp sau bốn tuần

Hướng ứng dụng LLM/RAG/AI Agent đã có [chương trình thực hành riêng](chuyen_sau/huong_01/README.md): thêm 6 tuần theo nhịp 43 giờ/tuần, với 36 lab và các mốc R1–R6. Bắt đầu sau khi đã đạt những kỹ năng nền tảng cần dùng.

| Nội dung | Bài tham khảo | Cách học tiếp |
|---|---|---|
| Python sâu | B19–B22 | Composition, generator, decorator, độ phức tạp; viết lại một pipeline đọc theo luồng |
| Toán và thống kê sâu | B31–B34 | Gradient nhiều biến, khoảng tin cậy, kiểm định và giả định |
| ML sâu | B42–B46 | Boosting, tuning, calibration, PCA, clustering, chia theo nhóm/thời gian |
| Deep Learning sâu | B55–B60 | CNN đầy đủ, transfer learning, ablation và đánh giá |
| RAG hoàn chỉnh và agent | B63–B72 | Dense/hybrid retrieval, bộ đánh giá lớn hơn, tool loop có giới hạn, LoRA |
| Vận hành đầy đủ | B75–B80 và nhánh N1–N8 | Docker/CI nếu chưa đạt, drift, hàng đợi, quantization và distributed training |

Bắt đầu ngày 1 bằng [BAT_DAU.md](BAT_DAU.md). Ngày không gắn sẵn với ngày tháng; điền ngày bắt đầu thực tế vào bảng tiến độ.
