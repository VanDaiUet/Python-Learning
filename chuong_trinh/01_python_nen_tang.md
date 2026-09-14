# Python nền tảng — Tuần 01–12

> Thư viện bài học đầy đủ; số tuần dưới đây thuộc bản 40 tuần. Lịch đang áp dụng là [4 tuần, N01–N28](../LO_TRINH_4_TUAN.md). Chỉ đọc và làm phần được chỉ định trong lịch mới.

Mục tiêu chặng này: từ chưa biết lập trình đến tự viết, kiểm thử và giải thích một ứng dụng dòng lệnh lưu dữ liệu. Đây là nền móng để xử lý dữ liệu và xây dựng dịch vụ AI ở các chặng sau. Bạn chưa cần GPU, tài khoản dịch vụ trả phí hay thư viện bên ngoài.

## Cách học mỗi tuần

- Dành 2 giờ cho hai bài học, 3–4 giờ viết bài tập, 2 giờ sửa lỗi/kiểm thử và 1–2 giờ ôn tập, đọc mã hoặc làm bài nâng cao.
- Với mỗi ví dụ: dự đoán kết quả → chạy → đổi một đầu vào → giải thích kết quả bằng lời của mình.
- **Cơ bản** và **Vận dụng** là bắt buộc. **Nâng cao** là tùy chọn; chưa làm được vẫn có thể sang tuần mới nếu đạt tiêu chí bắt buộc.
- Lưu bài làm độc lập, đầu vào mẫu và ghi chú lỗi đã sửa trong `bai_lam/tuan_XX/`. Với bài khởi đầu có sẵn, sửa đúng tệp được hướng dẫn trong `thuc_hanh/README.md`; muốn đổi dữ liệu mẫu, tạo bản sao trong `bai_lam/`. Không xem lời giải trước khi tự thử.
- Cuối tuần trả lời câu hỏi tự kiểm tra mà không mở tài liệu, rồi chạy lại bài với ít nhất một đầu vào bình thường và một trường hợp biên.
- Dùng môi trường `.venv` của dự án và Python 3.11. Các ví dụ tuần 01–12 chỉ dùng thư viện chuẩn. Lệnh chạy mẫu trên PowerShell: `.\.venv\Scripts\python.exe thuc_hanh\bai_01\demo.py`.
- Trước tuần 08, có thể kiểm tra bằng bảng “đầu vào / kết quả mong đợi / kết quả thật”; từ tuần 08 chuyển những tình huống quan trọng thành kiểm thử tự động.

## Tuần 01 — Chạy chương trình đầu tiên

### B01. Môi trường, tệp Python và đầu ra

