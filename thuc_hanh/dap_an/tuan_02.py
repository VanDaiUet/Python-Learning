"""Tuần 2: Điều kiện và phép toán.

Đáp án tham khảo; chỉ xem sau khi tự làm. Giữ tên biến đầu vào và đầu ra
để bộ kiểm tra tìm được. Dùng biến để tính, không chép cứng kết quả.
Sau khi đạt, sao chép sang bai_lam rồi đổi dữ liệu để thử thêm.
"""

diem = 7.5
phut = 125
du_kien = 10
da_hoc = 7

# Bài 1: Dùng if/else: diem >= 5 thì ket_luan là 'dat', ngược lại 'can_on'.
if diem >= 5:
    ket_luan = "dat"
else:
    ket_luan = "can_on"

# Bài 2: Đổi phut thành gio_nguyen và phut_le bằng // và %.
gio_nguyen = phut // 60
phut_le = phut % 60

# Bài 3: hoan_thanh là bool: True nếu da_hoc >= du_kien.
hoan_thanh = da_hoc >= du_kien
