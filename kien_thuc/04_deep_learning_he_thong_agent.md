# Deep Learning, hệ thống và agent — giải thích từ cơ chế đến thực hành

Tài liệu này giải thích phần PyTorch, API và agent trong các bài B49–B80 và L19–L36. Các phần LLM/RAG được giải thích thêm trong [tài liệu R](03_llm_rag.md). Đọc đúng mục được gắn trong bài học; thời gian đọc nằm trong khối kiến thức đã có của lịch 43 giờ/tuần.

Ví dụ `# RUN: stdlib` chạy độc lập bằng Python 3.11, không cần mô hình hoặc mạng. Ví dụ `# NEEDS: ...` cần thư viện ghi rõ và chưa được xác nhận chạy trong môi trường thư viện chuẩn của bộ học. Số liệu tự đặt để giải thích không phải kết quả huấn luyện hoặc benchmark thực tế.

<a id="h01"></a>
## H01 — Tensor, đồ thị tính toán và autograd

**Cần biết trước:** list, hàm, shape, phép nhân ma trận và đạo hàm; xem [D01](02_du_lieu_toan_ml.md#d01), [D04–D05](02_du_lieu_toan_ml.md#d04).

Tensor biểu diễn mảng số. `shape` nói mỗi trục dài bao nhiêu; `dtype` nói kiểu số; `device` nói dữ liệu nằm trên CPU hay thiết bị khác. Tensor ảnh `(32, 1, 8, 8)` có 32 ảnh, mỗi ảnh một kênh và 8×8 pixel. PyTorch không tự biết ý nghĩa “ảnh”; bạn đặt ý nghĩa cho các trục.

Tham số là các số mô hình sẽ học, như trọng số w và bias b. Forward dùng tham số hiện tại tính dự đoán. Loss biến sai lệch giữa dự đoán và mục tiêu thành một số. Backward tính đạo hàm của loss theo các tham số; optimizer mới thực hiện bước đổi tham số.

Xét một mẫu x=2, mục tiêu y=6, mô hình dự đoán y_hat=w*x với w=1:

| Bước | Phép tính | Kết quả |
|---|---|---:|
| Forward | y_hat = 1 × 2 | 2 |
| Sai số | y_hat − y | −4 |
| Loss bình phương | (−4)² | 16 |
| Gradient theo w | 2 × (y_hat − y) × x | −16 |
| Cập nhật với learning rate 0,1 | w − 0,1 × gradient | 2,6 |
| Loss sau cập nhật | (2,6 × 2 − 6)² | 0,64 |

Gradient âm cho biết tăng w một chút sẽ giảm loss tại vị trí đang xét. Dấu trừ trong cập nhật đi ngược hướng tăng loss; dấu của gradient không phải dấu của “đúng/sai” dự đoán.

```python
# RUN: stdlib
x, target, w, learning_rate = 2.0, 6.0, 1.0, 0.1
prediction = w * x
loss = (prediction - target) ** 2
gradient = 2 * (prediction - target) * x
new_w = w - learning_rate * gradient
new_loss = (new_w * x - target) ** 2
print(loss, gradient, new_w, round(new_loss, 2))
assert round(new_loss, 2) == 0.64
```

Đầu ra: `16.0 -16.0 2.6 0.64`. Đây là đạo hàm tính tay, chưa dùng autograd.

Đồ thị tính toán lưu quan hệ giữa các phép toán cần đạo hàm. Autograd áp dụng quy tắc dây chuyền ngược đồ thị. `requires_grad=True` yêu cầu theo dõi đạo hàm cho tensor phù hợp; thường cần cho tham số, không cần cho mọi dữ liệu đầu vào. `.grad` chứa gradient đã tính và có thể cộng dồn qua nhiều lần backward.

```python
# NEEDS: torch
import torch
w = torch.tensor(1.0, requires_grad=True)
loss = (w * 2.0 - 6.0) ** 2
loss.backward()
print(w.grad.item())  # -16.0
```

**Sai hay gặp:** coi backward là đã cập nhật trọng số; quên xóa gradient cũ; trộn tensor trên hai device; dùng `.item()` giữa phép tính cần đạo hàm rồi làm đứt đồ thị. Tách ba câu hỏi khi debug: dự đoán đúng shape chưa, gradient có xuất hiện không, optimizer có đổi tham số không?

**Tự kiểm và gợi ý:** (1) Backward xong w đã thành 2,6 chưa? Chưa; ví dụ torch chưa có optimizer/update. (2) Learning rate gấp 100 có chắc học nhanh hơn không? Không; bước quá lớn có thể vượt vùng giảm loss.

Tham khảo API: [PyTorch autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html).

<a id="h02"></a>
## H02 — Batch, epoch, vòng huấn luyện và checkpoint

**Cần biết trước:** H01, cách chia train/validation/test ở [D08](02_du_lieu_toan_ml.md#d08).

Một sample là một ví dụ. Batch gom một số sample để tính cùng lúc. Epoch là một lượt qua tập train theo quy trình đã chọn. Với 100 mẫu và batch size 32, nếu giữ batch cuối thì có bốn batch kích thước 32, 32, 32, 4. Batch cuối không mặc định có 32 mẫu.

`Dataset` định nghĩa lấy một sample; `DataLoader` tạo batch và thứ tự đọc. Shuffle thường giúp đổi thứ tự mẫu train; không được dùng shuffle để thay cho việc chia tập hợp lý. Với dữ liệu theo thời gian, vẫn phải giữ nguyên ranh giới train/đánh giá.

Một bước huấn luyện thường gồm: xóa gradient cũ → forward → loss → backward → optimizer step. Sau các batch, chạy validation để quan sát khả năng tổng quát hóa và chọn checkpoint. Không dùng test để chọn epoch.

Khi loss của mỗi batch là trung bình mẫu, loss toàn epoch phải cân theo số mẫu. Ví dụ bốn mẫu ở batch đầu có loss trung bình 1, một mẫu ở batch cuối có loss 3:

```python
# RUN: stdlib
batches = [(1.0, 4), (3.0, 1)]  # (loss trung bình, số mẫu)
weighted_loss = sum(loss * size for loss, size in batches) / sum(size for _, size in batches)
naive_loss = sum(loss for loss, _ in batches) / len(batches)
print(weighted_loss, naive_loss)
assert weighted_loss == 1.4
```

Đầu ra `1.4 2.0`: cách 2,0 cho batch một mẫu trọng lượng ngang batch bốn mẫu.

`model.train()` và `model.eval()` điều chỉnh hành vi của các lớp như dropout và BatchNorm. Chúng không bật/tắt tính gradient thay bạn. `torch.no_grad()` hoặc chế độ inference phù hợp giúp tránh tạo đồ thị khi đánh giá. Với BatchNorm mặc định có theo dõi thống kê, eval dùng thống kê đã lưu; hãy kiểm tra cấu hình lớp khi thay đổi hành vi mặc định.

Checkpoint để học tiếp cần kiến trúc/cấu hình, trọng số, optimizer, epoch và trạng thái liên quan. Artifact để dự đoán cần ít nhất kiến trúc, trọng số và phép biến đổi đầu vào. “Lưu một file” chưa đảm bảo biết thứ tự cột hoặc thang pixel mà mô hình cần.

**Sai hay gặp:** quên eval khi kiểm tra, augmentation ngẫu nhiên trên test, trung bình các batch không cân mẫu, hoặc nạp đúng trọng số nhưng dùng sai tiền xử lý. So đầu ra trước/sau lưu nạp ở cùng chế độ eval và cùng dữ liệu để kiểm tra kỹ thuật.

**Tự kiểm và gợi ý:** (1) 100 mẫu/batch 32 có luôn bốn batch? Không nếu cấu hình bỏ batch cuối. (2) Cùng seed có đảm bảo giống từng bit trên mọi máy? Không; thư viện, phần cứng và phép toán có thể khác.

<a id="h03"></a>
## H03 — MLP, CNN, attention và transfer learning

**Cần biết trước:** H01–H02, nhân ma trận và vector ở D04. Mục tiêu ở đây là hiểu dữ liệu đi qua mạng; phần xác suất token ở [R01](03_llm_rag.md#r01).

Một lớp tuyến tính tính `z = xW + b`. Với batch `X=(N,D)`, trọng số `W=(D,H)`, đầu ra có shape `(N,H)`. H là số đặc trưng ẩn, không phải số mẫu. MLP ghép nhiều lớp tuyến tính với hàm phi tuyến như ReLU `max(0,z)`. Nếu chỉ ghép các phép tuyến tính, cả chuỗi vẫn rút thành một phép tuyến tính nên không học được quan hệ phi tuyến nhờ tăng số lớp.

Ví dụ một mẫu `x=[1,2]`, `W=[[1,-1],[2,0]]`, `b=[0,1]`: tọa độ thứ nhất là `1×1+2×2+0=5`, tọa độ thứ hai là `1×(-1)+2×0+1=0`. Nếu đổi b thứ hai thành -1 thì z thành `[5,-2]`, ReLU cho `[5,0]`. Một head có trọng số `[2,3]` và bias 1 tạo điểm `5×2+0×3+1=11`. Đây là forward với trọng số tự đặt; muốn học phải tính loss và gradient như H01.

Quy ước trên đặt mẫu theo hàng. `torch.nn.Linear(D,H)` lưu weight shape `(H,D)` và tính `X @ weight.T + bias`; đó là cách lưu chuyển vị của cùng phép tính. Kiểm [tài liệu Linear của PyTorch](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html) khi so shape, không đổi trục chỉ để phép nhân hết báo lỗi.

Logit là điểm chưa chuẩn hóa của mỗi lớp. Softmax biến một vector logit thành các số không âm có tổng 1. Với phân loại nhiều lớp loại trừ nhau, CrossEntropyLoss của PyTorch thường nhận **logits** và nhãn lớp, không cần tự softmax logits trước khi đưa vào loss.

CNN dùng một bộ trọng số nhỏ quét nhiều vị trí trong ảnh. Việc dùng chung trọng số giúp phát hiện mẫu cục bộ ở các vị trí khác nhau. Kernel là bộ lọc; stride là bước di chuyển; padding thêm biên. Với dilation=1, chiều ra là `floor((H + 2P - K)/S) + 1`, nếu cấu hình tạo đầu ra hợp lệ.

```python
# RUN: stdlib
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# Bộ lọc 2x2 toàn 1, stride 1, không padding: tổng từng cửa sổ.
result = [
    [sum(grid[r + dr][c + dc] for dr in range(2) for dc in range(2))
     for c in range(2)]
    for r in range(2)
]
print(result)
assert result == [[12, 16], [24, 28]]
```

Ảnh 3×3 thành 2×2. Đây là phép lọc cố định minh họa; CNN thật học giá trị kernel, thường có nhiều kênh và nhiều bộ lọc. Không gọi ví dụ này là mô hình nhận diện đã huấn luyện.

Attention gán trọng số cho các value dựa trên mức phù hợp giữa query và key. Dạng phổ biến tính `softmax(QKᵀ / sqrt(d_k))V`; d_k là độ dài vector key. Với một query, cần tính điểm cho từng key, chuẩn hóa điểm bằng softmax, rồi lấy tổng value có trọng số. Attention không đảm bảo trọng số lớn tương đương “nguồn đúng”.

```python
# RUN: stdlib
import math
query = [1.0, 0.0]
keys = [[1.0, 0.0], [0.0, 1.0]]
values = [10.0, 20.0]
scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(2) for key in keys]
exp_scores = [math.exp(s - max(scores)) for s in scores]
weights = [s / sum(exp_scores) for s in exp_scores]
output = sum(w * value for w, value in zip(weights, values))
print([round(w, 3) for w in weights], round(output, 3))
assert math.isclose(sum(weights), 1.0)
```

Đầu ra xấp xỉ `[0.67, 0.33] 13.302`. Các vector tự đặt nên chỉ minh họa phép tính. Transformer kết hợp attention với các khối biến đổi khác, thông tin vị trí và cơ chế phù hợp bài toán; decoder sinh văn bản cần tránh nhìn token tương lai trong huấn luyện tự hồi quy.

Overfitting là học phù hợp train nhưng không tổng quát tốt. Theo dõi train/validation, regularization và early stopping giúp điều tra vấn đề. Dropout bỏ ngẫu nhiên một số thành phần khi train theo quy tắc lớp; nó không thay cho dữ liệu và đánh giá đúng. Bài “học thuộc một batch nhỏ” là kiểm tra đường huấn luyện có hoạt động, không phải bằng chứng tổng quát hóa.

Transfer learning bắt đầu từ tham số đã học ở bài toán khác. Backbone tạo đặc trưng; head biến đặc trưng thành đầu ra của bài toán mới. Có thể đóng băng backbone rồi học head, sau đó mở một phần trọng số nếu cần. Khi đóng băng cần xem cả gradient lẫn hành vi các lớp có trạng thái. Luôn kiểm tra tiền xử lý, kích thước ảnh và ý nghĩa nhãn của mô hình gốc.

**Sai hay gặp:** dùng logits như xác suất, đổi shape mà không hiểu trục, đưa ảnh 8×8 vào kiến trúc cần ảnh lớn mà không xem cấu hình, hoặc chọn mô hình bằng test. Hãy ghi bảng shape qua từng lớp và giữ cùng split khi so hai kiến trúc.

**Tự kiểm và gợi ý:** (1) Vì sao cần phi tuyến giữa lớp tuyến tính? Để biểu diễn quan hệ không rút về một ánh xạ tuyến tính. (2) Đóng băng backbone có làm tập test thành train không? Không; cách cập nhật tham số và vai trò dữ liệu là hai vấn đề riêng.

<a id="h04"></a>
## H04 — Từ hàm dự đoán đến API

**Cần biết trước:** hàm, JSON, ngoại lệ, module; xem [P05–P09](01_python.md#p05).

API là hợp đồng để một chương trình gọi chức năng của chương trình khác. Trong HTTP, client gửi method, địa chỉ/path, header và có thể có body; server trả status, header và body. Ví dụ `POST /predict` mang dữ liệu cần dự đoán, còn `GET /health` kiểm tra trạng thái dịch vụ.

Một URL như `http://127.0.0.1:8000/predict` gồm giao thức HTTP, địa chỉ máy cục bộ, cổng 8000 và path. Chạy được localhost không đồng nghĩa mọi máy trên mạng gọi được. Server phải đang chạy và lắng nghe đúng địa chỉ/cổng.

Luồng nên rõ: nhận request → parse JSON → kiểm tra schema → kiểm tra quy tắc nghiệp vụ → tiền xử lý → dự đoán → kiểm tra/định dạng output. Không huấn luyện hoặc tải mô hình mỗi request. Nạp artifact lúc khởi động và kiểm tra nó tương thích với schema.

| Lớp kiểm tra | Ví dụ lỗi | Ý nghĩa |
|---|---|---|
| Cú pháp | JSON thiếu dấu nháy | Không đọc được cấu trúc |
| Schema | `minutes` là list | Kiểu/trường không đúng hợp đồng |
| Nghiệp vụ | `minutes=-5` | Đúng kiểu nhưng giá trị không được phép |
| Dữ liệu mô hình | Thiếu một trong 13 cột Wine | Không có đầu vào mà artifact cần |
| Kết quả | Schema đúng nhưng dự đoán sai | Phải đánh giá chất lượng riêng |

```python
# RUN: stdlib
import json
request = json.loads('{"minutes": 45}')
minutes = request.get("minutes")
valid = type(minutes) is int and minutes > 0
response = {"ok": valid, "hours": minutes / 60 if valid else None}
print(json.dumps(response))
assert response == {"ok": True, "hours": 0.75}
```

Ví dụ chỉ mô phỏng handler bằng hàm Python; chưa mở cổng HTTP. `type(x) is int` ở đây cố ý loại bool vì `isinstance(True, int)` là True.

FastAPI dùng khai báo kiểu/schema để kiểm tra request và sinh tài liệu API. Hành vi status cần đọc theo framework: 2xx thường thành công; 4xx phản ánh vấn đề phía request/quyền; 5xx là lỗi phía server. 422 thường xuất hiện khi FastAPI báo lỗi validation, nhưng ứng dụng cần chốt hợp đồng lỗi cụ thể.

Liveness hỏi tiến trình còn hoạt động; readiness hỏi có sẵn sàng nhận việc không, ví dụ artifact đã nạp chưa. Một endpoint health luôn trả 200 có thể bỏ sót trường hợp model chưa sẵn sàng. Chọn những điều cần kiểm tra phù hợp hệ thống nhỏ trước khi thêm nhiều endpoint.

**Sai hay gặp:** coi HTTP 200 là câu trả lời đúng, trả nguyên traceback cho client, bỏ thứ tự cột, hoặc dùng một chuỗi “lỗi” ở nơi chương trình khác đang chờ JSON. Tạo ca test cho request hợp lệ, thiếu trường, sai kiểu và phụ thuộc lỗi.

**Tự kiểm và gợi ý:** (1) JSON hợp lệ có đảm bảo input hợp lệ? Không, còn schema và nghiệp vụ. (2) Một model tốt trong notebook đã là API chưa? Chưa; cần handler, server, hợp đồng và cách nạp/kiểm tra artifact.

<a id="h05"></a>
## H05 — Đồng thời, async, thread và process

**Cần biết trước:** hàm, ngoại lệ, HTTP ở H04. “Đồng thời” nghĩa nhiều công việc cùng đang được xử lý hoặc chờ; “song song” nghĩa có phần thực thi thật sự cùng lúc trên tài nguyên phù hợp.

Một lời gọi HTTP thường có thời gian chờ mạng. Trong lúc chờ, event loop có thể cho coroutine khác tiến hành. `async def` tạo hàm coroutine; `await` chờ một thao tác có hỗ trợ bất đồng bộ và có thể nhường điều khiển. Đặt từ `async` trước phép tính CPU dài không tự làm phép tính đó nhanh hơn hoặc nhường CPU.

```python
# RUN: stdlib
import asyncio

async def task(name):
    await asyncio.sleep(0)  # Chỉ nhường lượt, không mô phỏng độ trễ mạng thật.
    return f"xong {name}"

async def main():
    results = await asyncio.gather(task("A"), task("B"))
    print(results)
    assert results == ["xong A", "xong B"]

asyncio.run(main())
```

Đầu ra giữ thứ tự đối số của gather. Ví dụ chứng minh cách đợi nhiều coroutine; không đo được lợi ích hiệu năng trên mạng hoặc GPU.

| Công cụ | Có ích khi | Giới hạn cần hiểu |
|---|---|---|
| Coroutine/async | Chờ I/O qua thư viện hỗ trợ async | Lời gọi đồng bộ chặn vẫn có thể làm nghẽn event loop |
| Thread | Đưa I/O đồng bộ ra khỏi luồng đang phục vụ; một số thư viện số giải phóng GIL | Không mặc định tăng tốc vòng lặp Python thuần trên bản CPython có GIL |
| Process | Chia công việc CPU Python phù hợp | Có bộ nhớ riêng, chi phí khởi tạo/truyền dữ liệu; model lớn có thể bị nhân bản |
| Batch | Xử lý nhiều input trong một phép tính model | Cần chờ gom batch; throughput tăng có thể đổi lấy latency cao hơn |

GIL là cơ chế của nhiều bản CPython giới hạn việc thực thi bytecode Python đồng thời trong một tiến trình. Không suy ra mọi thư viện số đều chỉ chạy một lõi; thư viện native và cấu hình Python có thể khác. Đo đúng workload đang dùng.

Semaphore giới hạn số tác vụ vào một đoạn tại cùng thời điểm. Nếu model chỉ chịu ba request đang chạy, nhận vô hạn task rồi chờ không làm tài nguyên tăng; hàng chờ vẫn có thể lớn. Cần thêm giới hạn hàng chờ/kích thước request, deadline và phản hồi quá tải.

Trên Windows, mã khởi tạo process phải được bảo vệ bằng `if __name__ == "__main__":` để tránh khởi tạo lặp khi tiến trình con import module. Chỉ áp dụng process khi hiểu chi phí nạp model và truyền dữ liệu.

**Sai hay gặp:** gọi HTTP đồng bộ trong coroutine, bỏ quên await, tạo hàng nghìn task không giới hạn, tưởng cancel bên chờ chắc chắn dừng thread. Timeout/hủy và công việc nền được giải thích ở H08.

**Tự kiểm và gợi ý:** (1) Vì sao async không tự tăng tốc nhân ma trận? Nó điều phối chờ, không thay thuật toán hay phần cứng. (2) Hai request dùng cùng model có nên mặc định tạo hai process? Không; kiểm tra khả năng batch, bộ nhớ và nhu cầu tải trước.

Tra hành vi API theo phiên bản: [Python asyncio](https://docs.python.org/3/library/asyncio-task.html), [FastAPI async](https://fastapi.tiangolo.com/async/).

<a id="h06"></a>
## H06 — Tool là hợp đồng và quyền thực thi

**Cần biết trước:** H04, JSON/schema ở [R03](03_llm_rag.md#r03), hàm và ngoại lệ.

Tool là chức năng chương trình cho mô hình đề xuất sử dụng. Mô hình trả tên và args; dispatcher là phần mã chọn hàm tương ứng sau khi kiểm tra. Một mô tả bằng ngôn ngữ tự nhiên giúp model biết cách chọn, còn validation thực thi mới kiểm soát dữ liệu đầu vào.

Trong NovaLearn, `search_catalog` chỉ đọc corpus; `draft_plan` chỉ tính bản nháp. Không công cụ nào cấp quyền gửi email, ghi đăng ký hay sửa tài khoản.

```python
# RUN: stdlib
def draft_plan(topic, hours_per_week):
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("Chủ đề không được rỗng")
    if type(hours_per_week) is not int or not 1 <= hours_per_week <= 60:
        raise ValueError("Giờ phải là số nguyên từ 1 đến 60")
    minutes = hours_per_week * 60
    return {
        "topic": topic.strip(),
        "total_minutes": minutes,
        "sessions": [minutes // 5] * 5,
    }

result = draft_plan("Python", 10)
print(result)
assert result["sessions"] == [120, 120, 120, 120, 120]
assert sum(result["sessions"]) == 600
```

Mỗi giờ có 60 phút, chia năm buổi luôn ra số phút nguyên với input số giờ nguyên. Công cụ tính chính xác bằng Python; model có thể giải thích kết quả sau đó. Đây là bản nháp trong bộ nhớ, chưa phải lịch đã lưu.

Hợp đồng gồm: tên công cụ, trường bắt buộc, kiểu/miền giá trị, output, lỗi và tác động. Schema trả lời “input có đúng hình dạng không”; nghiệp vụ trả lời “giá trị này có hợp lệ không”; quyền trả lời “người dùng này được làm việc đó không”. Ba lớp này bổ sung nhau.

Allowlist là danh sách tên công cụ được ứng dụng cho phép. Không lấy bất kỳ tên hàm do model viết rồi tìm/chạy bằng `eval` hoặc `exec`. Với output model sai JSON hoặc có công cụ lạ, trả trạng thái lỗi có cấu trúc và giữ giới hạn tổng; không tự đoán quyền mới.

**Sai hay gặp:** chỉ mô tả “giờ phải dương” trong prompt mà không kiểm tra mã, chấp nhận True như số 1, coi tên tool được model đề xuất là quyền đã cấp, hoặc để tham số tùy ý đi thẳng đến shell.

**Tự kiểm và gợi ý:** (1) Vì sao `True` bị từ chối dù Python coi bool là một dạng int? Hợp đồng yêu cầu số giờ người dùng nhập, không phải giá trị logic. (2) Model trả tên tool “send_email” có làm tool đó tồn tại không? Không; dispatcher chỉ có các tên được ứng dụng đăng ký.

<a id="h07"></a>
## H07 — Workflow, agent, state và điểm dừng

**Cần biết trước:** H06, các bước RAG ở [R11](03_llm_rag.md#r11).

Workflow định sẵn cách chọn đường đi: câu hỏi chính sách → tìm nguồn → soạn câu trả lời; yêu cầu kế hoạch đủ dữ kiện → tính bản nháp. Model có thể viết văn bản trong workflow nhưng không vì vậy mà toàn bộ đường đi do model chọn.

Agent cho model chọn hành động tiếp theo dựa trên request, state và kết quả tool. State lưu những gì đã biết và đã làm; observation là kết quả quan sát từ một lần gọi tool. Trace ghi các sự kiện để giải thích tại sao chương trình trả kết quả đó. Tránh gọi mọi log văn bản là suy nghĩ nội bộ của model; điều cần ghi là hành động và bằng chứng quan sát được.

| Bước | Quyết định | Việc ứng dụng làm |
|---|---|---|
| 1 | Gọi tìm kiếm chính sách | Kiểm tra schema/quyền, chạy search, lưu observation |
| 2 | Tạo kế hoạch khi đã có số giờ | Kiểm tra args, gọi hàm tính, lưu kết quả |
| 3 | Trả final | Kiểm tra output, kết thúc lượt yêu cầu |
| Khi vượt giới hạn | Bất kỳ đề xuất nào | Ứng dụng dừng và báo trạng thái, không tiếp tục vô hạn |

Giới hạn phải đếm rõ: lượt model, lần tool thật sự chạy, retry và tổng thời gian. Với tối đa bốn lượt model, final cũng là một lượt. Cache hit không chạy tool lại nhưng model đã đề xuất hành động vẫn tiêu một lượt model.

Bộ khởi động dùng giao thức riêng dưới đây. Nếu lab chọn tên khác như `tool_call` hoặc `clarify`, phải viết adapter; không đưa tên khác thẳng vào `run_agent` rồi mong nó tự hiểu.

| Ý định | Giao thức starter | Lưu ý khi mở rộng |
|---|---|---|
| Gọi công cụ | `{"type":"tool","call":{"name":...,"args":...}}` | Validate tên/args trước executor |
| Kết thúc | `{"type":"final","answer":"..."}` | Starter nhận chuỗi; API RAG cần giữ citations và validation riêng |
| Hỏi làm rõ | Final chứa câu hỏi làm rõ | Ứng dụng ghi trạng thái đang chờ; câu trả lời người dùng đi vào lượt sau |
| Lỗi / hết bước | `invalid_action`, `error`, `step_limit` | Không giả thành câu trả lời thành công |

```python
# RUN: stdlib
actions = ["tool", "tool", "tool", "tool", "final"]
max_steps = 4
visited = []
status = "step_limit"
for action in actions[:max_steps]:
    visited.append(action)
    if action == "final":
        status = "completed"
        break
print(visited, status)
assert status == "step_limit"
```

Final ở bước thứ năm không được chạy. Đây là vòng lặp giả lập để hiểu giới hạn; hành động chưa do LLM sinh nên không chứng minh model có khả năng chọn tool.

Khi người dùng nói “lập kế hoạch Python” mà thiếu số giờ, hỏi làm rõ giúp tránh tự đặt số. State phải gắn với đúng phiên/người dùng và có thời hạn; câu “10 giờ” của phiên B không được dùng để hoàn tất kế hoạch của phiên A. Trả final của một lượt HTTP không có nghĩa mọi cuộc hội thoại nhiều lượt đã hoàn thành.

**Sai hay gặp:** đếm thiếu final/retry, lặp cùng truy vấn vô tận, dùng kết quả tool mà không kiểm tra lỗi, hoặc đo tool correctness chỉ từ câu model tự nói “tôi đã tìm”. Chấm từ dữ liệu quyết định và trace thực thi.

**Tự kiểm và gợi ý:** (1) Workflow có gọi LLM vẫn là workflow được không? Có, khi đường đi chính do chương trình định. (2) Schema final của starter có giữ citations không? Không; cần response/validation của tầng RAG, không tự suy ra citations từ một chuỗi final.

<a id="h08"></a>
## H08 — Timeout, retry, cache và idempotency

**Cần biết trước:** ngoại lệ ở [P07](01_python.md#p07), request/response ở [H04](#h04). Khi đến phần hủy công việc và cache cho agent, đọc thêm [H05](#h05) và [H07](#h07); ở L06 ưu tiên timeout, deadline và retry.

Timeout giới hạn thời gian chờ một thao tác theo cơ chế của thư viện. Deadline là thời điểm phải kết thúc toàn bộ request. Một request có nhiều bước cần cả timeout mỗi bước và deadline tổng. Tất cả lần thử lại đều tiêu thời gian và ngân sách.

Ví dụ deadline còn 3 giây, lần gọi đầu chờ 2 giây rồi timeout. Nếu muốn chờ backoff 0,5 giây, lần tiếp chỉ còn tối đa 0,5 giây; không được bắt đầu thêm một timeout 2 giây rồi khẳng định giữ deadline 3 giây. Backoff là khoảng nghỉ giữa các lần thử; jitter thêm biến thiên để nhiều client không cùng thử lại một lúc.

Chỉ retry lỗi đã xác định có thể tạm thời. Sai API key, sai schema hoặc input quá dài thường cần sửa nguyên nhân. 429/5xx và lỗi mạng cũng phải theo chính sách nhà cung cấp; không mặc định mọi lỗi đều đáng thử lại.

Cache ghi kết quả để dùng lại. Idempotency quy định khi xử lý lại cùng yêu cầu thì kết quả/tác động quan sát được cần nhất quán. Cache cục bộ là một phần hỗ trợ; nó không tự bảo đảm một thao tác bên ngoài chỉ xảy ra đúng một lần.

```python
# RUN: stdlib
import json

cache = {}
executions = []

def handle(request_id, payload):
    fingerprint = json.dumps(payload, sort_keys=True)
    if request_id in cache:
        old_fingerprint, old_result = cache[request_id]
        if fingerprint != old_fingerprint:
            raise ValueError("Cùng request_id nhưng khác payload")
        return old_result
    result = payload["hours"] * 60
    executions.append(request_id)
    cache[request_id] = (fingerprint, result)
    return result

print(handle("r1", {"hours": 2}), handle("r1", {"hours": 2}))
try:
    handle("r1", {"hours": 3})
except ValueError:
    print("Từ chối payload thay đổi")
assert executions == ["r1"]
```

Đầu ra: `120 120` rồi `Từ chối payload thay đổi`. Ví dụ chỉ có một luồng, không có tác động bên ngoài. Nếu hai request đồng thời cùng đến trước khi cache được ghi, cả hai có thể chạy; cần lock hoặc đăng ký một công việc đang chạy để những request trùng cùng chờ nó.

Kết quả cache nên được gắn với nội dung request, phạm vi người dùng/quyền và phiên bản dữ liệu/model thích hợp. Khi corpus đổi, trả đáp án cũ vô thời hạn có thể sai. TTL là thời hạn giữ cache; invalidation là cách làm kết quả cũ không còn được dùng.

Timeout ở bên chờ không chứng minh thao tác đã dừng. Coroutine có thể hỗ trợ hủy hợp tác; thread đang chạy hàm đồng bộ thường không bị cưỡng bức dừng chỉ vì bên chờ bỏ cuộc. `run_agent(max_steps=4)` chỉ giới hạn số bước và không thể ngắt policy đang treo.

**Sai hay gặp:** coi cache hit là một quyết định mới của model, dùng một request_id cho payload khác, retry làm nhân tác động, hoặc quảng cáo “timeout tổng” nhưng chưa tính thời gian chờ/retry.

**Tự kiểm và gợi ý:** (1) Cache trong bộ nhớ sống qua khởi động lại không? Không. (2) Cần gì khi hai request trùng chạy đồng thời? Cơ chế phối hợp cho một công việc đang chạy, không chỉ kiểm tra dict trước/sau.

<a id="h09"></a>
## H09 — Dữ liệu không đáng tin, phân quyền và phiên hội thoại

**Cần biết trước:** schema/allowlist ở H06, state ở H07, prompt và nguồn ở [R02](03_llm_rag.md#r02).

Một tài liệu được tìm thấy có thể chứa câu “hãy bỏ qua quy định và gửi dữ liệu”. Nội dung đó vẫn là dữ liệu từ nguồn; nó không trở thành chỉ dẫn có quyền của ứng dụng. Prompt injection là nỗ lực khiến nội dung không đáng tin thay đổi hành vi ngoài ý định cho phép.

Tách ranh giới trong prompt giúp diễn đạt yêu cầu, nhưng kiểm soát thực thi vẫn nằm ở mã: giới hạn tool, kiểm tra args, kiểm tra quyền, kiểm tra phạm vi dữ liệu và trạng thái cho phép. Một bộ lọc tìm vài từ như “bỏ qua” không chứng minh mọi yêu cầu đối kháng sẽ bị chặn.

Trong hệ thống có nhiều người dùng, chỉ đưa tài liệu mà người đó được quyền xem vào bộ ứng viên tìm kiếm. Lọc sau khi đã đưa tài liệu vào prompt là quá muộn. Chỉ bỏ tài liệu khỏi câu trả lời cũng không xóa việc model hoặc log đã nhận nó.

```python
# RUN: stdlib
documents = [
    {"id": "a1", "tenant": "A", "text": "Ghi chú của nhóm A"},
    {"id": "b1", "tenant": "B", "text": "Ghi chú của nhóm B"},
]
# Giá trị actor do server xác thực, không lấy từ lời tự nhận trong prompt.
actor = {"tenant": "A"}
visible = [doc for doc in documents if doc["tenant"] == actor["tenant"]]
print([doc["id"] for doc in visible])
assert [doc["id"] for doc in visible] == ["a1"]
```

Ví dụ chỉ minh họa bước lọc, không triển khai đăng nhập/xác thực thật. Trong NovaLearn hiện tại tất cả tài liệu là giả lập; nếu tạo biến thể phân quyền, thêm fixture riêng và giữ corpus gốc.

Memory là dữ liệu ứng dụng giữ để tiếp tục hội thoại: chủ đề, số giờ đã hỏi, các bước đã hoàn tất. Nó không phải trí nhớ vĩnh viễn tự động của mọi model. Gắn memory với session và người dùng đúng, giới hạn kích thước, đặt cách hết hạn/xóa, không lưu secret không cần thiết.

Với hành động có tác động bên ngoài, sự cho phép cần gắn với thao tác và nội dung cụ thể. Một câu trong tài liệu hoặc một trường `approved=true` do model tự viết không phải xác nhận của người dùng. Trong các lab này chỉ mô phỏng hành động có tác động bằng state trong bộ nhớ; tool thật của bài mẫu chỉ đọc và tính bản nháp.

**Sai hay gặp:** dùng chung lịch sử cho mọi phiên, coi metadata do client gửi là quyền đã xác thực, đưa secret vào prompt/debug log, hoặc cấp quyền mới vì model chọn một tool lạ.

**Tự kiểm và gợi ý:** (1) Nếu user B hỏi lại đúng query của user A, có thể trả cache của A không? Chỉ khi phạm vi quyền/dữ liệu cho phép và cache key thiết kế đúng; trùng chữ chưa đủ. (2) Đã chặn bốn ca đối kháng có chứng minh an toàn toàn diện? Không, chỉ có bằng chứng cho những ca đã thử.

<a id="h10"></a>
## H10 — Kiểm thử phần mềm, đánh giá nhiệm vụ và quan sát lỗi

**Cần biết trước:** test ở [P08](01_python.md#p08), metric/split ở [D08–D09](02_du_lieu_toan_ml.md#d08), đánh giá RAG ở [R12](03_llm_rag.md#r12).

Unit test kiểm tra một trách nhiệm nhỏ với đầu vào kiểm soát. Integration test kiểm tra các phần nối nhau đúng. Smoke test kiểm tra nhanh một luồng quan trọng để biết bản triển khai còn hoạt động. Đánh giá mô hình kiểm tra chất lượng trên tập tình huống đã chốt; nó trả lời câu hỏi khác với “hàm không phát sinh lỗi”.

Fake provider cố ý trả output hoặc lỗi định sẵn để tái hiện ca khó. Nếu fake luôn trả câu đúng từ fixture, điểm của nó không đo năng lực LLM. Để đánh giá thật, request chỉ chứa thông tin ứng dụng được phép có; đáp án chuẩn và expected_tools ở phía bộ chấm.

```python
# RUN: stdlib
cases = [
    {"id": "c1", "tool_correct": True, "task_success": True},
    {"id": "c2", "tool_correct": True, "task_success": False},
    {"id": "c3", "tool_correct": False, "task_success": False},
]
tool_rate = sum(c["tool_correct"] for c in cases) / len(cases)
task_rate = sum(c["task_success"] for c in cases) / len(cases)
print(round(tool_rate, 3), round(task_rate, 3))
assert tool_rate > task_rate
```

Đầu ra `0.667 0.333`. Ca c2 có thể đã chọn đúng search nhưng kết luận sai dữ kiện. Đây là bảng giả để học cách tính, không phải kết quả agent NovaLearn.

Khi so workflow với agent, giữ cùng nhóm request, dữ liệu, model/provider, chính sách chấm và ngân sách phù hợp. Ghi khác biệt không thể giữ nguyên. Dùng dev để chọn; khóa cấu hình trước test. Sửa sau khi xem test là một vòng phát triển mới, không giữ danh nghĩa “chưa nhìn test” cho tập đó.

Log là các sự kiện có cấu trúc; metric là số tổng hợp; trace liên kết các bước của một request. `request_id` giúp tìm từ response đến các lần retrieval/model/tool. Ghi thời gian, trạng thái, phiên bản và loại lỗi cần thiết; tránh toàn bộ prompt hoặc dữ liệu cá nhân khi không cần. Đo cả lỗi thay vì chỉ những request thành công.

Phân tích lỗi theo tầng: request sai → tìm thiếu nguồn → context thiếu → model đọc sai → tool chọn sai → executor lỗi → format response sai. Một sửa prompt không giải quyết việc chỉ mục thiếu tài liệu. Ghi bằng chứng để chọn tầng cần sửa.

**Sai hay gặp:** bỏ timeout khỏi mẫu số, chỉ báo accuracy tổng, dùng JSON đúng schema làm điểm groundedness, hoặc chọn mô hình theo test rồi báo như kết quả độc lập.

**Tự kiểm và gợi ý:** (1) Tool correctness 100% có đảm bảo task success 100%? Không; còn sử dụng kết quả và đầu ra cuối. (2) API trả 200 nhưng nội dung sai nên xếp vào lỗi nào? Vận chuyển có thể thành công, chất lượng nhiệm vụ thất bại; cần ghi riêng cả hai.

<a id="h11"></a>
## H11 — Artifact, môi trường, Docker, CI và rollback

**Cần biết trước:** module/môi trường ở [P09](01_python.md#p09), API ở H04, test ở H10.

Artifact là sản phẩm được tạo để chạy hoặc kiểm tra lại: trọng số, Pipeline, chỉ mục tìm kiếm, schema, cấu hình và báo cáo. Một phiên bản dịch vụ cần biết bộ artifact nào tương thích; đổi model mà giữ tokenizer hoặc index cũ không tương thích có thể làm hỏng hệ thống.

Môi trường ảo tách các gói Python giữa dự án. Ghi phiên bản sau khi cài và chạy thành công để người khác biết môi trường đã kiểm chứng. File dependency chưa được thử trên máy mới không tự chứng minh khả năng tái lập.

Image Docker đóng gói môi trường chạy; container là một lần chạy image. Image không phải máy ảo đầy đủ và không biến mọi phần cứng thành giống nhau. GPU hoặc hệ thống host vẫn cần hỗ trợ phù hợp. Dữ liệu thay đổi nên có vị trí lưu rõ, không chỉ nằm trong lớp container có thể bị thay.

| Thành phần | Cần lưu/chốt | Vì sao |
|---|---|---|
| Mã | Commit hoặc bản phát hành | Biết logic nào đã chạy |
| Gói | Python và phiên bản thư viện | Tránh thay API âm thầm |
| Model/index | Version/hash và schema tương thích | Nạp đúng sản phẩm đã đánh giá |
| Cấu hình | Tham số có ý nghĩa, không kèm secret | Tái lập hành vi và ngân sách |
| Dữ liệu đánh giá | ID và phiên bản | So cùng bài toán qua các lần chạy |

```python
# RUN: stdlib
import hashlib
import json
config = {"model": "demo-v1", "top_k": 3, "prompt_version": "p2"}
canonical = json.dumps(config, sort_keys=True, separators=(",", ":"))
digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
same_config = {"top_k": 3, "prompt_version": "p2", "model": "demo-v1"}
same_text = json.dumps(same_config, sort_keys=True, separators=(",", ":"))
print(len(digest), digest == hashlib.sha256(same_text.encode("utf-8")).hexdigest())
assert len(digest) == 64
```

Đầu ra `64 True`: cùng dữ liệu JSON theo cách chuẩn hóa này cho cùng dấu nhận diện dù thứ tự khóa khác. Hash không chứng minh model đúng, không thay kiểm thử và không tự chứng minh nguồn dữ liệu đáng tin.

CI là quy trình tích hợp thay đổi kèm kiểm tra tự động, thường được kích hoạt bởi commit/PR. Một script test chạy tay là bước chuẩn bị tốt; nếu chưa có trigger thì hãy mô tả đúng là bộ kiểm tra cục bộ. Trong lab có thể chạy pipeline kiểm tra tại máy; muốn chứng minh CI tự kích hoạt phải có sự kiện và log tương ứng.

Rollback đưa dịch vụ về một phiên bản đã biết hoạt động. Nó cần cả code, cấu hình và artifact phù hợp. Thử health và request mẫu sau rollback để kiểm tra phục hồi, không chỉ đổi tên file. Với hệ thống có migration dữ liệu, quay code lại còn cần xem dữ liệu có tương thích không; dự án hiện tại giữ phạm vi dữ liệu giả và chỉ mục nhỏ.

**Sai hay gặp:** bỏ secret vào image, không ghi model/index version, tải model mỗi request, gọi Dockerfile chưa build là container đã chạy, hoặc gọi rollback thành công trước khi thử request.

**Tự kiểm và gợi ý:** (1) Image chạy được có đảm bảo metric giống trên GPU khác không? Không. (2) Vì sao requirements và model file chưa đủ? Còn code, preprocessing/schema, dữ liệu và cấu hình quyết định hành vi.

Nguồn thao tác theo môi trường: [Docker Get Started](https://docs.docker.com/get-started/).

<a id="h12"></a>
## H12 — Độ trễ, throughput, chi phí, drift và tối ưu có đo lường

**Cần biết trước:** mean/percentile ở [D03](02_du_lieu_toan_ml.md#d03), thống kê ở [D06](02_du_lieu_toan_ml.md#d06), đồng thời H05, metric/trace H10.

Latency là thời gian một request chờ đến khi nhận kết quả theo mốc đo đã chọn. Throughput là số request hoặc đơn vị công việc hoàn tất trong một khoảng thời gian. Tăng số request đồng thời có thể tăng throughput trước khi tài nguyên bão hòa; sau đó hàng chờ có thể khiến latency tăng mạnh.

p50/p95 là phân vị, không phải phần trăm request “đúng”. Có nhiều quy ước tính phân vị; dưới đây dùng nearest-rank trên dữ liệu giả để hiểu cách đọc:

```python
# RUN: stdlib
import math
latencies_ms = [10, 20, 40, 80, 100]
ordered = sorted(latencies_ms)
def nearest_rank(values, p):
    if not values or not 0 < p <= 1:
        raise ValueError("Cần dữ liệu và 0 < p <= 1")
    return sorted(values)[math.ceil(p * len(values)) - 1]
print(nearest_rank(ordered, 0.5), nearest_rank(ordered, 0.95))
print("Thông lượng giả định:", 50 / 2, "request/giây")
assert nearest_rank(ordered, 0.95) == 100
```

Đầu ra `40 100`, rồi thông lượng giả định 25 request/giây. Năm mẫu không đủ ước lượng p95 ổn định của dịch vụ thật; đây là phép tính mẫu. Các thư viện có thể mặc định nội suy nên cần ghi phương pháp khi đối chiếu.

Warm-up là giai đoạn khởi động/nạp tài nguyên trước phép đo ổn định. Ghi riêng thời gian cold start nếu nó ảnh hưởng người dùng. Với streaming LLM, có thể đo thời gian đến token đầu và thời gian hoàn tất; không trộn hai số này dưới cùng tên “latency”.

Nếu có usage và đơn giá thực đã xác minh, chi phí API thường được tính theo các loại token và hạng mục nhà cung cấp quy định. Chưa có usage thì ghi unknown, không dùng số từ thay số token rồi gọi đó là hóa đơn thực. Model cục bộ dùng RAM/CPU/GPU và thời gian; API không thu tiền không đồng nghĩa tài nguyên không có chi phí.

Drift là thay đổi phân bố so với mốc tham chiếu, như câu hỏi dài hơn hoặc tỷ lệ chủ đề mới tăng. Drift là tín hiệu điều tra, không tự chứng minh chất lượng giảm. Muốn biết accuracy hoặc groundedness giảm cần nhãn, mẫu chấm hoặc phép đánh giá phù hợp.

Tối ưu nên bắt đầu bằng profiling: đo thời gian/bộ nhớ từng tầng để tìm phần chiếm nhiều tài nguyên. Batching, cache, thay model nhỏ hơn, quantization và giảm context có những đánh đổi khác nhau. Quantization dùng biểu diễn số với độ chính xác thấp hơn để giảm tài nguyên theo phương pháp; phải đo lại chất lượng và tốc độ thực, không suy ra mọi máy đều nhanh hơn.

Ở hệ thống lớn hơn, hàng đợi tách nhận việc khỏi xử lý, worker thực hiện công việc, backpressure giới hạn việc nhận thêm khi quá tải. Data parallel huấn luyện dùng bản sao model xử lý những phần batch khác rồi phối hợp gradient; nó cần runtime và phép so sánh thực, không được chứng minh chỉ bằng sơ đồ.

**Sai hay gặp:** tối ưu nơi chưa đo, báo p95 mà không ghi số mẫu/lỗi, đo fake thay model thật, hoặc giảm chất lượng nhiều nhưng chỉ khoe số request/giây.

**Tự kiểm và gợi ý:** (1) Throughput tăng nhưng p95 tăng mạnh có thể chấp nhận không? Tùy yêu cầu latency và tải, cần tiêu chí đã chốt. (2) Histogram input thay đổi có bắt buộc retrain ngay không? Không; cần kiểm tra tác động, dữ liệu và nguyên nhân.

## Cách học lại khi còn vướng

Tự vẽ một request qua các bước dữ liệu → model/tool → output, ghi shape/schema tại mỗi biên. Tại một phép tính, thay số để kiểm tra hiểu. Tại một quy tắc hệ thống, tự tạo ca lỗi để xem quy tắc có thực thi bằng mã không.

Hoàn thành phần giải thích nghĩa là tự trả lời được câu hỏi và làm một biến thể; không cần học thuộc toàn bộ câu chữ. Nếu câu hỏi nào chưa trả lời được, quay về mục tiên quyết của phần đó trước khi tăng độ phức tạp lab.
