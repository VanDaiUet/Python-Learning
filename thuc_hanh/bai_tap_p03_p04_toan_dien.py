"""BỘ BÀI TẬP THỰC HÀNH TOÀN DIỆN: P03 & P04
Chủ đề: Biến, Kiểu dữ liệu, Vòng lặp, Chuỗi, List, Tuple, Set, Dictionary

HƯỚNG DẪN:
1. Đọc kỹ phần lý thuyết và cú pháp (comment) ở từng phần.
2. Hoàn thiện các bài tập thực hành bằng cách thay thế chỗ `None` hoặc viết mã tại vùng `# TODO`.
3. Kiểm tra bài làm trực tiếp bằng lệnh:
       .\.venv\Scripts\python.exe thuc_hanh/bai_tap_p03_p04_toan_dien.py
   Bộ test tự động ở cuối file sẽ chấm điểm và báo kết quả từng bài.
"""

import socket
import copy
import sys

# Cấu hình UTF-8 cho console trên Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ==============================================================================
# PHẦN 1: BIẾN, CÁC KIỂU DỮ LIỆU CƠ BẢN & CƠ CHẾ BỘ NHỚ (P01 / P04)
# ==============================================================================
# [LÝ THUYẾT & CÚ PHÁP CẦN NẮM]:
# 1. Cơ chế biến trong Python:
#    - Biến không phải là "ngăn tủ" chứa giá trị, mà là một "nhãn dán" (tham chiếu/reference)
#      trỏ đến một đối tượng (object) được tạo ra trong bộ nhớ.
#    - Toán tử `=` là phép gán liên kết nhãn với đối tượng.
# 2. Các kiểu dữ liệu cơ sở:
#    - int: số nguyên (-5, 0, 42, ...)
#    - float: số thực dấu phẩy động (3.14, -0.01, 1e-3)
#    - bool: giá trị logic (chỉ gồm True hoặc False)
#    - str: chuỗi ký tự bất biến ("hello", 'Python')
#    - NoneType: giá trị `None` đại diện cho sự vắng mặt của dữ liệu / không có giá trị
# 3. Phân biệt Mutable (Có thể sửa) và Immutable (Bất biến):
#    - Immutable: int, float, bool, str, tuple, frozenset. Khi "thay đổi", Python thực chất
#      tạo đối tượng mới và gán lại nhãn!
#    - Mutable: list, dict, set. Có thể thay đổi trực tiếp nội dung bên trong vùng nhớ.
# 4. Ép kiểu (Type Casting):
#    - int("123") -> 123; float("3.14") -> 3.14; str(100) -> "100"
#    - bool(x):
#      + Falsy (tính sai): 0, 0.0, "", [], {}, set(), (), None, False.
#      + Truthy (tính đúng): tất cả các giá trị còn lại (khác 0, chuỗi không rỗng, tập không rỗng).
# 5. So sánh:
#    - `==`: So sánh GIÁ TRỊ (nội dung có bằng nhau không).
#    - `is`: So sánh DANH TÍNH VÙNG NHỚ (`id(a) == id(b)` - có cùng trỏ vào 1 ô nhớ không).
# 6. Cú pháp gán nhiều biến & hoán vị:
#    - `x, y = 10, 20` (gán song song)
#    - `x, y = y, x`   (hoán vị giá trị không cần biến tạm)
# ------------------------------------------------------------------------------

# --- BÀI TẬP PHẦN 1 ---
# Bài 1.1: Ép kiểu và kiểm tra chân trị (Truthy / Falsy)
# Cho danh sách các giá trị thô:
raw_values = ["150", "0", "", "3.75", None, "Python", 0]
# Yêu cầu:
# - Chuyển "150" thành số nguyên -> `val_int`
# - Chuyển "3.75" thành số thực -> `val_float`
# - Tạo danh sách `bool_results` chứa giá trị bool() tương ứng của từng phần tử trong `raw_values`
# TODO:
val_int = int("150")
val_float = float("3.75")
bool_results = [bool(r) for r in raw_values]

# Bài 1.2: So sánh giá trị (==) và danh tính ô nhớ (is)
list_goc = [1, 2, 3]
list_tham_chieu = list_goc       # Trỏ cùng ô nhớ
list_sao_chep = [1, 2, 3]        # Đối tượng mới có cùng giá trị
# Yêu cầu:
# - So sánh giá trị của list_goc và list_sao_chep -> `so_sanh_gia_tri` (bool)
# - So sánh danh tính của list_goc và list_tham_chieu bằng toán tử `is` -> `so_sanh_danh_tinh_1` (bool)
# - So sánh danh tính của list_goc và list_sao_chep bằng toán tử `is` -> `so_sanh_danh_tinh_2` (bool)
# TODO:
so_sanh_gia_tri = list_goc == list_sao_chep
so_sanh_danh_tinh_1 = list_tham_chieu is list_goc
so_sanh_danh_tinh_2 = list_goc is list_sao_chep


