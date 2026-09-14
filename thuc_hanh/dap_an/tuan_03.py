"""Tuần 3: Vòng lặp và biến tích lũy.

Đáp án tham khảo; chỉ xem sau khi tự làm. Giữ tên biến đầu vào và đầu ra
để bộ kiểm tra tìm được. Dùng biến để tính, không chép cứng kết quả.
Sau khi đạt, sao chép sang bai_lam rồi đổi dữ liệu để thử thêm.
"""

so_phut = [30, 0, 45, 60]
diem_so = [4, 8, 6, 3, 9]
n = 4

# Bài 1: Dùng for cộng các phần tử so_phut vào tong_phut. Chưa dùng sum().
tong_phut = 0
for phut in so_phut:
    tong_phut += phut

# Bài 2: Dùng for và if đếm số diem_so >= 5.
so_dat = 0
for diem in diem_so:
    if diem >= 5:
        so_dat += 1

# Bài 3: Tính 1**2 + 2**2 + ... + n**2 bằng range và vòng lặp.
tong_binh_phuong = 0
for i in range(1, n + 1):
    tong_binh_phuong += i ** 2
