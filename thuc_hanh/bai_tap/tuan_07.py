"""Bộ bài tập tuần 7: đọc đặc tả trong từng hàm trước khi viết mã."""

import csv
import json
from pathlib import Path

# Bài 1
def doc_json(path: str | Path):
    """Đọc file JSON UTF-8, trả về dữ liệu Python.
    Để FileNotFoundError / JSONDecodeError truyền ra nếu file thiếu / sai JSON."""
    raise NotImplementedError("Bạn hãy hoàn thành hàm này")

# Bài 2
def tong_phut_csv(path: str | Path) -> int:
    """Đọc CSV UTF-8 có cột ten,phut. Tổng các phut là số nguyên >= 0.
    File chỉ có header -> 0. Số âm hoặc chuỗi không đổi được sang int -> ValueError.
    Ví dụ ten,phut rồi An,30 và Binh,45 -> 75."""
    raise NotImplementedError("Bạn hãy hoàn thành hàm này")

# Bài 3
def ghi_json(path: str | Path, data) -> None:
    """Ghi data thành JSON UTF-8, giữ chữ có dấu. Thư mục cha đã tồn tại.
    Ghi đè file được chỉ định; trả về None. Dùng with để đóng file."""
    raise NotImplementedError("Bạn hãy hoàn thành hàm này")
