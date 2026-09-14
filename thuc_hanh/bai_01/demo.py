"""Bài mẫu đầu tiên: biến, phép tính và hiển thị kết quả."""

# Hai dòng hỗ trợ hiển thị tiếng Việt; bắt đầu học từ biến ten bên dưới.
import sys
sys.stdout.reconfigure(encoding="utf-8")

ten = "An"
so_buoi = 5
phut_moi_buoi = 45
tong_phut = so_buoi * phut_moi_buoi
tong_gio = tong_phut / 60

print(f"Xin chào, {ten}!")
print(f"Bạn học {so_buoi} buổi, mỗi buổi {phut_moi_buoi} phút.")
print(f"Tổng thời gian: {tong_phut} phút = {tong_gio:.2f} giờ.")