**Đọc để hiểu bài:** [P01 — Chạy mã, biến và kiểu](../kien_thuc/01_python.md#p01).

**Mục tiêu:** phân biệt terminal, trình soạn thảo và trình thông dịch; tự chạy được một tệp `.py`.

Python thực hiện các câu lệnh lần lượt từ trên xuống. Trình soạn thảo giúp sửa mã; terminal nhận lệnh; trình thông dịch thực thi mã. `print("Xin chào Python")` gọi hàm `print` với một chuỗi để hiển thị thông tin. Dấu `#` bắt đầu phần chú thích đến cuối dòng; chú thích dành cho người đọc, không được thực thi.

**Thử ngay:** mở `thuc_hanh/bai_01/demo.py`, chạy bằng lệnh ở đầu tài liệu, đổi một thông báo rồi chạy lại. Thêm `print(2 + 3)` và dự đoán vì sao kết quả khác `print("2 + 3")`.

### B02. Biến, kiểu dữ liệu và đầu vào

**Đọc để hiểu bài:** [P01 — Chạy mã, biến và kiểu](../kien_thuc/01_python.md#p01).

**Mục tiêu:** nhận tên, số giờ học và tạo thông báo bằng biến cùng f-string.

Phép gán `ten = "An"` gắn tên biến với một giá trị. Các kiểu đầu tiên cần biết là `str`, `int`, `float`, `bool`; `type(ten)` cho biết kiểu. `input()` luôn trả về chuỗi, nên `gio = float(input("Số giờ: "))` cần bước chuyển đổi trước khi tính toán. `print(f"{ten} đã học {gio} giờ")` ghép dữ liệu vào thông báo dễ đọc. Tuần này dùng đầu vào hợp lệ; tuần 08 sẽ xử lý lỗi nhập liệu.

**Thực hành:**

- **Cơ bản:** in hồ sơ học viên gồm tên, mục tiêu nghề nghiệp và số giờ học mỗi tuần; dùng ít nhất ba biến thay vì viết mọi thứ trong một chuỗi.
- **Vận dụng:** hỏi tên và số giờ đã học trong hai ngày, in tổng giờ và lời chào cá nhân hóa; thử số nguyên, số thập phân và số 0.
- **Nâng cao (tùy chọn):** dự đoán rồi giải thích khác biệt giữa `"3" + "4"`, `3 + 4`, `float("3.5")`.

**Tiêu chí đạt:** B01 chạy đúng tệp bằng Python trong `.venv`; B02 tổng giờ là phép cộng số, đầu ra có nhãn và không sửa mã để thay đổi đầu vào.

**Sản phẩm nộp:** tệp chương trình hồ sơ/học giờ, ba kết quả chạy mẫu và ghi chú vai trò của terminal, editor, interpreter.

**Tự kiểm tra:** 1. Vì sao `input()` cần chuyển kiểu? 2. Dấu `=` làm gì? 3. `print("5")` và `print(5)` giống nhau ở đầu ra nhưng khác nhau ở đâu?

## Tuần 02 — Tính toán và quyết định

### B03. Số, toán tử và biểu thức Boolean

**Đọc để hiểu bài:** [P02 — Biểu thức và điều kiện](../kien_thuc/01_python.md#p02).

**Mục tiêu:** tính đại lượng có đơn vị và xây dựng điều kiện đúng/sai.

`/` cho kết quả phép chia; `//` lấy phần nguyên theo hướng xuống; `%` lấy phần dư. Với số phút không âm, `gio = phut // 60` và `du = phut % 60` đổi phút thành giờ/phút. So sánh như `phut >= 30` trả về `bool`. `and`, `or`, `not` kết hợp điều kiện; ngoặc giúp thể hiện ý định rõ ràng. Số thực có sai số biểu diễn: tránh lấy `0.1 + 0.2 == 0.3` làm cách kiểm tra kết quả tính toán số thực.

**Thử ngay:** đổi 135 phút thành 2 giờ 15 phút; dự đoán `0 <= phut <= 600` với các giá trị -1, 0, 600 và 601.

### B04. Rẽ nhánh `if`, `elif`, `else`

**Đọc để hiểu bài:** [P02 — Biểu thức và điều kiện](../kien_thuc/01_python.md#p02).

**Mục tiêu:** phân loại đầu vào bằng các nhánh có thứ tự và không bỏ sót trường hợp biên.

Một chuỗi `if/elif/else` chỉ chạy nhánh đúng đầu tiên. Thụt lề xác định câu lệnh thuộc nhánh nào. Khi phân loại điểm, kiểm tra ngoài khoảng 0–100 trước, sau đó kiểm tra các ngưỡng từ cao xuống thấp. Hai câu `if` độc lập có thể cùng chạy; chúng không luôn tương đương một cặp `if/elif`.

**Thực hành:**

- **Cơ bản:** nhập tổng số phút không âm, hiển thị giờ/phút; nhập số âm thì in thông báo không hợp lệ.
- **Vận dụng:** đánh giá mức hoàn thành mục tiêu: dưới 50% là “cần tăng tốc”, từ 50% đến dưới 100% là “đang tiến bộ”, từ 100% là “đạt”; mục tiêu phải lớn hơn 0, số giờ thực tế không âm.
- **Nâng cao (tùy chọn):** tính phí GPU giả lập theo bậc giờ và giải thích khác biệt giữa tính lũy tiến và áp một mức giá cho toàn bộ số giờ.

**Tiêu chí đạt:** B03 đổi phút đúng với 0, 59, 60, 135; B04 xử lý đúng tại 0%, 50%, 100%, từ chối mục tiêu bằng 0 trước phép chia.

**Sản phẩm nộp:** hai chương trình tính toán và bảng ít nhất sáu trường hợp kiểm tra, gồm giá trị tại ngưỡng.

**Tự kiểm tra:** 1. `/` khác `//` thế nào? 2. Khi nào hai `if` cùng chạy? 3. Đổi thứ tự các nhánh có thể làm sai kết quả ra sao?

## Tuần 03 — Lặp lại công việc

### B05. `for`, `range` và biến tích lũy

**Đọc để hiểu bài:** [P03 — Vòng lặp và điều kiện dừng](../kien_thuc/01_python.md#p03).

**Mục tiêu:** xử lý một số lần lặp biết trước và theo dõi tổng hoặc số lượng.

`for` lần lượt nhận các phần tử; `range(1, 8)` sinh các số từ 1 đến 7, không gồm 8. Cú pháp `[30, 0, 45]` tạo một list chứa ba giá trị để vòng lặp lấy từng giá trị; tuần 04 sẽ học cách cập nhật list. Khởi tạo `tong = 0` trước vòng lặp rồi dùng `tong += phut` sau mỗi lần nhập. Nếu đặt lại tổng bên trong vòng lặp, kết quả chỉ còn dữ liệu của lần cuối. Đặt tên biến theo ý nghĩa như `ngay`, `phut`, `tong_phut` để dễ kiểm tra.

**Thử ngay:** nhập phút học trong ba ngày, in số thứ tự ngày và tổng cộng; ghi lại giá trị của `tong` sau từng vòng.

### B06. `while`, điều kiện dừng và menu

**Đọc để hiểu bài:** [P03 — Vòng lặp và điều kiện dừng](../kien_thuc/01_python.md#p03).

**Mục tiêu:** viết vòng lặp chạy đến khi người dùng chọn kết thúc.

`while` kiểm tra điều kiện trước mỗi lượt. Vòng lặp cần đường đi làm điều kiện sai hoặc gặp `break`; nếu không, chương trình có thể chạy mãi. `continue` bỏ phần còn lại của lượt hiện tại. Mẫu menu có thể dùng `while True`, nhận lựa chọn, rồi `break` khi lựa chọn bằng `"0"`; các lựa chọn khác thực hiện hành động tương ứng.

**Thực hành:**

- **Cơ bản:** nhập thời lượng học của bảy ngày bằng `for`, tính tổng và đếm ngày đạt ít nhất 30 phút.
- **Vận dụng:** làm menu “1: ghi một buổi học, 2: xem tổng, 0: thoát”; giữ tổng trong bộ nhớ, từ chối số phút âm và không cộng dữ liệu bị từ chối.
- **Nâng cao (tùy chọn):** hiển thị bảng nhân bằng vòng lặp lồng nhau; giải thích tổng số lượt chạy khi có 5 hàng, mỗi hàng 4 cột.

**Tiêu chí đạt:** B05 tổng đúng khi mọi ngày đều 0 và khi chỉ một ngày có dữ liệu; B06 cho phép nhiều thao tác, giữ tổng chính xác, có lệnh thoát và xử lý lựa chọn lạ.

**Sản phẩm nộp:** chương trình thống kê bảy ngày, menu đầu tiên và một bản ghi diễn tiến giá trị biến qua ba lượt lặp.

**Tự kiểm tra:** 1. `range(5)` gồm các số nào? 2. Đặt biến tích lũy ở đâu? 3. `break` khác `continue` thế nào?

## Tuần 04 — Chuỗi và danh sách

### B07. Xử lý văn bản và định dạng đầu ra

**Đọc để hiểu bài:** [P04 — Chuỗi và cấu trúc dữ liệu](../kien_thuc/01_python.md#p04).

**Mục tiêu:** chuẩn hóa văn bản nhập vào và tách/ghép các thành phần đơn giản.

Chuỗi là một dãy ký tự có chỉ số bắt đầu từ 0; `s[:3]` lấy ba ký tự đầu. Chuỗi không sửa trực tiếp từng ký tự được; các thao tác như `strip()` hay `lower()` trả về chuỗi mới. `"Python, SQL".split(",")` tách theo dấu phẩy, sau đó cần `strip()` từng phần. `split()` không truyền dấu phân cách sẽ tách theo các cụm khoảng trắng; `" ".join("  Python   cho AI  ".split())` cho `"Python cho AI"`. `", ".join(ds)` ghép một dãy chuỗi. Không dùng `split(",")` để thay thế trình đọc CSV có quy tắc dấu nháy.

**Thử ngay:** chuẩn hóa `"  PyThOn  "` thành `"python"`; dùng `f"{ty_le:.1f}%"` để hiển thị một chữ số thập phân mà không thay đổi giá trị gốc.

### B08. Danh sách, duyệt và sao chép

**Đọc để hiểu bài:** [P04 — Chuỗi và cấu trúc dữ liệu](../kien_thuc/01_python.md#p04).

**Mục tiêu:** lưu nhiều bản ghi, cập nhật dữ liệu và hiểu tác động khi hai biến trỏ cùng danh sách.

`list` có thứ tự và có thể thay đổi bằng `append`, phép gán phần tử hoặc `pop`. `enumerate(ds, start=1)` vừa lấy số thứ tự vừa lấy giá trị. Với `a = [1, 2]; b = a`, sửa `b` cũng ảnh hưởng `a`; `b = a.copy()` tách danh sách ngoài nhưng chưa sao chép sâu các phần tử lồng nhau. List comprehension như `[x * 2 for x in ds]` tạo danh sách mới; ưu tiên vòng lặp thường khi logic còn khó đọc.

**Thực hành:**

- **Cơ bản:** nhận chuỗi chủ đề ngăn bởi dấu phẩy, bỏ khoảng trắng thừa, bỏ mục rỗng và in các chủ đề kèm số thứ tự.
- **Vận dụng:** lưu thời lượng nhiều buổi học trong list, hiển thị tổng/trung bình/lớn nhất; cho phép xóa buổi theo số thứ tự và xử lý danh sách rỗng trước khi tính trung bình hoặc gọi `max`.
- **Nâng cao (tùy chọn):** tạo danh sách hai chiều, thử sao chép nông rồi sửa một phần tử con; viết lời giải thích bằng hình hoặc văn bản.

**Tiêu chí đạt:** B07 xử lý được chuỗi rỗng và `" Python, , SQL "`; B08 thống kê đúng, không truy cập vượt chỉ số, không chia cho 0 khi rỗng.

**Sản phẩm nộp:** bộ chuẩn hóa chủ đề, thống kê danh sách buổi học và ví dụ chứng minh tác động của phép gán danh sách.

**Tự kiểm tra:** 1. `strip()` có sửa chuỗi gốc không? 2. `a = b` khác `a = b.copy()` ở đâu? 3. Vì sao phải kiểm tra danh sách rỗng?

## Tuần 05 — Chọn cấu trúc dữ liệu

### B09. Tuple, set và phép kiểm tra thành viên

**Đọc để hiểu bài:** [P04 — Chuỗi và cấu trúc dữ liệu](../kien_thuc/01_python.md#p04).

**Mục tiêu:** chọn cách biểu diễn dữ liệu dựa trên thứ tự, trùng lặp và nhu cầu cập nhật.

Tuple như `(ngay, phut)` phù hợp nhóm giá trị có cấu trúc cố định; bản thân tuple không cho thay phần tử, nhưng phần tử bên trong vẫn có thể là đối tượng thay đổi được. Set giữ các phần tử duy nhất và không dùng để biểu diễn thứ tự. Với hai tập chủ đề, `a & b` là phần chung, `a | b` là hợp, `a - b` là phần chỉ có trong `a`. Toán tử `in` kiểm tra một giá trị có thuộc tập hợp/dãy hay không.

**Thử ngay:** từ `['python', 'sql', 'python']` lấy các chủ đề duy nhất; dùng `sorted(...)` khi cần in kết quả theo thứ tự ổn định.

### B10. Dictionary và dữ liệu lồng nhau

**Đọc để hiểu bài:** [P04 — Chuỗi và cấu trúc dữ liệu](../kien_thuc/01_python.md#p04).

**Mục tiêu:** mô hình hóa bản ghi theo tên trường và tổng hợp theo khóa.

Dictionary ánh xạ khóa sang giá trị, ví dụ `{"topic": "python", "minutes": 45}`. `record["topic"]` yêu cầu khóa tồn tại; `record.get("note", "")` cung cấp mặc định cho trường tùy chọn. Mẫu `totals[topic] = totals.get(topic, 0) + minutes` cộng thời lượng theo chủ đề. Một list chứa nhiều dict là bước đầu để hiểu dữ liệu bảng và tài liệu JSON dùng trong ứng dụng AI.

**Thực hành:**

- **Cơ bản:** so sánh tập chủ đề đã học với tập bắt buộc, in chủ đề còn thiếu theo thứ tự chữ cái; thử đầu vào có chủ đề trùng lặp.
- **Vận dụng:** dùng list các dict lưu ít nhất năm buổi học, tính tổng phút theo chủ đề, lọc buổi từ 30 phút và in báo cáo dễ đọc.
- **Nâng cao (tùy chọn):** xây chỉ mục `id → bản ghi`, phát hiện ID trùng trước khi thêm để tránh ghi đè bản ghi cũ.

**Tiêu chí đạt:** B09 kết quả không bị lặp và không phụ thuộc thứ tự hiển thị của set; B10 tổng theo chủ đề đúng, trường ghi chú thiếu có mặc định, khóa bắt buộc được kiểm tra.

**Sản phẩm nộp:** bộ dữ liệu mẫu trong mã, báo cáo tổng hợp và ghi chú vì sao chọn list, tuple, set hoặc dict ở từng vị trí.

**Tự kiểm tra:** 1. Set có giữ phần tử trùng không? 2. Khi nào dùng `get` thay cho `[]`? 3. Gán hai lần cùng khóa ảnh hưởng dữ liệu ra sao?

## Tuần 06 — Tách bài toán thành hàm

### B11. Hàm, tham số, giá trị trả về và phạm vi biến

**Đọc để hiểu bài:** [P05 — Hàm và hợp đồng](../kien_thuc/01_python.md#p05).

**Mục tiêu:** tách phép tính khỏi nhập/xuất để tái sử dụng và kiểm tra độc lập.

Hàm nhận tham số, thực hiện một nhiệm vụ rồi có thể `return` kết quả. `print` chỉ hiển thị, không thay thế giá trị trả về. Viết `def tong_phut(values): return sum(values)` cho phép cùng phép tính phục vụ CLI, kiểm thử và API sau này. Biến tạo trong hàm thường thuộc phạm vi cục bộ. Tránh hàm tính toán phụ thuộc biến toàn cục vì đầu vào thực tế trở nên khó thấy.

**Thử ngay:** viết `trung_binh(values)` với quy ước danh sách rỗng gây `ValueError`, thống nhất với bài khởi đầu tuần 06. Dùng `if not values:` rồi thụt lề câu `raise ValueError("Không thể tính trung bình của danh sách rỗng")` để từ chối dữ liệu không có trung bình xác định. `raise` chủ động báo lỗi; tuần 08 sẽ học cách bắt lỗi. Gọi trực tiếp bằng ba bộ đầu vào, không dùng `input()` trong hàm. Quy ước là một phần của hợp đồng: bài tuần 08 sẽ yêu cầu trả `None` cho dữ liệu rỗng và ghi rõ sự thay đổi này.

### B12. Hợp đồng hàm, type hint và docstring

**Đọc để hiểu bài:** [P05 — Hàm và hợp đồng](../kien_thuc/01_python.md#p05).

**Mục tiêu:** làm rõ hàm nhận gì, trả gì và có thay đổi dữ liệu đầu vào hay không.

`def tong_phut(values: list[int]) -> int:` giúp người đọc và công cụ hiểu ý định; type hint không tự kiểm tra kiểu lúc chạy. Docstring mô tả ý nghĩa tham số, đơn vị, kết quả và trường hợp biên. Tránh tham số mặc định dạng list/dict có thể thay đổi; dùng `None` rồi tạo đối tượng mới trong hàm. Khi lọc dữ liệu, quyết định rõ trả danh sách mới hay sửa danh sách được truyền vào.

**Thực hành:**

- **Cơ bản:** tách hàm chuẩn hóa chủ đề, tính tổng và tính trung bình; thêm type hint, docstring và ví dụ gọi hàm.
- **Vận dụng:** viết `tong_theo_chu_de(records)` và `loc_theo_phut(records, minimum)`; tái sử dụng trong báo cáo tuần 05, giữ `input`/`print` ở phần giao tiếp.
- **Nâng cao (tùy chọn):** viết hàm nhận một hàm điều kiện để lọc bản ghi; so sánh sự dễ đọc với hai hàm lọc viết riêng.

**Tiêu chí đạt:** B11 các hàm tính toán gọi được mà không tương tác terminal; B12 có kiểu tham số/kết quả, quy ước dữ liệu rỗng và không thay đổi đầu vào ngoài hợp đồng.

**Sản phẩm nộp:** bản tách hàm của báo cáo, bảng đầu vào/kết quả cho từng hàm và một ví dụ phân biệt `return` với `print`.

**Tự kiểm tra:** 1. Hàm không có `return` trả gì? 2. Type hint có tự chặn sai kiểu không? 3. Vì sao mặc định `items=[]` có thể gây lỗi khó thấy?

## Tuần 07 — Dữ liệu tồn tại sau khi tắt chương trình

### B13. Đường dẫn, tệp văn bản và CSV

**Đọc để hiểu bài:** [P06 — Tệp, CSV và JSON](../kien_thuc/01_python.md#p06).

**Mục tiêu:** đọc/ghi dữ liệu bảng có tiếng Việt bằng đường dẫn rõ ràng.

`Path` trong `pathlib` biểu diễn đường dẫn; `base / "data.csv"` ghép đường dẫn mà không tự nối dấu phân cách. Đường dẫn tương đối phụ thuộc thư mục đang chạy lệnh. Dùng `with path.open(..., encoding="utf-8") as f:` để đóng tệp khi ra khỏi khối. CSV cần `csv.DictReader`/`DictWriter` và `newline=""`; mỗi ô đọc từ CSV thường là chuỗi nên phải chuyển `minutes` về số trước khi tính toán.

**Thử ngay:** tạo CSV có cột `topic,minutes,note`, đọc bằng `DictReader`, in kiểu của `minutes`; thêm ghi chú có dấu phẩy để kiểm tra lý do cần thư viện `csv`.

### B14. JSON, cấu trúc bản ghi và kiểm tra dữ liệu

**Đọc để hiểu bài:** [P06 — Tệp, CSV và JSON](../kien_thuc/01_python.md#p06).

**Mục tiêu:** lưu/khôi phục list các dict và kiểm tra nội dung trước khi sử dụng.

JSON biểu diễn đối tượng, mảng và các giá trị cơ bản; `json.dump`/`load` làm việc với tệp, `dumps`/`loads` làm việc với chuỗi. `ensure_ascii=False` giúp nội dung tiếng Việt dễ đọc, `indent=2` giúp quan sát cấu trúc. JSON hợp lệ về cú pháp vẫn có thể sai nghiệp vụ, chẳng hạn `minutes` âm hoặc thiếu `topic`. Xác định rõ trường bắt buộc và điều kiện của từng trường trước khi viết mã kiểm tra.

**Thực hành:**

- **Cơ bản:** ghi ba bản ghi ra CSV UTF-8 rồi đọc lại, chuyển thời lượng thành số và xác nhận tổng giữ nguyên.
- **Vận dụng:** chuyển CSV sang JSON theo cấu trúc thống nhất; phát hiện dòng thiếu chủ đề, thời lượng âm hoặc không chuyển thành số được. Có thể ghi nhận lỗi bằng kiểm tra đơn giản; tuần 08 sẽ chuẩn hóa ngoại lệ.
- **Nâng cao (tùy chọn):** cho người dùng chỉ định thư mục đầu ra; tạo thư mục còn thiếu bằng `mkdir(parents=True, exist_ok=True)` và hiển thị đường dẫn tuyệt đối của tệp đã ghi.

**Tiêu chí đạt:** B13 dữ liệu tiếng Việt, dấu phẩy và dấu nháy được bảo toàn; B14 đọc lại JSON cho cùng dữ liệu nghiệp vụ, dữ liệu không hợp lệ không âm thầm đi vào báo cáo.

**Sản phẩm nộp:** chương trình chuyển đổi, một CSV hợp lệ, một JSON tương ứng, một tệp dữ liệu lỗi và mô tả các trường bắt buộc.

**Tự kiểm tra:** 1. Đường dẫn tương đối được tính từ đâu? 2. Vì sao không tự tách CSV bằng dấu phẩy? 3. JSON đúng cú pháp đã bảo đảm dữ liệu đúng chưa?

## Tuần 08 — Tìm lỗi và kiểm thử

### B15. Ngoại lệ và quy trình gỡ lỗi

**Đọc để hiểu bài:** [P07 — Ngoại lệ và debug](../kien_thuc/01_python.md#p07).

**Mục tiêu:** đọc traceback, thu hẹp nguyên nhân và đưa thông báo lỗi có ích.

Đọc loại lỗi và thông báo ở cuối traceback, rồi tìm dòng mã của mình gây lỗi. `try/except ValueError` xử lý lỗi chuyển đổi dự kiến; `FileNotFoundError` chỉ rõ tệp không tồn tại. Giữ khối `try` nhỏ và bắt loại lỗi cụ thể. Dùng `raise ValueError("minutes phải lớn hơn 0")` khi quy tắc nghiệp vụ bị vi phạm. Không dùng `except: pass` vì nó làm lỗi biến mất mà dữ liệu có thể đã sai.

**Thử ngay:** gây lỗi với `int("abc")`, đọc traceback, rồi đặt chuyển đổi trong hàm và thử debugger hoặc `breakpoint()` để xem giá trị trước dòng lỗi.

### B16. Kiểm thử đơn vị với `unittest`

**Đọc để hiểu bài:** [P08 — Kiểm thử](../kien_thuc/01_python.md#p08).

**Mục tiêu:** tự động kiểm tra hành vi đúng, trường hợp biên và lỗi mong đợi.

Một kiểm thử chuẩn bị dữ liệu, gọi hàm rồi so sánh kết quả với yêu cầu. Dùng `assertEqual` cho kết quả chính xác, `assertAlmostEqual` khi phù hợp với số thực và `assertRaises` cho lỗi dự kiến. Kiểm tra hành vi người dùng cần, chẳng hạn “dòng CSV có dấu phẩy giữ nguyên ghi chú”, thay vì lặp lại công thức của hàm trong phần mong đợi. `tempfile.TemporaryDirectory` giúp bài kiểm tra đọc/ghi tệp tự tạo và tự dọn dữ liệu riêng.

**Thực hành:**

- **Cơ bản:** sửa ba lỗi có chủ đích: sai ngưỡng, chia cho 0 và chuyển số thất bại; ghi nguyên nhân và đầu vào nhỏ nhất tái hiện được lỗi.
- **Vận dụng:** viết ít nhất tám test cho tổng hợp và kiểm tra bản ghi: dữ liệu thường, rỗng, biên, thiếu trường, sai kiểu, số âm, tiếng Việt và CSV đọc/ghi giữ nguyên nội dung.
- **Nâng cao (tùy chọn):** thêm bài kiểm tra xác nhận khi nhập lỗi thì tệp dữ liệu trước đó không thay đổi; dùng thư mục tạm cho toàn bộ kiểm tra.

**Tiêu chí đạt:** B15 lỗi dự kiến có thông báo cụ thể, lỗi bất ngờ không bị nuốt; B16 test chạy độc lập, không phụ thuộc thứ tự và thực sự thất bại khi cài lại một lỗi đã sửa.

**Sản phẩm nộp:** mã đã sửa, bộ `unittest` và nhật ký ngắn “triệu chứng → nguyên nhân → cách sửa → test ngăn lỗi quay lại”.

**Tự kiểm tra:** 1. Vì sao bắt mọi ngoại lệ có thể che lỗi? 2. Test có nên dùng tệp dữ liệu cá nhân thật không? 3. Test chạy xanh nhưng không phát hiện lỗi có ích không?

## Tuần 09 — Tổ chức một dự án Python

### B17. Module, package và môi trường ảo

**Đọc để hiểu bài:** [P09 — Module, môi trường và Git](../kien_thuc/01_python.md#p09).

**Mục tiêu:** chia chương trình thành các phần có trách nhiệm rõ và dùng đúng trình thông dịch.

Một tệp `.py` có thể được nhập như module; package nhóm nhiều module liên quan. `if __name__ == "__main__":` giới hạn phần chạy CLI để `import` không tự hỏi dữ liệu hay ghi tệp. Tách kiểm tra dữ liệu, lưu trữ và giao tiếp để từng phần có thể kiểm thử riêng. `.venv` tách môi trường dự án; nó không tự mang theo dữ liệu hay mã nguồn. Khi cần gọi pip sau này, dùng `python -m pip` qua đúng Python của môi trường.

**Thử ngay:** in `sys.executable` để xác nhận Python đang dùng; chuyển một hàm sang module khác rồi import, kiểm tra import không tạo tệp mới.

### B18. Git, README và lịch sử thay đổi

**Đọc để hiểu bài:** [P09 — Module, môi trường và Git](../kien_thuc/01_python.md#p09).

**Mục tiêu:** lưu được các mốc làm việc có ý nghĩa và hướng dẫn người khác chạy dự án.

Git ghi lịch sử mã nguồn bằng commit. `git status` cho biết thay đổi; `git diff` giúp đọc lại nội dung trước khi `git add` và `git commit`. `.gitignore` thường bỏ qua `.venv/`, `__pycache__/` và dữ liệu riêng; tệp đã được theo dõi không tự biến mất chỉ vì thêm vào ignore. README cần mục đích, phiên bản Python, cách chạy, kiểm thử và ví dụ đầu vào/đầu ra. Tuần này chỉ cần repo trên máy, không cần xuất bản lên mạng.

**Thực hành:**

- **Cơ bản:** tách chương trình hiện có thành các module logic, lưu trữ và CLI; thêm điểm vào chỉ chạy khi được gọi trực tiếp.
- **Vận dụng:** tạo hoặc dùng repo Git cục bộ, thiết lập `.gitignore`, tạo ba commit có ý nghĩa; viết README để mở terminal mới vẫn làm theo được lệnh chạy và kiểm thử.
- **Nâng cao (tùy chọn):** tạo nhánh cho một thay đổi nhỏ, xem diff, commit và hợp nhất về nhánh chính; tự giải thích lợi ích của mỗi bước.

**Tiêu chí đạt:** B17 import không phát sinh tương tác hay ghi dữ liệu; B18 lịch sử không chứa `.venv`, cache hoặc dữ liệu nhạy cảm, các lệnh README hoạt động từ thư mục được chỉ định.

**Sản phẩm nộp:** dự án đã chia module, README, `.gitignore` và lịch sử ít nhất ba mốc thay đổi có mô tả cụ thể.

**Tự kiểm tra:** 1. Module khác môi trường ảo thế nào? 2. Vì sao cần `__name__` guard? 3. `.gitignore` có xóa tệp đã commit không?

## Tuần 10 — Mô hình hóa bằng đối tượng

### B19. Class, instance và dataclass

**Đọc để hiểu bài:** [P10 — OOP, generator và CLI](../kien_thuc/01_python.md#p10).

**Mục tiêu:** tạo kiểu dữ liệu biểu diễn buổi học và phân biệt dữ liệu của từng đối tượng.

Class mô tả kiểu đối tượng; instance là một đối tượng cụ thể. Phương thức nhận `self` để truy cập trạng thái của instance. `@dataclass` tự sinh một số phương thức thường dùng cho lớp dữ liệu, giúp tập trung vào trường như `topic: str` và `minutes: int`. Nó không tự xác thực type hint hoặc quy tắc nghiệp vụ; cần kiểm tra khi tạo hoặc nhập dữ liệu. Trường mặc định dạng list dùng `field(default_factory=list)` để mỗi instance có danh sách riêng.

**Thử ngay:** tạo hai buổi học và sửa ghi chú của một buổi; xác nhận buổi còn lại không đổi. Dùng `dataclasses.asdict` khi cần chuyển dữ liệu cơ bản sang dict để lưu JSON.

### B20. Composition và thiết kế vừa đủ

**Đọc để hiểu bài:** [P10 — OOP, generator và CLI](../kien_thuc/01_python.md#p10).

**Mục tiêu:** ghép các đối tượng có trách nhiệm nhỏ và tránh phụ thuộc cứng vào cách lưu tệp.

Composition là để một đối tượng sử dụng đối tượng khác, ví dụ `LearningLog` nhận một `JsonStore` chịu trách nhiệm đọc/ghi. Điều này cho phép thay store thật bằng store trong bộ nhớ khi kiểm thử. Kế thừa thể hiện quan hệ “là một loại”, không phải cách mặc định để tái sử dụng mọi đoạn mã. Hàm vẫn phù hợp cho phép biến đổi không cần giữ trạng thái; chỉ tạo class khi trạng thái và hành vi thực sự liên quan.

**Thực hành:**

- **Cơ bản:** viết dataclass buổi học với kiểm tra chủ đề không rỗng và số phút dương; thêm test cho hai instance độc lập.
- **Vận dụng:** tạo lớp quản lý nhật ký nhận thành phần lưu trữ qua tham số, hỗ trợ thêm và thống kê; dùng store trong bộ nhớ để kiểm tra mà không chạm tệp thật.
- **Nâng cao (tùy chọn):** thêm store CSV cùng giao diện thao tác, giải thích phần mã nào có thể giữ nguyên khi đổi cách lưu trữ.

**Tiêu chí đạt:** B19 đối tượng được tạo có dữ liệu hợp lệ và không dùng chung mặc định mutable; B20 logic báo cáo không phải biết chi tiết định dạng tệp, kiểm thử chạy với store thay thế.

**Sản phẩm nộp:** mô hình buổi học, lớp quản lý nhật ký, hai ví dụ sử dụng và test cho kiểm tra dữ liệu/cô lập lưu trữ.

**Tự kiểm tra:** 1. Dataclass có tự kiểm tra kiểu không? 2. Composition giúp thay thành phần thế nào? 3. Khi nào một hàm đơn giản phù hợp hơn class?

## Tuần 11 — Những cơ chế Python dùng trong dữ liệu và dịch vụ

### B21. Iterable, iterator và generator

**Đọc để hiểu bài:** [P10 — OOP, generator và CLI](../kien_thuc/01_python.md#p10).

**Mục tiêu:** xử lý dữ liệu lần lượt và nhận biết khi nào dữ liệu bị đưa toàn bộ vào bộ nhớ.

Iterable cung cấp iterator; iterator giữ vị trí và trả từng phần tử qua `next`. Generator dùng `yield` để tạm dừng hàm rồi tiếp tục ở lần lấy tiếp theo. Ví dụ `def dem(n):` với `for i in range(n): yield i` tạo từng số theo nhu cầu. Generator thường dùng một lượt; gọi `list(generator)` vừa tiêu thụ nó vừa đưa toàn bộ kết quả vào bộ nhớ. Đọc từng dòng tệp là nền tảng cho luồng dữ liệu lớn hơn bộ nhớ.

**Thử ngay:** tạo generator ba số, gọi `next` một lần rồi chuyển phần còn lại thành list; giải thích vì sao số đầu đã không còn trong list.

### B22. Context manager, decorator và độ phức tạp cơ bản

**Đọc để hiểu bài:** [P10 — OOP, generator và CLI](../kien_thuc/01_python.md#p10).

**Mục tiêu:** hiểu việc quản lý tài nguyên, bọc hành vi hàm và đánh giá chi phí thuật toán đơn giản.

Context manager điều phối lúc vào/ra khối `with`, kể cả khi có lỗi; `with open(...)` vì vậy đóng tệp đúng lúc. Decorator nhận hàm và trả hàm bọc, ví dụ đo thời gian bằng `time.perf_counter`; dùng `functools.wraps` để giữ thông tin của hàm gốc. Về chi phí, một lượt duyệt n bản ghi là O(n); hai vòng lồng duyệt toàn bộ thường là O(n²). Tra cứu dict trung bình gần O(1), nhưng vẫn có chi phí bộ nhớ và trường hợp xấu; ký hiệu không thay thế đo đạc.

**Thực hành:**

- **Cơ bản:** viết generator đọc bản ghi CSV từng dòng, lọc buổi đạt 30 phút và tính tổng mà không tạo list toàn bộ dữ liệu.
- **Vận dụng:** dùng `with` cho đọc/ghi, viết decorator đo thời gian vẫn trả nguyên kết quả và truyền ngoại lệ; so sánh tìm ID bằng quét list với tạo dict chỉ mục, nêu cả chi phí xây chỉ mục.
- **Nâng cao (tùy chọn):** tạo context manager bằng `contextlib.contextmanager` để đo thời gian một khối mã; kiểm tra phần kết thúc vẫn chạy khi khối có lỗi.

**Tiêu chí đạt:** B21 không đọc toàn tệp rồi mới yield và giải thích được generator bị tiêu thụ; B22 wrapper giữ kết quả/ngoại lệ, phân biệt thời gian chạy thực tế với tốc độ tăng theo kích thước đầu vào.

**Sản phẩm nộp:** bộ đọc/lọc theo luồng, decorator có kiểm thử và ghi chú so sánh hai cách tra cứu với ít nhất hai kích thước dữ liệu.

**Tự kiểm tra:** 1. Generator có tự lưu mọi kết quả không? 2. Vì sao `list(...)` có thể mất lợi ích bộ nhớ? 3. Xây dict để tra cứu một lần có luôn tốt hơn quét list không?

## Tuần 12 — P01: Nhật ký học tập bằng dòng lệnh

### B23. Thiết kế và xây phiên bản chạy được

**Đọc để hiểu bài:** [P06 — Tệp, CSV và JSON](../kien_thuc/01_python.md#p06); [P09 — Module, môi trường và Git](../kien_thuc/01_python.md#p09); [P10 — OOP, generator và CLI](../kien_thuc/01_python.md#p10).

**Mục tiêu:** ghép các kỹ năng đã học thành công cụ sử dụng được qua nhiều lần chạy.

Ứng dụng cần các thao tác thêm buổi học, liệt kê, thống kê theo chủ đề và xuất CSV; dùng JSON làm nguồn lưu chính. Mỗi bản ghi gồm `id`, `date` dạng `YYYY-MM-DD`, `topic`, `minutes`, `note`. Định nghĩa dữ liệu trước: ID duy nhất, ngày hợp lệ theo `datetime.date.fromisoformat`, chủ đề sau chuẩn hóa không rỗng, số phút là số nguyên dương. Dùng `argparse` để nhận lệnh/phần trợ giúp; tách xử lý lệnh khỏi logic nghiệp vụ. Dữ liệu mẫu luôn là dữ liệu giả.

**Thử ngay:** phác thảo các lệnh `add`, `list`, `summary`, `export`; viết một luồng hoàn chỉnh “thêm → tắt chương trình → mở lại → thấy bản ghi” trước khi mở rộng chức năng.

### B24. Hoàn thiện, chứng minh và tự đánh giá

**Đọc để hiểu bài:** [P07 — Ngoại lệ và debug](../kien_thuc/01_python.md#p07); [P08 — Kiểm thử](../kien_thuc/01_python.md#p08); [P09 — Module, môi trường và Git](../kien_thuc/01_python.md#p09).

**Mục tiêu:** bàn giao một dự án có kiểm thử và hướng dẫn tái lập được.

Phân biệt “chưa có tệp” với “tệp đã tồn tại nhưng hỏng”: trường hợp đầu có thể bắt đầu nhật ký rỗng, trường hợp sau phải báo lỗi và không tự ghi đè. Kiểm tra bản ghi trước khi lưu; xuất CSV giữ nguyên tiếng Việt và dấu nháy. README mô tả cách chạy bằng Python trong `.venv`, dữ liệu mẫu, lệnh test và giới hạn hiện tại. Chạy mọi kiểm thử và thử thao tác qua CLI vì test hàm riêng chưa chứng minh các phần đã kết nối đúng.

**Thực hành:**

- **Cơ bản:** thực hiện đủ bốn thao tác, lưu/đọc JSON, xuất CSV và hiển thị trợ giúp; thống kê đúng cho dữ liệu rỗng và nhiều chủ đề.
- **Vận dụng:** viết ít nhất 12 test có ý nghĩa, gồm ngày không hợp lệ, thiếu trường, số phút sai kiểu/âm/0, ID trùng, tệp JSON hỏng, CSV có dấu phẩy/tiếng Việt và dữ liệu giữ nguyên khi thao tác bị từ chối. Thử ba lần chạy CLI liên tiếp để chứng minh lưu bền vững.
- **Nâng cao (tùy chọn):** thêm lọc khoảng ngày hoặc cập nhật bản ghi; dùng tệp tạm cùng thư mục rồi thay thế tệp đích để giảm nguy cơ tệp dở dang nếu ghi lỗi, ghi rõ giới hạn khi nhiều tiến trình cùng ghi.

**Tiêu chí đạt:** B23 đủ chức năng và dữ liệu còn sau khi khởi động lại; B24 toàn bộ test qua, README chạy theo được, dữ liệu lỗi không làm mất dữ liệu đã lưu. Lỗi cú pháp JSON không được hiểu thành nhật ký rỗng.

**Sản phẩm nộp:** mã nguồn P01/S1, README, dữ liệu giả tối thiểu mười buổi học, bộ test và bản tự đánh giá theo tiêu chí trong [DANH_GIA.md](../DANH_GIA.md). Đạt từ 75/100 và không có lỗi làm mất dữ liệu; chức năng bắt buộc phải đầy đủ, không lấy điểm nâng cao để bù chức năng thiếu.

**Tự kiểm tra:** 1. Tệp thiếu khác tệp hỏng thế nào? 2. Test nào phát hiện ghi dữ liệu trước khi xác thực? 3. Có thể giải thích luồng từ đối số CLI đến tệp lưu mà không đọc từng dòng mã không?

## Điều kiện sang chặng dữ liệu và AI

Bạn sẵn sàng khi tự viết được hàm xử lý list/dict, đọc/ghi CSV/JSON, đọc traceback, thêm một test cho lỗi mới và hoàn thành P01 đạt chuẩn. Nếu còn yếu phần nào, dành thêm một tuần làm lại bài vận dụng tương ứng với dữ liệu khác. Tốc độ hoàn thành là tham khảo; khả năng tự giải thích và sửa lỗi mới là điều kiện tiến lên.

Tài liệu tra cứu chính thức: [Python Tutorial](https://docs.python.org/3/tutorial/) và [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html). Dùng bộ chọn phiên bản 3.11 khi đối chiếu với môi trường dự án; không cần đọc hết tài liệu trước khi thực hành.