# ==============================================================================
# PHẦN 2: VÒNG LẶP, ĐIỀU KIỆN DỪNG VÀ BIẾN TÍCH LŨY (P03)
# ==============================================================================
# [LÝ THUYẾT & CÚ PHÁP CẦN NẮM]:
# 1. Vòng lặp `for`:
#    - Dùng khi biết trước tập dữ liệu hoặc cần duyệt tuần tự từng phần tử của iterable.
#    - Cú pháp `range()`:
#      + range(stop): 0 đến stop - 1
#      + range(start, stop): start đến stop - 1
#      + range(start, stop, step): nhảy theo bước `step` (có thể âm để lùi: range(10, 0, -1))
# 2. Vòng lặp `while`:
#    - Lặp khi điều kiện còn `True`. Phải luôn đảm bảo biến điều kiện được cập nhật để tránh lặp vô hạn.
# 3. Câu lệnh điều khiển luồng:
#    - `break`: Thoát ngay lập tức khỏi vòng lặp trong cùng gần nhất.
#    - `continue`: Bỏ qua phần còn lại của vòng lặp hiện tại, chuyển sang lần lặp kế tiếp.
#    - `pass`: Lệnh giữ chỗ (no-op), không làm gì cả.
# 4. Mệnh đề `else` trong vòng lặp:
#    - Cú pháp `for ... else:` hoặc `while ... else:`
#    - Khối `else` CHỈ CHẠY khi vòng lặp hoàn thành bình thường (không bị ngắt bởi `break`).
# 5. Các hàm trợ thủ vòng lặp cực phổ biến:
#    - `enumerate(iterable, start=0)`: Trả về cặp `(chỉ_số, giá_trị)`. Tránh dùng `range(len(...))`.
#    - `zip(it1, it2, ...)`: Ghép từng cặp phần tử tương ứng của nhiều danh sách lại với nhau.
#    - `reversed(seq)`: Trả về iterator duyệt ngược.
# 6. Biến tích lũy (Accumulator Pattern):
#    - Khởi tạo biến TRƯỚC vòng lặp (với tổng khởi tạo 0, với tích khởi tạo 1, với list/dict khởi tạo [] / {}).
#    - Sau mỗi lần lặp, cộng dồn / cập nhật giá trị vào biến tích lũy.
# ------------------------------------------------------------------------------

# --- BÀI TẬP PHẦN 2 ---
# Bài 2.1: Biến tích lũy có điều kiện
# Cho danh sách các số nguyên đại diện cho giao dịch/điểm số:
giao_dich = [120, -50, 300, -20, 0, 450, -100, 80]
# Yêu cầu: Dùng vòng lặp for (KHÔNG dùng hàm sum() sẵn):
# - Tính tổng các số DƯƠNG (> 0) -> gán vào `tong_duong`
# - Đếm số lượng các giao dịch ÂM (< 0) -> gán vào `so_giao_dich_am`
# TODO:
tong_duong = 0
so_giao_dich_am = 0
for i in giao_dich:
    if i > 0:
        tong_duong += i
    elif i < 0:
        so_giao_dich_am +=1

# Bài 2.2: Vòng lặp `while` và điều kiện dừng
# Một tài khoản có số dư ban đầu 1000 USD. Mỗi tháng số dư tăng thêm 5% (nhân 1.05).
# Yêu cầu: Dùng vòng lặp while để tính:
# Sau bao nhiêu tháng (`so_thang`) thì số dư tài khoản vượt quá hoặc bằng 2000 USD?
# Lưu giá trị số dư cuối cùng vào `so_du_cuoi`.
so_du_hien_tai = 1000.0
muc_tieu = 2000.0
# TODO:
so_thang = 0
so_du_cuoi = 0
while so_du_hien_tai < muc_tieu:
    so_thang +=1
    so_du_cuoi = so_du_hien_tai * 1.05
    so_du_hien_tai = so_du_cuoi


# Bài 2.3: Tìm kiếm với `for ... else`
# Cho danh sách các số:
ds_so = [4, 6, 8, 9, 10, 15]
# Yêu cầu: Duyệt qua `ds_so` để tìm số chẵn đầu tiên lớn hơn 10.
# Nếu tìm thấy, gán số đó vào `so_tim_duoc` và dùng `break` để thoát.
# Dùng khối `else` của vòng lặp: nếu không tìm thấy số nào thỏa mãn, gán `so_tim_duoc = None`.
# TODO:
so_tim_duoc = None
for i in ds_so:
    if i % 2 == 0 and i > 10:
        so_tim_duoc = i
        break


# Bài 2.4: Phối hợp `enumerate` và `zip`
hoc_vien = ["An", "Bình", "Cường", "Dung"]
diem_toan = [8.5, 7.0, 9.5, 6.0]
diem_tin = [9.0, 8.0, 10.0, 7.5]
# Yêu cầu:
# Duyệt song song tên học viên và hai cột điểm bằng zip() và enumerate(..., start=1).
# Tạo danh sách `bang_tong_ket` chứa các chuỗi có định dạng:
# "Thứ hạng {stt}: {ten} - Trung bình: {dtb:.2f}"
# Trong đó dtb là trung bình cộng của điểm toán và tin.
# TODO:
bang_tong_ket = []
for stt, (ten, toan, tin) in enumerate(zip(hoc_vien, diem_toan, diem_tin), start = 1):
    bang_tong_ket.append(f"Thứ hạng {stt}: {ten} - Trung bình: {(toan + tin)/2:.2f}")


