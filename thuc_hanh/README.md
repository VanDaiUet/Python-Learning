# Bài tập Python khởi động

Có 8 bộ bài tập, mỗi bộ gồm 3 nhiệm vụ. Trong [lịch 4 tuần](../LO_TRINH_4_TUAN.md), hoàn thành chúng trong ngày 1–4: mỗi ngày hai bộ. Tên file `tuan_XX.py` và cờ `--tuan` giữ nguyên từ giáo trình đầy đủ; số này là số bộ bài tập khi dùng lịch mới.

Trước khi điền mã, đọc phần giải thích tương ứng trong [tài liệu Python](../kien_thuc/01_python.md): bộ 1 → [P01](../kien_thuc/01_python.md#p01), bộ 2 → [P02](../kien_thuc/01_python.md#p02), bộ 3 → [P03](../kien_thuc/01_python.md#p03), bộ 4–5 → [P04](../kien_thuc/01_python.md#p04), bộ 6 → [P05](../kien_thuc/01_python.md#p05), bộ 7 → [P06](../kien_thuc/01_python.md#p06), bộ 8 → [P07–P08](../kien_thuc/01_python.md#p07). Mỗi mục có ví dụ và câu hỏi kèm gợi ý; làm biến thể trong thời gian thực hành của ngày.

| Bộ | Mã bài tập | Kỹ năng |
|---|---|---|
| 1 | [tuan_01.py](bai_tap/tuan_01.py) | Biến, lời chào, tính phút và giờ |
| 2 | [tuan_02.py](bai_tap/tuan_02.py) | Điều kiện, chia nguyên, so sánh |
| 3 | [tuan_03.py](bai_tap/tuan_03.py) | Cộng dồn, đếm, vòng lặp range |
| 4 | [tuan_04.py](bai_tap/tuan_04.py) | Làm sạch chuỗi, đảo list, slicing |
| 5 | [tuan_05.py](bai_tap/tuan_05.py) | Đếm tần suất, loại trùng, tổng hợp |
| 6 | [tuan_06.py](bai_tap/tuan_06.py) | Hàm, hợp đồng đầu vào, chia lô dữ liệu |
| 7 | [tuan_07.py](bai_tap/tuan_07.py) | Đọc CSV/JSON và ghi JSON UTF-8 |
| 8 | [tuan_08.py](bai_tap/tuan_08.py) | Xử lý lỗi, trường hợp rỗng và lỗi trạng thái dùng chung |

Chạy lệnh từ thư mục gốc `F:\Python Learning`:

```powershell
.\.venv\Scripts\python.exe thuc_hanh\kiem_tra.py --tuan 1
.\.venv\Scripts\python.exe thuc_hanh\kiem_tra.py --tat-ca
```

Bộ 1–5: sửa các biến kết quả đang là `None`; chưa cần viết hàm. Bộ kiểm tra chạy trên dữ liệu gốc, vì vậy giữ dữ liệu đó trong file được chấm. Để thử dữ liệu khác, sao chép sang `bai_lam/4_tuan/`. Không viết cứng kết quả; hãy giải thích công thức hoặc thuật toán cho người khác.

Bộ 6–8: điền thân hàm tại chỗ `NotImplementedError`. Câu lệnh `raise ValueError("...")` chủ động báo đầu vào vi phạm đặc tả; ngày 4 học cách bắt và trình bày lỗi. Đọc docstring để biết rõ cách xử lý rỗng, số âm và đường dẫn. Bộ kiểm tra thử nhiều đầu vào, dùng thư mục tạm cho bài file.

Dữ liệu minh họa nằm ở [hoc_tap.csv](du_lieu/hoc_tap.csv) và [hoc_tap.json](du_lieu/hoc_tap.json); tổng số phút là 135. Để thử đọc file sau khi hoàn thành bộ 7:

```powershell
.\.venv\Scripts\python.exe -c "from thuc_hanh.bai_tap.tuan_07 import tong_phut_csv; print(tong_phut_csv('thuc_hanh/du_lieu/hoc_tap.csv'))"
```

Đáp án tham khảo ở `dap_an/`. Xem sau khi đã tự thử, ghi lại khó khăn và đọc gợi ý trong giáo trình:

```powershell
.\.venv\Scripts\python.exe thuc_hanh\kiem_tra.py --tat-ca --dap-an
```

**Lệnh có `--dap-an` kiểm tra bản tham khảo, không đo kết quả học của bạn.** Các bài chưa hoàn thành sẽ báo FAIL/ERROR khi chạy bộ bài tập. Không sửa công cụ kiểm tra để làm bài sai trở thành đúng.

Từ ngày 4, hãy đọc [kiem_tra.py](kiem_tra.py), hiểu một test rồi bổ sung trường hợp biên có ý nghĩa. Các bộ bài tập 1–5 dùng dữ liệu cố định nên cần tự đổi dữ liệu ở bản sao để tránh chỉ học thuộc đầu ra.
