# Giai đoạn 3 — Deep Learning, LLM và triển khai hệ thống AI

> Thư viện bài học đầy đủ; số tuần dưới đây thuộc bản 40 tuần. Lịch đang áp dụng là [4 tuần, N01–N28](../LO_TRINH_4_TUAN.md). Chỉ đọc và làm phần được chỉ định trong lịch mới.

Tuần 25–40 · Bài B49–B80 · 8–10 giờ mỗi tuần. Học sau khi hoàn thành Python, NumPy, pandas, toán nền tảng, đánh giá mô hình và dự án ML P03 ở hai giai đoạn trước.

Đề và tiêu chí bàn giao P04/P05/P06 đầy đủ ở [DE_BAI.md](../du_an/DE_BAI.md); các bài dưới đây xây từng phần để tuần dự án tập trung tích hợp và đánh giá.

## Cách học và giới hạn tài nguyên

- Mỗi tuần: khoảng 2 giờ đọc và ghi chép, 4–5 giờ thực hành hai bài, 1–2 giờ kiểm tra và sửa lỗi, 1 giờ tổng kết. Tuần dự án dùng phần lớn thời gian để tích hợp bài đã làm.
- Mỗi tuần có **3 nhiệm vụ chung cho hai bài**: **Cơ bản** và **Ứng dụng** bắt buộc, **Mở rộng** tự chọn khi còn thời gian. Chưa đạt tiêu chí thì dành thêm thời gian củng cố; 40 tuần là lịch gợi ý, không phải cam kết thành thạo hay có việc làm.
- Dùng CPU làm mặc định. Mạng nhỏ, dữ liệu `sklearn.datasets.load_digits()` có sẵn trong gói, batch nhỏ và vài epoch đủ cho phần bắt buộc. Ghi cấu hình máy và thời gian chạy; không suy rộng tốc độ sang máy khác.
- Giới hạn một lần thử huấn luyện khoảng 10–15 phút; nếu vượt, giảm số mẫu hoặc số epoch và ghi rõ. Riêng kiểm tra học thuộc batch nhỏ cần sửa lỗi cho đến khi đạt, không lấy thiếu tài nguyên làm kết luận mô hình đúng.
- Phần LLM dùng giao diện chung `generate(messages, ...)`; fake provider trả dữ liệu được lập trình sẵn để kiểm tra luồng phần mềm, không cần khóa API hoặc dịch vụ trả phí. Tìm kiếm TF-IDF cũng chạy trên CPU.
- Đánh giá câu trả lời sinh tự do cần **mô hình thật**. Có thể dùng mô hình mở nhỏ chạy cục bộ sau khi kiểm tra model card, ngôn ngữ, giấy phép và bộ nhớ. Nếu chưa chạy được, tiếp tục phần kỹ thuật và ghi “chưa đánh giá chất lượng sinh”; P05 chỉ được nghiệm thu đầy đủ sau khi có đánh giá sinh thật, không tính kết quả giả lập thay thế.
- Các đoạn văn, câu hỏi và ngưỡng nghiệm thu bên dưới là bài tập do chương trình thiết kế. Ngưỡng chỉ áp dụng cho bộ dữ liệu nhỏ của bài học, không phải chuẩn chất lượng sản phẩm ngoài thực tế.
- Lưu mỗi bài vào thư mục riêng với mã nguồn, cách chạy, kết quả thật và ghi chú lỗi. Với số thực, dùng sai số cho phép thay vì bắt bằng nhau tuyệt đối. Chỉ nạp model/checkpoint từ nguồn mình tin cậy.

## Tuần 25 — Tensor và đạo hàm tự động

### B49 — Từ NumPy sang tensor