# ==============================================================================
# PHẦN 3: KIỂU CHUỖI (STRINGS) & XỬ LÝ VĂN BẢN (P01 / P04)
# ==============================================================================
# [LÝ THUYẾT & CÚ PHÁP CẦN NẮM]:
# 1. Tính chất của chuỗi:
#    - Chuỗi là dãy ký tự Unicode bất biến (immutable). Không thể gán `s[0] = 'a'`.
# 2. Cắt lát (Slicing): `s[start:stop:step]`
#    - `s[0]`: Ký tự đầu tiên; `s[-1]`: Ký tự cuối cùng.
#    - `s[:3]`: 3 ký tự đầu tiên (chỉ số 0, 1, 2).
#    - `s[2:]`: Từ chỉ số 2 đến hết.
#    - `s[::-1]`: Đảo ngược chuỗi.
# 3. Phương thức chuỗi phổ biến:
#    - Biến đổi hoa/thường: `.lower()`, `.upper()`, `.title()`, `.capitalize()`
#    - Cắt tỉa khoảng trắng: `.strip()` (2 đầu), `.lstrip()` (trái), `.rstrip()` (phải)
#    - Tách / Ghép chuỗi:
#      + `.split()`: Tách theo mọi khoảng trắng liên tiếp (rất sạch cho xử lý text!).
#      + `.split(sep)`: Tách theo ký tự phân cách cụ thể.
#      + `"dấu_nối".join(danh_sách_chuỗi)`: Ghép các chuỗi lại với nhau.
#    - Tìm kiếm / Thay thế:
#      + `.replace(old, new)`: Thay thế chuỗi con.
#      + `.find(sub)`: Trả về vị trí đầu tiên xuất hiện của sub, hoặc -1 nếu không có.
#      + `.startswith(prefix)` / `.endswith(suffix)`: Kiểm tra chuỗi bắt đầu/kết thúc.
#      + `.count(sub)`: Đếm số lần xuất hiện của sub.
#    - Kiểm tra loại ký tự: `.isdigit()`, `.isalpha()`, `.isalnum()`, `.isspace()`
# 4. Định dạng chuỗi (f-string):
#    - Căn lề và làm tròn: `f"{val:.2f}"` (2 số thập phân), `f"{ten:>10}"` (căn phải 10 ký tự),
#      `f"{ma_so:04d}"` (thêm số 0 ở đầu thành 4 chữ số).
# ------------------------------------------------------------------------------

# --- BÀI TẬP PHẦN 3 ---
# Bài 3.1: Chuẩn hóa dữ liệu văn bản thô
raw_name = "   nGuyễn   vĂn   aN   "
# Yêu cầu:
# 1. Bỏ khoảng trắng thừa ở hai đầu và giữa các từ (giữa các từ chỉ còn đúng 1 dấu cách).
# 2. Viết hoa chữ cái đầu của mỗi từ (Title Case).
# Kết quả mong muốn: "Nguyễn Văn An" -> gán vào `ten_chuan_hoa`
# TODO:
ten_chuan_hoa = " ".join(raw_name.title().split())
# Bài 3.2: Tách thông tin từ chuỗi nhật ký (Log parsing)
log_entry = "2026-09-22 | ERROR | Database connection timeout | code=504"
# Yêu cầu:
# Dùng các phương thức chuỗi (như split) để trích xuất:
# - `log_date`: "2026-09-22"
# - `log_level`: "ERROR"
# - `log_msg`: "Database connection timeout"
# - `error_code`: 504 (dưới dạng int, không phải str)
# TODO:
parts =log_entry.split(" | ")
log_date = parts[0]
log_level = parts[1]
log_msg = parts[2]
error_code = int(parts[3][5:])

# Bài 3.3: Slicing và kiểm tra chuỗi đối xứng (Palindrome)
# Một chuỗi là đối xứng nếu đọc xuôi đọc ngược đều như nhau.
cau_kiem_tra = "Radar"
# Yêu cầu:
# - Chuyển chuỗi về chữ thường -> `cau_thuong`
# - Đảo ngược chuỗi bằng slicing [::-1] -> `cau_dao_nguoc`
# - Kiểm tra `la_doi_xung`: True nếu cau_thuong == cau_dao_nguoc, ngược lại False.
# TODO:
cau_thuong = cau_kiem_tra.lower()
cau_dao_nguoc = cau_thuong[::-1]
la_doi_xung = cau_thuong == cau_dao_nguoc


