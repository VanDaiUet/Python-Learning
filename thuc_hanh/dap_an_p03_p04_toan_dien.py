"""ĐÁP ÁN THAM KHẢO & GIẢI THÍCH CHI TIẾT: P03 & P04
Chủ đề: Biến, Kiểu dữ liệu, Vòng lặp, Chuỗi, List, Tuple, Set, Dictionary

File này chứa lời giải mẫu chuẩn xác cho bộ bài tập thực hành toàn diện.
Dùng để đối chiếu, kiểm tra sau khi bạn đã tự làm bài.
"""

import copy
import sys

# Cấu hình UTF-8 cho console trên Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ==============================================================================
# PHẦN 1: BIẾN, CÁC KIỂU DỮ LIỆU CƠ BẢN & CƠ CHẾ BỘ NHỚ
# ==============================================================================
raw_values = ["150", "0", "", "3.75", None, "Python", 0]

# Ép kiểu int và float:
val_int = int(raw_values[0])
val_float = float(raw_values[3])

# bool() kiểm tra chân trị:
# "150" -> True, "0" -> True (chuỗi không rỗng!), "" -> False (chuỗi rỗng)
# "3.75" -> True, None -> False, "Python" -> True, 0 -> False
bool_results = [bool(x) for x in raw_values]

# So sánh == (giá trị) và is (danh tính ô nhớ):
list_goc = [1, 2, 3]
list_tham_chieu = list_goc       # Trỏ chung ô nhớ với list_goc
list_sao_chep = [1, 2, 3]        # Đối tượng mới có cùng nội dung

so_sanh_gia_tri = (list_goc == list_sao_chep)       # True: nội dung bằng nhau
so_sanh_danh_tinh_1 = (list_goc is list_tham_chieu) # True: cùng 1 ô nhớ (id giống nhau)
so_sanh_danh_tinh_2 = (list_goc is list_sao_chep)   # False: 2 ô nhớ độc lập trong RAM


# ==============================================================================
# PHẦN 2: VÒNG LẶP, ĐIỀU KIỆN DỪNG VÀ BIẾN TÍCH LŨY (P03)
# ==============================================================================
giao_dich = [120, -50, 300, -20, 0, 450, -100, 80]

# Bài 2.1: Accumulator lặp qua list
tong_duong = 0
so_giao_dich_am = 0
for gd in giao_dich:
    if gd > 0:
        tong_duong += gd
    elif gd < 0:
        so_giao_dich_am += 1

# Bài 2.2: While loop tính số dư kép
so_du_hien_tai = 1000.0
muc_tieu = 2000.0
so_thang = 0
while so_du_hien_tai < muc_tieu:
    so_du_hien_tai *= 1.05
    so_thang += 1
so_du_cuoi = so_du_hien_tai

# Bài 2.3: For ... else tìm kiếm
ds_so = [4, 6, 8, 9, 10, 15]
so_tim_duoc = None
for s in ds_so:
    if s > 10 and s % 2 == 0:
        so_tim_duoc = s
        break
else:
    # Nhánh else chạy khi duyệt hết ds_so mà không gặp lệnh break
    so_tim_duoc = None

# Bài 2.4: Enumerate + Zip
hoc_vien = ["An", "Bình", "Cường", "Dung"]
diem_toan = [8.5, 7.0, 9.5, 6.0]
diem_tin = [9.0, 8.0, 10.0, 7.5]

bang_tong_ket = []
for stt, (ten, t, tin) in enumerate(zip(hoc_vien, diem_toan, diem_tin), start=1):
    dtb = (t + tin) / 2
    bang_tong_ket.append(f"Thứ hạng {stt}: {ten} - Trung bình: {dtb:.2f}")


# ==============================================================================
# PHẦN 3: KIỂU CHUỖI (STRINGS) & XỬ LÝ VĂN BẢN (P04 / P01)
# ==============================================================================
raw_name = "   nGuyễn   vĂn   aN   "
# .split() tự động gom các khoảng trắng liên tiếp; sau đó join lại bằng 1 dấu cách và .title()
ten_chuan_hoa = " ".join(raw_name.split()).title()

# Parse chuỗi log:
log_entry = "2026-09-22 | ERROR | Database connection timeout | code=504"
parts = [p.strip() for p in log_entry.split("|")]
log_date = parts[0]
log_level = parts[1]
log_msg = parts[2]
# code=504 -> tách chuỗi con sau dấu '='
error_code = int(parts[3].split("=")[1])

# Slicing Palindrome
cau_kiem_tra = "Radar"
cau_thuong = cau_kiem_tra.lower()
cau_dao_nguoc = cau_thuong[::-1]
la_doi_xung = (cau_thuong == cau_dao_nguoc)


# ==============================================================================
# PHẦN 4: KIỂU LIST (DANH SÁCH) & LIST COMPREHENSION (P04)
# ==============================================================================
danh_sach_diem = [7.5, 9.0, 6.0, 8.5, 4.0, 9.0, 10.0]
danh_sach_diem.append(8.0)
danh_sach_diem.remove(4.0)

# sorted tạo list mới, không làm biến đổi danh_sach_diem gốc
diem_giam_dan = sorted(danh_sach_diem, reverse=True)
diem_max = max(danh_sach_diem)
diem_min = min(danh_sach_diem)
diem_tb = sum(danh_sach_diem) / len(danh_sach_diem)