**Đọc để hiểu bài:** [H01 — Tensor và autograd](../kien_thuc/04_deep_learning_he_thong_agent.md#h01); [D01 — Shape, axis và broadcasting](../kien_thuc/02_du_lieu_toan_ml.md#d01).

- **Mục tiêu:** đọc đúng shape, dtype và device; thực hiện phép toán theo batch.
- **Hiểu bản chất:** tensor là mảng nhiều chiều; tên trục là cách ta diễn giải dữ liệu. Batch ảnh có thể mang shape `(N, C, H, W)`, còn bảng đặc trưng là `(N, D)`. Nhân từng phần tử khác nhân ma trận; broadcasting có thể tạo kết quả hợp lệ về cú pháp nhưng sai ý nghĩa bài toán.
- **Nộp và đạt:** một script chạy CPU, bảng giải thích 6 shape, 4 assertion gồm cột hằng và phép nhân; sai lệch với NumPy dưới `1e-5`.
- **Tự kiểm 1:** vì sao tensor `(4, 1)` trừ tensor `(4,)` có thể cho kết quả `(4, 4)`?
- **Tự kiểm 2:** đổi shape bằng reshape khác hoán đổi trục bằng transpose ở điểm nào?

### B50 — Autograd và một bước cập nhật trọng số

**Đọc để hiểu bài:** [H01 — Tensor và autograd](../kien_thuc/04_deep_learning_he_thong_agent.md#h01); [D05 — Đạo hàm và gradient descent](../kien_thuc/02_du_lieu_toan_ml.md#d05).

- **Mục tiêu:** giải thích forward, loss, backward và optimizer bằng một ví dụ tính tay.
- **Hiểu bản chất:** forward tạo dự đoán; loss biến sai số thành một số; backward áp dụng quy tắc dây chuyền để tính đạo hàm theo tham số. Đạo hàm cho biết hướng thay đổi cục bộ của loss, không tự cập nhật tham số. Gradient mặc định cộng dồn nên mỗi bước học độc lập phải xóa gradient cũ. Đọc thêm [PyTorch: luồng học cơ bản](https://docs.pytorch.org/tutorials/beginner/basics/intro.html).
- **Nộp và đạt:** phép tính tay khớp trong `1e-5`; mô hình đạt MSE dưới `0.01` trên 10 điểm kiểm tra trong miền dữ liệu; giải thích được từng bước cập nhật.
- **Tự kiểm 1:** gọi `backward()` hai lần trên hai forward khác nhau mà không xóa gradient sẽ xảy ra điều gì?
- **Tự kiểm 2:** vì sao không phải tensor đầu vào nào cũng cần `requires_grad=True`?

### Thực hành tuần 25 — 3 nhiệm vụ

- **Cơ bản:** (B49) tạo tensor `X` shape `(4, 3)`, trọng số `W` shape `(3, 2)` và bias `(2,)`; dự đoán shape của `X @ W + b` trước khi chạy. (B50) với `y = w*x`, `x=2`, `w=1`, mục tiêu bằng 6 và loss bình phương, tính tay loss và đạo hàm theo `w`, rồi đối chiếu autograd.
- **Ứng dụng:** (B49) viết hàm chuẩn hóa từng cột của bảng 20 × 3; xử lý cột hằng bằng epsilon; so kết quả với NumPy trên cùng dữ liệu. (B50) học quan hệ `y=3x+2` từ 40 điểm không nhiễu bằng SGD; in loss trước/sau, `w`, `b` và gradient ở bước đầu.
- **Mở rộng:** (B49) đo thời gian phép nhân trên hai kích thước CPU; nếu có GPU, đo cả chi phí chuyển dữ liệu và đồng bộ trước khi kết luận. (B50) cố tình quên xóa gradient trong 5 bước, ghi sự khác biệt; thử learning rate quá lớn và nhận diện loss phân kỳ.

## Tuần 26 — Đưa dữ liệu vào mô hình và lưu kết quả

### B51 — Dataset, DataLoader và tách tập dữ liệu

**Đọc để hiểu bài:** [H02 — Batch, train/eval và checkpoint](../kien_thuc/04_deep_learning_he_thong_agent.md#h02); [D08 — Chia tập, baseline và leakage](../kien_thuc/02_du_lieu_toan_ml.md#d08).

- **Mục tiêu:** tạo pipeline dữ liệu có batch, nhãn đúng và không trộn tập đánh giá vào huấn luyện.
- **Hiểu bản chất:** `Dataset` quy định một mẫu gồm những gì; `DataLoader` gom mẫu thành batch và điều khiển thứ tự đọc. Tách train/validation/test trước khi học phép biến đổi có tham số. Augmentation chỉ dành cho train; cùng một ảnh test phải được tiền xử lý ổn định qua các lần đánh giá.
- **Nộp và đạt:** lưu chỉ số ba tập; giao giữa các tập rỗng; 10 batch kiểm tra đúng shape, kiểu nhãn và miền giá trị `[0, 1]`; test không bị augmentation.
- **Tự kiểm 1:** vì sao phải lưu chỉ số tách tập thay vì chỉ ghi “đã dùng seed 42”?
- **Tự kiểm 2:** vì sao không mặc định tăng số worker ngay khi pipeline đọc dữ liệu chậm?

### B52 — Vòng lặp train, eval và checkpoint

**Đọc để hiểu bài:** [H02 — Batch, train/eval và checkpoint](../kien_thuc/04_deep_learning_he_thong_agent.md#h02); [H11 — Artifact, Docker và CI](../kien_thuc/04_deep_learning_he_thong_agent.md#h11).

- **Mục tiêu:** viết một vòng lặp có thể dùng lại, lưu mô hình và khôi phục dự đoán.
- **Hiểu bản chất:** chế độ `train()`/`eval()` thay đổi hành vi các lớp như dropout; tắt theo dõi gradient khi suy luận là việc riêng. Checkpoint dùng để học tiếp cần tham số mô hình, trạng thái optimizer và tiến độ; artifact dự đoán còn cần cấu hình kiến trúc và tiền xử lý. Chọn checkpoint bằng validation, giữ test cho nghiệm thu cuối.
- **Nộp và đạt:** có lịch sử train/validation, không dùng test để chọn epoch; dự đoán ở `eval()` trước/sau nạp có sai lệch dưới `1e-6` trên cùng máy và dữ liệu.
- **Tự kiểm 1:** tại sao chỉ gọi `eval()` chưa có nghĩa là đã tắt tính gradient?
- **Tự kiểm 2:** nếu chỉ lưu trọng số nhưng bỏ cách chuẩn hóa ảnh, lần dự đoán sau có thể sai thế nào?

### Thực hành tuần 26 — 3 nhiệm vụ

- **Cơ bản:** (B51) đọc `load_digits()`, xem 12 ảnh 8 × 8 và phân bố 10 nhãn; tạo ba tập phân tầng với seed cố định theo tỉ lệ 60/20/20. (B52) viết `train_one_epoch()` và `evaluate()` cho mạng tuyến tính trên dữ liệu B51; tính loss trung bình có trọng số theo số mẫu, kể cả batch cuối nhỏ.
- **Ứng dụng:** (B51) viết dataset trả ảnh float shape `(1, 8, 8)` chia cho 16 và nhãn số nguyên; tạo loader batch 32, `num_workers=0` để bắt đầu trên Windows. (B52) chạy tối đa 5 epoch trên CPU, lưu checkpoint validation tốt nhất; khởi tạo lại mô hình từ cấu hình và so dự đoán trước/sau khi nạp.
- **Mở rộng:** (B51) thêm biến đổi nhẹ vào train, hiển thị ảnh trước/sau và chỉ ra một phép biến đổi có nguy cơ đổi ý nghĩa chữ số. (B52) dừng sau epoch 2 rồi học tiếp từ checkpoint; ghi cả seed và trạng thái liên quan, phân biệt gần tái lập với tái lập từng bit.

## Tuần 27 — MLP, regularization và sửa lỗi học máy

### B53 — MLP và bài kiểm tra học thuộc batch nhỏ

**Đọc để hiểu bài:** [H03 — MLP, CNN và attention](../kien_thuc/04_deep_learning_he_thong_agent.md#h03); [H02 — Batch, train/eval và checkpoint](../kien_thuc/04_deep_learning_he_thong_agent.md#h02).

- **Mục tiêu:** tạo mạng nhiều lớp và kiểm tra nó thực sự học được trước khi chạy lớn.
- **Hiểu bản chất:** các lớp tuyến tính nối tiếp mà không có phi tuyến vẫn tương đương một phép biến đổi tuyến tính. ReLU giúp mạng biểu diễn quan hệ phức tạp hơn. Học thuộc một batch 16 mẫu là phép chẩn đoán pipeline: nếu thất bại, hãy xem nhãn, loss, gradient và bước cập nhật trước khi tăng dữ liệu.
- **Nộp và đạt:** đúng 16/16 mẫu batch nhỏ; có biểu đồ loss và nhật ký một lỗi đã sửa; giải thích vì sao kết quả này chưa nói lên khả năng tổng quát hóa.
- **Tự kiểm 1:** thêm softmax trước cross-entropy có cần thiết trong bài này không, vì sao?
- **Tự kiểm 2:** gradient khác 0 nhưng trọng số không đổi gợi ý cần kiểm tra dòng lệnh nào?

### B54 — Overfitting, dropout và early stopping

**Đọc để hiểu bài:** [H03 — MLP, CNN và attention](../kien_thuc/04_deep_learning_he_thong_agent.md#h03); [H02 — Batch, train/eval và checkpoint](../kien_thuc/04_deep_learning_he_thong_agent.md#h02).

- **Mục tiêu:** phát hiện học quá khớp bằng train/validation và thực hiện một so sánh công bằng.
- **Hiểu bản chất:** train loss thấp cho biết mô hình khớp dữ liệu đã thấy; validation mới cung cấp bằng chứng về dữ liệu chưa học. Weight decay hạn chế độ lớn trọng số, dropout tạo nhiễu trong lúc học, early stopping chọn thời điểm dừng. Mỗi biện pháp có thể giúp hoặc làm hại; phải kiểm tra trên cùng cách tách dữ liệu.
- **Nộp và đạt:** bảng hai thí nghiệm và một quyết định dựa trên validation; mô tả ít nhất 2 giới hạn; không yêu cầu regularization phải thắng để được đạt.
- **Tự kiểm 1:** train và validation đều kém thường dẫn đến các giả thuyết nào khác với train tốt nhưng validation kém?
- **Tự kiểm 2:** vì sao chọn cấu hình bằng test rồi công bố điểm test sẽ khiến đánh giá quá lạc quan?

### Thực hành tuần 27 — 3 nhiệm vụ

- **Cơ bản:** (B53) tạo MLP `64 → 32 → 10`, ghi số tham số và shape sau mỗi lớp; dùng logits thô với cross-entropy cho nhãn lớp. (B54) dùng 200 ảnh train để tạo một thí nghiệm dễ thấy overfitting; vẽ train loss, validation loss và ghi checkpoint được chọn.
- **Ứng dụng:** (B53) cố định 16 ảnh train có nhãn sạch, tắt augmentation/dropout; huấn luyện chỉ batch này đến khi dự đoán đúng toàn bộ, giới hạn 1.000 bước. (B54) so hai cấu hình chỉ khác một yếu tố: có/không weight decay hoặc dropout; giữ split, số epoch tối đa và cách đánh giá giống nhau.
- **Mở rộng:** (B53) thêm một lỗi có chủ đích như không gọi optimizer step; ghi triệu chứng, giả thuyết và cách xác nhận lỗi. (B54) lặp 3 seed và báo trung bình, khoảng biến thiên; kiểm tra kết luận có đổi khi dữ liệu ít hay không.

## Tuần 28 — Thị giác máy tính và chuyển giao đặc trưng

### B55 — CNN nhỏ và kiểm tra shape

**Đọc để hiểu bài:** [H03 — MLP, CNN và attention](../kien_thuc/04_deep_learning_he_thong_agent.md#h03); [H02 — Batch, train/eval và checkpoint](../kien_thuc/04_deep_learning_he_thong_agent.md#h02).

- **Mục tiêu:** hiểu convolution, pooling và xây một CNN vừa CPU.
- **Hiểu bản chất:** convolution dùng cùng bộ lọc ở nhiều vị trí, giúp học mẫu cục bộ với ít tham số hơn kết nối đầy đủ trên ảnh lớn. Pooling giảm kích thước không gian, đồng thời làm mất một phần thông tin. CNN không tự miễn nhiễm với ảnh xoay, ánh sáng hoặc dữ liệu khác miền; cần đánh giá đúng bối cảnh.
- **Nộp và đạt:** phép tính tay khớp; sơ đồ shape hoàn chỉnh; có checkpoint và bảng MLP/CNN cùng split; phân tích ít nhất 5 ảnh dự đoán sai.
- **Tự kiểm 1:** tham số padding ảnh hưởng kích thước đầu ra và thông tin ở biên như thế nào?
- **Tự kiểm 2:** tại sao CNN không chắc chắn thắng MLP trên ảnh nhỏ 8 × 8?

### B56 — Transfer learning và đóng băng backbone

**Đọc để hiểu bài:** [H03 — MLP, CNN và attention](../kien_thuc/04_deep_learning_he_thong_agent.md#h03); [H02 — Batch, train/eval và checkpoint](../kien_thuc/04_deep_learning_he_thong_agent.md#h02).

- **Mục tiêu:** phân biệt học đầu phân loại, fine-tuning và học lại từ đầu.
- **Hiểu bản chất:** backbone biến đầu vào thành đặc trưng; head biến đặc trưng thành dự đoán của tác vụ. Đóng băng backbone giúp tái sử dụng biểu diễn đã học và giảm số tham số cần cập nhật, nhưng không bảo đảm đặc trưng phù hợp miền mới. Xem ví dụ [transfer learning của PyTorch](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html).
- **Nộp và đạt:** thực hiện được phương án CPU bằng backbone B55 là đủ; ghi số tham số được học, metric trước/sau và giới hạn do hai tác vụ cùng miền digits.
- **Tự kiểm 1:** vì sao backbone ngẫu nhiên bị đóng băng không phải ví dụ chuyển giao kiến thức đã học?
- **Tự kiểm 2:** nếu backbone có batch normalization, chỉ đặt `requires_grad=False` có đủ để cố định mọi trạng thái không?

### Thực hành tuần 28 — 3 nhiệm vụ

- **Cơ bản:** (B55) tự tính đầu ra của một bộ lọc 2 × 2 trên ảnh 3 × 3 nhỏ; đối chiếu bằng phép convolution với stride 1, padding 0. (B56) lấy backbone CNN B55 đã học 10 chữ số; thay head để dự đoán chữ số nhỏ hơn 5 hay từ 5 trở lên; giữ nguyên split ảnh.
- **Ứng dụng:** (B55) dùng hai lớp convolution tối đa 16 kênh trên digits B51; chạy 3–5 epoch, so validation accuracy và thời gian với MLP đã có. (B56) đóng băng backbone, chỉ học head trên 200 ảnh train; kiểm tra backbone không đổi và head có đổi; so validation với head khởi tạo chưa học.
- **Mở rộng:** (B55) thêm nhiễu nhỏ vào một bản sao validation để xem mức giảm điểm; ghi đây là kiểm tra độ bền bổ sung, không sửa test gốc. (B56) dùng backbone pretrained từ nguồn tin cậy trên 30–100 ảnh có giấy phép phù hợp, hoặc mở lớp cuối của backbone B55 để fine-tune nhẹ trên CPU.

## Tuần 29 — Văn bản, embedding và attention

### B57 — Tokenization và biểu diễn văn bản

**Đọc để hiểu bài:** [R01 — LLM và tokenization](../kien_thuc/03_llm_rag.md#r01); [R08 — Embedding và cosine](../kien_thuc/03_llm_rag.md#r08).

- **Mục tiêu:** chuyển văn bản thành ID, xử lý padding và giải thích embedding.
- **Hiểu bản chất:** token là đơn vị do tokenizer quy định, không nhất thiết bằng một từ; tiếng Việt và dấu câu làm giả định “mỗi từ một token” dễ sai. ID chỉ là chỉ số; embedding tra ID vào bảng vector có thể học. Vector khởi tạo ngẫu nhiên chưa mang bằng chứng về ý nghĩa ngôn ngữ. Tài liệu học tiếp: [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1).
- **Nộp và đạt:** 6 ca kiểm tra gồm từ lạ, câu rỗng, cắt ngắn và padding; thêm padding không làm đổi vector trung bình vượt `1e-6`.
- **Tự kiểm 1:** tại sao không thể so ID lớn/nhỏ để kết luận hai từ giống nghĩa?
- **Tự kiểm 2:** nếu tính trung bình cả padding, câu ngắn và dài chịu ảnh hưởng khác nhau ra sao?

### B58 — Attention và cấu trúc Transformer

**Đọc để hiểu bài:** [H03 — MLP, CNN và attention](../kien_thuc/04_deep_learning_he_thong_agent.md#h03); [R01 — LLM và tokenization](../kien_thuc/03_llm_rag.md#r01).

- **Mục tiêu:** tính được attention nhỏ và đọc được sơ đồ Transformer ở mức khái niệm.
- **Hiểu bản chất:** query so khớp key để tạo trọng số; trọng số dùng trộn các value thành biểu diễn phụ thuộc ngữ cảnh. Scaled dot-product attention là `softmax(QKᵀ / sqrt(d_k))V`. Transformer ghép attention với mạng feed-forward, kết nối dư và thông tin vị trí; causal mask ngăn nhìn token tương lai trong mô hình sinh tự hồi quy. Xem bài gốc [Attention Is All You Need](https://arxiv.org/abs/1706.03762).
- **Nộp và đạt:** phép tính shape đúng, kiểm tra mask đạt; một sơ đồ encoder/decoder có chú thích vai trò vị trí, attention và feed-forward; không yêu cầu train Transformer lớn.
- **Tự kiểm 1:** bỏ causal mask khi học dự đoán token tiếp theo gây rò rỉ thông tin thế nào?
- **Tự kiểm 2:** trọng số attention cao có đủ để chứng minh nguyên nhân mô hình trả lời như vậy không?

### Thực hành tuần 29 — 3 nhiệm vụ

- **Cơ bản:** (B57) viết tokenizer khoảng trắng cho 12 câu tự tạo, có `PAD` và `UNK`; xây từ vựng chỉ từ train và mã hóa một câu có từ mới. (B58) dùng 3 token, mỗi vector 2 chiều; tính ma trận điểm và trọng số attention bằng NumPy hoặc PyTorch.
- **Ứng dụng:** (B57) tạo embedding dimension 8 và tính vector trung bình cho từng câu, loại padding khỏi mẫu số; kiểm tra câu rỗng và câu dài hơn giới hạn. (B58) thêm causal mask; kiểm tra mỗi hàng tổng gần 1 và trọng số ở vị trí tương lai bằng 0; vẽ heatmap trước/sau mask.
- **Mở rộng:** (B57) tải một tokenizer công khai, ghi tên và revision; so số token trên 5 câu tiếng Việt/tiếng Anh, giải thích sự khác biệt mà không suy diễn chất lượng mô hình. (B58) dựng một block attention nhỏ hoặc mô hình dự đoán ký tự trên 20 câu, tối đa 10 phút CPU; nêu rõ đây là mô hình đồ chơi.

## Tuần 30 — P04: Dự án phân loại ảnh nhỏ

### B59 — P04: Chốt phạm vi và tái lập thí nghiệm

**Đọc để hiểu bài:** [H02 — Batch, train/eval và checkpoint](../kien_thuc/04_deep_learning_he_thong_agent.md#h02); [H03 — MLP, CNN và attention](../kien_thuc/04_deep_learning_he_thong_agent.md#h03).

- **Mục tiêu:** biến bài CNN/MLP đã làm thành một dự án có dữ liệu, baseline và cách chạy rõ ràng.
- **Hiểu bản chất:** một dự án tốt cần câu hỏi cụ thể, dữ liệu đại diện và tiêu chí thành công trước khi tinh chỉnh. Trong P04, tác vụ bắt buộc là phân loại digits; triển khai trên ảnh tự chụp là miền khác và cần kiểm chứng riêng. Tận dụng model, split và vòng lặp B51–B55 để dành thời gian cho tính tái lập.
- **Nộp và đạt:** chạy lại được từ hướng dẫn; artifact có kiến trúc, tiền xử lý, nhãn và phiên bản; lưu kết quả baseline/ứng viên với cùng split, seed và thời gian.
- **Tự kiểm 1:** ảnh tự chụp bằng điện thoại có thể khác dữ liệu digits ở những yếu tố nào?
- **Tự kiểm 2:** tại sao accuracy của hai mô hình dùng hai split khác nhau khó so sánh công bằng?

### B60 — P04: Đánh giá, lỗi và bàn giao

**Đọc để hiểu bài:** [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10); [D09 — Mô hình tuyến tính và metric](../kien_thuc/02_du_lieu_toan_ml.md#d09).

- **Mục tiêu:** chứng minh mô hình hoạt động trên phạm vi đã định và mô tả trung thực phần còn yếu.
- **Hiểu bản chất:** một điểm accuracy che giấu các cặp nhãn thường nhầm. Confusion matrix và ví dụ lỗi cho thấy điều kiện thất bại, còn latency cho biết chi phí suy luận trên máy đang dùng. Điểm softmax lớn không tự là xác suất được hiệu chuẩn; không gọi nó là độ tin cậy đã bảo đảm.
- **Nộp và đạt:** báo accuracy, macro-F1 và confusion matrix trên split test đã khóa sau khi chốt cấu hình; model nạp lại dự đoán khớp; có 3 giới hạn và 1 kế hoạch sửa lỗi. Nghiệm thu quy trình và bằng chứng trung thực, không tiếp tục tinh chỉnh để ép điểm test đạt một ngưỡng tùy ý.
- **Tự kiểm 1:** nếu tất cả lỗi tập trung ở một lớp hiếm, accuracy chung có thể gây hiểu nhầm ra sao?
- **Tự kiểm 2:** vì sao benchmark lần chạy đầu có thể khác các lần chạy sau?

### Thực hành tuần 30 — 3 nhiệm vụ

- **Cơ bản:** (B59) viết bản mô tả một trang: người dùng, đầu vào ảnh 8 × 8, 10 nhãn, giới hạn và metric chính; kiểm tra lại split cố định. (B60) đánh giá checkpoint đã chọn trên test một lần; xuất accuracy, macro-F1, confusion matrix và 10 dự đoán sai hoặc toàn bộ lỗi nếu ít hơn.
- **Ứng dụng:** (B59) gom cấu hình, train và evaluate thành lệnh độc lập; chạy một baseline và một ứng viên, chọn bằng validation; chỉ mở test sau khi chốt. (B60) viết hàm dự đoán nhận batch, kiểm tra shape/miền giá trị; đo thời gian sau 5 lượt khởi động; hoàn thiện README và bản demo CLI.
- **Mở rộng:** (B59) thêm một bản dữ liệu nhiễu có phiên bản để đánh giá phụ; không thay tiêu chí lựa chọn bằng điểm test mới thấy. (B60) thử ngưỡng từ chối theo điểm dự đoán chọn bằng validation và báo tỉ lệ bao phủ cùng độ chính xác trên phần được trả lời.

## Tuần 31 — Gọi mô hình ngôn ngữ như một thành phần phần mềm

### B61 — Prompt, ngữ cảnh và định dạng đầu ra

**Đọc để hiểu bài:** [R01 — LLM và tokenization](../kien_thuc/03_llm_rag.md#r01); [R02 — Prompt và ranh giới dữ liệu](../kien_thuc/03_llm_rag.md#r02).

- **Mục tiêu:** mô tả nhiệm vụ rõ ràng, quản lý ngữ cảnh và đánh giá prompt bằng dữ liệu.
- **Hiểu bản chất:** mô hình sinh chuỗi token theo ngữ cảnh được cung cấp; câu văn trôi chảy không bảo đảm sự thật. Prompt nên nêu nhiệm vụ, dữ liệu, ràng buộc và ví dụ đầu ra; giới hạn ngữ cảnh tính cả các phần cần gửi theo quy ước provider. JSON hợp lệ về cú pháp vẫn có thể sai nội dung hoặc thiếu bằng chứng.
- **Nộp và đạt:** có prompt, dữ liệu và bộ chấm bắt được 4 kiểu lỗi chủ đích; chỉ kết luận prompt nào tốt hơn nếu đã có đầu ra thực từ mô hình thật.
- **Tự kiểm 1:** yêu cầu “hãy chắc chắn” trong prompt có tự loại bỏ thông tin bịa không?
- **Tự kiểm 2:** vì sao đổi ví dụ đánh giá sau mỗi lần sửa prompt làm kết luận khó tin cậy?

### B62 — Provider abstraction, timeout và đầu ra có cấu trúc

**Đọc để hiểu bài:** [R03 — Provider, HTTP và schema](../kien_thuc/03_llm_rag.md#r03); [H04 — API và vòng đời model](../kien_thuc/04_deep_learning_he_thong_agent.md#h04); [H08 — Timeout, retry và idempotency](../kien_thuc/04_deep_learning_he_thong_agent.md#h08).

- **Mục tiêu:** thay được provider mà không sửa logic nghiệp vụ; kiểm thử lỗi ngoài mạng.
- **Hiểu bản chất:** giao diện provider định nghĩa đầu vào/đầu ra chung, còn adapter chuyển sang định dạng của dịch vụ hoặc mô hình cục bộ. Fake provider giúp tạo timeout và JSON lỗi một cách lặp lại được; nó kiểm tra phần mềm bao quanh mô hình. Retry cần giới hạn và chỉ dành cho lỗi tạm thời, tránh lặp vô hạn hoặc nhân chi phí.
- **Nộp và đạt:** thay fake provider qua tham số hoặc cấu hình; 6 test đạt; JSON sai có lỗi rõ, timeout dừng hữu hạn; không cần API trả phí để hoàn thành phần kỹ thuật.
- **Tự kiểm 1:** vì sao JSON hợp lệ nhưng sai schema không nhất thiết nên được retry giống lỗi kết nối?
- **Tự kiểm 2:** nếu fake provider luôn trả đúng đáp án, bộ test đã chứng minh điều gì và chưa chứng minh điều gì?

### Thực hành tuần 31 — 3 nhiệm vụ

- **Cơ bản:** (B61) viết hai prompt trích xuất `ten_khoa_hoc`, `thoi_luong_gio` từ 6 mô tả tự tạo; quy định `null` khi thiếu thông tin thay vì yêu cầu đoán. (B62) định nghĩa `GenerationResult` gồm `text`, `model_id`, `usage` có thể thiếu, và `latency_ms`; tạo fake provider có ba kịch bản thành công/timeout/JSON sai.
- **Ứng dụng:** (B61) tạo 12 ví dụ gồm đủ/thiếu/nhiễu thông tin và đáp án; viết bộ kiểm tra schema, kiểu dữ liệu và đúng giá trị trên các đầu ra mẫu tốt/xấu. (B62) thêm parser và schema validation; tối đa 2 lần thử lại cho lỗi tạm thời, có khoảng chờ tăng dần và tổng thời gian tối đa; viết 6 ca kiểm tra luồng.
- **Mở rộng:** (B61) chạy hai prompt trên mô hình thật phù hợp máy; giữ cùng 12 ví dụ, cấu hình sinh và phiên bản, ghi số lỗi và ví dụ sai. (B62) nối adapter tới mô hình cục bộ hoặc dịch vụ tự chọn; lấy cấu hình từ biến môi trường, ghi phiên bản và usage thực khi provider cung cấp.

## Tuần 32 — Tìm kiếm tài liệu trước khi sinh câu trả lời

### B63 — Tìm kiếm sparse/dense và cosine similarity

**Đọc để hiểu bài:** [R07 — Lexical, TF-IDF và BM25](../kien_thuc/03_llm_rag.md#r07); [R08 — Embedding và cosine](../kien_thuc/03_llm_rag.md#r08).

- **Mục tiêu:** dựng baseline tìm kiếm có thể đo, phân biệt vector từ vựng với embedding ngữ nghĩa.
- **Hiểu bản chất:** TF-IDF biểu diễn trọng số từ trong tài liệu; tìm kiếm sparse thường mạnh với thuật ngữ xuất hiện trực tiếp. Embedding từ mô hình đã học có thể hỗ trợ cách diễn đạt tương đương, nhưng vẫn có thể bỏ sót số hiệu hoặc tên hiếm. Cosine đo góc giữa vector; vector zero cần quy ước xử lý riêng, không chia trực tiếp cho 0.
- **Nộp và đạt:** lưu corpus, câu hỏi, nhãn và bảng top-3; hit-rate@3 ít nhất `0.70` trên 10 câu đã định; vector zero không gây NaN; nếu chưa chạy dense, ghi giới hạn so sánh.
- **Tự kiểm 1:** vì sao truy vấn chứa đúng mã lỗi có thể phù hợp tìm kiếm sparse?
- **Tự kiểm 2:** tại sao điểm cosine `0.8` không tự có nghĩa là xác suất câu trả lời đúng bằng 80%?

### B64 — Chunking, metadata và truy xuất nguồn

**Đọc để hiểu bài:** [R05 — Ingestion và nguồn gốc](../kien_thuc/03_llm_rag.md#r05); [R06 — Chunking và overlap](../kien_thuc/03_llm_rag.md#r06).

- **Mục tiêu:** cắt tài liệu thành đoạn có thể tìm kiếm và giữ được quan hệ với nguồn gốc.
- **Hiểu bản chất:** chunk nhỏ giúp tìm đúng phần liên quan nhưng có thể làm mất định nghĩa xung quanh; chunk lớn giữ ngữ cảnh nhưng chiếm nhiều chỗ trong prompt. Overlap giảm đứt câu đổi lại trùng lặp. Pipeline RAG đưa nội dung tìm được vào ngữ cảnh sinh; bản thân tìm kiếm không bảo đảm câu trả lời có căn cứ. Đọc bài gốc [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401).
- **Nộp và đạt:** mọi chunk truy ngược được đoạn nguồn; 10 kết quả có nguồn kiểm tra được; bản ghi so sánh hai cách cắt và context không vượt ngân sách đã chọn.
- **Tự kiểm 1:** cắt đúng giữa câu chứa điều kiện và câu chứa ngoại lệ có thể gây lỗi trả lời thế nào?
- **Tự kiểm 2:** vì sao tên file đơn lẻ đôi khi chưa đủ để làm trích dẫn có thể kiểm tra?

### Thực hành tuần 32 — 3 nhiệm vụ

- **Cơ bản:** (B63) gom 20 tài liệu ngắn về Python từ ghi chú tự viết các tuần trước, mỗi tài liệu có ID; dùng TF-IDF và cosine trả top-3 cho 10 câu hỏi có tài liệu đúng đã gán nhãn. (B64) giữ corpus 20 tài liệu B63, chọn hoặc bổ sung ghi chú để ít nhất 5 tài liệu dài 300–600 từ; cắt theo đoạn, lưu `doc_id`, `chunk_id`, tiêu đề và vị trí nguồn.
- **Ứng dụng:** (B63) tính hit-rate@3: số câu hỏi có ít nhất một tài liệu đúng trong top-3 chia tổng số câu hỏi; thêm 3 câu hỏi không có từ vựng phù hợp. (B64) so chunk khoảng 100 và 200 từ trên cùng 10 câu hỏi; gom top-3, loại trùng và dựng context có nhãn nguồn, ngân sách rõ ràng.
- **Mở rộng:** (B63) dùng mô hình embedding nhỏ trên CPU cho đúng tập này; so truy vấn dùng từ đồng nghĩa, từ khóa chính xác và tiếng Việt; không gọi vector ngẫu nhiên là embedding ngữ nghĩa đã học. (B64) đổi giới hạn từ sang token bằng tokenizer thật; bổ sung cập nhật/xóa một tài liệu và kiểm tra index không giữ đoạn cũ.

## Tuần 33 — Đánh giá RAG và ranh giới tin cậy

### B65 — Golden set và đánh giá từng tầng

**Đọc để hiểu bài:** [R12 — Đánh giá, ablation và LoRA](../kien_thuc/03_llm_rag.md#r12); [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10).

- **Mục tiêu:** tách lỗi tìm kiếm, lỗi sinh và lỗi dẫn nguồn; tránh tự chấm theo cảm giác.
- **Hiểu bản chất:** golden set là bộ câu hỏi có đáp án tham chiếu và bằng chứng do người kiểm tra. Retrieval tốt nhưng câu trả lời sai cần sửa phần sinh; retrieval bỏ sót bằng chứng cần sửa dữ liệu hoặc tìm kiếm. Dùng tập dev để chỉnh và tập test giữ riêng để báo cáo; bộ dữ liệu rất nhỏ chỉ cho bằng chứng ban đầu.
- **Nộp và đạt:** đủ 40 câu, split được lưu và script chấm retrieval chạy được; báo số mẫu cạnh mỗi tỉ lệ. Không chạy mô hình thật thì để metric sinh là `N/A`, không điền điểm fake; hoàn tất đánh giá sinh ở P05.
- **Tự kiểm 1:** retrieval hit-rate tốt nhưng câu trả lời bịa thêm chi tiết gợi ý kiểm tra phần nào?
- **Tự kiểm 2:** vì sao báo “90% chính xác” mà không ghi số câu, cách chấm và loại câu là chưa đủ?

### B66 — Không đủ bằng chứng, prompt injection và dữ liệu không đáng tin

**Đọc để hiểu bài:** [R02 — Prompt và ranh giới dữ liệu](../kien_thuc/03_llm_rag.md#r02); [R11 — RAG và kiểm bằng chứng](../kien_thuc/03_llm_rag.md#r11); [H09 — Phân quyền và prompt injection](../kien_thuc/04_deep_learning_he_thong_agent.md#h09).

- **Mục tiêu:** tạo hành vi từ chối hợp lý và không cho tài liệu tự biến thành quyền điều khiển.
- **Hiểu bản chất:** nội dung truy xuất có thể chứa câu giống chỉ thị, chẳng hạn yêu cầu bỏ qua nhiệm vụ hoặc tiết lộ cấu hình. Phải coi nó là dữ liệu cần đọc, giữ kiểm soát công cụ và quyền truy cập trong mã ứng dụng. Phân tách prompt và lọc nội dung chỉ là một lớp phòng vệ; không bảo đảm miễn nhiễm prompt injection. Tham khảo [hướng dẫn OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).
- **Nộp và đạt:** 6 test ràng buộc ứng dụng đạt, mọi citation giả bị phát hiện; báo rõ quy tắc nào cứng trong mã và hành vi nào chỉ được kỳ vọng ở mô hình.
- **Tự kiểm 1:** vì sao bọc tài liệu trong dấu phân cách chưa đủ để coi prompt injection đã được giải quyết?
- **Tự kiểm 2:** một câu trả lời có citation tồn tại vẫn có thể thiếu căn cứ ở điểm nào?

### Thực hành tuần 33 — 3 nhiệm vụ

- **Cơ bản:** (B65) soạn 40 câu: 20 câu có đáp án, 10 câu ngoài corpus và 10 câu gây nhiễu/trích dẫn sai/chỉ dẫn trong tài liệu; mỗi câu có loại, đáp án hoặc lý do không trả lời, ID bằng chứng. (B66) tạo 6 tài liệu thử có chỉ thị giả, nguồn thiếu, nội dung mâu thuẫn hoặc không liên quan để dùng trong nhóm gây nhiễu; xác định phản hồi mong muốn cho từng ca.
- **Ứng dụng:** (B65) chia 20 dev/20 test trước khi tinh chỉnh, mỗi tập có 10 câu có đáp án, 5 ngoài phạm vi và 5 gây nhiễu; chấm Recall@3 bằng số ID nguồn đúng tìm được chia tổng ID nguồn đúng của từng câu có bằng chứng, rồi lấy trung bình. Nếu mỗi câu chỉ có một nguồn đúng, Recall@3 tương đương hit-rate@3. (B66) chỉ chấp nhận citation ID có trong context; không có bằng chứng thì trả trạng thái `insufficient_evidence`; kiểm thử mã ứng dụng không thực thi lệnh từ tài liệu và không đưa secret vào context.
- **Mở rộng:** (B65) chạy mô hình thật trên tập test đã khóa; chấm từng câu theo rubric 0/1, đếm riêng từng nhóm; nhờ người thứ hai chấm 5 câu nếu có điều kiện. (B66) thử 6 ca với mô hình thật, ghi cả thành công lẫn thất bại; xem xét nguồn đáng tin, quyền đọc theo người dùng và xử lý tài liệu mâu thuẫn.

## Tuần 34 — Tools và vòng lặp agent có giới hạn

### B67 — Tool schema và điều phối có kiểm soát

**Đọc để hiểu bài:** [H06 — Hợp đồng và thực thi tool](../kien_thuc/04_deep_learning_he_thong_agent.md#h06); [H07 — Workflow, agent và state](../kien_thuc/04_deep_learning_he_thong_agent.md#h07).

- **Mục tiêu:** cho mô hình đề xuất gọi công cụ qua hợp đồng dữ liệu rõ ràng.
- **Hiểu bản chất:** tool call là yêu cầu có tên công cụ và đối số, không tự là hành động được phép. Ứng dụng kiểm tra schema, danh sách công cụ và quyền trước khi chạy. Workflow cố định dễ dự đoán cho quy trình đã biết; agent phù hợp khi cần chọn bước tiếp theo, nhưng tạo thêm trạng thái và khả năng thất bại.
- **Nộp và đạt:** 8 test gồm tên tool lạ, `top_k` quá lớn, ID không tồn tại, sai kiểu và chuỗi thành công; công cụ ngoài danh sách không được chạy.
- **Tự kiểm 1:** vì sao không nên chuyển nguyên chuỗi mô hình sinh thành câu lệnh shell hoặc Python để thực thi?
- **Tự kiểm 2:** khi chỉ cần tìm tài liệu rồi tóm tắt, lợi ích của workflow cố định là gì?

### B68 — Giới hạn vòng lặp, timeout và xác nhận tác động

**Đọc để hiểu bài:** [H07 — Workflow, agent và state](../kien_thuc/04_deep_learning_he_thong_agent.md#h07); [H08 — Timeout, retry và idempotency](../kien_thuc/04_deep_learning_he_thong_agent.md#h08); [H09 — Phân quyền và prompt injection](../kien_thuc/04_deep_learning_he_thong_agent.md#h09).

- **Mục tiêu:** dừng tác vụ lỗi hữu hạn và ngăn hành động có tác động diễn ra ngoài ý định người dùng.
- **Hiểu bản chất:** agent có thể lặp lại tool, đi sai hướng hoặc chờ mãi; giới hạn bước, thời gian và lượng đầu vào/đầu ra giúp kiểm soát. Hành động ghi hoặc gửi cần chính sách riêng, đối chiếu với yêu cầu người dùng và xác nhận cụ thể khi chưa được cho phép. Retry hành động ghi còn có nguy cơ tạo bản ghi trùng.
- **Nộp và đạt:** mọi luồng giả lập dừng trong giới hạn có dung sai nhỏ của bộ đo; chưa xác nhận thì không có file mới; retry cùng request ID chỉ tạo một kết quả.
- **Tự kiểm 1:** chỉ giới hạn số bước có ngăn được một tool chờ vô hạn không?
- **Tự kiểm 2:** vì sao xác nhận “ghi ghi chú A” không đủ để cho phép agent đổi nội dung thành B rồi ghi?

### Thực hành tuần 34 — 3 nhiệm vụ

- **Cơ bản:** (B67) định nghĩa hai tool chỉ đọc: `search_docs(query, top_k)` và `get_doc(doc_id)`; quy định kiểu, giới hạn và lỗi rõ ràng. (B68) đặt tối đa 4 lần gọi tool và tổng deadline 5 giây cho bản fake; tạo kịch bản lặp cùng truy vấn, tool chậm và lỗi liên tiếp.
- **Ứng dụng:** (B67) dùng fake provider đề xuất chuỗi search → get_doc → answer; bộ điều phối chỉ cho phép tool đã đăng ký, kiểm tra đối số trước khi gọi. (B68) thêm tool mô phỏng `save_note` chỉ ghi trong thư mục bài học; tạo bản xem trước với đối số cố định, chỉ thực thi sau tín hiệu xác nhận hợp lệ; dùng request ID chống ghi trùng.
- **Mở rộng:** (B67) thêm tool tính tổng trên danh sách số dùng hàm Python riêng; tránh thực thi biểu thức tùy ý bằng `eval`. (B68) thêm trạng thái hủy, trace từng bước và ngân sách usage khi provider cung cấp; kiểm tra thay đối số sau xác nhận bị từ chối.

## Tuần 35 — Chọn prompting, RAG hay fine-tuning

### B69 — Quyết định thích nghi mô hình bằng bằng chứng

**Đọc để hiểu bài:** [R11 — RAG và kiểm bằng chứng](../kien_thuc/03_llm_rag.md#r11); [R12 — Đánh giá, ablation và LoRA](../kien_thuc/03_llm_rag.md#r12).

- **Mục tiêu:** chọn phương pháp theo loại lỗi, tài nguyên và tính cập nhật của dữ liệu.
- **Hiểu bản chất:** prompt thay cách đặt nhiệm vụ; RAG đưa tri thức bên ngoài vào ngữ cảnh; fine-tuning thay trọng số để học hành vi từ ví dụ. Tài liệu thay đổi thường xuyên thường cần cơ chế cập nhật nguồn hơn là chỉ học lại trọng số. Không phương pháp nào tự bảo đảm sự thật; chất lượng dữ liệu, đánh giá và chi phí vẫn quyết định.
- **Nộp và đạt:** bảng quyết định 6 tình huống có lý do và phép thử; 5 lỗi có phân tích; nếu chưa chạy mô hình thật, đánh dấu so sánh chất lượng sinh là chưa thực hiện.
- **Tự kiểm 1:** nếu câu trả lời sai vì chunk cần thiết không được truy xuất, fine-tuning có trực tiếp sửa đúng điểm nghẽn không?
- **Tự kiểm 2:** vì sao có 50 ví dụ đẹp chưa đủ để kết luận nên fine-tune một mô hình lớn?

### B70 — LoRA qua một thí nghiệm ma trận nhỏ

**Đọc để hiểu bài:** [R12 — Đánh giá, ablation và LoRA](../kien_thuc/03_llm_rag.md#r12); [H01 — Tensor và autograd](../kien_thuc/04_deep_learning_he_thong_agent.md#h01).

- **Mục tiêu:** hiểu cập nhật hạng thấp và phân biệt thí nghiệm khái niệm với fine-tuning LLM thật.
- **Hiểu bản chất:** LoRA giữ trọng số gốc cố định và học phần cập nhật dạng tích hai ma trận nhỏ `ΔW = B A`, thường kèm hệ số tỉ lệ. Với `W` kích thước `d_out × d_in`, rank `r` cần khoảng `r(d_in+d_out)` tham số cập nhật thay cho `d_out*d_in`. Điều này giảm tham số học nhưng không xóa chi phí lưu/chạy mô hình nền. Xem [bài báo LoRA](https://arxiv.org/abs/2106.09685).
- **Nộp và đạt:** thí nghiệm CPU loss giảm ít nhất 50% so ban đầu, kiểm tra số tham số và trọng số gốc; được tính đạt khái niệm LoRA, không ghi là đã fine-tune LLM nếu chưa làm phần đó.
- **Tự kiểm 1:** rank tăng ảnh hưởng khả năng biểu diễn phần cập nhật và số tham số thế nào?
- **Tự kiểm 2:** tại sao adapter rất nhỏ vẫn có thể cần nhiều bộ nhớ khi chạy kèm mô hình nền?

### Thực hành tuần 35 — 3 nhiệm vụ

- **Cơ bản:** (B69) phân loại 6 tình huống: định dạng sai, thiếu kiến thức mới, phong cách không ổn định, retrieval sai, nhãn nghiệp vụ đặc thù và tài liệu cần trích dẫn. (B70) cho `W` 16 × 16 và rank 2, tính số tham số; khởi tạo một ma trận adapter ngẫu nhiên và ma trận còn lại bằng 0, giải thích vì sao không đặt cả hai bằng 0.
- **Ứng dụng:** (B69) lấy 5 lỗi từ golden set, nêu giả thuyết nguyên nhân và một can thiệp nhỏ; chạy lại retrieval hoặc bộ kiểm schema để kiểm tra phần đo được trên CPU. (B70) tạo bài toán tuyến tính đồ chơi có phần thay đổi hạng 2; đóng băng `W`, học adapter trên 100 mẫu CPU; kiểm tra `W` không đổi và loss giảm.
- **Mở rộng:** (B69) dùng mô hình thật so prompt cơ sở và prompt có retrieval trên 10 câu dev; giữ cấu hình sinh và báo cả chất lượng lẫn thời gian. (B70) fine-tune adapter cho mô hình nhỏ phù hợp phần cứng với dữ liệu có giấy phép, train/validation tách riêng; ghi tên model, phần module được gắn adapter và metric trước/sau.

## Tuần 36 — P05: Trợ lý tra cứu tài liệu có bằng chứng

### B71 — P05: Tích hợp pipeline RAG

**Đọc để hiểu bài:** [R11 — RAG và kiểm bằng chứng](../kien_thuc/03_llm_rag.md#r11); [R09 — Hybrid và RRF](../kien_thuc/03_llm_rag.md#r09); [R10 — Reranker](../kien_thuc/03_llm_rag.md#r10).

- **Mục tiêu:** ghép corpus, chunking, retrieval, provider và kiểm tra đầu ra thành một ứng dụng nhỏ.
- **Hiểu bản chất:** RAG là chuỗi nhiều thành phần; cần biết corpus nào, index nào và prompt nào đã tạo ra một kết quả. Tái dùng B62–B66 giúp việc tích hợp tập trung vào hợp đồng dữ liệu. Mặc định bài dự án chỉ tra cứu tài liệu học Python; công cụ ghi của tuần 34 là phần tự chọn.
- **Nộp và đạt:** index tái tạo được, cùng dữ liệu cho cùng tập chunk ID; 8 test tích hợp đạt; citation kiểm tra được trong context, mode luôn xuất hiện; CPU + fake đủ nghiệm thu tích hợp.
- **Tự kiểm 1:** vì sao cùng prompt nhưng index đã đổi vẫn có thể làm câu trả lời thay đổi?
- **Tự kiểm 2:** đâu là khác biệt người xem demo phải biết giữa mode fake và mode mô hình thật?

### B72 — P05: Nghiệm thu và báo cáo giới hạn

**Đọc để hiểu bài:** [R12 — Đánh giá, ablation và LoRA](../kien_thuc/03_llm_rag.md#r12); [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10).

- **Mục tiêu:** bàn giao bằng số đo và ca lỗi, không chỉ bằng một câu hỏi demo đẹp.
- **Hiểu bản chất:** chất lượng tìm kiếm, tính đúng của phần mềm và chất lượng sinh là ba bằng chứng khác nhau. Một pipeline mô phỏng đầy đủ là sản phẩm học tập có ích, nhưng chưa chứng minh trợ lý trả lời thực tế tốt. Báo cáo phải cho người đọc thấy phần nào đã đo, phần nào chưa và cách đo tiếp.
- **Nộp và đạt:** test phần mềm đạt, báo Recall@3 trên các câu test có bằng chứng và bảng chấm 20 đầu ra thật theo tính đúng/căn cứ/từ chối; có kế hoạch sửa lỗi. Nếu chưa chạy model thật, metric sinh là `N/A` và P05 ở trạng thái “đạt tích hợp, chưa hoàn thành nghiệm thu sinh”; có thể học tiếp API bằng P03 trong khi bổ sung phần này.
- **Tự kiểm 1:** vì sao retrieval đạt ngưỡng mà chưa có mô hình thật thì chưa thể tuyên bố trợ lý đạt 70% câu trả lời đúng?
- **Tự kiểm 2:** hai lỗi nào trong báo cáo cần sửa bằng ứng dụng, hai lỗi nào có thể cần thay dữ liệu hoặc mô hình?

### Thực hành tuần 36 — 3 nhiệm vụ

- **Cơ bản:** (B71) tạo lệnh index và lệnh hỏi cho 20 tài liệu B64, có thể mở rộng tới 50 nếu còn thời gian; đầu ra gồm `answer`, `citations`, `status`, `mode` và phiên bản corpus/index. (B72) chạy bộ test giữ riêng B65 cho retrieval và bộ test lỗi B66/B71; xuất kết quả theo từng câu cùng bằng chứng nguồn; viết hướng dẫn chạy từ corpus gốc.
- **Ứng dụng:** (B71) tích hợp provider có thể thay thế; mode fake gắn nhãn rõ “mô phỏng”; thêm đường đi không có kết quả, nguồn không hợp lệ và provider timeout. (B72) đánh giá mô hình thật trên 20 câu test theo rubric 0/1 cho đúng nội dung, căn cứ và từ chối phù hợp; báo Recall@3, số lỗi schema/citation, latency, 5 ca lỗi và model/revision/cấu hình. CPU với model nhỏ là lựa chọn, không yêu cầu API trả phí.
- **Mở rộng:** (B71) nối mô hình thật nhỏ chạy cục bộ, giới hạn câu trả lời ngắn và context; đo thời gian trên 5 câu trước khi chạy toàn bộ đánh giá. (B72) thêm 10 câu kiểm tra độc lập hoặc nhờ người thứ hai chấm; nếu cải tiến sau khi xem test thì báo bộ test đó đã trở thành dữ liệu phát triển và giữ riêng bộ kiểm tra mới.

## Tuần 37 — Biến mô hình thành API

### B73 — FastAPI, schema và vòng đời model

**Đọc để hiểu bài:** [H04 — API và vòng đời model](../kien_thuc/04_deep_learning_he_thong_agent.md#h04); [H11 — Artifact, Docker và CI](../kien_thuc/04_deep_learning_he_thong_agent.md#h11).

- **Mục tiêu:** bọc P03 hoặc P05 thành API có đầu vào/đầu ra rõ ràng.
- **Hiểu bản chất:** API là hợp đồng giữa bên gọi và ứng dụng; schema bắt lỗi sớm trước khi dữ liệu tới mô hình. Nạp model/index một lần trong vòng đời ứng dụng tránh lặp công việc nặng ở mỗi request. Hàm dự đoán nên dùng chung cho CLI và API để giảm sai khác tiền xử lý. Học theo [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/).
- **Nộp và đạt:** API chạy tại `127.0.0.1`, tài liệu tương tác mở được; 6 request mẫu có kết quả/trạng thái mong đợi; loader chạy một lần cho mỗi tiến trình ứng dụng.
- **Tự kiểm 1:** vì sao không nên huấn luyện lại mô hình trong endpoint dự đoán?
- **Tự kiểm 2:** nếu CLI và API chuẩn hóa dữ liệu khác nhau, kiểm tra tích hợp nào phát hiện được?

### B74 — Kiểm thử API, đồng thời và xử lý lỗi

**Đọc để hiểu bài:** [H05 — Async và giới hạn đồng thời](../kien_thuc/04_deep_learning_he_thong_agent.md#h05); [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10).

- **Mục tiêu:** kiểm thử hợp đồng API và tránh làm nghẽn ứng dụng vì hiểu sai async.
- **Hiểu bản chất:** async phối hợp khi chờ I/O có hỗ trợ bất đồng bộ; tác vụ CPU chạy trực tiếp trong coroutine sẽ chặn event loop. Thread hữu ích để đưa lời gọi I/O đồng bộ ra ngoài vòng lặp; process có không gian bộ nhớ riêng và phù hợp cho nhiều tác vụ Python CPU, đổi lại chi phí truyền dữ liệu. Một số thư viện số giải phóng GIL nên phải đo thay vì áp dụng máy móc; giới hạn số tác vụ đang chạy để tránh quá tải. TestClient kiểm tra route/schema mà không mở cổng. Đọc [FastAPI về async](https://fastapi.tiangolo.com/async/) và [Testing](https://fastapi.tiangolo.com/tutorial/testing/).
- **Lưu ý khi áp dụng:** timeout của bên chờ không luôn dừng công việc đồng bộ đang chạy trong thread; dùng timeout ở chính thư viện I/O và cơ chế hủy phù hợp. Với process trên Windows, đặt điểm khởi chạy dưới `if __name__ == "__main__":`; đọc [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) và [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html).
- **Nộp và đạt:** 6 test đạt, client nhận lỗi có cấu trúc; không trả stack trace/secret trong phản hồi; giải thích được tác vụ nào chờ I/O và tác vụ nào dùng CPU.
- **Tự kiểm 1:** thêm `async` trước hàm nhân ma trận lớn có làm phép tính chạy nhanh hơn không?
- **Tự kiểm 2:** vì sao test route bằng fake model cần bổ sung ít nhất một test với artifact thật nếu API phục vụ P03?

### Thực hành tuần 37 — 3 nhiệm vụ

- **Cơ bản:** (B73) chọn P03 để có dự đoán mô hình thật nhẹ hoặc P05 để có tra cứu; tạo `/health` và `/predict` hoặc `/ask`, định nghĩa schema có giới hạn kích thước. (B74) viết 6 test API: hợp lệ, thiếu trường, sai kiểu, đầu vào quá dài, dịch vụ lỗi và kiểm tra phiên bản; inject fake dependency khi cần tái hiện lỗi.
- **Ứng dụng:** (B73) dùng lớp dịch vụ gọi mã dự án cũ; trả phiên bản model/index và request ID; chạy localhost, thử request hợp lệ, thiếu trường và sai kiểu bằng script Python. (B74) thêm timeout tổng ở lời gọi provider, trả lỗi có mã và request ID; dùng semaphore giới hạn 5 request đồng thời, đo thời gian; thử `asyncio.sleep` và tác vụ CPU nhỏ để quan sát khả năng đáp ứng khác nhau.
- **Mở rộng:** (B73) thêm batch tối đa 16 mẫu hoặc truy xuất metadata; quy định giới hạn payload và cách báo lỗi cho client. (B74) thiết kế hàng đợi cho tác vụ CPU dài, mô phỏng quá tải bằng giới hạn số tác vụ đang chạy; không bắt buộc cài hệ thống phân tán.

## Tuần 38 — Đóng gói, cấu hình và tự động kiểm tra

### B75 — Docker và môi trường chạy tái tạo được

**Đọc để hiểu bài:** [H11 — Artifact, Docker và CI](../kien_thuc/04_deep_learning_he_thong_agent.md#h11).

- **Mục tiêu:** đóng gói API cùng phụ thuộc để chạy localhost theo một hướng dẫn cố định.
- **Hiểu bản chất:** image mô tả môi trường ứng dụng, container là một lần chạy image; dữ liệu thay đổi cần được đặt rõ ở volume hoặc vị trí lưu có quản lý. Docker không bảo đảm kết quả số học giống hệt trên mọi phần cứng. Chọn base image phù hợp, khóa phụ thuộc và tránh đưa dữ liệu không cần thiết vào build context. Xem [Docker Get Started](https://docs.docker.com/get-started/) và [build practices](https://docs.docker.com/build/building/best-practices/).
- **Nộp và đạt:** có log build và hai HTTP response thật; xóa container rồi tạo lại vẫn chạy từ hướng dẫn. Nếu máy chưa hỗ trợ Docker, nộp Dockerfile và thử môi trường ảo sạch, đánh dấu “chưa nghiệm thu container” và hoàn tất khi có môi trường phù hợp.
- **Tự kiểm 1:** file ghi chỉ trong filesystem của container có thể mất khi nào?
- **Tự kiểm 2:** vì sao không nên đưa API key vào Dockerfile hoặc commit file chứa khóa?

### B76 — Config, logging, secrets và CI

**Đọc để hiểu bài:** [H11 — Artifact, Docker và CI](../kien_thuc/04_deep_learning_he_thong_agent.md#h11); [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10); [H09 — Phân quyền và prompt injection](../kien_thuc/04_deep_learning_he_thong_agent.md#h09).

- **Mục tiêu:** tách cấu hình khỏi mã và tạo quy trình kiểm tra tự động, không cần dịch vụ trả phí.
- **Hiểu bản chất:** cấu hình quyết định model, đường dẫn và giới hạn chạy; secret cần truyền lúc chạy và tránh xuất ra log. Log có cấu trúc giúp nối các bước theo request ID, nhưng không mặc định ghi toàn bộ câu hỏi/tài liệu của người dùng. CI thực hiện cùng lệnh kiểm tra trong môi trường sạch để phát hiện thay đổi phá vỡ hợp đồng.
- **Nộp và đạt:** một lệnh kiểm tra chạy đạt trên môi trường ảo sạch; cấu hình lỗi dừng sớm với thông báo rõ; sentinel không xuất hiện trong log. CI chưa chạy trên máy chủ phải được ghi là “đã cấu hình, chưa chạy từ xa”.
- **Tự kiểm 1:** vì sao lưu `.env.example` khác lưu `.env` có khóa thật?
- **Tự kiểm 2:** một pipeline CI xanh dùng toàn fake provider còn thiếu bằng chứng nào về model thực tế?

### Thực hành tuần 38 — 3 nhiệm vụ

- **Cơ bản:** (B75) viết Dockerfile CPU cho API đã có; thêm `.dockerignore` cho môi trường ảo, cache, dữ liệu thừa và file secret; chạy bằng người dùng không đặc quyền khi khả thi. (B76) tạo `.env.example` chỉ chứa placeholder; xác thực cấu hình khi khởi động; log request ID, trạng thái, thời gian, phiên bản và loại lỗi.
- **Ứng dụng:** (B75) build, chạy container chỉ publish cổng vào localhost, gọi health và một dự đoán; mount artifact đã tạo để không huấn luyện hoặc tải model mỗi request. (B76) tạo script kiểm tra gồm format/lint phù hợp dự án, pytest và một smoke test; thêm cấu hình CI nếu dùng nền tảng có sẵn, dùng fake provider cho test tự động.
- **Mở rộng:** (B75) đo kích thước image, tối ưu lớp cache; thử thay phiên bản artifact bằng cấu hình mà không sửa mã ứng dụng. (B76) thêm quét secret bằng công cụ phù hợp hoặc kiểm tra fixture; giả lập secret bằng chuỗi sentinel để xác nhận log/response không chứa nó.

## Tuần 39 — Theo dõi, kiểm tra tải và quay lui

### B77 — Theo dõi chất lượng, drift, latency và chi phí

**Đọc để hiểu bài:** [H12 — Latency, chi phí và drift](../kien_thuc/04_deep_learning_he_thong_agent.md#h12); [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10).

- **Mục tiêu:** phân biệt hệ thống đang chạy với hệ thống đang trả kết quả hữu ích.
- **Hiểu bản chất:** request thành công về HTTP vẫn có thể trả dự đoán sai. Theo dõi vận hành gồm lỗi, latency và tài nguyên; theo dõi chất lượng cần nhãn hoặc mẫu được chấm. Data drift là thay đổi phân bố đầu vào; nó là tín hiệu kiểm tra, không tự chứng minh chất lượng giảm. Chi phí LLM cần usage thực và đơn giá có ngày hiệu lực nếu dùng dịch vụ.
- **Nộp và đạt:** báo cáo có latency p50/p95, lỗi dạng số đếm và phần trăm, hai histogram, 20 kết quả được chấm hoặc ghi rõ phần sinh chưa được đo; nêu một cảnh báo giả có thể xảy ra.
- **Tự kiểm 1:** phân bố đầu vào thay đổi nhưng nhãn dự đoán vẫn đúng có bắt buộc phải huấn luyện lại ngay không?
- **Tự kiểm 2:** tại sao latency trung bình thấp vẫn có thể đi kèm trải nghiệm tệ cho một nhóm request?

### B78 — Kiểm tra tải, ngân sách và rollback

**Đọc để hiểu bài:** [H12 — Latency, chi phí và drift](../kien_thuc/04_deep_learning_he_thong_agent.md#h12); [H11 — Artifact, Docker và CI](../kien_thuc/04_deep_learning_he_thong_agent.md#h11).

- **Mục tiêu:** đo giới hạn của dịch vụ trên máy đang dùng và khôi phục phiên bản ổn định.
- **Hiểu bản chất:** throughput là số request xử lý theo thời gian, latency là thời gian chờ của từng request; tăng đồng thời có thể cải thiện throughput rồi làm latency tăng mạnh khi tài nguyên bão hòa. Rollback cần cả mã và artifact tương thích, không chỉ đổi tên file model. Lần chạy nhỏ trên localhost là bằng chứng học tập, chưa đại diện lưu lượng thực tế.
- **Nộp và đạt:** có hai bảng benchmark và log rollback hoàn tất trong 5 phút trên localhost; sau quay lui, 5 request chuẩn đúng schema và đúng phiên bản mong muốn.
- **Tự kiểm 1:** throughput tăng nhưng p95 tăng gấp mười lần là đánh đổi gì đối với người dùng?
- **Tự kiểm 2:** nếu đổi model nhưng quên đổi tiền xử lý tương ứng, vì sao rollback vẫn có thể hỏng?

### Thực hành tuần 39 — 3 nhiệm vụ

- **Cơ bản:** (B77) ghi latency từng request, tỉ lệ lỗi và phiên bản; với P03 theo dõi phân bố một đặc trưng, với P05 theo dõi không tìm được bằng chứng và độ dài context. (B78) dùng script Python gửi 50 request ở mức đồng thời 1 rồi 5, giới hạn thời gian cả bài; ghi warm-up, payload, phần cứng, p50/p95 và lỗi.
- **Ứng dụng:** (B77) tạo hai batch đầu vào bình thường và bị dịch chuyển; vẽ histogram, đặt quy tắc cảnh báo có lý do; chấm thủ công 10 kết quả mỗi batch để đối chiếu. (B78) lưu hai phiên bản cấu hình/artifact; tạo một bản lỗi mô phỏng, dùng smoke test phát hiện rồi quay về bản tốt; xác nhận request mẫu hoạt động lại.
- **Mở rộng:** (B77) nếu có usage thật, tính chi phí 100 request theo đơn giá đã kiểm tra; nếu local/fake, báo thời gian và bộ nhớ, ghi chi phí API là không áp dụng. (B78) thêm giới hạn tác vụ đang chạy và phản hồi quá tải rõ ràng; so trước/sau trên cùng kịch bản, không gửi tải ra hệ thống không thuộc quyền mình quản lý.

## Tuần 40 — P06: Capstone và trình bày kỹ thuật

### B79 — P06: Tích hợp sản phẩm nhỏ có thể tái lập

**Đọc để hiểu bài:** [H11 — Artifact, Docker và CI](../kien_thuc/04_deep_learning_he_thong_agent.md#h11); [H04 — API và vòng đời model](../kien_thuc/04_deep_learning_he_thong_agent.md#h04); [H07 — Workflow, agent và state](../kien_thuc/04_deep_learning_he_thong_agent.md#h07).

- **Mục tiêu:** bàn giao một hệ thống AI xuyên suốt từ dữ liệu đến API và đánh giá.
- **Hiểu bản chất:** capstone chứng minh sự kết nối giữa các phần đã học. Chọn **một** hướng chính theo đề P06: phục vụ P03 hoặc trợ lý P05; dùng lại API, cấu hình, kiểm tra và giám sát tuần 37–39. Một phạm vi nhỏ được kiểm chứng tốt hữu ích hơn nhiều tính năng chưa đo; kết quả cần truy về dữ liệu và phiên bản.
- **Nộp và đạt:** một người khác hoặc chính mình trong môi trường sạch chạy được theo README; 3 kịch bản chuẩn và 3 lỗi có kiểm tra; Docker image chạy thật, CI thực hiện kiểm tra tự động; có phiên bản, giới hạn dữ liệu, metric và hướng dẫn quay lui theo đề P06.
- **Tự kiểm 1:** model card cần nói gì để người dùng không áp dụng model digits cho ảnh bất kỳ?
- **Tự kiểm 2:** những artifact nào cần đi cùng nhau để tái lập một kết quả P05?

### B80 — P06: Demo, phản biện và kế hoạch học tiếp

**Đọc để hiểu bài:** [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10); [H12 — Latency, chi phí và drift](../kien_thuc/04_deep_learning_he_thong_agent.md#h12).

- **Mục tiêu:** giải thích quyết định kỹ thuật bằng bằng chứng và nhận diện khoảng trống năng lực.
- **Hiểu bản chất:** đánh giá kỹ thuật không chỉ hỏi hệ thống chạy được hay không, mà còn hỏi vì sao chọn phương pháp, lỗi ở đâu và sửa thế nào khi yêu cầu thay đổi. Demo cần có một ca thành công, một ca thất bại được xử lý và một số đo tái lập được. Hoàn thành giáo trình là cột mốc học tập, chưa thay thế trải nghiệm vận hành hay yêu cầu tuyển dụng cụ thể.
- **Nộp và đạt:** demo chạy localhost, README và báo cáo thống nhất kết quả; chọn 2 khoảng trống để học tiếp. Docker chưa chạy thì P06 chưa hoàn thành; nếu chọn P05 thì phải có đánh giá sinh thật. GPU chưa thực hành là giới hạn nhánh nâng cao, không cản nghiệm thu bản CPU.
- **Tự kiểm 1:** nếu một metric đẹp chỉ xuất hiện sau nhiều lần tinh chỉnh trên test, nên mô tả lại bằng chứng và đánh giá tiếp thế nào?
- **Tự kiểm 2:** nếu được thêm một tuần, thay đổi nào giải quyết điểm yếu lớn nhất và sẽ đo bằng cách nào?

### Thực hành tuần 40 — 3 nhiệm vụ

- **Cơ bản:** (B79) vẽ sơ đồ dữ liệu → xử lý → model/retrieval → API → log/đánh giá; ghi yêu cầu chức năng, giới hạn đầu vào và tiêu chí từ dự án đã chọn. (B80) chuẩn bị demo 5–7 phút và báo cáo tối đa 3 trang: bài toán, dữ liệu, baseline, kiến trúc, metric, lỗi, giới hạn và bước tiếp theo.
- **Ứng dụng:** (B79) dựng từ môi trường ảo sạch, tái tạo artifact hoặc lấy artifact có mã băm đã ghi; chạy test, smoke test và đánh giá đã khóa; hoàn thiện README và model card/system card. (B80) tự trả lời 8 câu phản biện: leakage; metric; baseline; bottleneck; quyền dữ liệu; prompt injection nếu có; lỗi provider/model; rollback; dùng code hoặc kết quả thật làm bằng chứng.
- **Mở rộng:** (B79) thêm UI rất nhỏ hoặc Docker Compose khi thực sự cần nhiều dịch vụ; giao diện đồ họa và cloud không bắt buộc. (B80) thực hiện một cải tiến nhỏ trong 2 giờ với giả thuyết và số đo trước/sau trên dev; viết tóm tắt dự án cho hồ sơ và tổ chức review với bạn học nếu có.

## Gợi ý đối chiếu câu tự kiểm

Tự viết câu trả lời trước khi xem. Mỗi câu cần giải thích bằng lời của mình và một ví dụ từ bài làm; bảng này chỉ nêu ý chính, không thay việc chạy và sửa bài tập.

| Bài | Câu 1 — ý cần có | Câu 2 — ý cần có |
|---|---|---|
| B49 | Broadcasting mở hai trục thành bảng mọi cặp hiệu, không phải bốn hiệu theo hàng. | Reshape đổi cách nhóm phần tử; transpose hoán vị trục và thường đổi thứ tự đọc theo trục. |
| B50 | Gradient từ các lần backward được cộng vào thuộc tính `.grad` nếu chưa xóa. | Chỉ bật khi cần đạo hàm theo tensor đó; suy luận thông thường không cần đạo hàm đầu vào. |
| B51 | Lưu ID giúp kiểm tra trùng/rò rỉ và chống thay đổi thứ tự dữ liệu hay thuật toán chia. | Nút thắt có thể ở xử lý, bộ nhớ hoặc overhead process; cần đo trước. |
| B52 | Eval đổi hành vi lớp; no-grad/inference mode điều khiển việc ghi đồ thị gradient. | Phân bố đầu vào khác lúc học dù trọng số không đổi. |
| B53 | Cross-entropy của PyTorch nhận logits và đã kết hợp phép biến đổi cần thiết. | Kiểm tra optimizer step, learning rate và danh sách tham số trong optimizer. |
| B54 | Cả hai kém: thiếu học, đặc trưng yếu hoặc lỗi; train tốt/val kém: quá khớp hoặc lệch phân bố. | Test đã tham gia quyết định nên không còn là phép đo độc lập. |
| B55 | Padding thay số vị trí bộ lọc và cách xử lý biên; chọn theo shape cần thiết. | Dữ liệu nhỏ, kiến trúc và ngân sách tối ưu có thể thuận lợi cho MLP. |
| B56 | Chưa có biểu diễn học từ nhiệm vụ trước để chuyển giao. | Không đủ: running mean/variance là buffer; phải kiểm soát chế độ của backbone. |
| B57 | ID là nhãn tra cứu, không biểu diễn khoảng cách ý nghĩa. | Padding làm sai cả tổng hoặc mẫu số, đặc biệt ở câu ngắn. |
| B58 | Mô hình nhìn thấy đáp án tương lai khi học, khác điều kiện lúc sinh. | Attention chỉ là một phần tính toán; trọng số lớn không chứng minh quan hệ nhân quả. |
| B59 | Khác độ phân giải, nền, ánh sáng, nét chữ và tiền xử lý. | Độ khó mẫu đánh giá khác nhau, khó quy chênh lệch cho mô hình. |
| B60 | Lớp phổ biến lấn át tổng điểm; cần support và metric từng lớp. | Khởi tạo, nạp tài nguyên, cache hoặc biên dịch có thể làm lần đầu chậm. |
| B61 | Không; cần bằng chứng và bộ đánh giá, mô hình vẫn có thể sai. | Các phép đo không cùng đối tượng; dùng dev ổn định và test giữ riêng. |
| B62 | Schema sai thường là lỗi nội dung/hợp đồng; cần báo lỗi hoặc chính sách sửa hữu hạn riêng. | Chứng minh parser/luồng xử lý trong các ca test; chưa chứng minh chất lượng sinh. |
| B63 | Mã lỗi/tên chính xác thường là tín hiệu từ khóa mạnh. | Cosine là độ giống hình học, chưa được hiệu chuẩn thành xác suất đúng. |
| B64 | Mất điều kiện/ngoại lệ khiến ngữ cảnh dẫn tới kết luận sai. | Cần ID đoạn, phiên bản và vị trí để tìm đúng bằng chứng. |
| B65 | Kiểm tra context thực gửi, prompt, mô hình và hậu kiểm nội dung. | Thiếu mẫu số/rubric/nhóm câu thì không biết phạm vi và mức chắc chắn. |
| B66 | Dấu phân cách không tự tạo ranh giới quyền; cần kiểm soát trong ứng dụng. | Nguồn tồn tại nhưng không hỗ trợ đúng mệnh đề đang được khẳng định. |
| B67 | Nội dung mô hình không đáng tin để thực thi mã; phải dùng tool cố định và kiểm tra đối số. | Ít trạng thái hơn, dễ kiểm thử và dự đoán chi phí khi quy trình đã rõ. |
| B68 | Không; cần timeout/deadline ở lời gọi công cụ và cơ chế dừng phù hợp. | Xác nhận gắn với nội dung/đối số cụ thể; sửa nội dung cần đánh giá quyền lại. |
| B69 | Không trực tiếp; trước hết sửa truy xuất, chunking hoặc dữ liệu nguồn. | Cần mục tiêu, độ đại diện, tập đánh giá, baseline và ngân sách. |
| B70 | Rank cao tăng không gian cập nhật và tăng tham số tuyến tính theo rank. | Vẫn cần mô hình nền, activation và tài nguyên tính toán khi chạy. |
| B71 | Tài liệu được lấy và ngữ cảnh có thể đã thay đổi. | Fake có đầu ra lập trình sẵn; model thật phải được chấm khả năng sinh độc lập. |
| B72 | Metric retrieval không đo khả năng diễn đạt đúng/có căn cứ của bộ sinh. | Ứng dụng: schema/timeout; dữ liệu hoặc model: thiếu bằng chứng/sinh sai, cần chẩn đoán từng ca. |
| B73 | Tốn thời gian, khó kiểm soát phiên bản và làm request không ổn định. | Cùng input qua CLI/API phải có tiền xử lý và dự đoán tương đương. |
| B74 | Không; tính toán trực tiếp vẫn chiếm luồng thực thi và có thể chặn event loop. | Kiểm tra nạp artifact thật, shape, tiền xử lý và dự đoán khớp thay vì chỉ hợp đồng giả. |
| B75 | Xóa/thay container có thể mất lớp dữ liệu ghi; cần volume hoặc lưu ngoài. | Khóa dễ đi vào lịch sử Git/lớp image; truyền secret lúc chạy. |
| B76 | File example chứa tên biến và placeholder; file thật chứa giá trị cần bảo vệ. | Thiếu bằng chứng tải model, tiền xử lý và chất lượng dự đoán/sinh thực tế. |
| B77 | Không; kiểm tra nhãn/chất lượng và nguyên nhân trước khi quyết định. | Đuôi phân bố có request rất chậm dù trung bình thấp. |
| B78 | Hệ thống xử lý tổng nhiều hơn nhưng một số người chờ lâu; phải chọn theo mục tiêu dịch vụ. | Model và tiền xử lý là một hợp đồng cần quay lui đồng bộ. |
| B79 | Nguồn dữ liệu, 8×8 ảnh xám, thang pixel, 10 lớp, miền dùng và trường hợp chưa kiểm chứng. | Corpus/version, chunk/index, cấu hình retrieval, prompt, model/revision và cấu hình sinh. |
| B80 | Nêu test đã bị dùng để tối ưu; cần đánh giá cuối trên dữ liệu mới chưa tác động quyết định. | Chọn theo mức ảnh hưởng và bằng chứng lỗi; đặt metric và phép thử trước khi sửa. |

## Nhánh nâng cao tự chọn — thêm 8–16 tuần hoặc hơn

Chọn 4 nhánh × khoảng 2 tuần để đi sâu bước đầu; học đủ 8 nhánh thường cần ít nhất 16 tuần và có thể lâu hơn. Mỗi nhánh tạo một artifact đo được, giữ lịch 8–10 giờ/tuần. Hoàn tất thiết kế và thí nghiệm CPU được ghi nhận ở mức tương ứng; thực hành hệ thống GPU/phân tán thật cần môi trường phù hợp và không được suy ra từ mô phỏng.

| Nhánh | Nội dung và thực hành | Bằng chứng hoàn thành |
|---|---|---|
| N1 — Huấn luyện phân tán | Data parallel, đồng bộ gradient, gradient accumulation, checkpoint; thử 2 process CPU với mạng nhỏ nếu nền tảng hỗ trợ; GPU/multi-node là phần sau. | So gradient/cập nhật với batch tương đương ở một process trong sai số cho phép; sơ đồ giao tiếp và báo cáo điểm nghẽn. Nếu chỉ mô phỏng, ghi chưa thực hành distributed runtime. |
| N2 — Tối ưu suy luận | Batching, độ dài chuỗi, KV cache ở mức khái niệm, quantization, profiling bộ nhớ/compute; đo baseline trước khi tối ưu. | Bảng latency/throughput/bộ nhớ và mức đổi chất lượng trên cùng dữ liệu; CPU đo được phần CPU, GPU profiling cần trace thật từ GPU. |
| N3 — Retrieval nâng cao | BM25, dense retrieval, hybrid, reranking, hard negatives, Recall@k/MRR/nDCG; mở rộng tập đánh giá tới ít nhất 50 truy vấn. | So ít nhất hai pipeline trên split khóa, phân tích 10 truy vấn thất bại và latency; không chỉ báo một metric tổng. |
| N4 — Thiết kế hệ thống và điều phối | Hàng đợi, cache, idempotency, lịch job, registry, version dữ liệu/model, quyền tenant; thiết kế khi tải tăng 10 lần. | Sơ đồ, 3 lựa chọn có đánh đổi, mô phỏng mất worker hoặc retry trên localhost; đo phục hồi và kiểm tra không xử lý trùng. |
| N5 — Vision và đa phương thức | Detection/segmentation hoặc truy xuất ảnh–văn bản; chọn một tác vụ, dữ liệu có quyền sử dụng và model card rõ. | Demo 20–50 mẫu với metric phù hợp và 5 ca lỗi; CPU subset/mô hình nhỏ đủ thử nghiệm, không gọi là đã huấn luyện quy mô lớn. |
| N6 — Tái lập nghiên cứu | Chọn một kết quả nhỏ từ bài báo, đọc phương pháp/phụ lục, dựng baseline và ablation; ghi mọi khác biệt tài nguyên. | Bảng kết quả tái lập, cấu hình, ít nhất 2 seed khi khả thi và giải thích chênh lệch; phân biệt kết quả đồ chơi với tái lập đầy đủ. |
| N7 — Chất lượng và vận hành dài hạn | Theo dõi nhãn đến chậm, calibration, drift, đánh giá theo nhóm, data validation, audit dữ liệu và kiểm thử bảo mật ứng dụng. | Một báo cáo theo thời gian trên luồng dữ liệu mô phỏng có nhãn; cảnh báo, tiêu chí retrain và diễn tập khôi phục kèm bằng chứng. |
| N8 — Hồ sơ và phỏng vấn | Refactor dự án tốt nhất, luyện Python/SQL, giải thích toán/ML, system design và đọc tài liệu kỹ thuật tiếng Anh theo nhu cầu vị trí. | Hai dự án có README/metric/giới hạn rõ; 3 buổi phỏng vấn thử, nhật ký câu chưa trả lời được và bản sửa có bằng chứng. |

Để đi sâu theo công cụ đã học, bắt đầu từ [PyTorch Tutorials](https://docs.pytorch.org/tutorials/intro.html) cho distributed/profiling và [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) cho hệ sinh thái NLP/LLM; chọn đúng tài liệu ứng với phiên bản đang cài. Các liên kết tham khảo chính thức trong chương này được kiểm tra ngày 11/09/2026; kiến trúc bài học ưu tiên khái niệm và phép đo để có thể thay thư viện khi công cụ thay đổi.