# ==============================================================================
# PHẦN 4: KIỂU LIST (DANH SÁCH) & LIST COMPREHENSION (P04)
# ==============================================================================
# [LÝ THUYẾT & CÚ PHÁP CẦN NẮM]:
# 1. Đặc điểm:
#    - Dãy có thứ tự, có thể thay đổi (mutable), cho phép các phần tử trùng lặp.
# 2. Thao tác CRUD trên List:
#    - Thêm: `.append(x)` (thêm vào cuối), `.insert(i, x)` (chèn vào vị trí i),
#            `.extend(iterable)` (nối danh sách khác vào cuối).
#    - Xóa: `.remove(val)` (xóa phần tử đầu tiên bằng val), `.pop(i)` (lấy ra và xóa tại index i,
#           mặc định xóa cuối nếu không truyền i), `del lst[i]`, `.clear()` (xóa hết).
#    - Tra cứu: `.index(val)` (tìm vị trí), `.count(val)` (đếm số lần xuất hiện), `x in lst`.
# 3. Sắp xếp:
#    - `lst.sort()`: Sắp xếp TẠI CHỖ (in-place), thay đổi lst gốc, trả về `None`.
#    - `sorted(lst)`: KHÔNG đổi lst gốc, trả về một danh sách MỚI đã được sắp xếp.
#    - Tham số: `reverse=True` (giảm dần), `key=lambda x: ...` (tiêu chí sắp xếp).
# 4. List Comprehension:
#    - Cú pháp biến đổi / lọc: `[biểu_thức for x in iterable if điều_kiện]`
#    - Cú pháp kèm if-else: `[a if điều_kiện else b for x in iterable]`
# 5. Cơ chế bộ nhớ (Cực kỳ quan trọng trong AI / Lập trình):
#    - `b = a`: Chỉ sao chép tham chiếu! Thay đổi b làm a đổi theo.
#    - `b = a.copy()` hoặc `a[:]`: Sao chép nông (Shallow copy). Lớp ngoài được tách ra,
#      nhưng nếu có danh sách con bên trong thì danh sách con vẫn bị dùng chung!
#    - `b = copy.deepcopy(a)`: Sao chép sâu. Độc lập hoàn toàn cả các tầng lồng nhau.
# ------------------------------------------------------------------------------

# --- BÀI TẬP PHẦN 4 ---
# Bài 4.1: Các thao tác cơ bản và sắp xếp an toàn
danh_sach_diem = [7.5, 9.0, 6.0, 8.5, 4.0, 9.0, 10.0]
# Yêu cầu:
# 1. Thêm điểm 8.0 vào cuối danh sách.
# 2. Xóa điểm 4.0 khỏi danh sách.
# 3. Tạo `diem_giam_dan` là danh sách mới sắp xếp từ cao xuống thấp (GIỮ NGUYÊN `danh_sach_diem`).
# 4. Lấy điểm cao nhất (`diem_max`), điểm thấp nhất (`diem_min`) và điểm trung bình (`diem_tb`).
# TODO:
# (Thực hiện thêm/xóa trên danh_sach_diem tại đây)
diem_giam_dan = None
diem_max = None
diem_min = None
diem_tb = None

# Bài 4.2: List Comprehension nâng cao
du_lieu_so = [-10, 15, 0, 22, -3, 8, 14, -7, 30]
# Yêu cầu bằng List Comprehension:
# 1. `so_duong_chan`: Lọc các số vừa DƯƠNG vừa CHẴN từ `du_lieu_so`.
# 2. `chuan_hoa_am`: Tạo danh sách mới trong đó số âm được thay bằng 0, số không âm giữ nguyên.
# TODO:
so_duong_chan = None
chuan_hoa_am = None

# Bài 4.3: Ma trận và Deep Copy
ma_tran_goc = [
    [1, 2, 3],
    [4, 5, 6]
]
# Yêu cầu:
# 1. Dùng `copy.deepcopy` để tạo `ma_tran_sao_chep`.
# 2. Thay đổi phần tử hàng 0, cột 0 của `ma_tran_sao_chep` thành 99.
# 3. Đảm bảo phần tử hàng 0, cột 0 của `ma_tran_goc` VẪN LÀ 1.
# 4. Dùng nested list comprehension để làm phẳng `ma_tran_goc` thành 1 danh sách 1D -> `ma_tran_phang` ([1, 2, 3, 4, 5, 6]).
# TODO:
ma_tran_sao_chep = None
ma_tran_phang = None


# ==============================================================================
# PHẦN 5: KIỂU TUPLE (BỘ GIÁ TRỊ CỐ ĐỊNH) (P04)
# ==============================================================================
# [LÝ THUYẾT & CÚ PHÁP CẦN NẮM]:
# 1. Đặc điểm:
#    - Dãy có thứ tự, BẤT BIẾN (immutable). Không thể sửa, thêm, xóa phần tử sau khi tạo.
#    - Dùng khi muốn bảo vệ dữ liệu không bị vô tình sửa đổi (như tọa độ GPS, cấu hình server,
#      các giá trị trả về từ hàm).
#    - Nhẹ hơn list, tốc độ truy cập nhanh hơn và có thể dùng làm key trong Dictionary (nếu chứa các phần tử hashable).
# 2. Cú pháp:
#    - `t = (1, 2, 3)` hoặc `t = 1, 2, 3`
#    - Chú ý: Tuple 1 phần tử bắt buộc phải có dấu phẩy: `t_one = (42,)` (nếu viết `(42)` sẽ là số nguyên int!).
# 3. Phương thức:
#    - Chỉ có 2 phương thức: `.count(val)` và `.index(val)`
# 4. Tuple Unpacking (Mở gói bộ dữ liệu):
#    - Cơ bản: `a, b, c = (1, 2, 3)`
#    - Mở rộng với toán tử `*` (Extended Unpacking):
#      `first, *middle, last = (10, 20, 30, 40, 50)` -> first=10, middle=[20, 30, 40], last=50
#    - Bỏ qua giá trị không quan tâm: `ten, _, tuoi = ("An", "Hà Nội", 20)`
# ------------------------------------------------------------------------------

