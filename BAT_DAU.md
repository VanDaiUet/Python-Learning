# Bắt đầu học hôm nay

Áp dụng [lộ trình tăng tốc 4 tuần](LO_TRINH_4_TUAN.md): 43 giờ/tuần, trong đó 30 giờ thực hành. Tài liệu này hướng dẫn thao tác; lịch từng ngày và phạm vi bắt buộc nằm trong lộ trình.

Nếu mới bắt đầu, đọc [P01 — Chương trình, biến và kiểu dữ liệu](kien_thuc/01_python.md#p01) trước ví dụ đầu tiên; đọc [P02 — Biểu thức và điều kiện](kien_thuc/01_python.md#p02) trước bộ bài thứ hai. Các phần có ví dụ từng bước, kết quả dự kiến và câu hỏi kèm gợi ý. Tra phần còn vướng tại [mục lục kiến thức](kien_thuc/README.md); thời gian đọc nằm trong 1,5 giờ kiến thức mỗi ngày.

## 1. Mở đúng thư mục và Python

Thư mục làm việc: `F:\Python Learning`. Máy hiện có Python 3.11 và 3.14; bộ học sử dụng môi trường riêng `.venv` được tạo bằng Python 3.11 có sẵn. Các bài khởi động chỉ dùng thư viện chuẩn.

Mở PowerShell tại thư mục này và chạy lần lượt:

```powershell
Set-Location -LiteralPath 'F:\Python Learning'
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe thuc_hanh\bai_01\demo.py
```

Kết quả bài mẫu:

```text
Xin chào, An!
Bạn học 5 buổi, mỗi buổi 45 phút.
Tổng thời gian: 225 phút = 3.75 giờ.
```

Nếu chuyển bộ học sang máy khác hoặc chưa có `.venv`, xem các Python đã cài rồi tạo lại:

```powershell
py --list-paths
py -3.11 -m venv .venv
```

Lệnh tạo môi trường chỉ cần chạy khi chưa có môi trường. Có thể dùng bản Python khác đáp ứng yêu cầu các thư viện của giai đoạn đang học. Mỗi lần chạy `pip`, dùng đúng Python của môi trường đó. Hướng dẫn chính thức: [venv](https://docs.python.org/3/library/venv.html).

Gọi thẳng `.venv\Scripts\python.exe` như trên nên không cần thay đổi chính sách PowerShell để kích hoạt môi trường.

## 2. Hiểu chương trình đầu tiên

Mở [demo.py](thuc_hanh/bai_01/demo.py) bằng trình soạn thảo bất kỳ. Nếu dùng VS Code, chọn Python interpreter ở `.venv\Scripts\python.exe`.

- `ten = "An"`: gắn tên biến `ten` với một giá trị chuỗi.
- `so_buoi = 5`: lưu một số nguyên.
- `tong_phut = so_buoi * phut_moi_buoi`: tính biểu thức rồi lưu kết quả.
- `print(...)`: hiển thị ra màn hình.
- `f"...{ten}..."`: chèn giá trị vào chuỗi.
- Chương trình thực hiện các dòng từ trên xuống; dấu `=` là phép gán.

Sửa tên thành tên bạn, đổi số buổi thành 4 và thời gian thành 30. **Trước khi chạy**, dự đoán tổng phút và tổng giờ. Kết quả cần là 120 phút và 2.00 giờ. Sau đó đổi lại hoặc giữ bản cá nhân của bạn.

Để nhận dữ liệu từ bàn phím, thử tạo `bai_lam/loi_chao.py`:

```python
ten = input("Tên bạn: ")
so_buoi = int(input("Số buổi học: "))
print(f"{ten} có kế hoạch học {so_buoi} buổi.")
```

`input()` trả về chuỗi, nên cần `int()` khi muốn tính bằng số nguyên. Nếu nhập chữ vào ô số, Python báo `ValueError`; ngày 4 sẽ học cách xử lý lỗi có chủ đích.

## 3. Làm bài đầu tiên và tự kiểm tra

Mở [tuan_01.py](thuc_hanh/bai_tap/tuan_01.py), thay ba chỗ `None` theo đề trong file. Chưa cần hiểu hàm hoặc framework kiểm thử.

```powershell
.\.venv\Scripts\python.exe thuc_hanh\kiem_tra.py --tuan 1
```

- `OK`: các trường hợp được kiểm tra đã đạt; vẫn phải giải thích được cách làm.
- `FAIL`: kết quả khác mong đợi; đọc dòng tên bài và expected/actual.
- `ERROR`: mã chưa hoàn thành hoặc phát sinh lỗi khi chạy.

Bài chưa làm có thể báo lỗi; đó là trạng thái bình thường. Kiểm thử không chứng minh đúng với mọi đầu vào. Đến ngày 4, bạn sẽ tự bổ sung các trường hợp kiểm tra. Cờ `--tuan` chọn bộ bài tập theo tên cũ; không phải số tuần của lịch mới.

Sau khi đã thử và ghi lại chỗ vướng, có thể đọc `thuc_hanh/dap_an/tuan_01.py` hoặc kiểm tra bản tham khảo:

```powershell
.\.venv\Scripts\python.exe thuc_hanh\kiem_tra.py --tuan 1 --dap-an
```

Cờ `--dap-an` kiểm tra đáp án tham khảo, **không chấm bài bạn làm**. Không sao chép đáp án rồi đánh dấu hoàn thành.

## 4. Lịch tuần đầu

| Ngày | Việc cần hoàn thành |
|---|---|
| 1 — 7 giờ | B01–B04; chạy demo; biến và điều kiện; làm bộ bài tập 1–2 |
| 2 — 7 giờ | B05–B08; vòng lặp, chuỗi, list; làm bộ 3–4 |
| 3 — 7 giờ | B09–B12; dictionary và hàm; làm bộ 5–6 |
| 4 — 7 giờ | B13–B16; CSV/JSON, lỗi, unittest; làm bộ 7–8 và kiểm tra cả tám bộ |
| 5 — 7 giờ | B17–B20 chọn lọc; module, Git, OOP cơ bản; tổ chức mã S1 |
| 6 — 7 giờ | Hoàn thiện S1 nhật ký CLI lưu JSON; ít nhất 6 test và kiểm tra độc lập |
| 7 — 1 giờ | Ôn nhẹ, chấm S1 và cập nhật tiến độ; phần còn lại nghỉ |

Mỗi ngày chính gồm 1,5 giờ kiến thức + 5 giờ thực hành + 0,5 giờ ôn. Sau ngày 7, sang N08 trong [lộ trình 4 tuần](LO_TRINH_4_TUAN.md). Mã Bxx và tên các bộ bài tập giữ nguyên; các “tuần” trong giáo trình đầy đủ chỉ dùng làm địa chỉ tham khảo.

## 5. Cài thư viện khi đến giai đoạn cần dùng

Tuần 1 của lịch tăng tốc không bắt buộc cài thêm gói. Đầu ngày 8, tạo môi trường riêng cho ML; không cần chạy các lệnh sau ngay trong ngày 1:

```powershell
py -3.11 -m venv .venv-ml
.\.venv-ml\Scripts\python.exe -m pip install numpy pandas matplotlib scikit-learn jupyterlab
.\.venv-ml\Scripts\python.exe -m pip check
.\.venv-ml\Scripts\python.exe -m jupyterlab
```

Sau khi môi trường hoạt động, ghi lại phiên bản để phục dựng thí nghiệm:

```powershell
.\.venv-ml\Scripts\python.exe -m pip freeze > requirements-ml.txt
```

Đầu ngày 15, chọn lệnh cài PyTorch phù hợp hệ điều hành tại [PyTorch Get Started](https://pytorch.org/get-started/locally/); lịch tăng tốc dùng CPU và dữ liệu nhỏ. Lệnh và bản Python được hỗ trợ có thể thay đổi; kiểm tra yêu cầu ngay lúc cài.

Ngày 22, chuẩn bị môi trường dự án API rồi cài FastAPI và trình chạy theo [hướng dẫn FastAPI](https://fastapi.tiangolo.com/tutorial/), sẵn sàng cho ngày 24. Bộ học hiện chỉ chuẩn bị và kiểm tra môi trường thư viện chuẩn, chưa cài hay xác nhận các môi trường ML, GPU hoặc API. Thời gian cài đặt nằm trong khối thực hành, không cộng thêm ngoài lịch.
