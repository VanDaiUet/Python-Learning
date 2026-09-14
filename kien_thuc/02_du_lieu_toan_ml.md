# Hiểu dữ liệu, toán và Machine Learning — B25–B48

Tài liệu này giải thích kiến thức đứng sau [các bài B25–B48](../chuong_trinh/02_du_lieu_toan_ml.md).
Đọc mục tương ứng trước bài thực hành, tính ví dụ nhỏ bằng tay, rồi tự trả lời câu hỏi cuối mục.
Không cần thuộc mọi công thức ngay; cần chỉ được mỗi ký hiệu đại diện cho gì và kết quả dùng vào quyết định nào.
Các khối `# RUN: stdlib` chạy độc lập bằng Python, chỉ dùng thư viện chuẩn và không tạo tệp.
Các khối `# NEEDS: ...` cần thư viện ghi trên dòng đầu; chúng là ví dụ đối chiếu, không phải yêu cầu cài thêm ngay.
D1 là dữ liệu bán hàng giả lập rất nhỏ; D2 có quy luật tổng hợp; D3 là Wine dùng học quy trình phân loại.
Chất lượng của bài làm trước hết nằm ở phép tính đúng, giả định rõ và cách đánh giá trung thực.

| Bài đang học | Mục kiến thức nên đọc |
| --- | --- |
| B25–B26 | [D01 — Mảng và hình dạng](#d01) |
| B27–B28 | [D02 — Dữ liệu bảng và join](#d02) |
| B29–B30 | [D03 — EDA và biểu đồ](#d03) |
| B31 | [D04 — Vector và ma trận](#d04), [D05 — Đạo hàm](#d05) |
| B32 | [D05 — Loss và gradient descent](#d05) |
| B33–B34 | [D06 — Xác suất và thống kê](#d06) |
| B35–B36 | [D07 — SQL và ETL](#d07) |
| B37–B38 | [D08 — Bài toán ML và chia tập](#d08), [D09 — Metric](#d09) |
| B39–B40 | [D04](#d04), [D05](#d05), [D09 — Mô hình tuyến tính](#d09) |
| B41–B45 | [D08 — CV](#d08), [D10 — Cây, Pipeline và cấu trúc dữ liệu](#d10) |
| B46–B48 | [D09 — Lỗi và xác suất](#d09), [D10 — Đóng gói và tái lập](#d10) |

<a id="d01"></a>
## D01. Mảng: dữ liệu có hình dạng, trục và kiểu — B25–B26

**Cần biết trước:** list, chỉ số bắt đầu từ 0, vòng lặp, phép cộng và phép chia.

Một mảng là tập các giá trị được tổ chức theo các chiều; NumPy thường lưu các phần tử với một kiểu dữ liệu chung.
Với bảng ba người, mỗi người có chiều cao và cân nặng, ta quy ước mỗi hàng là một người, mỗi cột là một phép đo.
Khi đó `shape=(3, 2)` nghĩa là 3 hàng và 2 cột; `ndim=2` là số trục, còn `size=6` là số phần tử.
NumPy không biết cột nào là cân nặng: tên cột, đơn vị và thứ tự phải được người viết chương trình giữ đúng.
Trong AI, một lô dữ liệu bảng thường có shape `(n, d)`, trong đó `n` là số mẫu và `d` là số đặc trưng.
Ảnh có thể thêm trục chiều cao, chiều rộng, kênh màu; vì vậy kiểm tra shape là kiểm tra một phần ý nghĩa dữ liệu.

`axis` chỉ trục mà phép tổng hợp đi dọc theo để gom các giá trị.
Với `[[2, 10], [4, 20], [6, 30]]`, trung bình theo `axis=0` gom ba hàng, cho hai trung bình cột `[4, 20]`.
Trung bình theo `axis=1` gom hai cột trong từng hàng, cho `[6, 12, 18]`.
Shape lần lượt là `(2,)` và `(3,)`; “theo trục 0” không có nghĩa “giữ hàng 0”.
Gộp chiều cao và cân nặng thành một trung bình mỗi người có thể tính được nhưng không có ý nghĩa vì khác đơn vị.

**Broadcasting** cho phép ghép phép toán giữa những shape tương thích mà không cần viết vòng lặp từng hàng.
So các chiều từ bên phải: chúng phải bằng nhau hoặc một chiều bằng 1; chiều thiếu được xem như 1.
Ví dụ `(3, 2) - (2,)` tạo `(3, 2)`: mỗi hàng trừ cùng hai trung bình cột.
Xem quy tắc đầy đủ trong [tài liệu broadcasting của NumPy](https://numpy.org/doc/stable/user/basics.broadcasting.html).

```python
# NEEDS: numpy
import numpy as np

x = np.array([[2., 10.], [4., 20.], [6., 30.]])
mu = x.mean(axis=0)
centered = x - mu
print(x.shape, mu.shape)
print(mu.tolist())
print(centered.tolist())
part = x[:1]
part[0, 0] = 99
saved = x[:1].copy()
saved[0, 0] = -1
print(x[0, 0])
```

**Kết quả:** `(3, 2) (2,)`, rồi `[4.0, 20.0]`, rồi `[[-2.0, -10.0], [0.0, 0.0], [2.0, 10.0]]`, cuối cùng `99.0`.
Lát cắt `x[:1]` ở ví dụ chia sẻ vùng dữ liệu với `x`; sửa `part` sửa cả `x`. Bản `.copy()` độc lập về dữ liệu số này.
Không suy rộng rằng mọi phép chọn đều chia sẻ bộ nhớ: chọn bằng mảng chỉ số hoặc boolean mask thường tạo bản sao.

`dtype` là cách biểu diễn giá trị: số nguyên, số thực, boolean…; nó ảnh hưởng bộ nhớ, miền giá trị và độ chính xác.
Số nguyên NumPy có độ rộng cố định nên có thể tràn; số thực chỉ xấp xỉ, vì vậy thường so bằng `np.allclose`.
Gán `1.7` vào mảng số nguyên có thể mất phần thập phân; hãy tạo mảng số thực trước phép chuẩn hóa.
Một triệu phần tử `float64` cần khoảng 8 triệu byte cho dữ liệu; các mảng trung gian còn tốn thêm.

**Lỗi hay gặp và cách sửa.** `(3,)` là vector một trục, `(3, 1)` là ba hàng một cột, không thay thế nhau tùy ý.
Với `a=[1,2,3]`, phép `(3,1) - (3,)` cho ba hàng `[0,-1,-2]`, `[1,0,-1]`, `[2,1,0]`, không phải ba số 0.
Trước khi trừ nhãn và dự đoán, kiểm tra cả hai cùng shape `(n,)` hoặc cùng `(n,1)`; đừng chữa bằng reshape thiếu suy nghĩ.
Muốn sửa dữ liệu gốc thì gán rõ vào gốc; muốn thử trên bản riêng thì tạo `.copy()` trước khi sửa.

**Tự kiểm tra:** (1) Với shape `(5, 4)`, `sum(axis=0)` có shape gì? (2) Vì sao phép tính chạy được chưa chứng minh shape đúng?

**Đáp án:** (1) `(4,)`: mỗi cột có một tổng. (2) Broadcasting có thể tạo ma trận lớn ngoài ý muốn; cần đối chiếu cả shape lẫn ý nghĩa từng trục.

<a id="d02"></a>
## D02. Bảng dữ liệu, chất lượng và quan hệ giữa các bảng — B27–B28

**Cần biết trước:** dict, list các dict, dữ liệu CSV và [D01](#d01).

`Series` là một dãy có nhãn; `DataFrame` là bảng với tên cột và index cho các hàng.
Khác mảng số đồng nhất, mỗi cột trong bảng có thể có kiểu riêng: mã dạng chuỗi, ngày tháng, số lượng dạng số.
Index là nhãn kỹ thuật để chọn/căn hàng; nó không tự trở thành mã đơn hàng hay khóa duy nhất của nghiệp vụ.
`.loc` chọn theo nhãn, `.iloc` chọn theo vị trí: với index `[10,20]`, `.loc[20]` và `.iloc[1]` cùng lấy hàng thứ hai.
Phép cộng hai Series căn theo nhãn index, nên hai dãy cùng độ dài vẫn có thể cộng khác cặp bạn tưởng.
Ví dụ A có `a:10,b:20`, B có `b:1,a:2`; A+B cho `a:12,b:21`, không phải cộng theo thứ tự thành 11 và 22.

Trước khi làm sạch, cần một **hợp đồng dữ liệu**: mỗi hàng là gì, cột có nghĩa gì, giá trị và quan hệ nào hợp lệ.
Trong D1, mỗi hàng là một mặt hàng trong đơn; số lượng phải là số nguyên dương, ngày phải đọc được, mã phải tồn tại.
Số lượng thiếu là “chưa biết”, số lượng 0 là một con số cụ thể; đổi thiếu thành 0 làm thay đổi thông tin.
Dùng `.isna()` để nhận diện thiếu; chuỗi rỗng hoặc khoảng trắng có thể cần chuẩn hóa theo quy tắc riêng trước.
Lỗi chuyển kiểu nên có cờ giải trình: `to_numeric(..., errors="coerce")` biến dữ liệu không đổi được thành thiếu, không tự sửa nghĩa.

**Trùng hoàn toàn** là hai dòng giống mọi trường; **xung đột khóa** là cùng mã đơn nhưng khác nội dung.
D1 cho loại bản sao hoàn toàn và ghi nhật ký; xung đột mã đơn phải được báo để xử lý, không chọn tùy tiện dòng đầu.
Tách `raw` giữ nguyên, `clean` hợp lệ và `quarantine` có lý do giúp truy vết một tổng tiền trở lại dữ liệu ban đầu.
Một dòng có thể có nhiều lỗi, nhưng khi đếm tổng dòng cách ly phải đếm mã dòng duy nhất, tránh cộng lặp từng cờ lỗi.

**Join** tìm các dòng có cùng khóa giữa hai bảng. `left join` giữ mọi dòng bên trái; `inner join` chỉ giữ các dòng khớp.
Quan hệ nhiều-một nghĩa là nhiều đơn có thể dùng cùng sản phẩm nhưng bảng sản phẩm chỉ có một dòng cho mỗi mã.
Nếu có hai đơn P01 và ba dòng tra cứu P01, join tạo `2 × 3 = 6` dòng; doanh thu có thể tăng giả dù câu lệnh không lỗi.
`validate="many_to_one"` kiểm tra dạng quan hệ; `indicator=True` chỉ nguồn khớp, như `left_only` và `both`.
Khóa thiếu cần kiểm tra trước vì pandas có thể ghép các khóa null với nhau, khác hành vi JOIN SQL thông thường. [API merge chính thức](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html).

```python
# NEEDS: pandas
import pandas as pd

orders = pd.DataFrame({"product_id": ["P01", "P99"], "quantity": [2, 1]})
products = pd.DataFrame({"product_id": ["P01"], "price": [100000]})
joined = orders.merge(products, how="left", on="product_id",
                      validate="many_to_one", indicator=True)
print(len(joined))
print(joined["_merge"].astype(str).tolist())
clean = joined.loc[joined["_merge"] == "both"].copy()
clean["revenue"] = clean["quantity"] * clean["price"]
print(clean["revenue"].sum())
```

**Kết quả:** `2`, `['both', 'left_only']`, rồi `200000.0`; P99 còn hiện ra để điều tra thay vì mất dấu.
Giá thành số thực trong ví dụ vì dòng không khớp tạo giá thiếu; với tiền VND sạch có thể kiểm tra rồi dùng kiểu nguyên phù hợp.
Đây chỉ là minh họa join; quy trình D1 đầy đủ còn kiểm tra ngày, số lượng, khách hàng và xung đột khóa.
D1 chuẩn phải giải trình `12 raw = 1 bản sao + 5 cách ly + 6 sạch`; 6 dòng sạch có doanh thu 1.300.000 VND.
Trong AI, join nhầm cũng có thể ghép đặc trưng của người này với nhãn của người khác, làm hỏng cả học và đánh giá.

**Lỗi hay gặp và cách sửa.** Gọi `dropna()` cả bảng có thể loại nhiều dòng vì một cột không quan trọng; xác định cột bắt buộc trước.
Tự điền số lượng bằng trung bình tạo giao dịch chưa từng biết là có thật; giữ thiếu và cách ly theo hợp đồng D1.
Gán liên tiếp kiểu `df[mask]["x"] = ...` gây khó hiểu; dùng `df.loc[mask, "x"] = ...` hoặc sửa bản `.copy()` đã chủ động tạo.
Kiểm tra số dòng, tính duy nhất của khóa và tổng tiền trước/sau join, thay vì chỉ nhìn vài dòng đầu.

**Tự kiểm tra:** (1) Inner join che được lỗi gì trong ví dụ? (2) Hai dòng cùng mã đơn nhưng khác số lượng có được gọi là bản sao hoàn toàn?

**Đáp án:** (1) P99 không có trong bảng sản phẩm biến mất khỏi kết quả. (2) Không; đó là xung đột khóa, cần báo và giữ bằng chứng.

<a id="d03"></a>
## D03. EDA: hỏi đúng, tổng hợp đúng và nhìn đúng — B29–B30

**Cần biết trước:** [D02](#d02), phần trăm và trung bình cộng.

EDA, tức phân tích khám phá dữ liệu, là quá trình tìm hiểu cấu trúc, phân phối, lỗi và các quan hệ đáng kiểm tra.
Nó bắt đầu bằng câu hỏi có thể trả lời: “Doanh thu của các đơn hợp lệ trong D1 khác nhau giữa vùng thế nào?”
Phạm vi “đơn hợp lệ trong D1” giữ cho câu trả lời phù hợp dữ liệu; “vùng nào kinh doanh tốt nhất cả nước?” vượt quá bằng chứng.
Đơn vị quan sát quyết định mẫu số: trung bình mỗi dòng, mỗi đơn, mỗi khách và mỗi ngày là những đại lượng khác nhau.
Nếu một đơn có nhiều dòng hàng, đếm dòng không còn bằng đếm đơn; D1 chỉ đơn giản vì đã quy định mỗi dòng là một mặt hàng trong đơn.

**Tổng** trả lời quy mô, **trung bình** trả lời mức trên một đơn vị, **trung vị** là giá trị ở giữa sau sắp xếp.
Với `[100,100,100,1000]`, trung bình là 325 nhưng trung vị là 100: một giá trị lớn kéo trung bình lên.
Phân vị 25%, 50%, 75% mô tả các vị trí trong phân phối; khi mẫu nhỏ, quy tắc nội suy của công cụ có thể khác nhau.
“Ngoại lệ” chỉ là điểm khác phần lớn dữ liệu; cần kiểm tra đó là lỗi nhập hay một trường hợp lớn có thật trước khi loại.

Giá trị trung bình của một đơn D1 là `1.300.000 / 6 ≈ 216.666,67 VND`.
Doanh thu ba vùng là Bắc 500.000, Trung 600.000, Nam 200.000 VND; tổng phụ phải khớp tổng chung.
Trung có doanh thu lớn nhất **trong sáu dòng sạch này**; chưa đủ mẫu, độ phủ hay bối cảnh để giải thích hiệu quả kinh doanh.
Không có dòng hợp lệ một ngày có thể do không bán, thiếu ghi nhận hoặc toàn bộ dòng bị cách ly; chỉ dữ liệu hiện có chưa phân biệt được.

**Ví dụ tính tay và chạy đối chiếu:** hai nhóm có số đơn rất khác nhau.

```python
# RUN: stdlib
groups = {"A": [100, 100, 100], "B": [1000]}
means = {name: sum(values) / len(values) for name, values in groups.items()}
wrong = sum(means.values()) / len(means)
total = sum(sum(values) for values in groups.values())
count = sum(len(values) for values in groups.values())
print(means)
print(wrong, total / count)
```

**Kết quả:** `{'A': 100.0, 'B': 1000.0}`, rồi `550.0 325.0`.
550 gán mỗi nhóm cùng trọng số; 325 gán mỗi đơn cùng trọng số và là trung bình mỗi đơn cần tìm.
Công thức đúng là `(100 × 3 + 1000 × 1) / (3 + 1)`; trọng số chính là số đơn mỗi nhóm.

| Câu hỏi | Biểu đồ | Điều cần ghi rõ |
| --- | --- | --- |
| Nhóm nào có tổng lớn hơn? | Cột | Trục giá trị bắt đầu từ 0, đơn vị, phạm vi dữ liệu |
| Đại lượng đổi theo thời gian thế nào? | Đường | Thời gian theo thứ tự, khoảng thiếu được chú thích |
| Các giá trị tập trung ở đâu? | Histogram | Khoảng chia, số đếm hay mật độ, đơn vị |
| Hai phép đo đi cùng nhau thế nào? | Scatter | Mỗi điểm đại diện cho gì, tên và đơn vị hai trục |

Trong histogram, đổi độ rộng khoảng chia có thể làm hình dạng trông khác; xem nhiều cách chia hợp lý và báo lựa chọn.
Với biểu đồ cột doanh thu, trục bắt đầu từ 490.000 khiến 500.000 và 600.000 trông chênh lệch quá lớn so với tỷ lệ thật 1,2.
Với scatter, Pearson `r` nằm trong `[-1,1]` khi tính được và đo mức quan hệ tuyến tính, không đo mọi dạng quan hệ.
Ví dụ `x=[-2,-1,0,1,2]`, `y=x²` có quan hệ hoàn toàn xác định nhưng tương quan tuyến tính bằng 0 do tính đối xứng.
Hai đại lượng cùng tăng còn có thể do biến thứ ba; ví dụ nhiệt độ cùng ảnh hưởng lượng kem bán và số người đi bơi.
Để nói về nguyên nhân cần thiết kế nghiên cứu và giả định phù hợp, không chỉ đường xu hướng đẹp.
Trong ML, EDA giúp phát hiện cột sai đơn vị, lớp hiếm và nhóm thiếu đại diện trước khi chúng biến thành lỗi dự đoán.

**Lỗi hay gặp và cách sửa.** Gọi một cột là “revenue” nhưng không ghi VND hay triệu VND gây sai tỷ lệ 1.000.000 lần; ghi đơn vị ở cả dữ liệu và hình.
Xem test để chọn biến sau đó tuyên bố test độc lập là rò rỉ; từ B37, EDA phục vụ chọn mô hình chỉ dùng train.
Chỉ chọn biểu đồ ủng hộ nhận xét đã thích làm mất bối cảnh; đối chiếu với số mẫu, dữ liệu thiếu và các góc nhìn liên quan.

**Tự kiểm tra:** (1) Vì sao trung bình hai trung bình có thể sai? (2) Tương quan bằng 0 có chứng minh hai biến không liên quan?

**Đáp án:** (1) Nếu cỡ nhóm khác nhau, nó đổi trọng số từ mỗi mẫu sang mỗi nhóm. (2) Không; quan hệ cong như `y=x²` vẫn có thể rõ.

<a id="d04"></a>
## D04. Vector, ma trận và thang đo — B31, B39, B45

**Cần biết trước:** [D01](#d01), tổng, bình phương và căn bậc hai.

Vector là một danh sách số có thứ tự, có thể biểu diễn một mẫu hoặc một bộ trọng số.
Với hai đặc trưng, `x=[x₁,x₂]` là một mẫu, `w=[w₁,w₂]` là trọng số; đổi thứ tự đặc trưng mà giữ nguyên w làm đổi nghĩa dự đoán.
Tích vô hướng, viết `x · w`, bằng `x₁w₁ + x₂w₂`; kết quả là một số.
Mỗi đặc trưng đóng góp một phần vào tổng; trọng số âm làm điểm giảm khi đặc trưng tăng và những đặc trưng khác giữ nguyên.
Điều “giữ nguyên” này quan trọng: nó mô tả mô hình đã fit, không chứng minh can thiệp thực tế sẽ có cùng tác động.

Ma trận `X` gom `n` vector hàng, mỗi hàng có `d` phần tử; ký hiệu `Xᵀ` là chuyển vị, đổi hàng thành cột.
Quy tắc nhân là `(n,d) @ (d,k) → (n,k)`: hai chiều phía trong phải bằng nhau để ghép các phần tử của tích vô hướng.
Với vector w shape `(d,)`, `X @ w` cho `(n,)`; thêm số b sẽ cộng cùng một độ lệch vào mọi dự đoán.
Mô hình tuyến tính là `ŷ = Xw + b`; `ŷ` đọc “y mũ”, tức giá trị dự đoán, còn `y` là giá trị quan sát.
Ví dụ `X=[[1,2],[3,4]]`, `w=[2,-1]`, `b=3` cho hàng đầu `1×2+2×(-1)+3=3`, hàng sau `3×2+4×(-1)+3=5`.

```python
# RUN: stdlib
from math import sqrt

X = [[1, 2], [3, 4]]
w, b = [2, -1], 3
assert all(len(row) == len(w) for row in X)
prediction = [sum(value * weight for value, weight in zip(row, w)) + b for row in X]
v = [3, 4]
norm = sqrt(sum(value ** 2 for value in v))
distance = sqrt(sum((a - b_) ** 2 for a, b_ in zip(X[0], X[1])))
print(prediction)
print(norm, round(distance, 4))
```

**Kết quả:** `[3, 5]`, rồi `5.0 2.8284`; hai hàng cách nhau `√((1−3)²+(2−4)²)=√8`.
Chuẩn Euclid, ký hiệu `||v||₂`, là độ dài `√(v₁²+…+v_d²)`; khoảng cách giữa a và b là chuẩn của `a−b`.
Trong NumPy, `*` nhân từng phần tử, `@` nhân ma trận; hai phép có thể cùng chạy nhưng trả ý nghĩa khác nhau.

**Chuẩn hóa z-score** đưa một cột về thang đo dựa trên trung bình và độ lệch chuẩn đã học.
Với giá trị x, `z=(x−μ)/s`, trong đó μ là trung bình cột train và s là độ lệch chuẩn của cột train.
Ví dụ cột train `[10,20,30]` có μ=20; dùng phương sai chia n được `s²=(100+0+100)/3=200/3`.
Do đó s≈8,165 và z≈`[-1,2247; 0; 1,2247]`; giá trị mới 40 dùng cùng μ, s sẽ thành khoảng 2,4495.
Không tính lại trung bình trên từng lô dự đoán: cùng một người sẽ có đầu vào khác nhau tùy ai xuất hiện cùng lô.
Nếu cột train luôn là 7 thì s=0; quy ước chia cho 1 đưa train về 0 và tránh chia cho 0, không tạo thêm thông tin phân biệt.
Giá trị mới khác 7 vẫn phải được biến đổi theo trạng thái đã học và có thể cần kiểm tra thay đổi phân phối.

Chuẩn hóa có ích khi thuật toán dựa trên khoảng cách hoặc mức phạt trọng số: cột nghìn đơn vị dễ lấn cột chỉ vài đơn vị.
Ví dụ chênh 1 mét và 10 kilôgam cho bình phương khoảng cách `1+100`; đổi mét thành centimét cho `10000+100` dù vật không đổi.
KMeans, PCA và mô hình tuyến tính có regularization có thể chịu ảnh hưởng này; cây chia theo ngưỡng thường ít cần chuẩn hóa.
“Chuẩn hóa đặc trưng” không đồng nghĩa “chuẩn hóa từng vector về độ dài 1”; thao tác sau giữ hướng nhưng thay độ dài mỗi mẫu.
Cosine similarity so hướng bằng `(a·b)/(||a||₂||b||₂)` khi hai chuẩn khác 0; hai vector cùng hướng có cosine 1 dù độ dài khác.
Ý tưởng này xuất hiện khi so embedding văn bản, nhưng lựa chọn độ đo vẫn phải phù hợp cách embedding được tạo.

**Lỗi hay gặp và cách sửa.** `zip` dừng ở dãy ngắn hơn; kiểm tra chiều trước khi dùng ví dụ thuần Python cho dữ liệu bất kỳ.
Thấy hệ số cột A lớn hơn B rồi gọi A quan trọng hơn là thiếu thông tin: trước hết xem đơn vị, tương quan và cách mô hình được fit.
Đổi scaler sau huấn luyện khiến mô hình nhận hệ tọa độ mới; lưu và dùng lại scaler cùng mô hình.

**Tự kiểm tra:** (1) `(8,3) @ (3,2)` cho shape gì? (2) Vì sao dữ liệu validation không được tự chuẩn hóa bằng trung bình riêng?

**Đáp án:** (1) `(8,2)`. (2) Mô hình đã học trong hệ tọa độ train; cần áp dụng cùng phép biến đổi và giữ đánh giá độc lập với việc học trạng thái.

<a id="d05"></a>
## D05. Đạo hàm, loss và cách tham số được học — B31–B32

**Cần biết trước:** hàm Python, đồ thị hàm đơn giản và [D04](#d04).

Đạo hàm đo tốc độ thay đổi cục bộ: nếu tăng w một lượng nhỏ h thì `f(w+h)−f(w)` xấp xỉ `f′(w)×h`.
Với `f(w)=(w−3)²`, đạo hàm là `f′(w)=2(w−3)`; ở w=0 nó bằng −6, nghĩa là tăng w một chút làm f giảm.
Ở w=3, đạo hàm bằng 0; với hàm này đó là điểm thấp nhất, nhưng đạo hàm 0 của hàm bất kỳ cũng có thể là cực đại hoặc điểm yên ngựa.
Gradient là vector các đạo hàm theo từng tham số, cho biết mỗi tham số làm loss đổi thế nào khi các tham số còn lại giữ nguyên.

Mô hình dự đoán bằng tham số, rồi **loss** biến mức sai thành số để thuật toán tối ưu.
Đặt `eᵢ=ŷᵢ−yᵢ` là lỗi mẫu i; MSE, tức trung bình lỗi bình phương, bằng `L=(e₁²+…+eₙ²)/n`.
Bình phương làm lỗi âm và dương không triệt tiêu, đồng thời phạt lỗi lớn mạnh hơn; đơn vị MSE là bình phương đơn vị y.
Residual thường được viết `rᵢ=yᵢ−ŷᵢ`, ngược dấu e ở đây; nhất quán dấu khi suy ra gradient.

**Quy tắc dây chuyền** nối các bước phụ thuộc: L phụ thuộc e, e phụ thuộc ŷ và ŷ phụ thuộc w.
Với một mẫu `ŷ=wx+b`, ta có `d(e²)/de=2e`, `de/dŷ=1`, `dŷ/dw=x`, nên `d(e²)/dw=2ex`.
Lấy trung bình n mẫu cho `dL/dw=(2/n)Σeᵢxᵢ` và `dL/db=(2/n)Σeᵢ`; ký hiệu Σ nghĩa là cộng theo mọi mẫu.
Với nhiều đặc trưng, công thức gọn là `dw=2Xᵀe/n`; shape `(d,n) @ (n,)` trả d đạo hàm.
Chia n khiến mục tiêu là lỗi trung bình: lặp đôi đúng dữ liệu không tự nhân đôi gradient như khi dùng tổng lỗi.

**Gradient descent** cập nhật `w_mới=w_cũ−η×dw`, tương tự với b; η đọc eta là learning rate, tức cỡ bước.
Dấu trừ đi ngược hướng loss tăng; learning rate nhỏ đi chậm, quá lớn có thể vượt qua vùng tốt và làm loss tăng.
Tính mọi gradient ở cùng trạng thái tham số cũ trước khi cập nhật, tránh trộn w mới với b cũ khi chưa chủ đích.

```python
# RUN: stdlib
x, y = [1.0, 2.0], [2.0, 4.0]
w, b, rate = 0.0, 0.0, 0.1
n = len(x)
error = [w * value + b - target for value, target in zip(x, y)]
loss_before = sum(e * e for e in error) / n
dw = 2 * sum(e * value for e, value in zip(error, x)) / n
db = 2 * sum(error) / n
w, b = w - rate * dw, b - rate * db
prediction = [w * value + b for value in x]
loss_after = sum((p - target) ** 2 for p, target in zip(prediction, y)) / n
print(error, loss_before, dw, db)
print(round(w, 2), round(b, 2), [round(p, 2) for p in prediction], round(loss_after, 2))
```

**Tính theo từng bước:** ban đầu dự đoán `[0,0]`, lỗi `[-2,-4]`, MSE=`(4+16)/2=10`.
Gradient w là `2×((-2)×1+(-4)×2)/2=−10`; gradient b là `2×(-2−4)/2=−6`.
Sau một bước η=0,1, w=1 và b=0,6; dự đoán `[1,6; 2,6]`, MSE=`(0,16+1,96)/2=1,06`.
Hai dòng in là `[-2.0, -4.0] 10.0 -10.0 -6.0` và `1.0 0.6 [1.6, 2.6] 1.06`.
Loss đã giảm nhưng chưa bằng 0; quy luật dữ liệu ở đây là w=2,b=0, không thể kết luận đã học xong chỉ sau một bước.

Có thể kiểm tra công thức bằng sai phân trung tâm `[f(w+h)−f(w−h)]/(2h)` với h nhỏ, chẳng hạn `1e-5`.
h quá lớn đo thay đổi trên đoạn dài; h quá nhỏ có thể mất chữ số khi trừ hai số gần nhau trong số thực máy tính.
Mạng nơ-ron dùng cùng ý tưởng dây chuyền qua nhiều lớp; backpropagation tính các gradient có tổ chức và tái sử dụng kết quả trung gian.
Full-batch dùng toàn bộ train mỗi bước; mini-batch dùng một nhóm nhỏ nên gradient có biến động, đổi lại bước cập nhật thường nhẹ hơn.
Loss tối ưu và metric báo cáo có thể khác nhau: phân loại thường tối ưu log loss nhưng báo thêm macro-F1.

**Lỗi hay gặp và cách sửa.** Loss tăng liên tục: kiểm tra dấu gradient, shape, số hữu hạn, thang đo và learning rate.
Không mặc định tăng số vòng lặp chữa được mọi lỗi; mô hình có thể đang ghi nhớ nhiễu hoặc thiếu đặc trưng phù hợp.
Điều kiện dừng có thể dựa trên số bước, mức cải thiện nhỏ hoặc tiêu chí validation đã định; không dùng test để quyết định dừng.

**Tự kiểm tra:** (1) Nếu gradient dương, cập nhật descent tăng hay giảm tham số? (2) MSE train thấp chứng minh điều gì và chưa chứng minh điều gì?

**Đáp án:** (1) Giảm tham số khi learning rate dương. (2) Khớp tốt dữ liệu train theo MSE; chưa chứng minh dự đoán tốt trên mẫu mới hay đúng quan hệ nhân quả.

<a id="d06"></a>
## D06. Xác suất, lấy mẫu và mức độ bằng chứng — B33–B34

**Cần biết trước:** tỷ lệ, trung bình, bình phương; nên đọc [D03](#d03).

Một biến cố là điều có thể xảy ra, như “lấy được sản phẩm lỗi”; xác suất biểu diễn mức khả năng trong mô hình đang xét.
Biến ngẫu nhiên gán một số cho kết quả, chẳng hạn Z=1 nếu sản phẩm lỗi và Z=0 nếu không lỗi.
Kỳ vọng `E[Z]=Σz×P(Z=z)` là trung bình có trọng số xác suất; nếu xác suất lỗi p=0,1 thì E[Z]=0,1.
Không sản phẩm nào có trạng thái “0,1 lỗi”; kỳ vọng mô tả mức trung bình của biến qua nhiều lần lấy mẫu theo mô hình.
Phương sai `Var(Z)=E[(Z−E[Z])²]` đo độ phân tán quanh kỳ vọng; độ lệch chuẩn là căn của phương sai, cùng đơn vị với Z.

**Xác suất có điều kiện** `P(A|B)=P(A và B)/P(B)` khi P(B)>0: chỉ xét những trường hợp B xảy ra rồi hỏi tỷ lệ A.
Trong 100 sản phẩm có 20 sản phẩm từ máy B, trong đó 4 lỗi; cả xưởng có tổng 10 sản phẩm lỗi.
`P(lỗi|máy B)=4/20=0,2`, còn `P(máy B|lỗi)=4/10=0,4`; đổi thứ tự điều kiện là đổi câu hỏi và mẫu số.
Hai biến cố độc lập nếu biết một biến cố không đổi xác suất biến cố kia; đừng nhầm với “không thể xảy ra cùng lúc”.
Định lý Bayes viết `P(A|B)=P(B|A)P(A)/P(B)`, giúp đổi chiều điều kiện khi có các xác suất nền phù hợp.
Trong AI, precision và recall chính là hai kiểu điều kiện khác nhau; tỷ lệ lớp nền ảnh hưởng cách hiểu một cảnh báo.

**Tổng thể** là các đối tượng muốn kết luận về; **mẫu** là phần thực sự quan sát được.
Ước lượng trung bình mẫu `x̄=Σxᵢ/n` thay đổi theo mẫu; độ lệch chuẩn dữ liệu đo khác nhau giữa các mẫu quan sát trong một tập.
Sai số chuẩn của trung bình mô tả mức biến động của x̄ khi lấy mẫu lặp; với mẫu độc lập có cùng phân phối, ước lượng thường là `s/√n`.
Ở đây `s²=Σ(xᵢ−x̄)²/(n−1)` là phương sai mẫu dùng ước lượng phương sai tổng thể, cần n>1.
Chia n mô tả độ phân tán của tập đang có; chia n−1 bù phần thông tin đã dùng để ước lượng trung bình trong bối cảnh này.

```python
# RUN: stdlib
from statistics import mean, pvariance, variance
from math import sqrt

values = [2, 4, 6, 8]
print(mean(values), pvariance(values), round(variance(values), 4))
print(round(sqrt(variance(values) / len(values)), 4))
print(4 / 20, 4 / 10)
```

**Kết quả:** `5 5 6.6667`, rồi `1.291`, rồi `0.2 0.4`.
Tính tay: lệch khỏi 5 là `[-3,-1,1,3]`, tổng bình phương lệch bằng 20; chia 4 được 5, chia 3 được 6,6667.
Mẫu chỉ bốn điểm dùng để hiểu phép tính, chưa là lý do áp dụng máy móc khoảng chuẩn 95% bằng x̄±1,96×s/√n.

**Khoảng tin cậy 95%** là kết quả một quy trình có độ bao phủ khoảng 95% qua nhiều mẫu lặp nếu giả định phù hợp.
Ví dụ μ thật cố định là 10: tính 100 khoảng từ 100 mẫu mới, một quy trình đạt chuẩn sẽ bao phủ 10 khoảng 95 lần về lâu dài.
Không đảm bảo đúng 95 lần ở mọi nhóm 100 lần; cũng không có nghĩa 95% giá trị riêng lẻ nằm trong khoảng của trung bình.
Với khoảng đã tính theo cách hiểu tần suất, μ không được gán xác suất 95%; khoảng này hoặc chứa μ hoặc không.
Bootstrap lấy n phần tử **có hoàn lại** từ n điểm đang có, tính lại thống kê nhiều lần để xấp xỉ sự biến động do lấy mẫu.
Ví dụ mẫu `[2,4,6,8]` có thể cho lượt bootstrap `[4,4,8,2]`, trung bình 4,5; điểm 4 xuất hiện hai lần là hợp lệ.
Lấy phân vị 2,5% và 97,5% của các trung bình bootstrap tạo khoảng percentile; độ bao phủ thực phụ thuộc dữ liệu và phương pháp.
Bootstrap không chữa được mẫu chỉ thu từ một nhóm tiện tiếp cận; dữ liệu phụ thuộc theo người/thời gian cần cách lấy lại mẫu phù hợp.

**Kiểm định** bắt đầu bằng giả thuyết không H₀ và thống kê đã chọn trước, chẳng hạn chênh lệch trung bình B−A.
P-value là xác suất, dưới H₀ và giả định kiểm định, thu được thống kê ít nhất cực đoan như đã thấy; không phải xác suất H₀ đúng.
Trong kiểm định hoán vị, trộn nhãn nhóm hợp lệ khi các quan sát có thể hoán đổi dưới H₀; dữ liệu ghép cặp cần giữ cấu trúc cặp.
Nếu B−A quan sát là 0,8 và có 24 trong 999 hoán vị có trị tuyệt đối ≥0,8, ước lượng có hiệu chỉnh là `(24+1)/(999+1)=0,025`.
Đây là số đếm giả định để giải thích công thức, không phải kết quả đã đo trên D1 hay D3.
Ngưỡng α=0,05 đặt trước sẽ dẫn đến bác bỏ H₀ trong ví dụ; nó không chứng minh chênh lệch có ích hoặc nguyên nhân đã rõ.
**Kích thước hiệu ứng** báo chênh lệch 0,8 theo đơn vị gốc; một dạng chuẩn hóa là chênh lệch chia độ lệch chuẩn gộp phù hợp.
Giảm thời gian 0,01 giây có thể đạt p nhỏ khi mẫu lớn nhưng chẳng giúp đáng kể cho công việc; báo cả độ lớn và độ bất định.

**Lỗi hay gặp và cách sửa.** Thử nhiều giả thuyết rồi chỉ báo p nhỏ nhất làm tăng báo động giả; đặt kế hoạch trước và xử lý nhiều phép thử phù hợp.
Không bác bỏ H₀ nghĩa là bằng chứng hiện tại chưa đủ chống H₀, không phải đã chứng minh hai nhóm bằng nhau.
Độ lệch chuẩn điểm CV không tự là khoảng tin cậy 95% vì các fold dùng những tập học chồng lấn; báo đúng tên thống kê.

**Tự kiểm tra:** (1) P-value 0,03 có nghĩa H₀ chỉ có 3% khả năng đúng? (2) Lấy bootstrap 100.000 lần có sửa được mẫu thiên lệch không?

**Đáp án:** (1) Không; nó là xác suất về thống kê dưới H₀ và giả định. (2) Không; tăng số lượt chỉ giảm nhiễu mô phỏng của quy trình bootstrap đang dùng.

<a id="d07"></a>
## D07. SQL, khóa và transaction: giữ sự thật của dữ liệu — B35–B36

**Cần biết trước:** bảng và join ở [D02](#d02), hàm và quản lý tài nguyên với `with`.

SQL mô tả bảng kết quả muốn có; hệ quản trị quyết định cách thực hiện truy vấn.
`SELECT` chọn cột/biểu thức, `FROM` chỉ bảng, `WHERE` lọc hàng, `GROUP BY` chia nhóm để tổng hợp, `HAVING` lọc nhóm sau tổng hợp.
`ORDER BY` xác định thứ tự kết quả; nếu không có, không dựa vào thứ tự tình cờ khi so với pandas hoặc xuất báo cáo.
Ví dụ lọc đơn số lượng >0 bằng WHERE, cộng doanh thu từng vùng bằng GROUP BY, rồi giữ vùng tổng >300.000 bằng HAVING.
Đó là thứ tự tư duy logic; hệ quản trị có thể tối ưu cách chạy mà vẫn giữ ý nghĩa truy vấn.

Khóa chính nhận diện duy nhất mỗi bản ghi; nên khai báo rõ ràng `PRIMARY KEY` và `NOT NULL` cho mã bắt buộc.
Khóa ngoại ràng buộc mã ở bảng con tham chiếu một khóa hợp lệ ở bảng cha; nó không thay mọi kiểm tra nghiệp vụ.
Đơn có sản phẩm tồn tại vẫn có thể có số lượng âm, nên cần thêm quy tắc hoặc `CHECK` phù hợp.
SQL `NULL` biểu diễn thiếu/không biết; kiểm tra bằng `IS NULL`, không dùng `= NULL`; `COUNT(*)` đếm hàng, `COUNT(cột)` bỏ giá trị NULL.
Trong Python sqlite3, bật khóa ngoại trước transaction; truyền **giá trị** qua placeholder `?`, không nối trực tiếp vào SQL.
Placeholder không thay được tên bảng/cột; tên động cần được chọn từ danh sách cho phép. [Hướng dẫn sqlite3 của Python](https://docs.python.org/3/library/sqlite3.html).

```python
# RUN: stdlib
import sqlite3

con = sqlite3.connect(":memory:")
try:
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("CREATE TABLE products (id TEXT NOT NULL PRIMARY KEY, price INTEGER NOT NULL)")
    con.execute("""CREATE TABLE orders (
        id TEXT NOT NULL PRIMARY KEY,
        product_id TEXT NOT NULL REFERENCES products(id),
        quantity INTEGER NOT NULL CHECK (quantity > 0))""")
    with con:
        con.execute("INSERT INTO products VALUES (?, ?)", ("P01", 100000))
        con.executemany("INSERT INTO orders VALUES (?, ?, ?)",
                        [("O1", "P01", 2), ("O2", "P01", 3)])
    rows = con.execute("""SELECT p.id, SUM(o.quantity * p.price) AS revenue
        FROM orders AS o JOIN products AS p ON o.product_id = p.id
        WHERE o.quantity >= ? GROUP BY p.id
        HAVING SUM(o.quantity * p.price) > ? ORDER BY p.id""", (2, 300000)).fetchall()
    print(rows)
    try:
        with con:
            con.execute("INSERT INTO orders VALUES (?, ?, ?)", ("O3", "P01", 1))
            con.execute("INSERT INTO orders VALUES (?, ?, ?)", ("O4", "P99", 1))
    except sqlite3.IntegrityError:
        print("rollback")
    print(con.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
finally:
    con.close()
```

**Kết quả:** `[('P01', 500000)]`, rồi `rollback`, rồi `2`; cơ sở dữ liệu chỉ tồn tại trong bộ nhớ kết nối này.
Hai đơn hợp lệ cho `(2+3)×100000=500000`; phép JOIN lấy đúng giá từ bảng sản phẩm.
Trong transaction sau, O3 chèn được tạm thời nhưng O4 vi phạm khóa ngoại P99; lỗi thoát khối `with con` khiến cả hai thay đổi bị hoàn tác.
Transaction gom các thao tác thành một lần chấp nhận bằng commit hoặc hoàn tác bằng rollback; trạng thái dở dang không được coi là kết quả hoàn tất.
Khối `with con` quản lý transaction theo chế độ kết nối trong ví dụ, không tự đóng kết nối; `finally` làm việc đóng rõ ràng.

**ETL** là Extract → Transform → Load: lấy dữ liệu, biến đổi có quy tắc, rồi nạp vào nơi sử dụng.
Với P02, tách đọc raw, kiểm tra, cách ly, join, nạp và báo cáo giúp biết tổng sai xuất hiện từ bước nào.
Tính idempotent nghĩa là chạy lại cùng đầu vào vẫn tạo cùng trạng thái đích, không nhân đôi đơn; khóa chính giúp phát hiện nhưng chưa tự thiết kế toàn bộ quy trình.
Có thể xây lại bảng đích riêng của dự án hoặc nạp theo khóa với quy tắc xung đột rõ ràng; không âm thầm bỏ qua mọi lỗi chèn.
Trong AI, nhiều đặc trưng được trích bằng SQL; sai điều kiện thời gian ở truy vấn có thể đưa dữ liệu tương lai vào train.

**Lỗi hay gặp và cách sửa.** Thấy kết nối có khai báo khóa ngoại rồi tưởng đã cưỡng chế: kiểm tra PRAGMA ở chính kết nối đang dùng.
Nối tên vùng do người dùng nhập vào chuỗi SQL gây lỗi và SQL injection; dùng `WHERE region = ?` với tuple tham số.
So hai bảng khác thứ tự rồi kết luận sai số: sắp theo cùng khóa và đối chiếu cả số hàng, kiểu và giá trị.

**Tự kiểm tra:** (1) Vì sao O3 cũng không còn dù chính nó hợp lệ? (2) WHERE và HAVING khác nhau ở thời điểm lọc nào?

**Đáp án:** (1) O3 thuộc cùng transaction thất bại với O4. (2) WHERE lọc hàng trước tổng hợp, HAVING lọc nhóm sau tổng hợp.

<a id="d08"></a>
## D08. ML học gì, và một phép đánh giá công bằng cần gì? — B37–B38, B44

**Cần biết trước:** hàm, bảng dữ liệu, [D05](#d05) và ý tưởng lấy mẫu ở [D06](#d06).

Học máy xây một hàm từ dữ liệu: đầu vào x qua mô hình f cho dự đoán `ŷ=f(x)`.
Trong học có giám sát, mỗi ví dụ train có đặc trưng x và nhãn y; thuật toán điều chỉnh tham số để giảm một mục tiêu học.
Hồi quy dự đoán đại lượng số có ý nghĩa khoảng cách, như thời gian; phân loại chọn nhóm, như ba lớp Wine.
Nhãn phân loại viết 0,1,2 không biến bài toán thành hồi quy: sai từ lớp 0 sang 2 chưa mặc định “gấp đôi” sai từ 0 sang 1.
Mẫu là đơn vị dự đoán; đặc trưng là thông tin có sẵn khi dự đoán; label là thứ muốn biết sau đó hoặc cần phân biệt.
Trước model, viết rõ “dự đoán cho ai, vào lúc nào, bằng thông tin nào”; cột xuất hiện sau lúc ấy có thể không dùng được.
Mã `row_id` dùng theo dõi dòng, không phải phép đo ẩn chứa quy luật cần cho D3; label tuyệt đối không nằm trong X.

**Train** học tham số; **validation** hỗ trợ chọn mô hình, siêu tham số, ngưỡng và quyết định tiền xử lý.
**Test** đo hệ thống đã chốt trên dữ liệu chưa tham gia những lựa chọn đó; xem test nhiều lần để sửa là biến nó thành validation.
Đúng quy trình D3: giữ cố định 106 train, 36 validation, 36 test; stratify duy trì gần đúng tỷ lệ lớp, không đảm bảo mọi tập đại diện thế giới thực.
Tách chỉ số gốc trước, lưu lại chúng và dùng cùng split khi so các ứng viên để giảm khác biệt do đổi mẫu đánh giá.

```python
# RUN: stdlib
train = {0, 1, 2, 3}
validation = {4, 5}
test = {6, 7}
assert not train & validation
assert not train & test
assert not validation & test
assert train | validation | test == set(range(8))
print(len(train), len(validation), len(test))
values = {0: 2, 1: 4, 2: 6, 3: 8, 4: 100, 5: 200, 6: 300, 7: 400}
mu_train = sum(values[i] for i in train) / len(train)
print(mu_train, values[4] - mu_train)
```

**Kết quả:** `4 2 2`, rồi `5.0 95.0`; đây là mô hình nhỏ về chỉ số, không thay split phân tầng của D3.
Trung bình học được chỉ bằng `(2+4+6+8)/4=5`; hàng validation có giá trị 100 được trừ 5, không làm thay đổi scaler.
**Leakage**, tức rò rỉ, xuất hiện khi việc học/lựa chọn tiếp cận thông tin mà phép đánh giá đáng lẽ giữ lại.
Nó có thể đến từ fit scaler cả dữ liệu, chọn cột bằng test, trùng đối tượng hoặc dùng thông tin chỉ có sau thời điểm dự đoán.
Pipeline giúp đặt các bước có học trạng thái vào đúng phần train, nhưng không tự phát hiện cột tương lai do người làm đưa vào. [Các lỗi thường gặp của scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html).

**Baseline** là mốc đơn giản: phân loại luôn chọn lớp phổ biến train; hồi quy có thể luôn đoán trung bình hoặc trung vị train.
Trung bình tối thiểu hóa tổng lỗi bình phương khi dùng một hằng số; trung vị tối thiểu hóa tổng lỗi tuyệt đối.
Ứng viên chỉ có ý nghĩa khi được so cùng dữ liệu, metric và điều kiện; 90% accuracy có thể bằng baseline vô dụng cho lớp hiếm.
**Cross-validation (CV)** chia train thành k phần: mỗi lượt học trên k−1 phần và đánh giá trên phần còn lại, rồi tổng hợp điểm.
Mỗi lượt phải học lại imputer, scaler, chọn cột và PCA chỉ trên phần học của lượt đó; xem [Pipeline ở D10](#d10).
Điểm CV giúp so cấu hình; sau chọn cấu hình tốt nhất trong nhiều thử nghiệm, điểm tốt nhất ấy có thể lạc quan do lựa chọn.
Ghi ngân sách thử trước, giữ validation cho quyết định đã định và test cho phép đánh giá cuối; nghiên cứu phức tạp có thể cần nested CV.

Chia ngẫu nhiên phù hợp khi mục tiêu và sự độc lập của mẫu cho phép; nó không phải mặc định cho mọi dữ liệu.
Dự đoán khách mới cần tách theo khách, tránh cùng khách ở train/test; dự đoán tương lai cần học từ quá khứ và đánh giá trên thời gian sau.
Nếu nhãn dùng cửa sổ tương lai, còn phải xem các cửa sổ có chồng lấn và cần khoảng cách thời gian giữa các tập hay không.
**Lỗi hay gặp và cách sửa.** Đổi seed đến khi điểm đẹp là chọn theo kết quả; cố định kế hoạch và báo biến động phù hợp.
Validation cao, test thấp không phải lời mời chỉnh theo test; báo kết quả và thiết kế đánh giá độc lập cho phiên bản kế tiếp.

**Tự kiểm tra:** (1) Có thể fit scaler trên toàn bộ train trước khi CV chỉ model không? (2) Baseline học tỷ lệ lớp từ đâu?

**Đáp án:** (1) Không, vì fold đánh giá đã góp vào scaler; đưa scaler vào Pipeline của CV. (2) Từ phần train tương ứng, không từ validation/test.

<a id="d09"></a>
## D09. Mô hình tuyến tính, xác suất và cách đo lỗi — B38–B40, B46

**Cần biết trước:** [D04](#d04), [D05](#d05), xác suất có điều kiện ở [D06](#d06) và [D08](#d08).

Hồi quy tuyến tính dùng `ŷ=Xw+b` để dự đoán số; fit tìm w,b, còn predict giữ chúng cố định để tính cho dữ liệu mới.
Logistic regression nhị phân dùng điểm `z=w·x+b`, rồi sigmoid `p=1/(1+exp(−z))` để đưa điểm vào khoảng (0,1).
Ở z=0, p=0,5; z≈1,0986 cho p≈0,75; đây là xác suất mô hình gán cho lớp được quy định là 1.
Quy tắc dự đoán `p≥t → lớp 1` dùng ngưỡng t; với p=0,75, ngưỡng 0,5 chọn 1, còn ngưỡng 0,8 chọn 0.
Trong nhiều lớp, mô hình có thể dùng softmax: `p_k=exp(z_k)/Σexp(z_j)` cho xác suất các lớp cộng thành 1.
`predict_proba` trả các xác suất theo thứ tự `classes_`; `predict` trả nhãn theo quy tắc mô hình, thường chọn lớp có xác suất lớn nhất.

**Regularization** thêm chi phí cho tham số lớn vào mục tiêu, hạn chế các lời giải phức tạp hoặc không ổn định.
Ridge dùng phạt L2, tỷ lệ với tổng bình phương trọng số; alpha lớn hơn tăng mức phạt theo quy ước Ridge.
Trong LogisticRegression của scikit-learn với regularization tương ứng, C là nghịch đảo độ mạnh phạt: C nhỏ thường phạt mạnh hơn.
Phạt quá mạnh có thể underfit; mô hình quá linh hoạt có thể overfit: tốt trên train nhưng kém hơn trên dữ liệu mới.
Các đặc trưng gần trùng có thể làm hệ số thay đổi lớn trong khi dự đoán ít đổi; đừng xem một bộ hệ số là lời giải thích nhân quả duy nhất.

**Metric hồi quy:** MAE=`Σ|ŷᵢ−yᵢ|/n`; RMSE=`√(Σ(ŷᵢ−yᵢ)²/n)`; cả hai cùng đơn vị y.
Với y=`[10,20,30]`, dự đoán=`[12,18,40]`, lỗi tuyệt đối là `[2,2,10]`: MAE=14/3≈4,6667, RMSE=√(108/3)=6.
RMSE lớn hơn MAE ở đây vì lỗi 10 được bình phương, tạo ảnh hưởng mạnh; metric thích hợp phụ thuộc chi phí lỗi thực tế.
R² so tổng lỗi bình phương với cách dùng trung bình y của tập đánh giá làm mốc; R² âm nghĩa là lỗi còn lớn hơn mốc này.
Nếu y của tập đánh giá là hằng số, công thức R² thông thường có mẫu số 0; xem cách công cụ xử lý thay vì diễn giải như trường hợp thường.

Với một lớp được coi là dương, **TP** là dương đoán đúng, **FP** là âm đoán thành dương, **FN** là dương bị bỏ sót, **TN** là âm đoán đúng.
Precision=`TP/(TP+FP)` hỏi “trong những cảnh báo dương, bao nhiêu là đúng?”; recall=`TP/(TP+FN)` hỏi “trong những dương thật, tìm được bao nhiêu?”.
F1=`2TP/(2TP+FP+FN)` kết hợp precision và recall; accuracy là tổng dự đoán đúng chia tổng mẫu.
Với nhiều lớp, tính từng lớp so với phần còn lại; **macro-F1** là trung bình F1 các lớp, không phải F1 của trung bình precision và recall.
Support là số mẫu thật của một lớp; weighted-F1 dùng support làm trọng số, nên lớp lớn vẫn ảnh hưởng nhiều hơn.

```python
# RUN: stdlib
from math import sqrt

true, pred = [0, 0, 0, 1, 1, 2], [0, 0, 1, 1, 2, 2]
labels = [0, 1, 2]
matrix = [[sum(a == i and b == j for a, b in zip(true, pred))
           for j in labels] for i in labels]
scores = []
for k in labels:
    tp = matrix[k][k]
    fp = sum(row[k] for row in matrix) - tp
    fn = sum(matrix[k]) - tp
    denominator = 2 * tp + fp + fn
    scores.append(2 * tp / denominator if denominator else 0.0)
print(matrix)
print(round(sum(a == b for a, b in zip(true, pred)) / len(true), 4))
print([round(score, 4) for score in scores], round(sum(scores) / len(scores), 4))
errors = [12 - 10, 18 - 20, 40 - 30]
print(round(sum(abs(e) for e in errors) / 3, 4), sqrt(sum(e * e for e in errors) / 3))
```

**Kết quả:** ma trận `[[2,1,0],[0,1,1],[0,0,1]]`, accuracy `0.6667`, F1 `[0.8,0.5,0.6667]`, macro-F1 `0.6556`, MAE/RMSE `4.6667 6.0`.
Quy ước hàng là lớp thật, cột là lớp dự đoán; lớp 1 có TP=1, FP=1, FN=1 nên precision=recall=F1=0,5.
Lớp 2 có recall 1 vì tìm được mẫu thật duy nhất, nhưng precision 0,5 vì còn nhận nhầm một mẫu lớp 1.
Nếu mẫu số bằng 0, một metric có thể không xác định; ghi quy tắc báo cáo như `zero_division=0` và support, đừng che việc thiếu mẫu/dự đoán.

Với 90 âm và 10 dương, luôn đoán âm đạt accuracy 90% nhưng recall dương bằng 0; đây là lý do phải xem lỗi theo lớp.
Giảm ngưỡng nhị phân làm tập dự đoán dương mở rộng nên recall không giảm trên cùng dữ liệu; precision có thể tăng hoặc giảm tùy các điểm mới.
Chọn ngưỡng theo chi phí và validation, rồi cần test độc lập; ngưỡng 0,5 không tự là phương án tốt nhất cho mọi mục tiêu.
**Average precision** tổng hợp precision theo các mức tăng recall khi thay đổi ngưỡng, hữu ích để xem khả năng xếp hạng ở bài lớp hiếm.
**Log loss** nhị phân là `−mean(y log(p)+(1−y)log(1−p))`; đo chất lượng xác suất và phạt dự đoán rất tự tin nhưng sai.
Với y=1, p=0,9 cho loss≈0,1053, còn p=0,01 cho loss≈4,6052; hai dự đoán sai cùng nhãn có thể khác xa về chất lượng xác suất.

**Calibration** hỏi trong những mẫu được gán p khoảng 0,8 cho lớp 1, tỷ lệ thật thuộc lớp 1 có gần 80% không.
Reliability plot so xác suất trung bình và tỷ lệ dương thật trong từng khoảng; cần báo số mẫu vì khoảng thưa rất nhiễu.
Log loss/Brier không chỉ đo calibration mà còn phản ánh khả năng phân biệt; hiệu chỉnh xác suất cần dữ liệu đánh giá phù hợp, không fit rồi tự chấm trên cùng mẫu. [Tài liệu calibration](https://scikit-learn.org/stable/modules/calibration.html).
**Lỗi hay gặp và cách sửa.** Gọi xác suất 0,9 là “đúng 90% cho riêng mẫu này” mà chưa kiểm tra mô hình; xem calibration theo tập và bối cảnh sử dụng.
Với test 36 mẫu D3, đổi một dự đoán làm accuracy đổi khoảng 2,78 điểm phần trăm; báo số đếm, lỗi từng lớp và giới hạn của tập nhỏ.

**Tự kiểm tra:** (1) FP tăng khi TP giữ nguyên thì precision đổi thế nào? (2) Accuracy cao có chứng minh xác suất được hiệu chỉnh tốt không?

**Đáp án:** (1) Precision giảm nếu TP>0; kiểm tra trường hợp mẫu số 0 theo quy ước. (2) Không; metric nhãn và chất lượng xác suất trả lời các câu hỏi khác nhau.

<a id="d10"></a>
## D10. Cây, Pipeline, cấu trúc ẩn và mô hình có thể bàn giao — B41–B48

**Cần biết trước:** [D04](#d04), [D08](#d08) và [D09](#d09).

Cây quyết định chia dữ liệu bằng các câu hỏi dạng “x₁≤ngưỡng?”; đi từ gốc qua các điều kiện tới lá để lấy dự đoán.
Ví dụ bốn mẫu `x=[1,2,8,9]`, `y=[0,0,1,1]`: điều kiện `x≤5` tách hai lớp hoàn toàn trên train.
Trước chia, tỷ lệ hai lớp là 1/2,1/2 nên Gini=`1−(1/2)²−(1/2)²=0,5`; sau chia, mỗi lá chỉ có một lớp nên Gini=0.
Gini là độ lẫn nhãn dùng đánh giá một cách chia; mức giảm có trọng số theo số mẫu ở lá con, không phải bằng chứng quy luật đúng ngoài train.
Một điểm mới x=4 đi trái và được dự đoán 0; cây sâu hơn có thể dùng những ngưỡng hẹp để ghi nhớ cả nhiễu.
`max_depth` giới hạn số tầng, `min_samples_leaf` buộc lá có đủ mẫu; đó là siêu tham số chọn qua quá trình đánh giá.
Ngưỡng và nội dung lá được học từ train là tham số đã fit, khác với giới hạn độ sâu do ta đặt trước.

Random forest huấn luyện nhiều cây với sự ngẫu nhiên ở mẫu/đặc trưng, rồi gộp kết quả để giảm biến động của một cây riêng.
Với bộ phân loại forest của scikit-learn, dự đoán dựa trên trung bình xác suất các cây; không cần mọi cây đồng ý.
Boosting xây các mô hình theo chuỗi để cải thiện mục tiêu còn chưa tốt; trong hồi quy lỗi bình phương có thể hiểu là học phần residual còn lại.
Gradient boosting tổng quát dùng hướng giảm loss, vì vậy “sửa những nhãn sai” chỉ là trực giác chưa đủ cho mọi loss.
Số cây, độ sâu và learning rate ảnh hưởng chất lượng, thời gian và bộ nhớ; thêm cây không đảm bảo cải thiện đáng kể.

**Pipeline** ghép các bước thành một đối tượng: khi fit, các biến đổi học trạng thái rồi chuyển dữ liệu cho mô hình.
Khi predict, các bước dùng trạng thái đã học; không fit lại scaler hay imputer trên đầu vào mới.
Trong CV, truyền cả Pipeline cho bộ đánh giá để mỗi fold fit các bước trên đúng phần học. [API Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html).
Imputer học giá trị điền như median; `ColumnTransformer` áp dụng nhánh số và nhánh chữ khác nhau rồi nối đặc trưng lại.
One-hot encoding biến danh mục thành các cột chỉ báo; `handle_unknown="ignore"` cho phép gặp danh mục mới, nhưng không có nghĩa model hiểu danh mục đó.
Không mã hóa “web=1, store=2, phone=3” rồi vô tình gán ý nghĩa khoảng cách/thứ tự cho các nhóm vốn không có thứ tự.

```python
# NEEDS: scikit-learn
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

X_train = [[-3.0], [-2.0], [-1.0], [1.0], [2.0], [3.0]]
y_train = [0, 0, 0, 1, 1, 1]
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(C=1.0, max_iter=2000)),
])
pipeline.fit(X_train, y_train)
print(pipeline.named_steps["imputer"].statistics_.tolist())
print(pipeline.named_steps["scaler"].mean_.tolist())
print(pipeline.predict([[-2.5], [2.5]]).tolist())
```

**Kết quả đối chiếu:** median `[0.0]`, trung bình `[0.0]`, dự đoán `[0,1]`; các điểm có dấu âm/dương nằm hai phía ranh giới đã học.
Ví dụ không có dữ liệu thiếu nên imputer chưa phải thay phần tử nào, nhưng vẫn học median để dùng khi cần.
Tên bước cho phép chỉ định cấu hình như `model__C` trong GridSearchCV; số cấu hình nhân số fold cho biết phần lớn số lượt fit tìm kiếm.
Ví dụ 12 cấu hình ×5 fold cần 60 lượt fit, thường còn một lượt refit cấu hình được chọn; dự tính ngân sách trước khi chạy.

**PCA** tìm các hướng tuyến tính trực giao giữ nhiều phương sai của X sau khi trừ trung bình, không dùng y để tìm hướng tốt cho phân lớp.
Sau chuẩn hóa theo train nếu phù hợp, hai điểm chiếu gần nhau nghĩa là gần trong không gian đã giữ, không đảm bảo gần ở mọi đặc trưng gốc.
`explained_variance_ratio_=[0.6,0.2]` nghĩa là hai thành phần giữ tổng 80% phương sai theo phép đo này, không phải 80% thông tin về nhãn.
Scikit-learn PCA tự trừ trung bình nhưng không tự chia mỗi cột cho độ lệch chuẩn; scaler là quyết định riêng. [API PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).
Nếu PCA phục vụ bộ dự đoán, đặt nó trong Pipeline/CV; fit PCA lên cả test vẫn là học trạng thái từ test dù không dùng nhãn.

**Phân cụm** tìm cách nhóm điểm theo một tiêu chí, không học dự đoán nhãn có sẵn như phân loại.
KMeans luân phiên gán điểm về tâm gần nhất rồi cập nhật tâm bằng trung bình nhóm để giảm tổng bình phương khoảng cách tới tâm.
Ví dụ điểm 1,2,8,9 có hai cụm `{1,2}` và `{8,9}`, tâm là 1,5 và 8,5; tổng bình phương khoảng cách là 1.
Số cụm và khởi tạo ảnh hưởng nghiệm; đổi thứ tự tên “cụm 0/1” không đổi cách chia, nên không so trực tiếp tên cụm với nhãn lớp 0/1.
Cụm có thể phản ánh thiết bị đo hoặc thang đơn vị, chưa chắc là các nhóm có ý nghĩa nghiệp vụ; cần kiểm tra thêm.

**Feature importance** mô tả vai trò đặc trưng theo một mô hình và phép đo cụ thể; không tự xác định tác động nhân quả.
Importance dựa trên giảm độ lẫn của cây có thể thiên về cột có nhiều cách chia; permutation importance đo mức giảm metric khi xáo một cột trên tập đánh giá.
Hai cột gần trùng có thể thay nhau cung cấp thông tin nên xáo một cột ít làm điểm giảm; importance thấp chưa chứng minh thông tin hoàn toàn vô ích.
**Đóng gói:** lưu cả Pipeline đã fit, schema tên/thứ tự/kiểu cột, thứ tự lớp, cấu hình, seed, phiên bản thư viện và mã nhận diện artifact.
Seed cố định hỗ trợ tái lập ngẫu nhiên; vẫn cần cùng dữ liệu, split, thứ tự xử lý, phiên bản và môi trường vì seed không khóa mọi khác biệt.
Chỉ tải pickle/joblib do mình tạo hoặc từ nguồn tin cậy vì giải tuần tự có thể thực thi mã; kiểm tra lưu/tải giữ dự đoán trên mẫu kỹ thuật lấy từ train.
Ở B47 chốt quyết định rồi refit cả Pipeline trên train+validation; lúc ấy scaler được phép học lại trên phần gộp này.
Ở B48 đo artifact đã chốt trên 36 test; ghi riêng điểm CV, validation và test, không sửa cấu hình để làm test đẹp hơn.

**Lỗi hay gặp và cách sửa.** Chỉ lưu model rồi viết lại scaler ở API làm sai hệ tọa độ; tải cùng Pipeline và kiểm tra schema đầu vào.
Đảo cột mà vẫn dự đoán được có thể âm thầm sai; xác thực tên và sắp về thứ tự đã lưu, hoặc báo lỗi rõ theo hợp đồng.

**Tự kiểm tra:** (1) PCA giữ 90% phương sai có đảm bảo giữ 90% khả năng phân loại? (2) Lưu seed có đủ để tái lập mô hình và dự đoán?

**Đáp án:** (1) Không; phương sai lớn không đồng nghĩa thông tin về nhãn. (2) Không; cần dữ liệu, split, toàn bộ Pipeline/trạng thái, schema, cấu hình, phiên bản và quy trình chạy.