# --- BÀI TẬP PHẦN 5 ---
# Bài 5.1: Khởi tạo và Unpacking
thong_tin_toa_do = ("Server_A", 10.762622, 106.660172, 8080)
# Yêu cầu:
# 1. Dùng unpacking để gán:
#    - `ten_server`: phần tử đầu tiên ("Server_A")
#    - `toa_do_lat_lon`: tuple chứa 2 tọa độ (10.762622, 106.660172)
#    - `cong_port`: phần tử cuối cùng (8080)
# 2. Tạo một tuple 1 phần tử `tuple_don` chứa duy nhất số 999.
# TODO:
ten_server = None
toa_do_lat_lon = None
cong_port = None
tuple_don = None

# Bài 5.2: Extended Unpacking với chuỗi thời gian
lich_su_diem = (5.0, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0)
# Yêu cầu:
# Dùng cú pháp unpacking với `*` để tách:
# - `diem_dau`: điểm số đầu tiên (float)
# - `diem_giua`: danh sách (list) chứa các điểm ở giữa
# - `diem_cuoi`: điểm số cuối cùng (float)
# TODO:
diem_dau = None
diem_giua = None
diem_cuoi = None


# ==============================================================================
# PHẦN 6: KIỂU SET (TẬP HỢP) & CÁC PHÉP TOÁN TẬP HỢP (P04)
# ==============================================================================
# [LÝ THUYẾT & CÚ PHÁP CẦN NẮM]:
# 1. Đặc điểm:
#    - Tập hợp các phần tử DUY NHẤT (không trùng lặp), KHÔNG CÓ THỨ TỰ (unordered).
#    - Không thể truy cập qua chỉ số `s[0]`.
#    - Các phần tử phải hashable (bất biến: str, int, float, tuple; không thể chứa list, dict, set).
#    - Tốc độ kiểm tra thành viên `x in s` cực kỳ nhanh: O(1) (so với O(n) của list).
# 2. Khởi tạo:
#    - `s = {1, 2, 3}`
#    - `s_empty = set()` (LƯU Ý: `{}` tạo ra dictionary rỗng, KHÔNG PHẢI set rỗng!).
# 3. Phương thức thêm/xóa:
#    - `.add(x)`: Thêm một phần tử.
#    - `.update(iterable)`: Thêm nhiều phần tử từ một collection khác.
#    - `.remove(x)`: Xóa phần tử x. Báo lỗi `KeyError` nếu x không tồn tại!
#    - `.discard(x)`: Xóa an toàn. Nếu x không có trong set thì KHÔNG báo lỗi.
#    - `.pop()`: Lấy và xóa một phần tử bất kỳ.
#    - `.clear()`: Xóa toàn bộ set.
# 4. Các phép toán tập hợp đại số (Set Operations):
#    - Hợp (Union): `A | B` hoặc `A.union(B)` (lấy tất cả phần tử thuộc A hoặc B).
#    - Giao (Intersection): `A & B` hoặc `A.intersection(B)` (chỉ lấy phần tử vừa thuộc A vừa thuộc B).
#    - Hiệu (Difference): `A - B` hoặc `A.difference(B)` (thuộc A nhưng KHÔNG thuộc B).
#    - Hiệu đối xứng (Symmetric Diff): `A ^ B` (thuộc A hoặc B nhưng không thuộc cả hai).
#    - Quan hệ: `A <= B` (A là tập con của B), `A.isdisjoint(B)` (A và B không có phần tử chung).
# ------------------------------------------------------------------------------

# --- BÀI TẬP PHẦN 6 ---
# Bài 6.1: Khử trùng lặp và chuyển đổi
tokens_thô = ["python", "ai", "machine_learning", "python", "data", "ai", "deep_learning"]
# Yêu cầu:
# 1. Tạo `tokens_unique` là một list chứa các từ khóa không trùng lặp,
#    được sắp xếp theo thứ tự bảng chữ cái A-Z.
# TODO:
tokens_unique = None

# Bài 6.2: Phân tích người học giữa 2 lớp
lop_python = {"An", "Bình", "Cường", "Dung", "Giang"}
lop_data   = {"Bình", "Dung", "Hải", "Khánh", "Lam"}
# Yêu cầu: Dùng các phép toán tập hợp (&, |, -, ^):
# 1. `hoc_ca_hai`: Tập hợp những người học CẢ HAI lớp.
# 2. `chi_hoc_python`: Tập hợp những người CHỈ HỌC lớp Python (không học Data).
# 3. `tong_sinh_vien`: Tập hợp TẤT CẢ sinh viên tham gia ít nhất 1 trong 2 lớp.
# 4. `hoc_dung_mot_lop`: Tập hợp những người CHỈ HỌC ĐÚNG MỘT LỚP (thuộc Python hoặc Data nhưng không phải cả 2).
# TODO:
hoc_ca_hai = None
chi_hoc_python = None
tong_sinh_vien = None
hoc_dung_mot_lop = None


