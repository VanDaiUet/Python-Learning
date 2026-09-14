# Đánh giá chương trình 4 tuần

Áp dụng cho [lịch N01–N28](LO_TRINH_4_TUAN.md), 43 giờ/tuần với 30 giờ thực hành.


## Theo dõi hằng ngày

Dùng [TIEN_DO.csv](TIEN_DO.csv): ngày 1–6 mỗi tuần dự kiến 1,5 giờ kiến thức + 5 giờ thực hành + 0,5 giờ ôn; ngày 7 chỉ ôn 1 giờ. Các cột `*_thuc_te` ghi thời gian bạn thực sự học, không điền tự động bằng kế hoạch.

Trạng thái: `chua_bat_dau`, `dang_hoc`, `can_on`, `hoan_thanh`. Với phần mở rộng chưa làm, ghi rõ trong cột ghi chú; không dùng test của đáp án tham khảo làm bằng chứng hoàn thành bài của bạn.

Cuối ngày ghi ba dòng: tôi tự làm được gì; lỗi nào đã sửa và vì sao; điều nào tôi chưa tự giải thích được. Ngày ôn nhẹ kiểm tra lại một kiến thức cũ bằng lời và cập nhật bảng.

## Thang điểm cho S1–S4

| Tiêu chí | Điểm | Bằng chứng |
|---|---:|---|
| Đúng chức năng cốt lõi | 30 | Đầu vào/đầu ra đúng đặc tả của lịch tăng tốc |
| Hiểu và tự sửa mã | 25 | Giải thích được luồng và tự xử lý yêu cầu thay đổi |
| Kiểm thử hoặc đánh giá đáng tin | 20 | Có test biên; với ML có split và baseline; với retrieval có tập đánh giá |
| Tổ chức mã và khả năng chạy lại | 15 | Mã rõ, phụ thuộc được ghi, chạy lại theo hướng dẫn |
| Ghi chép và demo | 10 | README, kết quả thực, giới hạn và việc cần làm tiếp |

**Đạt từ 75/100 và đủ điều kiện bắt buộc.** Không lấy điểm trình bày bù cho mất dữ liệu, rò rỉ dữ liệu, mô hình chưa chạy hoặc API không hoạt động.

| Mốc | Kiểm tra độc lập trong khối thực hành | Điều kiện bắt buộc |
|---|---|---|
| S1 — N06 | 60 phút: thêm lọc chủ đề hoặc báo cáo tổng phút vào CLI | Tám bộ bài tập đạt trên bài làm; lưu JSON qua lần chạy; ít nhất 6 test; báo lỗi không phá file |
| S2 — N13 | Dùng batch mới lấy từ train để kiểm tra dự đoán trước/sau save/load; giải thích split | D1 đúng tổng; Wine có baseline/Pipeline; giữ test kín đến lúc chốt; báo metric và số mẫu |
| S3 — N18/N20 | Nạp checkpoint rồi dự đoán; giải thích một batch và truy về nguồn tìm kiếm | MLP đã huấn luyện thật, split rõ, có đường cong và đánh giá; tìm kiếm có ID nguồn |
| S4 — N27 | 90 phút: chạy API theo README, sửa một yêu cầu nhỏ rồi chạy test | API Wine hoạt động; 6 ca test; log và phiên bản; latency; báo cáo retrieval test; hướng dẫn tái lập |

ML không dùng một ngưỡng accuracy chung cho mọi bài. Nếu chưa hơn baseline, báo đúng kết quả và lý do; không dùng test để thử nhiều cấu hình rồi gọi điểm tốt nhất là đánh giá độc lập.

## Phần mở rộng ghi riêng

- CNN: chỉ đánh dấu đã làm khi có thí nghiệm thực và so sánh phù hợp; không bắt buộc để đạt MLP.
- RAG sinh: chỉ đánh dấu đã làm khi gọi mô hình thật và chấm đầu ra; fake chỉ kiểm thử giao diện. Nếu chưa chạy được, ghi `generation_chua_hoan_thanh`.
- Docker/CI: chỉ ghi đã chạy khi có bằng chứng container/job chạy thật. S4 cho phép nghiệm thu API bằng môi trường ảo sạch; P06 đầy đủ có yêu cầu cao hơn.
- Các chủ đề fine-tuning, distributed training và agent nhiều bước chưa nằm trong phần bắt buộc bốn tuần.

## Nếu học không kịp

Giữ lại Python, xử lý dữ liệu, đánh giá ML và API. Dùng phần mở rộng ở N18/N23 để sửa phần nền; thu hẹp số mô hình/thử nghiệm. Không bỏ test và đánh giá chỉ để kịp thêm tính năng.

Nếu vẫn chưa đạt một mốc vào ngày 28, ghi rõ sản phẩm nào đã đạt và phần nào cần học tiếp. Kết thúc bốn tuần là mốc tổng kết thời gian, không tự biến phần chưa hiểu thành đã thành thạo.

## Dùng AI để học

Tự thử 20–30 phút, thu nhỏ lỗi rồi hỏi một gợi ý. Sau khi được giúp, đóng lời giải và tự viết lại. Mẫu yêu cầu:

> Tôi đang học bài này, đây là đề và mã của tôi. Hãy chỉ ra một chỗ cần suy nghĩ và cho một gợi ý; chưa đưa toàn bộ lời giải.

> Hãy hỏi tôi ba câu về cách chia train/validation/test và nhận xét từng câu trả lời.

Điểm hiểu kiến thức chỉ được tính khi bạn giải thích và sửa được mã đã dùng. Có thể tra tài liệu cú pháp trong bài kiểm tra; không chép lời giải cho chính đề đang được kiểm tra.