# List Comprehension
du_lieu_so = [-10, 15, 0, 22, -3, 8, 14, -7, 30]
so_duong_chan = [x for x in du_lieu_so if x > 0 and x % 2 == 0]
chuan_hoa_am = [x if x >= 0 else 0 for x in du_lieu_so]

# Deep copy và Flatten Matrix
ma_tran_goc = [
    [1, 2, 3],
    [4, 5, 6]
]
ma_tran_sao_chep = copy.deepcopy(ma_tran_goc)
ma_tran_sao_chep[0][0] = 99
ma_tran_phang = [phan_tu for hang in ma_tran_goc for phan_tu in hang]


# ==============================================================================
# PHẦN 5: KIỂU TUPLE (BỘ GIÁ TRỊ CỐ ĐỊNH) (P04)
# ==============================================================================
thong_tin_toa_do = ("Server_A", 10.762622, 106.660172, 8080)
ten_server = thong_tin_toa_do[0]
toa_do_lat_lon = (thong_tin_toa_do[1], thong_tin_toa_do[2])
cong_port = thong_tin_toa_do[3]
tuple_don = (999,)

lich_su_diem = (5.0, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0)
diem_dau, *diem_giua, diem_cuoi = lich_su_diem


# ==============================================================================
# PHẦN 6: KIỂU SET (TẬP HỢP) & CÁC PHÉP TOÁN TẬP HỢP (P04)
# ==============================================================================
tokens_thô = ["python", "ai", "machine_learning", "python", "data", "ai", "deep_learning"]
tokens_unique = sorted(list(set(tokens_thô)))

lop_python = {"An", "Bình", "Cường", "Dung", "Giang"}
lop_data   = {"Bình", "Dung", "Hải", "Khánh", "Lam"}

hoc_ca_hai = lop_python & lop_data
chi_hoc_python = lop_python - lop_data
tong_sinh_vien = lop_python | lop_data
hoc_dung_mot_lop = lop_python ^ lop_data


# ==============================================================================
# PHẦN 7: KIỂU DICTIONARY (TỪ ĐIỂN / BẢNG ÁNH XẠ) (P04)
# ==============================================================================
doan_van = "ai là trí tuệ nhân tạo ai giúp tự động hóa và ai thay đổi thế giới"
cac_tu = doan_van.split()
tan_suat_tu = {}
for tu in cac_tu:
    tan_suat_tu[tu] = tan_suat_tu.get(tu, 0) + 1

nhat_ky_hoc = [
    {"mon": "Python", "phut": 45},
    {"mon": "SQL", "phut": 30},
    {"mon": "Python", "phut": 60},
    {"mon": "Machine Learning", "phut": 90},
    {"mon": "SQL", "phut": 45},
    {"mon": "Python", "phut": 30},
]
tong_phut_theo_mon = {}
for phien in nhat_ky_hoc:
    mon = phien["mon"]
    phut = phien["phut"]
    tong_phut_theo_mon[mon] = tong_phut_theo_mon.get(mon, 0) + phut

bang_diem = {
    "An": 8.5,
    "Bình": 4.5,
    "Cường": 9.0,
    "Dung": 6.0,
    "Giang": 3.8
}
hoc_vien_dat = {ten: d for ten, d in bang_diem.items() if d >= 5.0}
xep_loai = {ten: ("Đạt" if d >= 5.0 else "Học lại") for ten, d in bang_diem.items()}


# ==============================================================================
# PHẦN 8: BÀI TẬP TỔNG HỢP (MINI-PROJECT P03 & P04)
# ==============================================================================
raw_logs = [
    "  user:AN  ; topic:python ; duration:45 ; status:COMPLETED ",
    "  user:BINH ; topic:data   ; duration:60 ; status:COMPLETED ",
    "  user:an   ; topic:sql    ; duration:30 ; status:COMPLETED ",
    "  user:CUONG; topic:python ; duration:15 ; status:FAILED    ",
    "  user:Binh ; topic:python ; duration:45 ; status:COMPLETED ",
    "  user:An   ; topic:DATA   ; duration:50 ; status:COMPLETED ",
    "  user:Dung ; topic:sql    ; duration:40 ; status:COMPLETED ",
]

danh_sach_sach = []
for line in raw_logs:
    cac_phan = [item.strip() for item in line.strip().split(";")]
    info = {}
    for part in cac_phan:
        k, v = part.split(":")
        k = k.strip()
        v = v.strip()
        info[k] = v

    user = info["user"].capitalize()
    topic = info["topic"].lower()
    duration = int(info["duration"])
    status = info["status"].lower()

    if status == "completed":
        danh_sach_sach.append({
            "user": user,
            "topic": topic,
            "duration": duration,
            "status": status
        })

cac_mon_hoc = {item["topic"] for item in danh_sach_sach}

tong_phut_nguoi_dung = {}
for item in danh_sach_sach:
    u = item["user"]
    tong_phut_nguoi_dung[u] = tong_phut_nguoi_dung.get(u, 0) + item["duration"]

nguoi_hoc_nhieu_nhat = max(tong_phut_nguoi_dung, key=tong_phut_nguoi_dung.get)


# ==============================================================================
# HỆ THỐNG TỰ ĐỘNG CHẤM ĐIỂM (SELF-TEST RUNNER)
# ==============================================================================
def chay_kiem_tra():
    print("=" * 70)
    print(" BẮT ĐẦU CHẤM ĐIỂM BỘ ĐÁP ÁN THAM KHẢO P03 - P04")
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
