# Chặng 2 — Dữ liệu, toán thực dụng và Machine Learning

> Thư viện bài học đầy đủ; số tuần dưới đây thuộc bản 40 tuần. Lịch đang áp dụng là [4 tuần, N01–N28](../LO_TRINH_4_TUAN.md). Chỉ đọc và làm phần được chỉ định trong lịch mới.

**Tuần 13–24 · Bài B25–B48 · khoảng 8–10 giờ/tuần.** Đầu vào: đã viết được hàm, đọc/ghi tệp, xử lý ngoại lệ, dùng môi trường ảo và kiểm thử hàm Python. Đầu ra: P02 báo cáo dữ liệu có thể tái tạo và P03 bộ phân loại dữ liệu bảng, chuẩn bị dùng lại khi xây API ở chặng sau.

Mỗi tuần dành khoảng 2 giờ đọc và chạy ví dụ của hai bài, 4 giờ làm phần Cơ bản/Vận dụng, 1–2 giờ sửa lỗi và giải thích kết quả. Mỗi tuần có ba bài thực hành tổng hợp: Cơ bản, Vận dụng và Mở rộng. Phần Mở rộng là tùy chọn, làm trong thời gian còn lại hoặc sau chặng. Không cần GPU hay dịch vụ trả phí. Khi gặp công thức, hãy tính một ví dụ nhỏ bằng tay rồi mới viết NumPy.

**Cách nộp bài:** tự tạo thư mục `bai_lam/tuan_13` … `bai_lam/tuan_24`, mỗi tuần có mã nguồn và ghi chú ngắn: đầu vào, cách chạy, kết quả, một lỗi đã sửa. Các tên tệp đầu ra dưới đây là những tệp người học sẽ tạo, không phải dữ liệu đã được cung cấp sẵn. Chỉ chuyển tuần khi đạt tiêu chí của phần bắt buộc và trả lời được câu hỏi bằng lời của mình.

## Dữ liệu dùng xuyên suốt

### D1 — CSV bán hàng giả lập cho B27–B30 và P02

Tự tạo ba tệp UTF-8 từ các khối CSV sau, hoặc đọc chuỗi bằng `pd.read_csv(io.StringIO(chuoi_csv))`. Giá tính bằng VND nguyên; `quantity` là số sản phẩm. Mỗi dòng đơn là một mặt hàng, không phải giỏ hàng nhiều mặt hàng. Các mã và số liệu đều giả lập.

`customers.csv`:

```csv
customer_id,region
C01,Bac
C02,Trung
C03,Nam
```

`products.csv`:

```csv
product_id,unit_price_vnd
P01,100000
P02,200000
P03,50000
```

`orders.csv`:

```csv
order_id,date,customer_id,product_id,quantity
O001,2026-01-01,C01,P01,2
O002,2026-01-02,C02,P02,1
O003,2026-01-03,C03,P03,3
O004,2026-01-04,C01,P01,
O005,khong-hop-le,C02,P02,1
O006,2026-01-06,C03,P03,-1
O007,2026-01-07,C01,P99,2
O008,2026-01-08,C02,P02,2
O009,2026-01-09,C03,P03,1
O010,2026-01-10,C01,P01,3
O002,2026-01-02,C02,P02,1
O011,2026-01-11,C99,P01,1
```

Quy tắc đã thống nhất trước phân tích: giữ dữ liệu gốc; loại bản sao giống hoàn toàn; đưa dòng thiếu/sai ngày, số lượng không phải số nguyên dương hoặc khóa khách hàng/sản phẩm không tồn tại sang bảng cách ly kèm lý do. Không tự điền số lượng bằng trung bình. Hai dòng cùng `order_id` nhưng khác nội dung là xung đột cần báo lỗi, không tùy ý chọn một dòng.

Kết quả chuẩn: 12 dòng đầu vào = 1 bản sao bị loại + 5 dòng cách ly + 6 dòng hợp lệ. Tổng số lượng hợp lệ là 12, doanh thu là 1.300.000 VND; Bắc 500.000, Trung 600.000, Nam 200.000. Bộ rất nhỏ này dùng kiểm tra tính đúng; không đủ để kết luận xu hướng thị trường hoặc hành vi khách hàng.

### D2 — Hồi quy có quy luật biết trước

Tạo mới bằng `rng = np.random.default_rng(42)`; `X = rng.normal(size=(300, 2))`; `y = 3 * X[:, 0] - 2 * X[:, 1] + 5 + rng.normal(0, 0.2, 300)`. Hai cột là đặc trưng giả lập, `y` là đại lượng liên tục không có đơn vị. Lưu seed, công thức và thứ tự tạo dữ liệu để chạy lại được.

### D3 — Wine cho bài toán phân loại và P03

Dùng `from sklearn.datasets import load_wine` rồi `data = load_wine(as_frame=True)`, `X = data.data`, `y = data.target`. Bộ dữ liệu đi kèm scikit-learn có 178 mẫu, 13 đặc trưng số và 3 lớp. Đây là bài tập phân biệt ba nhóm rượu theo phép đo, không phải dự đoán điểm chất lượng rượu. Bộ nhỏ phù hợp học quy trình; kết quả không chứng minh mô hình dùng được trong sản xuất. Xem [mô tả Wine chính thức](https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-recognition-dataset).

Từ B37, giữ cố định `row_id` là chỉ số gốc. Chia bằng `train_test_split` có `stratify=y`, `random_state=42`: tách 20% test trước, sau đó lấy 25% phần còn lại làm validation với seed 42 và phân tầng theo nhãn phần còn lại. Thu được 106 train, 36 validation, 36 test. Chỉ số không được trùng giữa các tập. `row_id` không phải đặc trưng đầu vào.

Train dùng học tham số; validation dùng so sánh các quyết định đã ghi lại; test được giữ kín đến B48. Từ B37 đến B47, EDA liên quan đến lựa chọn mô hình chỉ dùng train, phân tích lỗi dùng validation. Chia tập cần nhãn để phân tầng nhưng không xem đặc trưng hay kết quả dự đoán test để lựa chọn. Chỉ fit scaler, imputer, PCA và bộ chọn đặc trưng trên dữ liệu huấn luyện tương ứng.

## Tuần 13 — Tư duy mảng với NumPy