# ==============================================================================
# PHẦN 7: KIỂU DICTIONARY (TỪ ĐIỂN / BẢNG ÁNH XẠ) (P04)
# ==============================================================================
# [LÝ THUYẾT & CÚ PHÁP CẦN NẮM]:
# 1. Đặc điểm:
#    - Lưu trữ theo cặp `khóa: giá_trị` (key: value).
#    - Key phải là duy nhất và phải hashable (chuỗi, số, tuple). Value có thể là bất kỳ kiểu gì.
#    - Từ Python 3.7+, dictionary bảo toàn thứ tự chèn (insertion order).
#    - Truy xuất và tìm kiếm theo key với độ phức tạp trung bình O(1).
# 2. Truy xuất giá trị:
#    - `d[key]`: Ném lỗi `KeyError` nếu key không có trong dict.
#    - `d.get(key, default)`: An toàn. Nếu không có key thì trả về `default` (mặc định là `None`),
#      không gây crash chương trình.
# 3. Thêm / Sửa / Xóa:
#    - `d[key] = new_value`: Thêm mới nếu chưa có, ghi đè giá trị nếu key đã có.
#    - `d.update({k1: v1, k2: v2})`: Cập nhật nhiều cặp key-value cùng lúc.
#    - `d.pop(key, default)`: Lấy ra và xóa cặp key-value khỏi dict.
#    - `del d[key]`: Xóa key khỏi dict.
#    - Gộp dict (Python 3.9+): `d3 = d1 | d2` (nếu trùng key, giá trị của d2 sẽ đè d1).
# 4. Duyệt qua Dictionary:
#    - `for k in d:` hoặc `for k in d.keys():` -> Duyệt các khóa.
#    - `for v in d.values():` -> Duyệt các giá trị.
#    - `for k, v in d.items():` -> Duyệt đồng thời cả khóa và giá trị (dùng nhiều nhất!).
# 5. Mẫu đếm tần suất (Frequency Counter Pattern):
#    ```python
#    counts = {}
#    for x in items:
#        counts[x] = counts.get(x, 0) + 1
#    ```
# 6. Dict Comprehension:
#    - `{k: v for x in iterable if điều_kiện}`
#    - Đảo ngược key và value: `{v: k for k, v in d.items()}` (chỉ an toàn khi các value là duy nhất và hashable).
# ------------------------------------------------------------------------------

# --- BÀI TẬP PHẦN 7 ---
# Bài 7.1: Đếm tần suất từ (Word Frequency Counter)
doan_van = "ai là trí tuệ nhân tạo ai giúp tự động hóa và ai thay đổi thế giới"
# Yêu cầu:
# 1. Tách đoạn văn thành danh sách các từ (bằng split()).
# 2. Dùng vòng lặp và phương thức `dict.get()` để tạo dictionary `tan_suat_tu`
#    lưu số lần xuất hiện của mỗi từ. Ví dụ: `{"ai": 3, ...}`
# TODO:
tan_suat_tu = None

# Bài 7.2: Nhóm và tính tổng theo nhóm (Grouping & Aggregation)
# Cho danh sách các phiên học:
nhat_ky_hoc = [
    {"mon": "Python", "phut": 45},
    {"mon": "SQL", "phut": 30},
    {"mon": "Python", "phut": 60},
    {"mon": "Machine Learning", "phut": 90},
    {"mon": "SQL", "phut": 45},
    {"mon": "Python", "phut": 30},
]
# Yêu cầu:
# Dùng vòng lặp duyệt qua `nhat_ky_hoc` để tính tổng số phút cho từng môn.
# Lưu kết quả vào dictionary `tong_phut_theo_mon`:
# Ví dụ: {"Python": 135, "SQL": 75, "Machine Learning": 90}
# TODO:
tong_phut_theo_mon = None

# Bài 7.3: Dict Comprehension & Lọc dữ liệu
bang_diem = {
    "An": 8.5,
    "Bình": 4.5,
    "Cường": 9.0,
    "Dung": 6.0,
    "Giang": 3.8
}
# Yêu cầu:
# 1. Dùng Dict Comprehension để tạo `hoc_vien_dat`: chỉ lấy những học viên có điểm >= 5.0.
# 2. Dùng Dict Comprehension để tạo `xep_loai`: ánh xạ tên -> "Đạt" nếu điểm >= 5.0, ngược lại "Học lại".
# TODO:
hoc_vien_dat = None
xep_loai = None


# ==============================================================================
# PHẦN 8: BÀI TẬP TỔNG HỢP (MINI-PROJECT P03 & P04)
# ==============================================================================
# Bối cảnh: Bạn nhận được dữ liệu nhật ký học tập thô dạng chuỗi từ hệ thống (log strings).
# Dữ liệu bị thừa khoảng trắng, chữ hoa thường lộn xộn, và cần được làm sạch,
# thống kê tổng hợp để báo cáo.

