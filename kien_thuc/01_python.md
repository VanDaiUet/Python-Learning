# Hiểu Python từ chương trình đầu tiên đến dự án nhỏ

Tài liệu giải thích kiến thức cho B01–B24 và tám bộ bài khởi động. Đọc mục được liên kết trong bài đang học, dự đoán đầu ra, chạy ví dụ rồi thay dữ liệu. Không cần đọc hết trước ngày 1.

Các khối `# RUN: stdlib` chạy độc lập với Python 3.11 và thư viện chuẩn. Sao chép từng khối vào một tệp riêng trong `bai_lam/`, chạy bằng `.venv\Scripts\python.exe đường_dẫn_tệp`. Ví dụ ghi tệp ở đây dùng thư mục tạm để không đụng dữ liệu bài làm.

| Bài | Đọc trước |
|---|---|
| B01–B02 | [P01 — Chạy mã, biến, kiểu](#p01) |
| B03–B04 | [P02 — Biểu thức và điều kiện](#p02) |
| B05–B06 | [P03 — Vòng lặp](#p03) |
| B07–B10 | [P04 — Chuỗi và cấu trúc dữ liệu](#p04) |
| B11–B12 | [P05 — Hàm và hợp đồng](#p05) |
| B13–B14 | [P06 — Tệp, CSV, JSON](#p06) |
| B15–B16 | [P07 — Debug](#p07), [P08 — Test](#p08) |
| B17–B18 | [P09 — Môi trường và Git](#p09) |
| B19–B22 | [P10 — Tổ chức mã và xử lý dữ liệu](#p10) |
| B23–B24 | P06–P10; ghép các phần vào CLI S1 |

<a id="p01"></a>
## P01 — Mã được chạy thế nào? Biến và kiểu dữ liệu

**Cần biết trước:** mở thư mục, tạo và lưu tệp văn bản. Chưa cần biết lập trình.

Chương trình là các chỉ dẫn xử lý dữ liệu. Trình soạn thảo giúp viết mã; trình thông dịch Python đọc và thực thi mã; terminal nhận lệnh để gọi chương trình. Viết trong editor chưa làm chương trình chạy, và sửa nhưng chưa lưu thì Python vẫn đọc bản đã lưu trên đĩa.

Tệp `.py` chứa mã Python, không phải tài liệu Word. Trong lệnh `.\.venv\Scripts\python.exe bai_lam\vi_du.py`, phần đầu chọn Python nào, phần sau chọn tệp nào. Thư mục đang đứng quyết định cách hiểu đường dẫn tương đối. Lệnh PowerShell nhập vào terminal; câu như `print(123)` viết trong tệp Python hoặc phiên tương tác Python, không trộn hai ngôn ngữ.

Một **giá trị** có kiểu: `str` cho văn bản, `int` cho số nguyên, `float` cho số thực xấp xỉ, `bool` cho đúng/sai. **Biến** là tên gắn với một đối tượng. Dấu `=` tính phía phải rồi gắn kết quả cho tên bên trái; nó không phải dấu hỏi hai giá trị có bằng nhau không. Python phân biệt chữ hoa/thường: `Minutes` khác `minutes`.

```python
# RUN: stdlib
name = "An"
sessions = 5
minutes_per_session = 45
total_minutes = sessions * minutes_per_session
total_hours = total_minutes / 60
print(f"{name}: {total_minutes} phút = {total_hours:.2f} giờ")
print(type(sessions).__name__, type(total_hours).__name__)
```

Đầu ra: `An: 225 phút = 3.75 giờ`, rồi `int float`. Trước hết Python tạo các giá trị, sau đó nhân 5 với 45, chia 225 cho 60, cuối cùng định dạng chuỗi. `f"...{biểu_thức}..."` chèn kết quả vào văn bản; `:.2f` hiển thị hai chữ số sau dấu thập phân, không thay đổi giá trị gốc.

`input()` chờ người dùng gõ và trả một chuỗi, kể cả khi gõ `45`. Muốn tính số phải chuyển kiểu, như `int("45")`. Chuyển `"4.5"` thẳng bằng `int()` không hợp lệ; việc chấp nhận số thập phân phải dựa vào yêu cầu bài. Dấu `#` bắt đầu chú thích tới hết dòng; chú thích giải thích lý do, không được thực thi.

```python
# RUN: stdlib
raw = "45"  # Giả lập chuỗi đã nhận từ input, không chờ bàn phím.
print(raw + "15")
print(int(raw) + 15)
old = 10
new = old
old = 20
print(old, new)
```

Đầu ra `4515`, `60`, `20 10`. Cộng chuỗi nối văn bản; cộng số tính toán. Gán `old = 20` gắn lại tên `old`, không làm tên `new` tự đổi theo. Đến P04 sẽ xem trường hợp hai tên cùng tham chiếu một list có thể sửa được.

**Liên hệ AI:** dữ liệu đọc từ CSV/API có thể là chuỗi; không thể huấn luyện đúng nếu nhầm `"12"` với `12`. Biết Python nào đang chạy giúp chẩn đoán thiếu thư viện.

**Lỗi hay gặp:** quên dấu nháy quanh văn bản gây `NameError`; lưu thành `vi_du.py.txt`; gọi nhầm Python; dùng biến trước khi gán. Đọc đường dẫn và tên lỗi, không chỉ chạy lại cùng lệnh.

**Tự kiểm:** (1) `"3" * 2` là gì? (2) `:.2f` có biến số thành chính xác tuyệt đối không?

**Gợi ý đáp án:** (1) Chuỗi `"33"`; muốn 6 thì chuyển thành số. (2) Không; đó là cách hiển thị.

<a id="p02"></a>
## P02 — Biểu thức, số thực và quyết định bằng điều kiện

**Cần biết trước:** P01; phép cộng, trừ, nhân, chia.

Biểu thức tạo ra giá trị: `2 + 3 * 4` cho 14 vì nhân trước cộng; `(2 + 3) * 4` cho 20. Python có `/` chia thông thường, `//` chia lấy phần nguyên theo hướng âm vô cùng, `%` lấy dư, `**` lũy thừa. Với số phút không âm, `135 // 60` là số giờ trọn, `135 % 60` là phút còn lại. Với số âm, `-7 // 3` bằng -3, không phải -2; đừng suy quy tắc cắt phần thập phân cho mọi dấu.

Phép so sánh `==`, `!=`, `<`, `<=`, `>`, `>=` cho `True` hoặc `False`. `and` cần cả hai điều kiện, `or` cần ít nhất một, `not` đảo tính đúng/sai. Chúng xét ngắn mạch: nếu đã biết kết quả thì không cần tính vế còn lại. Trong Python, `and/or` trả một toán hạng theo tính đúng/sai của nó; khi ghép các phép so sánh như dưới đây, kết quả là boolean.

```python
# RUN: stdlib
minutes = 135
print(minutes // 60, minutes % 60)
score = 72
if score >= 80:
    level = "vững"
elif score >= 60:
    level = "cần ôn thêm"
else:
    level = "học lại phần nền"
print(level)
count = 0
print(count > 0 and 100 / count > 10)
```

Đầu ra `2 15`, `cần ôn thêm`, `False`. Nhánh đầu không đạt, nhánh thứ hai đạt nên `else` bị bỏ qua. Phép chia ở cuối không được chạy vì `count > 0` đã sai. Dấu `:` mở khối và thụt lề bốn dấu cách cho biết câu lệnh thuộc nhánh; thụt lề có ý nghĩa trong Python.

`None` biểu thị chưa có/không có giá trị theo quy ước chương trình; nó khác số 0, chuỗi rỗng và `False`. Kiểm tra bằng `value is None`. Các giá trị 0, chuỗi/list/dict rỗng, `None` có tính sai khi dùng trong điều kiện, nhưng khác nhau về nghĩa. `if not score` gộp điểm 0 với dữ liệu thiếu; nếu cần phân biệt hãy kiểm `is None` trước.

Số thực máy tính thường dùng biểu diễn nhị phân hữu hạn nên một số thập phân không biểu diễn chính xác. Không dùng phép so tuyệt đối cho mọi kết quả tính số thực.

```python
# RUN: stdlib
from math import isclose
print(0.1 + 0.2 == 0.3)
print(isclose(0.1 + 0.2, 0.3, rel_tol=1e-9, abs_tol=1e-12))
value = 0
print(value is None, bool(value))
```

Đầu ra `False`, `True`, `False False`. `isclose` xét sai số tương đối/tuyệt đối theo mức ta chọn; mức phù hợp phụ thuộc đơn vị và bài toán. Tiền VND nguyên có thể lưu bằng `int`; các phép tiền tệ cần thập phân chính xác có thể dùng `Decimal` với quy tắc làm tròn rõ ràng.

**Liên hệ AI:** điều kiện dùng kiểm đầu vào và chọn ngưỡng dự đoán. `True` là một dạng số nguyên trong Python (`isinstance(True, int)` là đúng); hợp đồng chỉ cho số giờ nguyên thường phải loại bool bằng `type(hours) is int`.

**Lỗi hay gặp:** dùng `=` thay `==`; đặt nhánh `>=60` trước `>=80` làm nhánh điểm cao không tới được; viết `x == 1 or 2` luôn có tính đúng vì số 2; sửa thành `x in (1, 2)`.

**Tự kiểm:** (1) Vì sao `if value` không đủ phân biệt chưa nhập với 0? (2) Điểm 80 vào nhánh nào ở ví dụ?

**Gợi ý đáp án:** (1) Cả `None` và 0 đều có tính sai. (2) Nhánh đầu vì kiểm theo thứ tự và chỉ lấy nhánh đạt đầu tiên.

<a id="p03"></a>
## P03 — Vòng lặp, biến tích lũy và điều kiện dừng

**Cần biết trước:** P01–P02; đọc list đơn giản như `[30, 45, 60]`.

`for` lấy lần lượt từng phần tử của một đối tượng duyệt được. Dùng khi muốn xử lý mỗi mẫu, mỗi dòng hoặc mỗi phần tử. `range(start, stop, step)` tạo dãy số nguyên không gồm `stop`; `range(1,4)` sinh 1,2,3. `while` lặp khi điều kiện vẫn đúng; phù hợp menu hoặc công việc có số lượt chưa biết nhưng phải có cách dừng.

Biến tích lũy lưu kết quả của những phần tử đã xử lý. Với tổng, khởi đầu là 0 vì thêm 0 không thay đổi tổng. Đặt biến bên ngoài vòng lặp để không xóa kết quả cũ mỗi lượt.

```python
# RUN: stdlib
sessions = [30, 45, 60]
total = 0
for index, minutes in enumerate(sessions, start=1):
    total += minutes
    print(index, minutes, total)
print("Tổng:", total)
```

Đầu ra lần lượt `1 30 30`, `2 45 75`, `3 60 135`, rồi `Tổng: 135`. `total += minutes` tương đương lấy tổng cũ cộng thêm phút rồi gán lại. `enumerate` cung cấp cặp số thứ tự và giá trị, tránh tự tăng chỉ số sai.

Sau lượt thứ i, `total` bằng tổng i phần tử đầu: đây là một **bất biến vòng lặp** để tự kiểm lập luận. Nếu dữ liệu rỗng thì không có lượt nào, tổng vẫn là 0. Với tìm giá trị lớn nhất, khởi đầu 0 lại có thể sai nếu mọi số đều âm; cần chính sách rỗng và giá trị đầu phù hợp.

```python
# RUN: stdlib
remaining = 3
while remaining > 0:
    print(remaining)
    remaining -= 1
print("Dừng")
positive = []
for value in [-1, 2, 0, 3]:
    if value <= 0:
        continue
    positive.append(value)
print(positive)
```

Đầu ra `3`, `2`, `1`, `Dừng`, `[2, 3]`. `continue` bỏ phần còn lại của lượt hiện tại; `break` thoát vòng lặp gần nhất. Trong menu thực tế, người dùng chọn thoát dẫn đến `break`; `while True` không có đường thoát có thể chạy mãi.

List comprehension viết gọn phép biến đổi/lọc, như `[x * 2 for x in [1,2,3] if x > 1]` cho `[4,6]`. Đầu tiên hiểu bản vòng lặp, sau đó dùng dạng gọn nếu còn dễ đọc. Hai vòng lặp lồng nhau thường tạo các cặp kết hợp: n mẫu × m cấu hình là n×m lượt, có thể tốn nhiều thời gian.

**Liên hệ AI:** batching, đọc dữ liệu, chạy nhiều thí nghiệm đều dựa vào duyệt và tích lũy; giới hạn bước agent cũng là điều kiện dừng.

**Lỗi hay gặp:** đặt `total=0` trong vòng; quên tăng/giảm biến của while; loại phần tử khỏi list đang duyệt làm bỏ sót phần tử; mong `range(5)` có số 5. Hãy ghi bảng trạng thái hai hoặc ba lượt đầu.

**Tự kiểm:** (1) `sum(range(1,4))` bằng gì? (2) `continue` trước dòng cập nhật biến của while có thể gây gì?

**Gợi ý đáp án:** (1) 6. (2) Điều kiện không đổi, có thể lặp vô hạn; thiết kế đường cập nhật/thoát cho mọi nhánh.

<a id="p04"></a>
## P04 — Chuỗi, list, tuple, set, dict và bộ nhớ dùng chung

**Cần biết trước:** P01–P03; chỉ số bắt đầu từ 0.

Chọn cấu trúc theo câu hỏi cần trả lời. `list` giữ một dãy có thứ tự, cho phép lặp và sửa. `tuple` giữ một dãy không thể thay trực tiếp các phần tử, thường biểu diễn bộ giá trị cố định. `set` giữ các phần tử phân biệt, tiện kiểm thành viên; không dùng thứ tự duyệt set làm cam kết đầu ra. `dict` ánh xạ khóa duy nhất đến giá trị, như chủ đề → tổng phút. Python 3.11 giữ thứ tự thêm khóa của dict.

Chuỗi là dãy ký tự Unicode không sửa trực tiếp từng vị trí. `strip()` tạo chuỗi đã bỏ khoảng trắng hai đầu; `split()` không truyền dấu phân cách tách theo các vùng trắng; `join()` nối các chuỗi bằng dấu phân cách đã chọn. `lower()` đổi về chữ thường nhưng không xóa dấu tiếng Việt.

```python
# RUN: stdlib
raw = "  HỌC\t Python  "
normalized = " ".join(raw.lower().split())
values = [10, 20, 30, 40]
print(normalized)
print(values[0], values[-1], values[1:3], values[::-1])
print(raw.startswith("HỌC"))
```

Đầu ra `học python`, `10 40 [20, 30] [40, 30, 20, 10]`, `False` vì đầu chuỗi gốc có khoảng trắng. Slice `[start:stop:step]` không gồm stop. Chọn một chỉ số ngoài list gây `IndexError`; một slice vượt biên được cắt theo giới hạn dãy.

Một **tham chiếu** giúp tên trỏ đến đối tượng. `b=a` không sao chép list; cả hai tên có thể cùng nhìn thấy một đối tượng sửa được. Bản sao nông tạo lớp ngoài mới nhưng các đối tượng con vẫn có thể dùng chung.

```python
# RUN: stdlib
from copy import deepcopy
a = [[1], [2]]
b = a
shallow = a.copy()
deep = deepcopy(a)
b.append([3])
shallow[0].append(9)
print(a)
print(shallow)
print(deep)
```

Đầu ra `[[1, 9], [2], [3]]`, `[[1, 9], [2]]`, `[[1], [2]]`. `b.append` đổi list ngoài của a nên a thêm hàng, shallow không thêm hàng. Nhưng hàng đầu của shallow và a là cùng một list con nên cả hai thấy số 9. Deep copy trong ví dụ tách cả các list con; không cần deep copy mọi nơi, hãy hiểu phần nào dự định sửa.

Dict cho tra cứu `record["minutes"]`; thiếu khóa thì `KeyError`. `record.get("minutes", 0)` trả 0 khi thiếu khóa, nhưng chỉ hợp lệ nếu hợp đồng thật sự cho phép coi thiếu là 0. `in` trên dict kiểm khóa; trên list kiểm các phần tử.

```python
# RUN: stdlib
topics = ["Python", "SQL", "Python"]
counts = {}
for topic in topics:
    counts[topic] = counts.get(topic, 0) + 1
unique_in_order = list(dict.fromkeys(topics))
print(counts, unique_in_order)
pair = ("Python", 45)
topic, minutes = pair
print(topic, minutes, "SQL" in counts)
```

Đầu ra `{'Python': 2, 'SQL': 1} ['Python', 'SQL']`, rồi `Python 45 True`. Phép unpacking tách hai phần tử thành hai tên. Khóa dict/phần tử set phải hash được; chuỗi và tuple chứa toàn phần tử hash được thường phù hợp, list thì không. Tuple không làm các đối tượng con tự bất biến: tuple chứa list vẫn có list con sửa được.

**Liên hệ AI:** bản ghi dữ liệu thường là dict, batch là list các bản ghi; sửa corpus dùng chung khi thử một truy vấn có thể ảnh hưởng những lần tìm sau. Chuẩn hóa text phải giữ thông tin cần thiết cho bài toán.

**Lỗi hay gặp:** `values = values.sort()` làm values thành `None` vì sort sửa tại chỗ; dùng `sorted(values)` khi muốn list mới. `[[0]*2]*3` dùng chung các hàng; dùng `[[0]*2 for _ in range(3)]` để tạo từng hàng.

**Tự kiểm:** (1) Bỏ trùng bằng set có cam kết giữ thứ tự xuất hiện không? (2) Khi nào `.copy()` chưa đủ?

**Gợi ý đáp án:** (1) Không; muốn giữ thứ tự với phần tử hash được có thể dùng `dict.fromkeys`. (2) Khi cần sửa đối tượng con dùng chung mà vẫn giữ bản gốc.

<a id="p05"></a>
## P05 — Hàm, phạm vi biến, hợp đồng và type hint

**Cần biết trước:** P01–P04.

Hàm đặt tên cho một công việc có đầu vào và đầu ra. `def` định nghĩa hàm, thân hàm chỉ chạy khi gọi. **Tham số** là tên trong định nghĩa; **đối số** là giá trị truyền ở lần gọi. `return` trả giá trị cho nơi gọi và kết thúc hàm; `print` chỉ hiển thị, không thay cho return. Hàm đi hết thân mà không return trả `None`.

```python
# RUN: stdlib
def to_hours(minutes: int) -> float:
    """Đổi số phút nguyên không âm sang giờ."""
    if type(minutes) is not int:
        raise TypeError("minutes phải là int, không nhận bool")
    if minutes < 0:
        raise ValueError("minutes không được âm")
    return minutes / 60

result = to_hours(minutes=90)
print(result, to_hours(0))
```

Đầu ra `1.5 0.0`. `minutes=90` là truyền theo tên; `to_hours(90)` truyền theo vị trí. Type hint `int`, `-> float` mô tả ý định cho người đọc/công cụ, không tự cưỡng chế lúc chạy. Các câu `if` mới thực thi kiểm tra. Docstring là chuỗi đầu thân hàm mô tả mục đích và hợp đồng.

**Hợp đồng** phải nói rõ kiểu, miền giá trị, đầu ra, có sửa đầu vào không, và lỗi/trường hợp rỗng xử lý thế nào. Hai hàm cùng tên gọi “trung bình” có thể khác chính sách: bộ 6 yêu cầu dữ liệu không rỗng và báo `ValueError` khi rỗng; bộ 8 có hàm trả `None` khi rỗng. Hãy đọc đúng docstring; không đoán từ tên hàm.

Biến được gán trong hàm thường thuộc phạm vi cục bộ, không tự sửa biến cùng tên bên ngoài. Nếu nhận list rồi sửa phần tử/append, hàm vẫn có thể thay đối tượng mà nơi gọi đang dùng. Hàm thuần tính kết quả mà không đổi trạng thái bên ngoài thường dễ test và dùng lại.

```python
# RUN: stdlib
def add_topic(topic, items=None):
    if items is None:
        items = []
    return [*items, topic]

original = ["Python"]
print(add_topic("SQL", original))
print(original)
print(add_topic("A"), add_topic("B"))
```

Đầu ra `['Python', 'SQL']`, `['Python']`, rồi `['A'] ['B']`. Tham số mặc định được tạo khi định nghĩa hàm. Nếu dùng `items=[]` rồi append trực tiếp, nhiều lần gọi bỏ đối số có thể chia sẻ cùng list; dùng `None` rồi tạo list khi cần. Ở ví dụ trên, kết quả luôn là list mới, kể cả khi người gọi truyền một list.

`*args` gom đối số vị trí dư thành tuple; `**kwargs` gom đối số có tên dư thành dict. Chúng hữu ích cho wrapper nhưng không cần dùng cho mọi hàm. Chia một hàm dài theo trách nhiệm như parse → validate → calculate → format để test từng phần; đừng tách thành hàng chục hàm không mang nghĩa.

**Liên hệ AI:** preprocessing, metric và lời gọi tool đều cần hợp đồng rõ. Cùng dữ liệu nhưng hàm vô tình sửa list dùng chung có thể khiến kết quả thí nghiệm khó tái lập.

**Lỗi hay gặp:** chỉ print nên nơi gọi nhận None; return quá sớm trong vòng lặp nên chỉ xử lý phần tử đầu; tin type hint tự từ chối input sai; bắt mọi lỗi rồi trả 0 khiến không phân biệt lỗi với kết quả thật.

**Tự kiểm:** (1) Type hint có tự ngăn `to_hours("90")` không? (2) Vì sao cần ghi có sửa đầu vào hay không?

**Gợi ý đáp án:** (1) Không; ví dụ từ chối nhờ kiểm kiểu trong thân hàm. (2) Nơi gọi cần biết có thể dùng lại bản dữ liệu ban đầu hay phải sao chép.

Tra cú pháp khi cần ở [Python: điều khiển luồng và định nghĩa hàm](https://docs.python.org/3/tutorial/controlflow.html).

<a id="p06"></a>
## P06 — Đường dẫn, UTF-8, CSV, JSON và lưu dữ liệu

**Cần biết trước:** P04–P05; hiểu dữ liệu trong bộ nhớ sẽ mất khi tiến trình kết thúc nếu không lưu.

Đường dẫn tuyệt đối chỉ đầy đủ vị trí, như `F:\Python Learning\README.md`; đường dẫn tương đối như `thuc_hanh/du_lieu/hoc_tap.csv` tính từ thư mục làm việc hiện tại. Vị trí tệp mã và thư mục đang đứng không bắt buộc giống nhau. `pathlib.Path` giúp ghép đường dẫn bằng toán tử `/` thay vì tự nối các dấu gạch của từng hệ điều hành.

Tệp lưu byte; **encoding** quy định cách biến ký tự thành byte và ngược lại. UTF-8 hỗ trợ tiếng Việt. `encoding="utf-8"` ghi rõ quy ước, không dựa vào mặc định máy. Một ký tự Unicode có thể chiếm nhiều byte; `len(text)` và `len(text.encode("utf-8"))` không luôn bằng nhau.

CSV lưu bảng dạng văn bản với quy tắc phân cách và dấu nháy. Không tách một dòng CSV bằng `split(",")` nếu trường có thể chứa dấu phẩy; dùng `csv.DictReader`. JSON mô tả object, array, string, number, boolean và null; Python ánh xạ phổ biến thành dict, list, str, int/float, bool và None. JSON hợp lệ chưa chứng minh có đủ trường và đúng quy tắc nghiệp vụ.

```python
# RUN: stdlib
import csv
import io
import json

csv_text = 'topic,minutes\n"Python, cơ bản",30\nSQL,45\n'
rows = list(csv.DictReader(io.StringIO(csv_text)))
print(rows[0]["topic"], type(rows[0]["minutes"]).__name__)
total = sum(int(row["minutes"]) for row in rows)
payload = {"total_minutes": total, "done": False, "note": None}
encoded = json.dumps(payload, ensure_ascii=False)
print(total)
print(encoded)
print(json.loads(encoded) == payload)
```

Đầu ra `Python, cơ bản str`, `75`, `{"total_minutes": 75, "done": false, "note": null}`, `True`. CSV trả phút là chuỗi nên cần chuyển kiểu sau kiểm tra. `dumps/loads` làm việc với chuỗi; `dump/load` làm việc với đối tượng tệp. JSON dùng chữ thường `false/null`, Python dùng `False/None`. Tra API tại [Python: JSON](https://docs.python.org/3/library/json.html).

`with` quản lý vòng đời tài nguyên: khi rời khối, tệp được đóng kể cả lúc có ngoại lệ. Mở chế độ `"r"` để đọc; `"w"` có thể xóa nội dung cũ ngay khi mở; `"a"` nối thêm nhưng nối nhiều object JSON riêng không tự thành một tệp JSON hợp lệ. JSONL dùng mỗi dòng một JSON, là quy ước khác cần đọc theo dòng.

```python
# RUN: stdlib
from pathlib import Path
from tempfile import TemporaryDirectory
import json

records = [{"id": "s1", "date": "2026-09-12", "topic": "Python", "minutes": 30}]
with TemporaryDirectory() as temporary:
    path = Path(temporary) / "sessions.json"
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
    with path.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    print(loaded[0]["topic"], sum(item["minutes"] for item in loaded))
```

Đầu ra `Python 30`; thư mục tạm được dọn khi rời khối ngoài. Ví dụ chỉ minh họa ghi/đọc. Dự án S1 cần thêm xác thực bản ghi, xử lý JSON hỏng và giữ dữ liệu qua những lần chạy thực.

Luồng lưu S1 nên là: nhận đầu vào → chuyển kiểu → kiểm ngày/chủ đề/phút → đọc dữ liệu hiện có → thêm bản ghi hợp lệ → ghi kết quả. Thiếu tệp có thể khởi đầu list rỗng theo đề; JSON hỏng phải báo lỗi và giữ tệp để sửa, không tự coi là rỗng rồi ghi đè. Cùng một đối tượng JSON đúng cú pháp vẫn có thể sai dạng, như dict thay vì list hoặc `minutes=-1`.

Để tránh ghi dở làm mất bản cũ, mức mở rộng có thể ghi tệp tạm cùng thư mục rồi thay thế khi ghi thành công. Cách này chưa tự giải quyết nhiều tiến trình ghi đồng thời hoặc mọi tình huống mất điện; S1 bắt đầu với một tiến trình và dữ liệu nhỏ.

**Liên hệ AI:** cấu hình, nhãn và corpus thường ở CSV/JSON; lỗi encoding hoặc mất ID nguồn làm pipeline khó truy vết.

**Lỗi hay gặp:** dùng `eval` để đọc JSON; ghép đường dẫn sai; ghi đè trước khi validate; coi `FileNotFoundError` và `JSONDecodeError` là cùng một lỗi. Hãy dùng parser phù hợp và xử lý từng loại theo hợp đồng.

**Tự kiểm:** (1) Vì sao không dùng `split(",")` ở ví dụ? (2) Thiếu file và file JSON hỏng có cùng cách xử lý trong S1 không?

**Gợi ý đáp án:** (1) Chủ đề có dấu phẩy nằm trong dấu nháy, vẫn là một trường. (2) Không; thiếu thì khởi tạo rỗng theo đề, hỏng thì báo lỗi và giữ bằng chứng.

<a id="p07"></a>
## P07 — Ngoại lệ và cách tìm nguyên nhân lỗi

**Cần biết trước:** P02, P05–P06.

Có ba nhóm cần phân biệt: lỗi cú pháp khiến mã không được phân tích đúng; ngoại lệ khi thực thi một thao tác; lỗi logic khi chương trình chạy nhưng cho kết quả sai. Ví dụ thiếu dấu `:` là lỗi cú pháp, `int("abc")` gây `ValueError`, còn chia tổng phút cho 100 thay vì 60 là lỗi logic.

**Traceback** là chuỗi vị trí gọi dẫn đến ngoại lệ. Đọc dòng cuối để biết loại lỗi và thông báo, rồi tìm dòng thuộc mã mình để xem giá trị đã đi vào thao tác đó. Vị trí phát hiện lỗi có thể không phải nơi dữ liệu sai bắt đầu; hãy lần ngược dữ liệu.

```python
# RUN: stdlib
def parse_minutes(raw):
    try:
        value = int(raw)
    except ValueError as error:
        raise ValueError("Nhập số phút nguyên, ví dụ 45") from error
    if value <= 0:
        raise ValueError("Số phút phải lớn hơn 0")
    return value

for raw in ["45", "abc", "0"]:
    try:
        print("OK", parse_minutes(raw))
    except ValueError as error:
        print("Lỗi:", error)
```

Đầu ra `OK 45`, `Lỗi: Nhập số phút nguyên, ví dụ 45`, `Lỗi: Số phút phải lớn hơn 0`. `raise` chủ động báo vi phạm hợp đồng; `try/except` quyết định xử lý loại lỗi đã dự kiến ở biên ứng dụng. `from error` giữ nguyên nhân gốc khi đổi thông báo. Ví dụ nhận chuỗi; không tuyên bố xử lý mọi loại đối tượng.

`else` của try chạy nếu khối try hoàn tất không có ngoại lệ; `finally` phục vụ việc dọn dẹp khi rời try theo luồng thông thường hoặc ngoại lệ. Với tệp, ưu tiên `with` để tránh tự quản lý đóng tệp phức tạp. `except Exception: pass` che lỗi; `except:` còn có thể bắt tín hiệu dừng như KeyboardInterrupt.

Quy trình debug có thể làm ngay: tạo đầu vào nhỏ tái hiện → viết kết quả mong đợi → đọc traceback/so đầu ra → kiểm kiểu và giá trị trước dòng nghi ngờ → sửa một nguyên nhân → chạy lại ca lỗi và ca từng đúng. Dùng `repr(text)` để nhìn khoảng trắng/ký tự xuống dòng thay vì chỉ print văn bản.

```python
# RUN: stdlib
raw = " 45\n"
print(repr(raw), type(raw).__name__)
minutes = int(raw)
wrong_hours = minutes / 100
correct_hours = minutes / 60
print(wrong_hours, correct_hours)
```

Đầu ra đầu là biểu diễn `' 45\n'` và `str`; dòng sau `0.45 0.75`. Không có ngoại lệ nhưng công thức đầu sai đơn vị. Ghi đơn vị cạnh biến và phép tính giúp bắt lỗi này.

**Liên hệ AI:** shape sai thường phát hiện ở phép nhân, nhưng nguyên nhân có thể là bước reshape trước đó. Provider lỗi cần phân loại để quyết định có retry; không phải lỗi nào cũng nên thử lại.

**Lỗi hay gặp:** đổi nhiều dòng cùng lúc rồi không biết dòng nào chữa lỗi; bắt ngoại lệ rộng rồi trả dữ liệu mặc định giống dữ liệu thật; sửa test để khớp lỗi của chương trình.

**Tự kiểm:** (1) Chương trình không báo lỗi có chứng minh phép tính đúng không? (2) Nên bắt lỗi ở hàm tính hay ở chỗ giao tiếp người dùng?

**Gợi ý đáp án:** (1) Không; còn lỗi logic. (2) Hàm tính báo vi phạm hợp đồng, biên CLI/API thường chuyển lỗi dự kiến thành thông báo phù hợp; tùy trách nhiệm cụ thể, không nuốt mọi lỗi ở mọi tầng.

<a id="p08"></a>
## P08 — Kiểm thử: biến yêu cầu thành bằng chứng

**Cần biết trước:** P05 và P07.

Một test có đầu vào, thao tác và kết quả mong đợi được suy từ yêu cầu. Unit test kiểm một đơn vị nhỏ, như chuyển phút sang giờ. Không chỉ kiểm ca bình thường: cần ca biên, rỗng, sai kiểu/miền nếu nằm trong hợp đồng và việc không sửa dữ liệu gốc nếu đã cam kết.

Kết quả mong đợi phải đủ độc lập với cách cài đặt. Nếu test tự tính cùng công thức sai như hàm rồi so, cả hai có thể sai giống nhau. Dùng ca nhỏ tính tay được và ca có khả năng phát hiện một lỗi thực tế.

```python
# RUN: stdlib
import unittest

def mean(values):
    if not values:
        raise ValueError("Cần ít nhất một số")
    return sum(values) / len(values)

class MeanTests(unittest.TestCase):
    def test_unequal_values(self):
        self.assertAlmostEqual(mean([10, 20, 60]), 30.0)

    def test_empty_is_rejected(self):
        with self.assertRaises(ValueError):
            mean([])

    def test_input_unchanged(self):
        data = [3, 1]
        mean(data)
        self.assertEqual(data, [3, 1])

suite = unittest.defaultTestLoader.loadTestsFromTestCase(MeanTests)
result = unittest.TextTestRunner(verbosity=1).run(suite)
assert result.wasSuccessful()
```

Kết quả có `Ran 3 tests` và `OK`; thời gian chạy thay đổi. Test thứ nhất bắt lỗi cộng/sai mẫu số với giá trị không đều, test thứ hai chốt hợp đồng rỗng, test thứ ba kiểm tác động lên đầu vào. Đây là ví dụ cách kiểm tra, không thay bộ chấm 24 bài.

`assertEqual` so giá trị bằng nhau, `assertAlmostEqual` phù hợp một số kiểm tra số thực, `assertRaises` xác nhận loại ngoại lệ; xem [Python unittest](https://docs.python.org/3/library/unittest.html). `assert` trong ví dụ tính toán là cách đối chiếu nhanh khi học; có thể bị bỏ khi chạy Python tối ưu `-O`, nên không dùng làm cơ chế validate đầu vào bên ngoài.

Fixture là dữ liệu/trạng thái chuẩn bị cho test. Test tệp nên tạo thư mục tạm, không phụ thuộc file cá nhân. Fake là đối tượng giả lập phản hồi theo kịch bản, giúp tái hiện lỗi khó; fake không chứng minh dịch vụ hoặc mô hình thật đã chạy đúng. Test chạy được tại máy là bằng chứng cho các ca đã kiểm tra, không chứng minh mọi đầu vào.

Trong bộ khởi động, `--dap-an` chọn mã tham khảo. Thấy OK ở chế độ này xác nhận bản tham khảo trên các test đó; muốn chấm bài mình phải bỏ cờ. Bài trống có thể FAIL/ERROR và đó là trạng thái chưa làm.

**Liên hệ AI:** test phần mềm kiểm schema, batching, lưu/nạp; đánh giá ML kiểm chất lượng dự đoán. Một API trả đúng kiểu và không lỗi vẫn có thể dự đoán sai.

**Lỗi hay gặp:** chỉ kiểm một ca đẹp; test dùng dữ liệu mạng thay đổi; test phụ thuộc thứ tự chạy; mở đáp án rồi viết cứng đầu ra. Khi sửa bug, thêm ca tái hiện có ý nghĩa nếu bộ test chưa bắt được nó.

**Tự kiểm:** (1) Test trả về đúng kiểu có đủ kiểm đúng nội dung không? (2) Vì sao test rỗng của hai hàm mean có thể khác nhau?

**Gợi ý đáp án:** (1) Không; cần kết quả mong đợi theo nhiệm vụ. (2) Hợp đồng có thể chọn báo lỗi hoặc trả None; test phải bám đúng đặc tả.

<a id="p09"></a>
## P09 — Module, package, môi trường ảo và Git

**Cần biết trước:** P05–P08, biết chạy tệp ở terminal.

Module thường là một tệp Python có tên import được; package tổ chức nhiều module dưới một tên chung. Thư viện chuẩn đi kèm Python, như `json`, `csv`, `pathlib`; thư viện ngoài như NumPy phải cài vào môi trường được dùng. `pip` cài gói, còn `import` nạp module để sử dụng. Tên gói cài và tên import đôi khi khác nhau: cài `scikit-learn`, import `sklearn`.

Import chạy mã ở mức module trong lần nạp đầu thông thường. Nếu một module vừa khai báo hàm vừa đọc input ngay, import nó trong test sẽ chờ bàn phím. Đặt điểm chạy ứng dụng dưới `if __name__ == "__main__":` để phân biệt chạy trực tiếp với được import.

```python
# RUN: stdlib
def describe(minutes):
    return f"{minutes} phút"

def main():
    print(describe(45))

if __name__ == "__main__":
    main()
```

Chạy tệp trực tiếp in `45 phút`; khi import tệp để dùng `describe`, phần gọi main không chạy. Import có thể vẫn thực thi những dòng khác ở mức module; guard không tự bảo vệ mã đặt ngoài nó.

Môi trường ảo giữ bộ gói riêng cho dự án, giúp hai dự án dùng phiên bản khác nhau. Nó không phải máy ảo hoặc rào bảo mật; vẫn dùng hệ điều hành và quyền của tiến trình. Trong bộ học, gọi rõ `.\.venv\Scripts\python.exe` tránh cài một nơi rồi chạy nơi khác. `python -m pip` gắn pip với đúng Python đã gọi.

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip --version
```

Hai lệnh kiểm thông tin, không cài thêm. Khi cần gói ML, làm theo BAT_DAU ở tuần tương ứng, sau khi chạy được mới ghi các phiên bản đã kiểm chứng. Ghi danh sách dependency là cần thiết nhưng chưa chứng minh môi trường mới chạy được; còn phiên bản Python, hệ điều hành và cấu hình liên quan.

Git ghi lịch sử các phiên bản mã. Thư mục làm việc chứa bản đang sửa; staging area chứa phần chọn cho lần commit; commit ghi một mốc. `git status` cho biết trạng thái, `git diff` cho thấy nội dung đổi, `git add <tệp>` chọn thay đổi, `git commit` ghi mốc ở máy. Push là đưa commit lên remote và là bước riêng; không cần công khai bài để học Git.

README nên có mục đích, cách cài/chạy/test, ví dụ đầu vào/đầu ra, dữ liệu và giới hạn đã biết. `.gitignore` giúp bỏ qua `.venv`, cache, dữ liệu lớn hoặc secret khỏi các lần thêm thông thường; nó không xóa bí mật đã được commit. Lưu khóa truy cập theo cơ chế cấu hình phù hợp, không trong code hoặc ảnh demo.

**Liên hệ AI:** mã, cấu hình và phiên bản dữ liệu/model phải đi cùng thí nghiệm. Commit giúp biết thay đổi nào tạo ra kết quả mới; seed một mình không mô tả toàn bộ môi trường.

**Lỗi hay gặp:** đặt tệp tên `json.py` che thư viện chuẩn; cài bằng pip của Python khác; commit `.venv`; chạy bằng đường dẫn tương đối từ sai thư mục. Kiểm tên tệp, interpreter và thư mục làm việc trước khi cài lại mọi thứ.

**Tự kiểm:** (1) Commit có tự gửi lên Internet không? (2) Vì sao có thể cài NumPy thành công mà import vẫn lỗi?

**Gợi ý đáp án:** (1) Không; commit là thao tác ghi lịch sử cục bộ. (2) pip và chương trình có thể đang dùng hai môi trường Python khác nhau.

<a id="p10"></a>
## P10 — Đối tượng, composition, iterator và tổ chức dự án CLI

**Cần biết trước:** P04–P09. Ngày đầu chỉ cần tra phần đang dùng; generator/decorator là phần đọc khi đến B21–B22.

Class mô tả kiểu đối tượng với dữ liệu và hành vi liên quan; instance là một đối tượng cụ thể. `self` tham chiếu instance đang nhận lời gọi phương thức. Dataclass tạo giúp một số phương thức như khởi tạo và biểu diễn từ các trường đã khai báo; không tự kiểm miền giá trị hay cưỡng chế type hint.

```python
# RUN: stdlib
from dataclasses import dataclass, field

@dataclass
class StudyLog:
    name: str
    minutes: list[int] = field(default_factory=list)

    def total(self):
        return sum(self.minutes)

a, b = StudyLog("An"), StudyLog("Bình")
a.minutes.append(45)
print(a.name, a.total(), b.total())
```

Đầu ra `An 45 0`. `default_factory=list` tạo list riêng cho từng instance. Khi gọi `a.total()`, a được truyền làm self. Class không bắt buộc cho hàm chuyển phút hoặc phép tính nhỏ; dùng khi nhóm trạng thái và trách nhiệm rõ hơn.

Composition là tạo đối tượng có các thành phần, như Service có Repository để lưu và Validator để kiểm. Service gọi các thành phần qua hợp đồng, dễ thay file repository bằng fake trong test. Inheritance mô tả quan hệ kiểu con; đừng dùng chỉ để chia sẻ vài dòng mã khi hàm hoặc composition đơn giản hơn. Đây là lựa chọn thiết kế, không phải yêu cầu biến mọi bài thành OOP. Tra cơ chế tại [Python: classes](https://docs.python.org/3/tutorial/classes.html).

Iterable là đối tượng có thể lấy iterator để duyệt. Iterator giữ vị trí hiện tại, `next()` lấy phần tử tiếp theo, hết thì báo `StopIteration`. List có thể tạo iterator mới để duyệt lại; một iterator đã hết không tự quay về đầu. Generator dùng `yield` để tạo iterator theo từng bước, giữ trạng thái giữa những lần lấy phần tử.

```python
# RUN: stdlib
def batches(values, size):
    if type(size) is not int or size <= 0:
        raise ValueError("size phải là số nguyên dương")
    for start in range(0, len(values), size):
        yield values[start:start + size]

stream = batches([10, 20, 30, 40, 50], 2)
print(next(stream))
print(list(stream))
print(list(stream))
```

Đầu ra `[10, 20]`, `[[30, 40], [50]]`, `[]`. Generator chỉ tạo batch khi được yêu cầu; list đầu vào vẫn nằm trong bộ nhớ và mỗi slice tạo list con. Muốn streaming toàn bộ cần nguồn cũng đọc từng phần, như duyệt dòng tệp, không đọc toàn bộ rồi gọi generator và kết luận không tốn bộ nhớ.

Context manager hỗ trợ `with`, quản lý việc vào/rời một phạm vi tài nguyên; P06 đã dùng với tệp và thư mục tạm. Decorator nhận một hàm và thường trả hàm được bọc để thêm hành vi. `@decorator` về ý tưởng thay hàm bằng kết quả `decorator(hàm)` lúc định nghĩa, không phải lúc mỗi lần gọi mới trang trí.

```python
# RUN: stdlib
from functools import wraps

def announce(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Gọi:", function.__name__)
        return function(*args, **kwargs)
    return wrapper

@announce
def double(value):
    return value * 2

print(double(3))
```

Đầu ra `Gọi: double`, rồi `6`. `*args/**kwargs` chuyển tiếp đối số; wrapper phải return kết quả để giữ hợp đồng. `wraps` giữ metadata thường cần cho debug/tài liệu. Logging hoặc đo thời gian có thể dùng wrapper, nhưng không log dữ liệu nhạy cảm chỉ vì tiện.

Độ phức tạp mô tả mức tăng công việc theo cỡ n. Duyệt tất cả n bản ghi là O(n); so mọi cặp thường O(n²); sắp xếp so sánh thường O(n log n). Kiểm thành viên set/dict có kỳ vọng trung bình O(1), không phải cam kết mọi trường hợp. Big-O không thay đo thời gian thực: hằng số, bộ nhớ, I/O và thư viện cũng ảnh hưởng. Trước hết chọn thuật toán đúng, sau đó đo phần chậm.

**Ghép vào S1:** tách CLI đọc tham số → hàm validate/calculate → lớp hoặc hàm lưu JSON → format kết quả. CLI là chương trình điều khiển bằng dòng lệnh. `argparse` giúp định nghĩa tên tham số, trợ giúp và chuyển kiểu; kiểm quy tắc nghiệp vụ vẫn ở mã mình.

```python
# RUN: stdlib
import argparse
from datetime import date

parser = argparse.ArgumentParser(description="Ví dụ kiểm một buổi học")
parser.add_argument("--topic", required=True)
parser.add_argument("--minutes", type=int, required=True)
parser.add_argument("--date", required=True)
# Danh sách thay cho tham số thật để ví dụ tự chạy, không đọc terminal.
args = parser.parse_args(["--topic", "Python", "--minutes", "45", "--date", "2026-09-12"])
day = date.fromisoformat(args.date)
if day.isoformat() != args.date or not args.topic.strip() or args.minutes <= 0:
    raise ValueError("Ngày cần YYYY-MM-DD, chủ đề không rỗng, phút dương")
print(day.isoformat(), args.topic.strip(), args.minutes)
```

Đầu ra `2026-09-12 Python 45`. Ở ứng dụng thật, `parse_args()` không truyền danh sách sẽ đọc tham số dòng lệnh. Ngày sai lịch như 30/2 bị parser ngày từ chối; so lại dạng chuẩn giúp giữ định dạng YYYY-MM-DD. ID bản ghi phải không trùng trong kho; có thể tạo UUID rồi kiểm tính duy nhất, không dùng số thứ tự hiển thị làm ID bất biến khi xóa/sắp xếp.

**Lỗi hay gặp:** chia sẻ list giữa các instance; duyệt generator lần hai mong dữ liệu còn; decorator quên return; argparse chuyển được int nhưng phút âm vẫn lọt; chương trình lưu trước rồi mới validate.

**Tự kiểm:** (1) Khi nào generator còn tốn bộ nhớ lớn? (2) Dataclass có tự từ chối `minutes=[-5]` không?

**Gợi ý đáp án:** (1) Nguồn hoặc kết quả bị giữ toàn bộ, hoặc mỗi bước tạo vật lớn; xem cả luồng dữ liệu. (2) Không; phải thực thi kiểm tra ở nơi phù hợp.

Sau mỗi mục, đóng tài liệu và tự giải thích một ví dụ, đổi ít nhất một đầu vào rồi dự đoán lại. Nếu làm được, quay về bài B hoặc bộ bài tập tương ứng. Nếu chưa làm được, xem lại mục tiên quyết thay vì chép đáp án.