### B25. Mảng, kiểu số và hình dạng dữ liệu

**Đọc để hiểu bài:** [D01 — Shape, axis và broadcasting](../kien_thuc/02_du_lieu_toan_ml.md#d01).

**Mục tiêu:** tạo và đọc được mảng 1–3 chiều, hiểu `shape`, `dtype`, `axis`, slicing và boolean mask. Với bảng `X.shape == (n, d)`, hàng là mẫu và cột là đặc trưng; ý nghĩa này do ta quy ước, NumPy không tự biết. Tổng theo `axis=0` gom các hàng để trả kết quả cho từng cột. Slicing có thể chia sẻ dữ liệu gốc nên cần biết khi nào phải `.copy()`.

### B26. Broadcasting và tính toán theo mảng

**Đọc để hiểu bài:** [D01 — Shape, axis và broadcasting](../kien_thuc/02_du_lieu_toan_ml.md#d01).

**Mục tiêu:** thay vòng lặp phù hợp bằng phép toán mảng, phát hiện lỗi shape trước khi chạy. Broadcasting so khớp các chiều từ bên phải; mỗi cặp chiều phải bằng nhau hoặc có một chiều bằng 1. Vector hóa giúp biểu đạt phép tính trên cả lô mẫu, nhưng biểu thức tạo nhiều mảng trung gian vẫn có thể tốn bộ nhớ.

### Thực hành tuần 13

- **Cơ bản:** tạo `a = np.arange(24).reshape(6, 4)`; lấy hàng cuối, hai cột đầu và các phần tử chẵn; tính trung bình theo hàng/cột. Thay một phần tử trong `a[:2]`, rồi lặp lại với `.copy()` để quan sát sự khác biệt.
- **Vận dụng:** với `X = np.array([[1., 10., 7.], [3., 20., 7.], [5., 30., 7.]])`, viết hàm chuẩn hóa z-score bằng broadcasting; thay độ lệch chuẩn bằng 1 ở cột hằng. Đối chiếu kết quả vòng lặp bằng `np.allclose` và ghi shape từng bước.
- **Mở rộng:** đo hai cách chuẩn hóa trên mảng `(10000, 10)` bằng `timeit`, chạy nhiều lần; báo shape, dtype, `nbytes`, môi trường và thời gian, không kết luận một cách luôn nhanh hơn.

**Đầu ra:** `arrays.py`, `normalize.py` và bảng kết quả trong thư mục tuần.
**Tiêu chí đạt:** tổng của `a` trước khi sửa là 276; trung bình theo cột có shape `(4,)`; hai cách chuẩn hóa khớp nhau; cột hằng thành 0, các cột khác có trung bình gần 0, không có `NaN`/`inf`.
**Tự kiểm tra:** `(6,)` khác `(6,1)` ở đâu? Vì sao trừ mảng `(n,)` cho `(n,1)` có thể tạo `(n,n)`? Khi nào cần `.copy()` thay vì giữ lát cắt?

## Tuần 14 — Đọc, làm sạch và kết hợp dữ liệu bảng

### B27. Series, DataFrame và hợp đồng dữ liệu

**Đọc để hiểu bài:** [D02 — Bảng dữ liệu và join](../kien_thuc/02_du_lieu_toan_ml.md#d02).

**Mục tiêu:** đọc CSV, chọn hàng/cột bằng `.loc`/`.iloc`, kiểm tra kiểu, giá trị thiếu và trùng lặp. DataFrame gắn nhãn cho dữ liệu nên phép toán có thể căn theo index; đó là lý do hai cột bằng độ dài chưa chắc ghép đúng hàng. Hợp đồng dữ liệu mô tả mỗi cột có ý nghĩa gì và giá trị nào hợp lệ trước khi xử lý.

### B28. Join có kiểm soát và bảng dữ liệu sạch

**Đọc để hiểu bài:** [D02 — Bảng dữ liệu và join](../kien_thuc/02_du_lieu_toan_ml.md#d02).

**Mục tiêu:** phân biệt left/inner join, hiểu quan hệ nhiều-một, làm sạch theo quy tắc D1. Join là ghép theo khóa, không phải ghép theo thứ tự dòng; khóa trùng ở bảng tra cứu có thể nhân số dòng và làm tăng doanh thu giả. Bắt đầu bằng left join giúp nhìn thấy đơn không tìm được sản phẩm/khách hàng.

### Thực hành tuần 14

- **Cơ bản:** tự tạo D1; đọc ba CSV, lập bảng kiểu dữ liệu, số lượng thiếu và trùng. Giữ mã dưới dạng chuỗi; chuyển ngày bằng `pd.to_datetime(..., errors="coerce")`, số lượng bằng `pd.to_numeric(..., errors="coerce")`; ghi hợp đồng dữ liệu và các cờ lỗi, giữ nguyên raw.
- **Vận dụng:** áp dụng quy tắc D1, left join bảng tra cứu bằng `merge(..., validate="many_to_one", indicator=True)` để tìm khóa không khớp; đổi/xóa indicator trước join kế tiếp. Xuất clean/quarantine/audit và tính `revenue_vnd = quantity * unit_price_vnd` trên dòng sạch.
- **Mở rộng:** thêm sản phẩm P01 trùng khóa và một đơn cùng ID khác nội dung vào bản sao dữ liệu; chương trình phải phát hiện hai lỗi thay vì âm thầm đổi tổng tiền.

**Đầu ra:** `clean_data.py`, hợp đồng dữ liệu, `orders_clean.csv`, `orders_quarantine.csv`, `duplicate_audit.csv`.
**Tiêu chí đạt:** nhận ra số lượng thiếu, ngày sai, số lượng âm và khóa không tồn tại; 12 raw = 6 sạch + 5 cách ly + 1 bản sao; doanh thu đúng 1.300.000 VND; mọi dòng gốc được giải trình và khóa bảng tra cứu duy nhất.
**Tự kiểm tra:** inner join có thể che mất lỗi nào? Khi nào join làm số dòng tăng? Vì sao không nên tự điền số lượng bằng trung bình hoặc gọi `dropna()` cho cả bảng ngay lập tức?

## Tuần 15 — Phân tích khám phá và biểu đồ có ý nghĩa

### B29. Đặt câu hỏi và tổng hợp bằng pandas

**Đọc để hiểu bài:** [D03 — EDA và biểu đồ](../kien_thuc/02_du_lieu_toan_ml.md#d03).

**Mục tiêu:** chuyển một câu hỏi thành nhóm, phép tổng hợp và mẫu số rõ ràng. “Doanh thu theo vùng” cần tổng tiền; “giá trị trung bình một đơn” cần tổng tiền chia số đơn hợp lệ. Hai câu hỏi không thể thay nhau. EDA là tìm cấu trúc và vấn đề dữ liệu, đồng thời ghi lại giới hạn của nhận xét.

### B30. Chọn biểu đồ và kiểm tra cách diễn giải

**Đọc để hiểu bài:** [D03 — EDA và biểu đồ](../kien_thuc/02_du_lieu_toan_ml.md#d03).

**Mục tiêu:** dùng Matplotlib vẽ cột để so nhóm, đường cho thứ tự thời gian, histogram cho phân phối và scatter cho quan hệ hai biến. Biểu đồ là lập luận bằng dữ liệu: tên trục, đơn vị, mẫu số và phạm vi thời gian phải đủ để người khác hiểu. Quan hệ trên biểu đồ không tự chứng minh nguyên nhân.

### Thực hành tuần 15

- **Cơ bản:** dùng D1 sạch tính số đơn, tổng số lượng, doanh thu, giá trị trung bình một đơn; tổng hợp theo vùng/ngày/sản phẩm bằng `groupby`; xác nhận các tổng phụ khớp tổng toàn bộ.
- **Vận dụng:** viết báo cáo ngắn gồm biểu đồ cột doanh thu theo vùng, ba nhận xét có số liệu và hai giới hạn. Tạo bài minh họa riêng bằng RNG seed 42: `x=rng.normal(size=200)`, `y=2*x+rng.normal(size=200)`; vẽ histogram của x và scatter x-y để thực hành hai loại biểu đồ.
- **Mở rộng:** tạo lịch đủ 01–11/01 cho D1; phân biệt ngày không có dòng hợp lệ với ngày chắc chắn không bán hàng, rồi so hai cách hiển thị dữ liệu thiếu mà không mặc nhiên coi mọi giá trị điền 0 là sự thật kinh doanh.

**Đầu ra:** `eda.py`, CSV tổng hợp, ba ảnh PNG và `report.md` có chú thích từng hình.
**Tiêu chí đạt:** 6 đơn, tổng số lượng 12, doanh thu 1.300.000 VND, giá trị trung bình khoảng 216.666,67 VND; biểu đồ có tên trục/đơn vị, cột doanh thu bắt đầu từ 0; không kết luận xu hướng thị trường từ sáu dòng hoặc nhân quả từ scatter.
**Tự kiểm tra:** trung bình của các trung bình vùng có luôn bằng trung bình chung không? Khi nào biểu đồ đường tạo cảm giác thứ tự không có thật? Cần thêm dữ liệu gì trước khi khẳng định một vùng hoạt động tốt hơn?

## Tuần 16 — Toán đủ để hiểu mô hình học

### B31. Vector, ma trận và đạo hàm

**Đọc để hiểu bài:** [D04 — Vector, ma trận và thang đo](../kien_thuc/02_du_lieu_toan_ml.md#d04); [D05 — Đạo hàm và gradient descent](../kien_thuc/02_du_lieu_toan_ml.md#d05).

**Mục tiêu:** đọc được `y_hat = X @ w + b`, dot product, norm và đạo hàm của hàm đơn giản. Mỗi dự đoán tuyến tính là tổng các đặc trưng nhân trọng số cộng độ lệch. Đạo hàm cho biết một thay đổi nhỏ ở tham số làm đầu ra/loss đổi theo hướng nào; gradient gom thông tin này cho nhiều tham số.

### B32. Tự viết gradient descent cho hồi quy

**Đọc để hiểu bài:** [D05 — Đạo hàm và gradient descent](../kien_thuc/02_du_lieu_toan_ml.md#d05).

**Mục tiêu:** hiểu loss, learning rate, vòng lặp tối ưu và điều kiện dừng. Với `e=X@w+b-y`, dùng `MSE=mean(e**2)`, `dw=2*X.T@e/n`, `db=2*mean(e)` rồi cập nhật `w -= lr*dw`, `b -= lr*db`. Learning rate quá lớn có thể làm loss tăng hoặc phân kỳ; loss huấn luyện giảm chưa nói mô hình tổng quát hóa tốt.

### Thực hành tuần 16

- **Cơ bản:** tính tay rồi kiểm tra `X@w+b` với `X=[[1,2],[3,4]]`, `w=[2,-1]`, `b=3`. Với `f(w)=(w-3)**2`, so đạo hàm `2*(w-3)` tại 0, 2, 3 với sai phân trung tâm dùng `h=1e-5`; ghi shape và ý nghĩa các phép tính.
- **Vận dụng:** dùng D2 để tự viết gradient descent từ `w=zeros(2)`, `b=0`, learning rate 0,05, tối đa 1.000 bước; lưu loss và vẽ đường học. Thêm kiểm tra số hữu hạn; quan sát một lần thử learning rate 1,0 để nhận diện khả năng phân kỳ.
- **Mở rộng:** đối chiếu nghiệm với `np.linalg.lstsq` trên ma trận thêm cột 1; kiểm tra gradient nhiều chiều bằng sai phân và giải thích vì sao h quá lớn/quá nhỏ có thể gây sai số.

**Đầu ra:** `math_checks.py`, `gradient_descent.py`, biểu đồ loss và một trang tính tay.
**Tiêu chí đạt:** ví dụ dự đoán là `[3,5]`; sai số đạo hàm nhỏ hơn `1e-4`; D2 với thiết lập chuẩn có MSE cuối dưới 0,1, w gần `[3,-2]` và b gần 5 trong sai số 0,1. Đây là kiểm tra khôi phục quy luật tổng hợp, chưa chứng minh năng lực dự đoán thực tế.
**Tự kiểm tra:** `*` khác `@` ở đâu? Vì sao công thức gradient MSE có chia cho n? Loss train giảm hoặc gradient bằng 0 có đủ để khẳng định mô hình tốt trên dữ liệu mới không?

## Tuần 17 — Xác suất và thống kê để đánh giá bằng chứng

### B33. Biến ngẫu nhiên, lấy mẫu và khoảng tin cậy

**Đọc để hiểu bài:** [D06 — Xác suất và thống kê](../kien_thuc/02_du_lieu_toan_ml.md#d06).

**Mục tiêu:** phân biệt tổng thể, mẫu, kỳ vọng, phương sai và sai số do lấy mẫu. Trung bình của một mẫu là một ước lượng có thể đổi khi lấy mẫu khác. Khoảng tin cậy 95% mô tả độ bao phủ của một quy trình qua nhiều lần lấy mẫu; nó không có nghĩa tham số cố định có xác suất 95% nằm trong khoảng đã tính.

### B34. Kiểm định, kích thước hiệu ứng và tương quan

**Đọc để hiểu bài:** [D06 — Xác suất và thống kê](../kien_thuc/02_du_lieu_toan_ml.md#d06).

**Mục tiêu:** đặt giả thuyết trước khi tính, hiểu p-value có điều kiện theo giả thuyết không và các giả định; nó không phải xác suất giả thuyết không đúng. Chênh lệch nhỏ vẫn có thể có ý nghĩa thống kê khi mẫu lớn; ý nghĩa thực tế cần xét kích thước hiệu ứng và chi phí/quyết định liên quan.

### Thực hành tuần 17

- **Cơ bản:** với RNG mới seed 42, tạo 1.000 lần tung đồng xu bằng `binomial(1,0.5,size=1000)` và tính tỷ lệ mặt 1 ở 10/100/1.000 lượt đầu. Dùng RNG mới seed 42 tạo 200 số `normal(10,2,200)`; bootstrap có hoàn lại 2.000 lần, mỗi lần 200 số, lấy phân vị 2,5%/97,5% của trung bình để minh họa khoảng tin cậy.
- **Vận dụng:** dùng RNG mới seed 42 tạo A rồi B, mỗi nhóm 100 số, lần lượt từ `normal(10,2)` và `normal(10.5,2)`; đặt giả thuyết không “hai nhóm có cùng phân phối” trước khi tính chênh lệch trung bình B-A. Hoán vị nhãn 5.000 lần, chia lại 100/100; báo chênh lệch quan sát và p-value hai phía `(1+số |chênh_lệch_hoán_vị| >= |quan_sát|)/(5000+1)` cùng giả định hoán đổi được dưới giả thuyết không.
- **Mở rộng:** tạo `z=rng.normal(size=500)`, `x=z+rng.normal(0,0.2,500)`, `y=z+rng.normal(0,0.2,500)`; tính tương quan x-y, giải thích biến chung z và rủi ro chỉ báo kết quả nhỏ nhất sau khi thử nhiều giả thuyết.

**Đầu ra:** `sampling.py`, `permutation_test.py` và `evidence.md` chứa seed, khoảng bootstrap, giả thuyết và kết luận có điều kiện.
**Tiêu chí đạt:** bootstrap lấy mẫu có hoàn lại đúng kích thước; khoảng có hai đầu hữu hạn, đúng thứ tự; p-value nằm trong `[0,1]`; không đổi giả thuyết sau khi thấy kết quả, không diễn giải p-value là xác suất giả thuyết không đúng hay “chưa bác bỏ” là “đã chứng minh bằng nhau”.
**Tự kiểm tra:** bootstrap có sửa được mẫu thu thập thiên lệch không? Khoảng tin cậy 95% nói gì về quy trình lấy mẫu lặp lại? Vì sao một chênh lệch có ý nghĩa thống kê vẫn có thể không đáng kể trong thực tế?

## Tuần 18 — SQL, ETL và dự án P02

### B35. Truy vấn SQLite và đối chiếu bằng Python

**Đọc để hiểu bài:** [D07 — SQL và transaction](../kien_thuc/02_du_lieu_toan_ml.md#d07); [D02 — Bảng dữ liệu và join](../kien_thuc/02_du_lieu_toan_ml.md#d02).

**Mục tiêu:** dùng `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `JOIN`, khóa chính/ngoại và transaction. SQL mô tả kết quả bảng mong muốn; Python điều phối nhập, kiểm tra và xuất. Tham số truy vấn phải truyền qua placeholder `?`, không nối dữ liệu người dùng vào câu SQL. Khi cần SQLite kiểm tra khóa ngoại, bật `PRAGMA foreign_keys = ON` cho kết nối trước transaction.

### B36. P02 — Pipeline dữ liệu và báo cáo doanh thu

**Đọc để hiểu bài:** [D07 — SQL và transaction](../kien_thuc/02_du_lieu_toan_ml.md#d07); [D02 — Bảng dữ liệu và join](../kien_thuc/02_du_lieu_toan_ml.md#d02).

**Mục tiêu:** ghép đọc dữ liệu → kiểm tra → làm sạch → nạp → tổng hợp → báo cáo thành quy trình chạy lại được. ETL là trích xuất, biến đổi rồi nạp dữ liệu; mỗi giai đoạn cần đầu vào/đầu ra và cách giải trình lỗi. “Chạy lại được” còn có nghĩa chạy lần hai không nhân đôi đơn hoặc âm thầm đổi quy tắc xử lý.

### Thực hành tuần 18

- **Cơ bản:** nạp D1 sạch và hai bảng tra cứu vào SQLite bằng `sqlite3`; định nghĩa khóa chính/ngoại, bật thực thi khóa ngoại và dùng transaction. Truy vấn doanh thu theo vùng, lọc vùng bằng placeholder `?`; đối chiếu với pandas sau khi sắp xếp cùng khóa.
- **Vận dụng:** hoàn thành P02 bằng các hàm `load_raw`, `validate_and_clean`, `load_sqlite`, `summarize`, nhận đường dẫn qua `argparse`; tái sử dụng mã tuần 14–15. Xuất CSV, database, hai biểu đồ và báo cáo 1–2 trang; lưu số dòng qua từng bước, dùng khóa duy nhất và cách nạp idempotent để chạy lần hai không cộng dồn.
- **Mở rộng:** tạo 5.000 đơn hợp lệ với seed 42 từ các mã D1 và ngày tháng 1; cấy lỗi có kiểm soát, lưu số lỗi đã cấy rồi kiểm tra pipeline phát hiện được.

**Đầu ra:** `P02_data_report` gồm mã, raw CSV, SQLite, clean/quarantine/audit, CSV tổng hợp, hình, `report.md` và README có một lệnh chạy.
**Tiêu chí đạt:** hai lần chạy cho cùng tổng tiền/số dòng, SQL/pandas khớp số chuẩn D1; đầu vào vùng lạ trả rỗng; đơn tham chiếu P99 bị ràng buộc từ chối. Báo cáo nêu dữ liệu giả lập, giải trình sáu dòng không dùng, có ba phát hiện và hai giới hạn; một bước nạp lỗi không để database ở trạng thái nạp một phần.
**Tự kiểm tra:** `WHERE` khác `HAVING` ở đâu? Vì sao chỉ khai báo khóa ngoại có thể chưa đủ để SQLite thực thi? Khi nguồn được sửa, làm sao nhận biết thay đổi và tránh nhân đôi đơn?

## Tuần 19 — Biến vấn đề thành thí nghiệm ML

### B37. Đặc trưng, nhãn và chiến lược chia tập

**Đọc để hiểu bài:** [D08 — Chia tập, baseline và leakage](../kien_thuc/02_du_lieu_toan_ml.md#d08); [D09 — Mô hình tuyến tính và metric](../kien_thuc/02_du_lieu_toan_ml.md#d09).

**Mục tiêu:** xác định đầu vào có sẵn tại thời điểm dự đoán, nhãn cần dự đoán và đơn vị quan sát. Leakage xảy ra khi thông tin mà lúc dự đoán thật chưa có lọt vào huấn luyện hoặc lựa chọn mô hình. Tách test sớm giúp có phép đánh giá cuối ít chịu ảnh hưởng từ các quyết định phát triển.

### B38. Baseline và lựa chọn metric

**Đọc để hiểu bài:** [D08 — Chia tập, baseline và leakage](../kien_thuc/02_du_lieu_toan_ml.md#d08); [D09 — Mô hình tuyến tính và metric](../kien_thuc/02_du_lieu_toan_ml.md#d09).

**Mục tiêu:** biết mô hình có cải thiện hơn một quy tắc đơn giản hay không. Accuracy đo tỷ lệ dự đoán đúng; precision/recall trả lời hai loại câu hỏi về một lớp; macro-F1 lấy trung bình F1 từng lớp để mỗi lớp có trọng số ngang nhau. Metric chính cần chọn theo yêu cầu trước khi xem kết quả; nhãn nhiều lớp không có một lớp “dương” duy nhất nếu chưa quy định.

### Thực hành tuần 19

- **Cơ bản:** mô tả bài toán D3 bằng đầu vào → đầu ra, đơn vị mẫu và thời điểm dự đoán; đọc tên/ý nghĩa 13 đặc trưng và ba lớp. Chia, lưu chỉ số đúng hướng dẫn D3 vào `split_indices.json`; mọi EDA phục vụ lựa chọn mô hình từ đây chỉ dùng train, giữ test kín đến B48.
- **Vận dụng:** tự tính accuracy/ma trận nhầm lẫn cho `y_true=[0,0,0,1,1,2]`, `y_pred=[0,0,1,1,2,2]`; đối chiếu thư viện. Fit `DummyClassifier(strategy="most_frequent")` bằng D3 train, báo validation với macro-F1 chính, accuracy/recall từng lớp phụ; ghi số mẫu từng lớp và cách xử lý lớp không có dự đoán, ví dụ `zero_division=0`.
- **Mở rộng:** với `y=[10,20,30]`, `pred=[12,18,40]`, tính MAE/RMSE; giải thích vì sao RMSE nhạy với lỗi lớn hơn và đề xuất một baseline cho hồi quy.

**Đầu ra:** `problem.md`, script chia tập, `split_indices.json`, `baseline.py` và bảng baseline validation.
**Tiêu chí đạt:** split 106/36/36, không giao nhau, tổng đúng 178; row_id/nhãn không nằm trong đặc trưng; accuracy ví dụ là 4/6; metric chính được chọn trước kết quả, chưa đánh giá test. Ghi ít nhất một cột giả định có sẵn sau thời điểm dự đoán và lý do phải loại.
**Tự kiểm tra:** cùng khách hàng xuất hiện ở cả train/test có thể gây vấn đề gì? Accuracy cao có thể che recall kém của lớp hiếm thế nào? Vì sao đổi seed liên tục để lấy kết quả đẹp làm sai mục tiêu đánh giá?

## Tuần 20 — Mô hình tuyến tính và regularization

### B39. Hồi quy tuyến tính và residual

**Đọc để hiểu bài:** [D05 — Đạo hàm và gradient descent](../kien_thuc/02_du_lieu_toan_ml.md#d05); [D09 — Mô hình tuyến tính và metric](../kien_thuc/02_du_lieu_toan_ml.md#d09).

**Mục tiêu:** phân biệt tham số mô hình với siêu tham số, fit với predict và lỗi huấn luyện với lỗi trên mẫu chưa học. Residual `y-y_hat` cho biết phần mô hình chưa giải thích; cấu trúc có hệ thống trong residual có thể gợi ý mô hình thiếu quan hệ quan trọng. Hệ số lớn/nhỏ còn phụ thuộc đơn vị đặc trưng.

### B40. Logistic regression và độ phức tạp mô hình

**Đọc để hiểu bài:** [D09 — Mô hình tuyến tính và metric](../kien_thuc/02_du_lieu_toan_ml.md#d09).

**Mục tiêu:** hiểu logistic regression là bộ phân loại; điểm tuyến tính được chuyển thành xác suất và quy tắc chọn lớp. Regularization phạt độ lớn tham số để hạn chế khớp quá mức; với cấu hình regularization tương ứng trong scikit-learn, `C` nhỏ hơn thường nghĩa là phạt mạnh hơn. Xác suất dự đoán vẫn cần được kiểm tra, không tự động là độ tin cậy đúng.

### Thực hành tuần 20

- **Cơ bản:** chia D2 train/validation 80/20 với seed 42; so `DummyRegressor`, `LinearRegression` và Pipeline scaler/`Ridge(alpha=1.0)` trên cùng split bằng MAE/RMSE; xem hệ số và vẽ residual của hồi quy tuyến tính trên validation.
- **Vận dụng:** với D3, tạo Pipeline `StandardScaler`/`LogisticRegression(max_iter=2000)`, thử trước ba C `[0.1,1,10]`; báo macro-F1 validation, baseline tuần 19 và cảnh báo hội tụ nếu có. Lưu xác suất cho một batch, kiểm tra có ba cột và tổng từng hàng gần 1.
- **Mở rộng:** thêm đặc trưng gần trùng `X[:,0]+rng.normal(0,0.01,300)` vào D2; quan sát hệ số hồi quy tuyến tính/Ridge thay đổi thế nào khi dự đoán vẫn gần nhau, giải thích ảnh hưởng của đa cộng tuyến.

**Đầu ra:** `regression.py`, `logistic.py`, bảng metric và biểu đồ residual; ghi rõ D2/D3 là hai bài riêng.
**Tiêu chí đạt:** mọi preprocessing fit chỉ trên train, cùng split cho các mô hình được so; dự đoán được một hàng D2 shape `(1,2)`; chọn C theo tiêu chí đã ghi, không dùng test D3. Giải thích được tại sao bài D2 mới chỉ có validation, chưa có phép đánh giá test độc lập cuối.
**Tự kiểm tra:** R² âm có ý nghĩa gì? `predict_proba` khác `predict` thế nào? Vì sao tăng số vòng lặp không tự chữa overfitting và hệ số lớn chưa chứng minh quan hệ nhân quả?

## Tuần 21 — Cây quyết định và mô hình tổ hợp

### B41. Cây quyết định và overfitting

**Đọc để hiểu bài:** [D10 — Cây, Pipeline, PCA và artifact](../kien_thuc/02_du_lieu_toan_ml.md#d10).

**Mục tiêu:** đọc một đường đi từ gốc đến lá như chuỗi điều kiện. Cây sâu có thể chia dữ liệu đến mức ghi nhớ các trường hợp hiếm; hạn chế độ sâu hoặc số mẫu tối thiểu ở lá là cách giới hạn độ phức tạp. Một cây dễ minh họa, nhưng sự thay đổi nhỏ của dữ liệu có thể làm cây thay đổi nhiều.

### B42. Random forest, boosting và đánh đổi chi phí

**Đọc để hiểu bài:** [D10 — Cây, Pipeline, PCA và artifact](../kien_thuc/02_du_lieu_toan_ml.md#d10).

**Mục tiêu:** hiểu forest gom nhiều cây học trên dữ liệu/đặc trưng có biến đổi để giảm biến động; boosting thêm mô hình theo chuỗi để sửa phần lỗi còn lại. Nhiều cây hơn có thể tăng thời gian và kích thước mà không cải thiện đủ metric. Chọn mô hình cần tính cả độ dễ bảo trì và chi phí dự đoán.

### Thực hành tuần 21

- **Cơ bản:** fit `DecisionTreeClassifier` với `max_depth` `[2,4,None]`, seed 42 trên D3 train; ghi macro-F1 train/validation và số lá. Xuất quy tắc cây độ sâu 2 bằng `export_text`, giải thích đường đi của một hàng validation.
- **Vận dụng:** fit `RandomForestClassifier(n_estimators=100,max_depth=4,random_state=42)`; lập bảng so với logistic và cây gồm metric validation, thời gian fit, thời gian predict trên cùng batch. Nêu lựa chọn sơ bộ dựa trên chất lượng và chi phí, không ép mô hình phức tạp phải thắng.
- **Mở rộng:** thêm `GradientBoostingClassifier(n_estimators=100,max_depth=2,random_state=42)` vào bảng; giải thích cách cây được xây theo chuỗi khác forest ra sao và chi phí có đáng với kết quả quan sát không.

**Đầu ra:** `trees.py`, quy tắc cây và `model_comparison.csv` kèm mô tả cách đo thời gian.
**Tiêu chí đạt:** giữ nguyên split D3 và seed, phân biệt điểm train với validation; nhận diện dấu hiệu overfitting nếu xuất hiện; chưa mở test. Không kết luận một feature importance là bằng chứng nhân quả hoặc một cấu hình luôn tốt nhất ngoài bộ dữ liệu này.
**Tự kiểm tra:** một lá chỉ có một mẫu mang lại rủi ro gì? Vì sao cây thường không cần chuẩn hóa như hồi quy có regularization? Forest và boosting khác nhau thế nào về cách kết hợp cây?

## Tuần 22 — Pipeline, cross-validation và tìm siêu tham số

### B43. Tiền xử lý đúng chỗ với Pipeline/ColumnTransformer

**Đọc để hiểu bài:** [D08 — Chia tập, baseline và leakage](../kien_thuc/02_du_lieu_toan_ml.md#d08); [D10 — Cây, Pipeline, PCA và artifact](../kien_thuc/02_du_lieu_toan_ml.md#d10).

**Mục tiêu:** đóng gói biến đổi và mô hình thành một đối tượng nhận dữ liệu thô; áp dụng cách xử lý khác nhau cho cột số và cột phân loại. `fit` học trạng thái như trung bình/median/danh mục, còn `transform` áp dụng trạng thái đã học. Đặt chúng trong Pipeline giúp quá trình huấn luyện và dự đoán dùng cùng quy tắc.

### B44. Cross-validation và ngân sách tìm kiếm

**Đọc để hiểu bài:** [D08 — Chia tập, baseline và leakage](../kien_thuc/02_du_lieu_toan_ml.md#d08); [D10 — Cây, Pipeline, PCA và artifact](../kien_thuc/02_du_lieu_toan_ml.md#d10).

**Mục tiêu:** dùng nhiều cách chia trong train để so cấu hình ổn định hơn một lần chia. Mỗi fold có phần học và phần đánh giá riêng; toàn bộ tiền xử lý phải fit lại chỉ trong phần học của fold đó. CV dùng chọn cấu hình, do đó điểm tốt nhất từ nhiều thử nghiệm không phải phép đánh giá cuối độc lập.

### Thực hành tuần 22

- **Cơ bản:** tạo 200 dòng riêng với `i=np.arange(200)`, `amount=10+(i%17)`, `channel=np.where(i%2==0,"web","store")`, `y=(amount>18).astype(int)`; chia 80/20 seed 42. Sau khi chia, đặt mỗi dòng thứ 10 của từng tập thiếu amount và một hàng validation có channel `phone`; tạo ColumnTransformer với nhánh số impute/scale, nhánh chữ impute/`OneHotEncoder(handle_unknown="ignore")`, rồi ghép mô hình trong Pipeline.
- **Vận dụng:** với D3 train, dùng `StratifiedKFold(5,shuffle=True,random_state=42)` và `GridSearchCV` cho logistic/forest, tổng tối đa 12 cấu hình đã đặt trước. Estimator của CV là toàn bộ Pipeline có imputer và bước xử lý phù hợp; báo từng điểm fold/trung bình/độ lệch chuẩn, so ứng viên tốt nhất trên validation và lưu quyết định.
- **Mở rộng:** vẽ learning curve trong D3 train với cả Pipeline để xem thêm mẫu có thể giúp hay không; giữ nguyên test và không tăng ngân sách tìm kiếm theo kết quả đẹp/xấu.

**Đầu ra:** `mixed_columns.py`, `search.py`, `experiments.csv` chứa cấu hình, seed, metric, thời gian và quyết định.
**Tiêu chí đạt:** category `phone` dự đoán được nhưng không tự xuất hiện trong danh mục encoder sau predict; y không lọt vào X. Không fit imputer/scaler trước CV; mỗi fold chỉ học preprocessing từ phần train của fold; test còn kín, độ lệch chuẩn fold không bị gọi là khoảng tin cậy 95%.
**Tự kiểm tra:** fit scaler trên cả train rồi chỉ CV mô hình sai ở đâu? `handle_unknown="ignore"` có đồng nghĩa category mới được hiểu đúng không? Vì sao thử quá nhiều cấu hình dễ chọn trúng kết quả may mắn?

## Tuần 23 — Khám phá cấu trúc và đánh giá trong tình huống khó

### B45. Phân cụm và PCA

**Đọc để hiểu bài:** [D10 — Cây, Pipeline, PCA và artifact](../kien_thuc/02_du_lieu_toan_ml.md#d10); [D04 — Vector, ma trận và thang đo](../kien_thuc/02_du_lieu_toan_ml.md#d04).

**Mục tiêu:** phân biệt học không giám sát với phân loại có nhãn. KMeans nhóm điểm theo khoảng cách và tâm cụm; số cụm là lựa chọn của người làm. PCA tìm các hướng tuyến tính giữ nhiều phương sai, không tự tìm hướng tốt nhất cho nhãn. Cả hai đều chịu ảnh hưởng thang đo; “cụm 0” không đồng nghĩa “lớp 0”.

### B46. Lỗi theo nhóm, lớp hiếm và xác suất dự đoán

**Đọc để hiểu bài:** [D09 — Mô hình tuyến tính và metric](../kien_thuc/02_du_lieu_toan_ml.md#d09); [D08 — Chia tập, baseline và leakage](../kien_thuc/02_du_lieu_toan_ml.md#d08).

**Mục tiêu:** đọc lỗi từng lớp, hiểu ngưỡng quyết định và chọn cách chia theo bối cảnh. Dữ liệu theo thời gian phải tránh học từ tương lai; các dòng cùng đối tượng cần được chia theo nhóm khi mục tiêu là dự đoán đối tượng mới. Calibration hỏi: trong những dự đoán có xác suất khoảng 0,8, tần suất đúng có xấp xỉ 80% không? Đây là kỹ năng nhập môn tuần này, chưa phải yêu cầu tối ưu toàn bộ các trường hợp.

### Thực hành tuần 23

- **Cơ bản:** tạo `make_blobs(n_samples=300,centers=3,n_features=2,cluster_std=1.2,random_state=42)`, fit KMeans với `n_clusters=3,n_init=10,random_state=42`, vẽ cụm/tâm. Trên D3 train, fit StandardScaler rồi `PCA(n_components=2)`; vẽ hai thành phần và báo tổng `explained_variance_ratio_`.
- **Vận dụng:** xuất confusion matrix, lỗi theo row_id và recall từng lớp của ứng viên D3 cố định trên validation; nếu không có lỗi, xem năm hàng có `max(predict_proba)` nhỏ nhất. Làm thêm minh họa lớp hiếm bằng `make_classification(n_samples=1000,n_features=10,n_informative=5,n_redundant=2,weights=[0.9,0.1],random_state=42)`, split 80/20 phân tầng; so Dummy với Pipeline scaler/logistic qua precision, recall, average precision và log loss, quan sát ngưỡng `[0.3,0.5,0.7]` trên validation.
- **Mở rộng:** chọn một nhánh: hiệu chỉnh bài nhị phân bằng `CalibratedClassifierCV` với estimator là cả Pipeline, `cv=3`, fit chỉ train rồi so reliability plot/log loss validation; hoặc viết hai bài chia chỉ số với `groups=np.repeat(np.arange(50),4)`/GroupKFold và 200 ngày liên tiếp/TimeSeriesSplit.

**Đầu ra:** `structure.py`, hai biểu đồ, `errors.md` và bảng metric; ghi bằng lời chiến lược chia cho dữ liệu nhóm/thời gian dù chưa chọn nhánh mã mở rộng.
**Tiêu chí đạt:** không đánh đồng cụm với lớp hay giữ phương sai với giữ thông tin dự đoán; PCA dùng trong bộ dự đoán phải nằm trong Pipeline/CV. Phân biệt metric phân lớp/chất lượng xác suất; tránh giao nhóm và học từ tương lai khi bối cảnh yêu cầu. Bài lớp hiếm/calibration không dùng test D3; sau chọn ngưỡng bằng validation cần test độc lập trước tuyên bố chất lượng cuối.
**Tự kiểm tra:** đổi đơn vị một cột có thể thay KMeans thế nào? Accuracy 90% có thể đạt bằng quy tắc vô dụng nào trong bài lớp 90/10? Vì sao dự đoán đối tượng mới và lần mua tiếp theo của khách cũ có thể cần cách chia khác nhau?

## Tuần 24 — P03: bộ phân loại có thể bàn giao

### B47. Đóng gói thí nghiệm và chốt quyết định

**Đọc để hiểu bài:** [D10 — Cây, Pipeline, PCA và artifact](../kien_thuc/02_du_lieu_toan_ml.md#d10); [H11 — Artifact, Docker và CI](../kien_thuc/04_deep_learning_he_thong_agent.md#h11).

**Mục tiêu:** chuyển notebook thử nghiệm thành mã huấn luyện/dự đoán có schema, cấu hình và artifact rõ ràng. Một artifact dùng để phục vụ dự đoán phải chứa cả tiền xử lý đã học và mô hình; chỉ lưu trọng số rồi viết lại scaler riêng dễ làm đầu vào thay đổi. D3 là dự án giáo dục, nên ưu tiên quy trình dễ kiểm tra và tái tạo hơn tuyên bố chất lượng sản xuất.

### B48. Đánh giá test một lần và trình bày portfolio

**Đọc để hiểu bài:** [D08 — Chia tập, baseline và leakage](../kien_thuc/02_du_lieu_toan_ml.md#d08); [D09 — Mô hình tuyến tính và metric](../kien_thuc/02_du_lieu_toan_ml.md#d09); [H10 — Test, đánh giá và trace](../kien_thuc/04_deep_learning_he_thong_agent.md#h10).

**Mục tiêu:** tách việc sửa mô hình khỏi phép đánh giá cuối, trình bày bằng chứng cùng giới hạn. Sau khi pipeline và quy tắc dự đoán đã chốt, dùng test đo toàn bộ hệ thống đó. Test nhỏ tạo ước lượng có biến động; điểm cao không thay thế dữ liệu ngoài phân phối, kiểm tra vận hành hay xác thực yêu cầu thực tế.

### Thực hành tuần 24

- **Cơ bản:** tạo `P03_wine_classifier` từ mã các tuần trước, có `train.py`, `predict.py`, `config.json`; predict nhận CSV đúng 13 tên đặc trưng, không dùng target/row_id. Viết `decision.md` chốt đặc trưng, preprocessing, mô hình, siêu tham số và metric trước khi mở test; refit toàn bộ Pipeline trên train+validation, lưu artifact cùng schema, lớp, seed, phiên bản thư viện và dấu nhận diện artifact.
- **Vận dụng:** sau khi chốt ở B47, đánh giá artifact đúng một lần trên 36 hàng test ở B48; lưu macro-F1 chính, accuracy và precision/recall/F1/support từng lớp, confusion matrix, dự đoán theo row_id. Hoàn thành README, model card và demo batch, ghi riêng baseline validation, CV, validation và test; trình bày nguồn dữ liệu, quyết định, giới hạn và lệnh tái tạo.
- **Mở rộng:** kiểm tra đầu vào thiếu/dư cột, đảo thứ tự, số không hợp lệ và batch rỗng; chọn báo lỗi rõ hoặc sắp lại theo schema, không âm thầm bỏ cột. Thiết kế JSON đầu vào/đầu ra để dùng artifact này xây API ở chặng sau.

**Đầu ra:** dự án có mã, artifact, metadata, split, nhật ký thí nghiệm, `decision.md`, `test_metrics.json`, model card, README và demo dự đoán.
**Tiêu chí đạt:** chạy từ terminal, vòng lưu/tải giữ nguyên dự đoán trên mẫu kiểm tra kỹ thuật lấy từ train; chỉ tải pickle/joblib từ nguồn do mình tạo/tin cậy. Test được mở sau khi chốt quyết định, không đổi cấu hình theo test và không dùng ngưỡng accuracy tùy tiện để bắt thử lại. Nếu test kém, báo đúng kết quả và kế hoạch cải thiện; phiên bản tiếp theo cần đánh giá độc lập mới. Có thể chạy lại cùng artifact để xác nhận tái lập kỹ thuật, nhưng không coi đó là phép đánh giá độc lập mới.
**Tự kiểm tra:** refit train+validation có được học lại scaler trên phần này không? Vì sao dùng test chọn giữa hai artifact làm mất vai trò test? Cần lưu gì để xác nhận API đang chạy đúng artifact đã đánh giá và bộ 178 mẫu còn thiếu bằng chứng nào về vận hành thực tế?

## Cổng hoàn thành chặng

- **Dữ liệu:** P02 giải trình được 100% dòng D1, SQL/pandas khớp nhau, chạy lại không nhân đôi dữ liệu; biểu đồ có đơn vị và giới hạn.
- **Toán:** tự viết và giải thích được dự đoán tuyến tính, MSE, gradient descent; phân biệt biến động lấy mẫu với lỗi code và tương quan với nhân quả.
- **ML:** P03 giữ test kín đến sau quyết định, tiền xử lý nằm trong Pipeline của từng fold, có baseline và lỗi theo lớp; `predict.py` dùng đúng schema và artifact đã đánh giá.
- **Bàn giao:** người khác làm theo README có thể chạy lại; trình bày trong 5–7 phút vấn đề, dữ liệu, cách tránh leakage, kết quả và một giới hạn. Chưa đạt phần nào thì làm lại bài liên quan trước khi đi tiếp.

## Tài liệu chính thức để đọc đúng lúc

- B25–B26: [NumPy cho người mới](https://numpy.org/doc/stable/user/absolute_beginners.html), tra shape, axis, slicing và broadcasting khi gặp lỗi mảng.
- B27–B29: [pandas Getting started tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html), thực hành đọc bảng, chọn dữ liệu, tổng hợp và kết hợp bảng.
- B35–B36: [Python sqlite3](https://docs.python.org/3/library/sqlite3.html), tra kết nối, placeholder và transaction theo phiên bản đang dùng.
- B37–B44: [scikit-learn Getting Started](https://scikit-learn.org/stable/getting_started.html), tra mô hình estimator, `fit`, `predict` và Pipeline.
- B37–B48: [Các lỗi thường gặp và leakage](https://scikit-learn.org/stable/common_pitfalls.html). Quy tắc trọng tâm: tách dữ liệu trước biến đổi có học tham số; không `fit` preprocessing bằng dữ liệu đánh giá; đưa preprocessing vào Pipeline khi CV.
- B44–B46: [Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) để chọn splitter theo dữ liệu, và [Probability calibration](https://scikit-learn.org/stable/modules/calibration.html) để học đánh giá xác suất. Tài liệu API có thể thay đổi; đối chiếu phiên bản đã lưu trong dự án.