raw_logs = [
    "  user:AN  ; topic:python ; duration:45 ; status:COMPLETED ",
    "  user:BINH ; topic:data   ; duration:60 ; status:COMPLETED ",
    "  user:an   ; topic:sql    ; duration:30 ; status:COMPLETED ",
    "  user:CUONG; topic:python ; duration:15 ; status:FAILED    ",
    "  user:Binh ; topic:python ; duration:45 ; status:COMPLETED ",
    "  user:An   ; topic:DATA   ; duration:50 ; status:COMPLETED ",
    "  user:Dung ; topic:sql    ; duration:40 ; status:COMPLETED ",
]

# Yêu cầu:
# Bước 1: Làm sạch và chuẩn hóa:
# - Duyệt qua từng dòng trong `raw_logs`.
# - Dùng các phương thức chuỗi (strip, lower, split, replace) để bóc tách:
#   + user (str): tên chuẩn hóa (chữ cái đầu viết hoa, ví dụ: "An", "Binh", "Cuong", "Dung")
#   + topic (str): tên môn viết thường ("python", "data", "sql")
#   + duration (int): số phút học (chuyển sang kiểu int)
#   + status (str): trạng thái viết thường ("completed", "failed")
# - CHỈ LẤY những bản ghi có status == "completed" (bỏ qua bản ghi "failed").
# - Lưu danh sách các dict bản ghi hợp lệ này vào `danh_sach_sach`.

# Bước 2: Thống kê từ `danh_sach_sach`:
# - `cac_mon_hoc`: kiểu `set` chứa tất cả các môn học duy nhất xuất hiện trong danh sách hợp lệ.
# - `tong_phut_nguoi_dung`: kiểu `dict` ánh xạ tên user -> tổng số phút học completed của người đó.
# - `nguoi_hoc_nhieu_nhat`: chuỗi tên user có tổng số phút học cao nhất.

# TODO:
danh_sach_sach = None
cac_mon_hoc = None
tong_phut_nguoi_dung = None
nguoi_hoc_nhieu_nhat = None


# ==============================================================================
# HỆ THỐNG TỰ ĐỘNG CHẤM ĐIỂM (SELF-TEST RUNNER)
# ==============================================================================
def chay_kiem_tra():
    print("=" * 70)
    print(" BẮT ĐẦU CHẤM ĐIỂM BỘ BÀI TẬP THỰC HÀNH P03 - P04")
    print("=" * 70)
    
    so_bai_dat = 0
    tong_so_bai = 20
    
    def danh_gia(ten_bai, dieu_kien, thong_bao_loi=""):
        nonlocal so_bai_dat
        if dieu_kien:
            print(f" [OK]   {ten_bai}")
            so_bai_dat += 1
        else:
            print(f" [FAIL] {ten_bai} -> {thong_bao_loi}")

    # P1
    danh_gia("Bài 1.1: Ép kiểu và chân trị",
             val_int == 150 and val_float == 3.75 and bool_results == [True, True, False, True, False, True, False],
             f"Kết quả nhận được: val_int={val_int}, val_float={val_float}, bool_results={bool_results}")
    
    danh_gia("Bài 1.2: So sánh == và is",
             so_sanh_gia_tri is True and so_sanh_danh_tinh_1 is True and so_sanh_danh_tinh_2 is False,
             f"Kết quả: ==: {so_sanh_gia_tri}, is_1: {so_sanh_danh_tinh_1}, is_2: {so_sanh_danh_tinh_2}")

    # P2
    danh_gia("Bài 2.1: Tích lũy có điều kiện",
             tong_duong == 950 and so_giao_dich_am == 3,
             f"Kết quả: tong_duong={tong_duong} (kỳ vọng 950), so_am={so_giao_dich_am} (kỳ vọng 3)")
    
    danh_gia("Bài 2.2: While loop số dư",
             so_thang == 15 and round(so_du_cuoi, 2) == 2078.93,
             f"Kết quả: so_thang={so_thang} (kỳ vọng 15), so_du_cuoi={so_du_cuoi}")

    danh_gia("Bài 2.3: For-else tìm kiếm",
             so_tim_duoc is None,
             f"Kết quả: so_tim_duoc={so_tim_duoc} (kỳ vọng None vì trong ds không có số chẵn nào > 10)")

    danh_gia("Bài 2.4: Enumerate và Zip",
             bang_tong_ket == [
                 "Thứ hạng 1: An - Trung bình: 8.75",
                 "Thứ hạng 2: Bình - Trung bình: 7.50",
                 "Thứ hạng 3: Cường - Trung bình: 9.75",
                 "Thứ hạng 4: Dung - Trung bình: 6.75"
             ],
             f"Kết quả: {bang_tong_ket}")

    # P3
    danh_gia("Bài 3.1: Chuẩn hóa tên",
             ten_chuan_hoa == "Nguyễn Văn An",
             f"Kết quả: '{ten_chuan_hoa}' (kỳ vọng 'Nguyễn Văn An')")

    danh_gia("Bài 3.2: Parse log",
             (log_date, log_level, log_msg, error_code) == ("2026-09-22", "ERROR", "Database connection timeout", 504),
             f"Kết quả: {(log_date, log_level, log_msg, error_code)}")

    danh_gia("Bài 3.3: Slicing Palindrome",
             cau_thuong == "radar" and cau_dao_nguoc == "radar" and la_doi_xung is True,
             f"Kết quả: cau_dao_nguoc={cau_dao_nguoc}, la_doi_xung={la_doi_xung}")

    # P4
    danh_gia("Bài 4.1: Thao tác List & Sort",
             danh_sach_diem == [7.5, 9.0, 6.0, 8.5, 9.0, 10.0, 8.0] and
             diem_giam_dan == [10.0, 9.0, 9.0, 8.5, 8.0, 7.5, 6.0] and
             diem_max == 10.0 and diem_min == 6.0 and round(diem_tb, 2) == 8.29,
             f"danh_sach_diem={danh_sach_diem}, diem_giam_dan={diem_giam_dan}, max={diem_max}, min={diem_min}, tb={diem_tb}")

    danh_gia("Bài 4.2: List Comprehension",
             so_duong_chan == [22, 8, 14, 30] and chuan_hoa_am == [0, 15, 0, 22, 0, 8, 14, 0, 30],
             f"so_duong_chan={so_duong_chan}, chuan_hoa_am={chuan_hoa_am}")

    danh_gia("Bài 4.3: Deepcopy & Flatten Matrix",
             ma_tran_goc == [[1, 2, 3], [4, 5, 6]] and
             ma_tran_sao_chep == [[99, 2, 3], [4, 5, 6]] and
             ma_tran_phang == [1, 2, 3, 4, 5, 6],
             f"goc={ma_tran_goc}, sao_chep={ma_tran_sao_chep}, phang={ma_tran_phang}")

    # P5
    danh_gia("Bài 5.1: Tuple Unpacking",
             ten_server == "Server_A" and toa_do_lat_lon == (10.762622, 106.660172) and cong_port == 8080 and tuple_don == (999,),
             f"ten={ten_server}, toa_do={toa_do_lat_lon}, port={cong_port}, don={tuple_don}")

    danh_gia("Bài 5.2: Extended Unpacking",
             diem_dau == 5.0 and diem_giua == [6.5, 7.0, 8.0, 8.5, 9.0] and diem_cuoi == 10.0,
             f"dau={diem_dau}, giua={diem_giua}, cuoi={diem_cuoi}")

    # P6
    danh_gia("Bài 6.1: Set loại trùng & Sort",
             tokens_unique == ["ai", "data", "deep_learning", "machine_learning", "python"],
             f"Kết quả: {tokens_unique}")

    danh_gia("Bài 6.2: Phép toán Set",
             hoc_ca_hai == {"Bình", "Dung"} and
             chi_hoc_python == {"An", "Cường", "Giang"} and
             tong_sinh_vien == {"An", "Bình", "Cường", "Dung", "Giang", "Hải", "Khánh", "Lam"} and
             hoc_dung_mot_lop == {"An", "Cường", "Giang", "Hải", "Khánh", "Lam"},
             f"ca_hai={hoc_ca_hai}, chi_py={chi_hoc_python}, tong={tong_sinh_vien}, mot_lop={hoc_dung_mot_lop}")

    # P7
    danh_gia("Bài 7.1: Đếm tần suất từ",
             tan_suat_tu == {'ai': 3, 'là': 1, 'trí': 1, 'tuệ': 1, 'nhân': 1, 'tạo': 1, 'giúp': 1, 'tự': 1, 'động': 1, 'hóa': 1, 'và': 1, 'thay': 1, 'đổi': 1, 'thế': 1, 'giới': 1},
             f"Kết quả: {tan_suat_tu}")

    danh_gia("Bài 7.2: Nhóm & Cộng dồn Dict",
             tong_phut_theo_mon == {"Python": 135, "SQL": 75, "Machine Learning": 90},
             f"Kết quả: {tong_phut_theo_mon}")

    danh_gia("Bài 7.3: Dict Comprehension",
             hoc_vien_dat == {"An": 8.5, "Cường": 9.0, "Dung": 6.0} and
             xep_loai == {"An": "Đạt", "Bình": "Học lại", "Cường": "Đạt", "Dung": "Đạt", "Giang": "Học lại"},
             f"dat={hoc_vien_dat}, loai={xep_loai}")

    # P8
    danh_gia("Bài 8: Tổng hợp Mini-project P03 & P04",
             len(danh_sach_sach or []) == 6 and
             cac_mon_hoc == {"python", "data", "sql"} and
             tong_phut_nguoi_dung == {"An": 125, "Binh": 105, "Dung": 40} and
             nguoi_hoc_nhieu_nhat == "An",
             f"so_luong={len(danh_sach_sach or [])}, cac_mon={cac_mon_hoc}, tong_user={tong_phut_nguoi_dung}, top={nguoi_hoc_nhieu_nhat}")

    print("=" * 70)
    print(f" KẾT QUẢ TỔNG KẾT: {so_bai_dat}/{tong_so_bai} bài đạt yêu cầu.")
    if so_bai_dat == tong_so_bai:
        print(" CHÚC MỪNG! BẠN ĐÃ LÀM CHỦ TOÀN BỘ KIẾN THỨC P03 & P04!")
    else:
        print(" HÃY KIỂM TRA LẠI CÁC BÀI [FAIL] Ở TRÊN VÀ THỬ LẠI NHÉ!")
    print("=" * 70)


if __name__ == "__main__":
    chay_kiem_tra()
