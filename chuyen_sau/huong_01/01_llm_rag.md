# Tuần chuyên sâu 1–3 — LLM và RAG có đánh giá

Học phần này tiếp nối nền tảng Python/AI 4 tuần; đây là ba tuần đầu của hướng chuyên sâu 6 tuần. Bạn phát triển trợ lý tra cứu tài liệu **NovaLearn**, một tổ chức hoàn toàn giả lập. Đầu ra là phần mềm chạy được, tập kết quả thật và phân tích lỗi; không chỉ là prompt hoặc notebook đã chạy sẵn.

**Mỗi tuần: 43 giờ = 9 giờ kiến thức + 30 giờ thực hành + 4 giờ ôn.** Mỗi lab L01–L18 chiếm một ngày: 1,5 giờ kiến thức, 5 giờ thực hành và 0,5 giờ ôn. Ngày thứ bảy chỉ ôn 1 giờ. Ba tuần có 129 giờ, trong đó 90 giờ thực hành. Mọi bước cài môi trường, tải mô hình, debug và ghi bằng chứng đều nằm trong quỹ này.

## Đầu vào và quy ước chung

- **D:** [documents.json](thuc_hanh/du_lieu/documents.json), gồm 24 tài liệu; mỗi tài liệu có `doc_id`, `title`, `text`, `source`, `updated_at`. Giữ bản gốc để đối chiếu nguồn.
- **V:** [eval_dev.jsonl](thuc_hanh/du_lieu/eval_dev.jsonl), gồm 24 câu phát triển: 16 `answerable`, 4 `out_of_scope`, 4 `adversarial`. Trong 16 câu có đáp án, 4 câu cần nhiều tài liệu.
- **T:** [eval_test.jsonl](thuc_hanh/du_lieu/eval_test.jsonl), có cùng cơ cấu 24 câu nhưng câu hỏi khác; giữ kín đến mốc R6 cuối tuần chuyên sâu 6. Tổng V và T là 48 câu; L01–L18 chỉ dùng V để phát triển và đánh giá.
- Mỗi câu có `id`, `category`, `question`, `relevant_doc_ids`, `expected_answer`. Câu đa nguồn là câu `answerable` có hơn một `relevant_doc_ids`. Không đưa `expected_answer`, nhãn hoặc ID nguồn chuẩn vào prompt đang được đánh giá.
- Khi yêu cầu lấy “n câu đầu”, sắp xếp tăng dần theo `id` rồi lọc nhóm được chỉ định. Với D, sắp xếp theo `doc_id`. Cách lấy này giúp tái lập đầu vào.
- **A:** 16 câu `answerable` của V; **M:** 4 câu đa nguồn của A; **U:** 4 câu `out_of_scope` của V; **X:** 4 câu `adversarial` của V. Các ký hiệu này luôn chỉ tập phát triển.
- Mỗi lab lưu mã, cấu hình, đầu vào thực tế, kết quả và nhật ký tại `bai_lam/huong_01/novalearn/` tính từ gốc kho học. Tên artifact do bạn chọn; ghi lệnh chạy lại và phiên bản dữ liệu.
- Các hàm khởi đầu dùng ở phần LLM/RAG này gồm `normalize_text`, `chunk_words`, `lexical_search`, `recall_at_k`, `reciprocal_rank_fusion`, `validate_answer`; bộ khởi động còn ba bài về công cụ và điều phối cho phần agent. Các bộ ghép provider và pipeline trong lab là phần bạn tự xây. Đọc hợp đồng hàm trong mã trước khi gọi.

Trong 1,5 giờ kiến thức mỗi ngày, dùng khoảng 45 phút đọc khái niệm/tài liệu được dẫn, 30 phút phân tích ví dụ và 15 phút dự đoán kết quả. Trong 0,5 giờ ôn, đóng tài liệu để giải thích một quyết định và ghi một lỗi cùng cách phát hiện. Phần **đổi bài** tùy chọn thay thế thời gian trong khối 5 giờ, không cộng giờ và không bỏ tiêu chí bắt buộc.

Không bắt buộc API trả phí. Có thể dùng mô hình cục bộ hoặc quyền truy cập sẵn có; chọn theo RAM, thời gian và model card, ghi đúng tên/phiên bản. Không đưa dữ liệu cá nhân hay khóa truy cập vào bài nộp. Nếu chưa có tài nguyên, vẫn làm phần dùng thư viện chuẩn và ghi phần mô hình `chua_hoan_thanh`; fake provider không chứng minh chất lượng LLM. **Muốn đạt đầy đủ R3 phải chạy mô hình sinh thật.**

## Tuần 1 — Hợp đồng LLM, prompt và độ tin cậy

### L01 — Biến yêu cầu thành hợp đồng đầu vào/đầu ra

**Đọc để hiểu bài:** [R01 — LLM và tokenization](../../kien_thuc/03_llm_rag.md#r01); [R03 — Provider, HTTP và schema](../../kien_thuc/03_llm_rag.md#r03).

**Mục tiêu và kiến thức:** mô tả được ứng dụng trả lời gì, nhận dữ liệu nào và báo thiếu bằng chứng ra sao. Hợp đồng là điều phần mềm có thể kiểm tra; một đoạn văn nghe hợp lý chưa đủ để chứng minh thực hiện đúng yêu cầu.
**Đầu vào:** D, 3 câu đầu của A và câu đầu của U; chỉ dùng tài liệu liên quan trong D để tự xác định câu trả lời mẫu.

1. **1 giờ:** viết 4 tình huống sử dụng; xác định phạm vi tra cứu NovaLearn và hành vi khi không đủ thông tin.
2. **2 giờ:** thiết kế request gồm câu hỏi và ngữ cảnh có ID; output tối thiểu gồm `answer` dạng chuỗi, `citations` là danh sách `doc_id`, `abstain` dạng bool. Soạn 4 output bằng tay và ghi đây là fixture, chưa phải kết quả mô hình.
3. **2 giờ:** xây luồng đọc request → gọi provider thay thế được → xử lý output; fake trả fixture theo tình huống, thử câu hỏi rỗng và ngữ cảnh rỗng.

**Nghiệm thu:** có bản hợp đồng một trang, 4 fixture đúng kiểu và 2 ca lỗi đầu vào; luồng chạy lại không cần mạng. Bản ghi chỉ rõ fixture nào dùng để kiểm thử.
**Đổi bài:** thay 30 phút chỉnh giao diện bằng thêm giới hạn độ dài câu hỏi và thử đúng biên.

### L02 — Prompt rõ nhiệm vụ và ranh giới dữ liệu

**Đọc để hiểu bài:** [R02 — Prompt và ranh giới dữ liệu](../../kien_thuc/03_llm_rag.md#r02).

**Mục tiêu và kiến thức:** viết prompt tách yêu cầu ứng dụng, câu hỏi và tài liệu. Ví dụ mẫu giúp diễn đạt định dạng; nội dung nằm trong tài liệu vẫn là dữ liệu, không tự trở thành chỉ dẫn có quyền điều khiển ứng dụng.
**Đầu vào:** D, 4 câu đầu của A và câu đầu của X; dùng output mẫu L01 để minh họa định dạng, không chép đáp án chuẩn vào request đánh giá.

1. **1,5 giờ:** viết hai phiên bản prompt: chỉ dẫn ngắn và chỉ dẫn kèm một ví dụ định dạng bằng nội dung tự tạo ngoài bộ đánh giá.
2. **2 giờ:** dựng 5 request, phân cách từng tài liệu và ID; thêm quy tắc chỉ trả lời dựa trên ngữ cảnh, dẫn nguồn và báo thiếu thông tin.
3. **1,5 giờ:** chạy qua fake để kiểm tra dữ liệu được ghép đúng; nếu có mô hình thật, chạy hai prompt trên cùng 5 câu và phân loại lỗi, nếu chưa có thì tự rà soát request và ghi chưa đo chất lượng.

**Nghiệm thu:** 10 request lưu được; không chứa `expected_answer`; chỉ rõ chỗ tách chỉ dẫn và dữ liệu, ít nhất 3 rủi ro còn lại. Chỉ so chất lượng khi có output thật.
**Đổi bài:** thay 30 phút sửa văn phong bằng thử tài liệu chứa dấu phân cách giống prompt và bảo đảm cấu trúc không bị phá.

### L03 — Provider thay thế được và lần chạy mô hình đầu tiên

**Đọc để hiểu bài:** [R03 — Provider, HTTP và schema](../../kien_thuc/03_llm_rag.md#r03); [H04 — API và vòng đời model](../../kien_thuc/04_deep_learning_he_thong_agent.md#h04).

**Mục tiêu và kiến thức:** giữ logic ứng dụng độc lập với nơi chạy mô hình. Provider chuyển request và kết quả giữa hai giao diện; nó không bảo đảm nội dung đúng, kể cả khi lời gọi thành công.
**Đầu vào:** 3 request đầu của L02; fake với ba hành vi: trả hợp lệ, timeout, trả văn bản không phải JSON; D làm ngữ cảnh.

1. **1,5 giờ:** triển khai provider fake có kết quả xác định; thống nhất thông tin lỗi, thời gian và tên provider để pipeline gọi bằng một giao diện.
2. **2 giờ:** kiểm tra môi trường hiện có, đọc hướng dẫn chính thức/model card của mô hình bạn chọn; xây adapter thật và thử một request ngắn. Giới hạn bước này trong 2 giờ, ghi trở ngại cụ thể nếu chưa chạy được.
3. **1,5 giờ:** chạy cùng ba request qua provider có sẵn; lưu output nguyên bản, kết quả parse, thời gian, tên mô hình và cờ phân biệt `fake`/`real`.

**Nghiệm thu:** cả ba hành vi fake được xử lý có chủ đích; adapter không buộc đổi logic prompt. Có bản ghi chạy thật hoặc trạng thái chưa chạy cùng điều kiện còn thiếu, không điền kết quả giả.
**Đổi bài:** nếu adapter thật chạy sớm, dùng thời gian còn lại thử thêm hai lần cùng request để quan sát biến thiên.

### L04 — JSON đúng kiểu và câu trả lời có căn cứ

**Đọc để hiểu bài:** [R03 — Provider, HTTP và schema](../../kien_thuc/03_llm_rag.md#r03); [R11 — RAG và kiểm bằng chứng](../../kien_thuc/03_llm_rag.md#r11).

**Mục tiêu và kiến thức:** phân biệt JSON parse được, đúng schema và đúng nội dung. Kiểm tra kiểu/ID bắt được lỗi cấu trúc; xác định nguồn có thực sự hỗ trợ phát biểu cần đối chiếu nội dung.
**Đầu vào:** 4 fixture L01; D; 6 biến thể lỗi: thiếu trường, sai kiểu `abstain`, `citations` không phải list, ID không tồn tại, nguồn không được gửi trong context, từ chối nhưng vẫn đưa đáp án khẳng định.

1. **2 giờ:** hoàn thiện `validate_answer` theo hợp đồng starter; ghép kiểm tra JSON parse và giới hạn trường/kiểu tại biên pipeline theo phần còn thiếu.
2. **1,5 giờ:** kiểm tra ID nguồn thuộc tập context đã gửi, phát hiện nguồn lạ và xử lý trạng thái từ chối nhất quán; không tự sửa ID thành một nguồn có vẻ đúng.
3. **1,5 giờ:** chạy đủ 10 ca; chọn một fixture có ID hợp lệ nhưng nội dung không được nguồn hỗ trợ và viết lý do validator cấu trúc chưa phát hiện được.

**Nghiệm thu:** 4 fixture hợp lệ qua kiểm tra, 6 ca lỗi bị từ chối hoặc được chuyển thành lỗi có tên; có ví dụ phân biệt “nguồn tồn tại” với “nguồn hỗ trợ câu trả lời”.
**Đổi bài:** thay 30 phút viết thêm thông báo lỗi bằng một ca `abstain` là chuỗi `"false"`, giải thích vì sao không ép bool tùy tiện.

### L05 — Ngân sách token và ngữ cảnh

**Đọc để hiểu bài:** [R04 — Ngân sách context/token](../../kien_thuc/03_llm_rag.md#r04).

**Mục tiêu và kiến thức:** tính chỗ cho chỉ dẫn, câu hỏi, tài liệu và câu trả lời. Token phụ thuộc tokenizer của mô hình; số từ không phải số token. Dùng đúng tokenizer và mẫu chat của mô hình khi đo đầu vào thực. [Tài liệu tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer).
**Đầu vào:** D, câu đầu của A, câu đầu của M và prompt L02; hai ngân sách giả định 512 và 1.024 token, mỗi mức dành 128 token cho output.

1. **1,5 giờ:** tách các phần prompt; đếm bằng tokenizer của mô hình đã chọn nếu có. Khi chưa có tokenizer, dùng số từ để luyện phép phân bổ nhưng gắn nhãn ước lượng, không gọi đó là token đo thực.
2. **2 giờ:** xếp đoạn theo ưu tiên, thêm từng đoạn đến khi đầy ngân sách; giữ ID và một đơn vị bằng chứng đọc được, xử lý cả trường hợp chỉ dẫn/câu hỏi đã quá dài.
3. **1,5 giờ:** kiểm tra hai câu × hai ngân sách; ghi tài liệu giữ/bỏ, phần output dành trước và hành vi khi không còn chỗ. Kiểm tra giới hạn thật của model trước lời gọi thật.

**Nghiệm thu:** có bảng 4 trường hợp, phép cộng từng thành phần và ca vượt giới hạn; không âm thầm cắt mất ID nguồn hoặc gửi prompt vượt ngân sách đã kiểm tra.
**Đổi bài:** thay 30 phút trình bày bảng bằng so số từ/số token của cùng câu tiếng Việt khi tokenizer đã có.

### L06 — Timeout, retry hữu hạn và bàn giao R1

**Đọc để hiểu bài:** [H08 — Timeout, retry và idempotency](../../kien_thuc/04_deep_learning_he_thong_agent.md#h08); [R03 — Provider, HTTP và schema](../../kien_thuc/03_llm_rag.md#r03).

**Mục tiêu và kiến thức:** giữ chương trình dừng được khi phụ thuộc lỗi. Retry chỉ phù hợp với lỗi tạm thời và phải có trần; lặp lại vô hạn hoặc thử lại lỗi cấu hình chỉ làm tăng thời gian và số lượt gọi.
**Đầu vào:** provider L03, validator L04, bộ phân bổ L05; 6 kịch bản: thành công, timeout rồi thành công, timeout liên tục, lỗi cấu hình, JSON sai, output quá dài.

1. **2 giờ:** đặt timeout, tối đa 2 lần thử cho lỗi tạm thời và ngân sách tổng; fake ghi số lượt gọi, dùng đồng hồ giả trong test để khỏi chờ thực.
2. **1,5 giờ:** chạy 6 kịch bản; log mã request, provider/model, thời gian và lỗi; loại khóa truy cập khỏi log, không lấy exception làm câu trả lời cho người dùng.
3. **1,5 giờ:** tích hợp và chạy lại luồng R1; viết cách chạy, giới hạn, bằng chứng thật/giả. Dùng thời gian còn lại xử lý trở ngại model của L03 nếu cần.

**Nghiệm thu R1:** 6 kịch bản cho kết quả dự kiến, số lượt không vượt 2, không retry lỗi cấu hình, schema và ngân sách có kiểm tra. Phần provider thật có bằng chứng hoặc trạng thái chờ riêng; R1 phần mềm không thay cho nghiệm thu generation.
**Đổi bài:** thay 30 phút dọn mã bằng đo việc kết thúc khi ngân sách tổng đã hết trước lượt retry.

**Ngày thứ bảy — 1 giờ ôn:** 20 phút vẽ lại luồng, 20 phút chạy một ca lỗi không xem hướng dẫn, 20 phút cập nhật tiến độ R1. Không giao thêm lab.

## Tuần 2 — Ingestion, truy hồi và reranking

### L07 — Ingestion giữ được nguồn gốc

**Đọc để hiểu bài:** [R05 — Ingestion và nguồn gốc](../../kien_thuc/03_llm_rag.md#r05).

**Mục tiêu và kiến thức:** chuyển tài liệu thành dữ liệu có thể tìm kiếm mà vẫn truy về bản gốc. Chuẩn hóa phục vụ tìm kiếm; xóa dấu, số, phủ định hoặc metadata tùy tiện có thể làm mất nghĩa cần trả lời.
**Đầu vào:** toàn bộ D; bản sao trong bộ nhớ với 4 lỗi tự tạo: thiếu `doc_id`, trùng `doc_id`, `text` rỗng, `updated_at` sai định dạng. Không sửa file D.

1. **1,5 giờ:** kiểm tra 24 bản ghi và trường bắt buộc; xác định định dạng ngày đang dùng, ghi dữ liệu lỗi thay vì âm thầm bỏ qua.
2. **2 giờ:** hoàn thiện `normalize_text` theo starter, giữ Unicode tiếng Việt và nội dung gốc; lưu quan hệ văn bản tìm kiếm → `doc_id` → nguồn/ngày cập nhật.
3. **1,5 giờ:** chạy nhập hai lần, so số tài liệu và ID; chạy riêng 4 ca lỗi, báo rõ tài liệu nào không được nhập và lý do.

**Nghiệm thu:** dữ liệu chuẩn có đúng 24 ID duy nhất, nhập lại không nhân đôi; cả 4 lỗi được phát hiện; lấy một đoạn chuẩn hóa vẫn tìm được nguyên văn và nguồn gốc.
**Đổi bài:** thay 30 phút trình bày báo cáo bằng thử khoảng trắng lặp và dấu tiếng Việt ở hai dạng Unicode.

### L08 — Chunking có biên và có bằng chứng

**Đọc để hiểu bài:** [R06 — Chunking và overlap](../../kien_thuc/03_llm_rag.md#r06).

**Mục tiêu và kiến thức:** chia tài liệu để đơn vị truy hồi vừa đủ nhỏ, nhưng vẫn chứa thông tin hoàn chỉnh. Overlap tạo cơ hội giữ bằng chứng ở ranh giới, đồng thời tăng số đoạn trùng và chi phí.
**Đầu vào:** D sau L07; 4 câu M; ba cấu hình số từ `(32, 0)`, `(32, 8)`, `(64, 16)` với cặp `(kích thước, overlap)`.

1. **2 giờ:** hoàn thiện `chunk_words`; gắn mỗi đoạn với ID ổn định, `doc_id`, thứ tự và khoảng từ trong văn bản chuẩn hóa; giữ liên kết đến bản gốc.
2. **1,5 giờ:** tạo ba bộ chunk; thống kê số đoạn, chiều dài và tỷ lệ phần lặp, xem thủ công đoạn đầu/cuối của hai tài liệu.
3. **1,5 giờ:** lần theo bằng chứng của M để xem chỗ bị cắt; thử văn bản rỗng, ngắn hơn chunk và overlap không hợp lệ. Chọn một cấu hình tạm trên V.

**Nghiệm thu:** không vòng lặp vô hạn, không mất phần cuối, ID đoạn không trùng; có bảng ba cấu hình và ít nhất 2 nhận xét về ranh giới bằng chứng. Corpus ngắn có thể cho ít khác biệt; ghi đúng quan sát.
**Đổi bài:** thay 45 phút phân tích thêm bằng thử cắt theo đoạn văn và so trên cùng hai tài liệu.

### L09 — Baseline lexical và Recall@k

**Đọc để hiểu bài:** [R07 — Lexical, TF-IDF và BM25](../../kien_thuc/03_llm_rag.md#r07); [R12 — Đánh giá, ablation và LoRA](../../kien_thuc/03_llm_rag.md#r12).

**Mục tiêu và kiến thức:** dựng mức so sánh đơn giản bằng từ xuất hiện trong câu hỏi/tài liệu. Baseline lexical trong starter không dùng embedding học được; nó giúp phát hiện lỗi dữ liệu và truy vấn trước khi thêm mô hình.
**Đầu vào:** D/chunk đã chọn ở L08; toàn bộ A; ba giá trị `k=1,3,5`. Chỉ dùng `relevant_doc_ids` để chấm sau khi truy hồi.

1. **2 giờ:** hoàn thiện `lexical_search`; ghi quy tắc tính điểm và phá hòa, trả điểm cùng ID đoạn và `doc_id`, xử lý câu hỏi rỗng và không có từ khớp.
2. **1,5 giờ:** hoàn thiện `recall_at_k`; gộp các chunk cùng `doc_id` trước khi lấy top-k tài liệu. Mỗi câu có Recall = số ID đúng trong top-k / số ID đúng cần tìm; trung bình trên 16 câu A.
3. **1,5 giờ:** lập bảng Recall@1/3/5, số câu M tìm đủ mọi nguồn trên mẫu 4; kiểm tra tay hai câu, gồm một câu đa nguồn.

**Nghiệm thu:** có ranking cho 16 câu, đối chiếu tay khớp chương trình và ít nhất 3 lỗi truy hồi cụ thể; không gọi tỷ lệ “có ít nhất một nguồn” là Recall của câu đa nguồn.
**Đổi bài:** thay 45 phút dọn mã bằng lexical có trọng số IDF; báo như biến thể mới, vẫn giữ baseline ban đầu.

### L10 — Dense retrieval bằng embedding thật

**Đọc để hiểu bài:** [R08 — Embedding và cosine](../../kien_thuc/03_llm_rag.md#r08).

**Mục tiêu và kiến thức:** biểu diễn câu hỏi và đoạn bằng vector từ mô hình đã học, rồi tìm vector gần nhau. Bi-encoder mã hóa hai phía riêng; chọn model card phù hợp tiếng Việt và tuân thủ cách mã hóa query/document của mô hình. [Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html).
**Đầu vào:** cùng chunk và A của L09; một mô hình embedding thật phù hợp tài nguyên hiện có; giữ nguyên corpus và tập câu để so công bằng.

1. **1,5 giờ:** chọn mô hình, ghi model ID/revision, giấy phép, giới hạn đầu vào và phiên bản thư viện; chạy batch nhỏ để kiểm tra chiều vector và giá trị hữu hạn.
2. **2 giờ:** mã hóa corpus một lần, lưu cấu hình gắn với vector; mã hóa query, xếp hạng bằng phép tương đồng phù hợp model card và trả lại nguồn.
3. **1,5 giờ:** đo Recall@1/3/5 trên A, thời gian tạo chỉ mục và truy vấn; đối chiếu 3 câu có thay đổi ranking so lexical. Nếu chưa tải/chạy được model, hoàn thiện adapter và ghi `dense_chua_hoan_thanh`.

**Nghiệm thu:** có vector thực, manifest tái lập và bảng so cùng 16 câu để đạt phần dense; vector ngẫu nhiên/hash chỉ là test kỹ thuật, không đạt phần mô hình.
**Đổi bài:** nếu model đã chạy ổn, thay 30 phút báo cáo bằng so batch nhỏ/lớn; không tải thêm nhiều model trong ngày.

### L11 — Hybrid search với Reciprocal Rank Fusion

**Đọc để hiểu bài:** [R09 — Hybrid và RRF](../../kien_thuc/03_llm_rag.md#r09).

**Mục tiêu và kiến thức:** hợp nhất thứ hạng để tận dụng hai kiểu tìm kiếm. RRF cộng `1 / (c + rank)` từ mỗi danh sách có tài liệu; rank bắt đầu từ 1. Không cộng trực tiếp hai loại điểm có thang đo khác nhau.
**Đầu vào:** ranking lexical L09 và dense L10 của A; top-10 tài liệu mỗi nhánh, `c=60`; ba ID đầu của D dùng cho ví dụ tính tay.

1. **1,5 giờ:** hoàn thiện `reciprocal_rank_fusion`; tính tay hai danh sách chứa ba ID trên, gồm một ID chỉ xuất hiện ở một nhánh; mỗi ID chỉ có một thứ hạng trong mỗi danh sách.
2. **2 giờ:** gộp ranking đã bỏ trùng `doc_id`, giữ trace về điểm/thứ hạng từng nhánh; thử danh sách rỗng, ID lặp và điểm hòa.
3. **1,5 giờ:** so lexical, dense và hybrid trên cùng A ở k=5; chỉ chọn cấu hình theo V. Khi chưa có dense thật, dùng ranking tự tạo để test hàm và ghi hybrid mô hình chưa hoàn thành.

**Nghiệm thu:** phép tính tay khớp, không cộng hai lần ID lặp trong một nhánh; báo đủ 16 câu và số câu M tìm đủ nguồn. Không mặc định hybrid phải thắng baseline.
**Đổi bài:** thay 30 phút dọn trace bằng so thêm `c=20` trên V; ghi cả hai kết quả, không sửa theo T.

### L12 — Reranker và bàn giao R2

**Đọc để hiểu bài:** [R10 — Reranker](../../kien_thuc/03_llm_rag.md#r10); [R12 — Đánh giá, ablation và LoRA](../../kien_thuc/03_llm_rag.md#r12).

**Mục tiêu và kiến thức:** chấm lại cặp câu hỏi–đoạn trong một tập ứng viên nhỏ. Cross-encoder nhìn hai phần cùng lúc; reranker chỉ sắp xếp ứng viên đã có, không cứu được nguồn bị bỏ khỏi tập ứng viên. [Hướng dẫn hai giai đoạn](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html).
**Đầu vào:** top-10 tài liệu hybrid của 16 câu A; mỗi tài liệu lấy đoạn có hạng cao nhất trong các nhánh làm đại diện; một reranker thật có model card phù hợp ngôn ngữ.

1. **1,5 giờ:** nối reranker, ghi cách chọn đoạn, giới hạn input và số cặp; giữ ranking trước khi chấm lại để đối chiếu.
2. **2 giờ:** so hybrid và hybrid + reranker ở top-5; đo thời gian trên cùng máy và phân loại ít nhất 3 ca đổi hạng, gồm tác động của việc chọn đoạn đại diện.
3. **1,5 giờ:** bàn giao R2 với manifest, lệnh chạy, bảng lexical/dense/hybrid/rerank và lỗi còn lại. Nếu thiếu model, giữ kết quả baseline và ghi rõ các nhánh chưa chạy.

**Nghiệm thu R2:** nguồn truy vết được, có đo trên 16 câu A; mục tiêu học tập là macro Recall@5 ≥ 0,80 và đủ nguồn ở ít nhất 3/4 câu M. Đạt đầy đủ phần mô hình cần dense và reranker thật; nếu chưa đạt điểm thì nộp kết quả thật cùng phân tích lỗi, không sửa nhãn để qua mốc.
**Đổi bài:** thay 30 phút trình bày bằng so rerank top-5 với top-10; giữ cả chất lượng và thời gian, không tuyên bố tối ưu cho dữ liệu lớn từ corpus này.

**Ngày thứ bảy — 1 giờ ôn:** 20 phút tính Recall một câu đa nguồn, 20 phút giải thích lexical/dense/RRF/reranker, 20 phút ghi tiến độ R2 và điều kiện tài nguyên còn thiếu.

## Tuần 3 — RAG có nguồn, từ chối và đánh giá thật

### L13 — Ghép truy hồi với mô hình sinh

**Đọc để hiểu bài:** [R11 — RAG và kiểm bằng chứng](../../kien_thuc/03_llm_rag.md#r11).

**Mục tiêu và kiến thức:** đưa bằng chứng lấy từ kho ngoài vào ngữ cảnh trước khi mô hình trả lời. Truy hồi đúng tạo điều kiện cho trả lời đúng; mô hình vẫn có thể bỏ qua bằng chứng hoặc thêm điều không có trong nguồn. [Bài báo RAG](https://arxiv.org/abs/2005.11401).
**Đầu vào:** D, cấu hình retrieval chọn trên V ở R2, provider R1; 4 câu đầu trong A không đa nguồn và toàn bộ M, tổng 8 câu.

1. **1,5 giờ:** ghép query → retrieval → chọn đoạn trong ngân sách → prompt → model → validator; context chỉ lấy từ kết quả truy hồi, không lấy nguồn chuẩn từ nhãn.
2. **2 giờ:** chạy mô hình sinh thật trên 8 câu; lưu prompt đã gửi, ID/đoạn ngữ cảnh, raw output, output đã parse và phiên bản cấu hình.
3. **1,5 giờ:** lần theo 3 câu sai hoặc thiếu căn cứ; xác định lỗi ở retrieval, context bị cắt, generation hay parser. Nếu model chưa chạy, hoàn thiện trace bằng fake và ghi generation chưa hoàn thành.

**Nghiệm thu:** đủ 8 trace chạy thật để đạt phần generation của lab; mọi ID dẫn nguồn truy được về D. Trace fake chỉ nghiệm thu đường đi dữ liệu.
**Đổi bài:** thay 30 phút dọn mã bằng so thứ tự hai đoạn nguồn trên một câu M; ghi quan sát, không khái quát từ một ví dụ.

### L14 — Kiểm tra nguồn theo từng phát biểu

**Đọc để hiểu bài:** [R11 — RAG và kiểm bằng chứng](../../kien_thuc/03_llm_rag.md#r11); [R03 — Provider, HTTP và schema](../../kien_thuc/03_llm_rag.md#r03).

**Mục tiêu và kiến thức:** xác định đoạn trích hỗ trợ chính xác điều gì. ID tồn tại chỉ chứng minh liên kết hợp lệ; một câu chứa hai khẳng định có thể cần hai bằng chứng khác nhau.
**Đầu vào:** 8 output thật và context đã gửi ở L13; D; ba output biến đổi bằng tay: ID lạ, ID đúng nhưng sai nội dung, bỏ một nguồn trong câu đa nguồn.

1. **1,5 giờ:** tạo bảng từng phát biểu → trích đoạn hỗ trợ → `doc_id`; gắn nhãn được hỗ trợ, trái nguồn hoặc không có bằng chứng.
2. **2 giờ:** ghép kiểm tra ID trong context bằng validator và rà soát ngữ nghĩa bằng người chấm; thử cả ba biến thể, giữ nguyên raw output để không che lỗi mô hình.
3. **1,5 giờ:** đo tỷ lệ phát biểu có trích dẫn được nguồn hỗ trợ và tỷ lệ phát biểu cần bằng chứng đã được hỗ trợ; sửa cách yêu cầu dẫn nguồn trên V rồi chạy lại tối đa 4 câu sai.

**Nghiệm thu:** bảng chấm đủ 8 output, 3 lỗi tạo sẵn đều có kết luận đúng; báo tử/mẫu và tách lỗi ID với lỗi nội dung. Nếu chưa có output thật, bảng fixture mang trạng thái luyện chấm.
**Đổi bài:** thay 30 phút sửa prompt bằng chấm lại hai câu sau một khoảng nghỉ và ghi bất đồng của chính mình.

### L15 — Thiếu bằng chứng và chỉ dẫn gây nhiễu

**Đọc để hiểu bài:** [R02 — Prompt và ranh giới dữ liệu](../../kien_thuc/03_llm_rag.md#r02); [R11 — RAG và kiểm bằng chứng](../../kien_thuc/03_llm_rag.md#r11); [H09 — Phân quyền và prompt injection](../../kien_thuc/04_deep_learning_he_thong_agent.md#h09).

**Mục tiêu và kiến thức:** trả lời thiếu dữ kiện bằng sự từ chối rõ lý do, đồng thời giữ ranh giới chỉ dẫn. Điểm truy hồi không phải xác suất câu trả lời đúng; từ chối mọi câu cũng không tạo ra trợ lý hữu ích.
**Đầu vào:** U + X + 4 câu đầu trong A không đa nguồn, tổng 12 câu V; D và pipeline L13/L14. X dùng nguyên câu hỏi gây nhiễu trong dữ liệu, không thêm bí mật thật.

1. **1,5 giờ:** định nghĩa từ chối hợp lệ, câu trả lời thiếu phần nào phải nói rõ phần đó, và cách xử lý câu yêu cầu bỏ qua quy tắc hoặc làm theo chỉ dẫn trong tài liệu.
2. **2 giờ:** chạy model thật trên 12 câu; ghi đáp án sai do suy đoán, câu có bằng chứng bị từ chối nhầm và hành vi làm theo chỉ dẫn gây nhiễu.
3. **1,5 giờ:** sửa một chính sách trên V, chẳng hạn điều kiện thiếu bằng chứng hoặc mẫu output; chạy lại cùng 12 câu và so cả giảm lỗi lẫn giảm khả năng trả lời.

**Nghiệm thu:** bảng trước/sau với tử/mẫu cho U, X và 4 câu có đáp án; không ép X luôn phải từ chối nếu có phần hỏi hợp lệ có thể trả lời an toàn từ nguồn. Fake chỉ kiểm tra nhánh từ chối.
**Đổi bài:** thay 30 phút sửa prompt bằng che một nguồn của câu M để kiểm tra cách báo thiếu bằng chứng.

### L16 — Bộ chấm development tách từng loại lỗi

**Đọc để hiểu bài:** [R12 — Đánh giá, ablation và LoRA](../../kien_thuc/03_llm_rag.md#r12); [H10 — Test, đánh giá và trace](../../kien_thuc/04_deep_learning_he_thong_agent.md#h10).

**Mục tiêu và kiến thức:** đo retrieval và generation riêng để biết phải sửa đâu. Một điểm tổng duy nhất dễ che việc truy hồi tốt nhưng sinh sai, hoặc từ chối hết khiến câu ngoài phạm vi có vẻ đạt cao.
**Đầu vào:** toàn bộ 24 câu V, D, pipeline hiện tại; `expected_answer` và `relevant_doc_ids` chỉ được đưa cho bộ chấm sau khi hệ thống đã lưu output.

1. **1,5 giờ:** viết bộ chạy theo ID, khóa cấu hình cho lượt đo; lưu ranking, context thực gửi, output, lỗi, số lượt model, thời gian và token thực nếu có.
2. **2 giờ:** chạy 24 câu bằng model thật; chấm 16 câu có đáp án về đúng/đủ ý và căn cứ, 4 câu U về từ chối phù hợp, 4 câu X về giữ quy tắc và xử lý yêu cầu hợp lệ.
3. **1,5 giờ:** xuất bảng từng câu và bảng nhóm; báo Recall@5, đủ nguồn cho M, đúng/16, từ chối đúng/4, xử lý gây nhiễu đúng/4, độ hợp lệ schema/24 và chỉ số nguồn của L14.

**Nghiệm thu:** 24 dòng đều có kết quả hoặc lỗi; không xóa câu lỗi khỏi mẫu số. Khi không có trích dẫn, chỉ số nguồn có mẫu số 0 ghi “không áp dụng”, kèm độ bao phủ bằng chứng để tránh điểm đẹp giả.
**Đổi bài:** thay 30 phút làm biểu đồ bằng chấm lại 4 câu khó theo tiêu chí viết sẵn và ghi lý do đổi điểm.

### L17 — Ablation tìm phần tạo ra khác biệt

**Đọc để hiểu bài:** [R12 — Đánh giá, ablation và LoRA](../../kien_thuc/03_llm_rag.md#r12); [H10 — Test, đánh giá và trace](../../kien_thuc/04_deep_learning_he_thong_agent.md#h10).

**Mục tiêu và kiến thức:** thay một thành phần trong khi giữ phần còn lại để đánh giá đóng góp. So hai pipeline dùng model, câu hỏi hoặc ngân sách khác nhau không đủ để quy khác biệt cho retrieval.
**Đầu vào:** 4 câu đầu của A không đa nguồn + M + 2 câu đầu U + 2 câu đầu X, tổng 12 câu V; bốn cấu hình: không context, lexical RAG, hybrid RAG, hybrid + reranker RAG.

1. **1,5 giờ:** cố định model, tham số sinh, ngân sách, prompt và quy tắc chấm; với cấu hình không context, giữ cùng chính sách cho phép từ chối khi thiếu nguồn.
2. **2 giờ:** chạy 4 × 12 = 48 output thật; chỉ thay nhánh truy hồi/context tương ứng. Ghi thứ tự chạy, lỗi và thời gian; không thay model giữa chừng để lấy kết quả đẹp hơn.
3. **1,5 giờ:** so chất lượng, đủ nguồn đa tài liệu, số token và thời gian; phân tích ít nhất 3 câu thay đổi. Chọn một cấu hình cuối bằng V và ghi lý do, kể cả khi baseline thắng.

**Nghiệm thu:** có bảng 4 cấu hình, cùng 12 ID, bằng chứng 48 lượt hoặc lỗi từng lượt và ít nhất 3 phân tích nguyên nhân. Nhánh chưa có model thật ghi chưa hoàn thành, không dùng ranking/đáp án dựng sẵn để lấp bảng.
**Đổi bài:** thay 30 phút trình bày bằng chạy lặp một câu ở hai cấu hình để nhận diện biến thiên; không cộng thành mẫu đánh giá mới.

### L18 — Lưu phiên bản, đánh giá dev và bàn giao R3

**Đọc để hiểu bài:** [R12 — Đánh giá, ablation và LoRA](../../kien_thuc/03_llm_rag.md#r12); [H11 — Artifact, Docker và CI](../../kien_thuc/04_deep_learning_he_thong_agent.md#h11).

**Mục tiêu và kiến thức:** lưu được phiên bản có thể chạy lại và kiểm tra lỗi quay lại sau thay đổi. Điểm trên dev phản ánh kết quả phát triển đã nhìn thấy dữ liệu; nó chưa phải bằng chứng chất lượng độc lập. Test phải còn nguyên vai trò đến lúc chốt cả phần agent/triển khai ở R6.
**Đầu vào:** D, cấu hình chọn từ L17, bộ chấm L16 và toàn bộ 24 câu V. Không mở nội dung T; lưu dấu phiên bản trước lượt đo R3.

1. **1 giờ:** lưu phiên bản mã, model/provider, prompt, chunking, retrieval, ngân sách và chính sách từ chối; xác nhận ứng dụng chỉ nhận câu hỏi, không nhận nhãn hoặc đáp án chuẩn từ bộ chấm.
2. **2,5 giờ:** chạy một lượt dev bằng model thật trên phiên bản vừa lưu, có retry theo R1; lưu đủ 24 output hoặc lỗi, chấm như L16. Báo thêm đủ bằng chứng cho 4 câu đa nguồn và thời gian p50/p95 của 24 request, nêu quy ước tính percentile.
3. **1,5 giờ:** viết báo cáo R3, demo một câu có nguồn và một câu thiếu bằng chứng; phân tích ít nhất 3 lỗi, so với L16 để phát hiện lỗi quay lại. Đánh dấu mọi số đo là `dev`; chuyển danh sách cần sửa sang tuần tiếp theo.

**Nghiệm thu R3:** mô hình sinh thật, 24 kết quả/lỗi dev, không rò nhãn vào prompt, trích dẫn truy vết và báo cáo tái lập là điều kiện bắt buộc. Mục tiêu học tập trên V: đúng có căn cứ ≥ 12/16 câu có đáp án, đủ ý/nguồn ≥ 3/4 câu đa nguồn, từ chối phù hợp ≥ 3/4 câu U, xử lý đúng ≥ 4/4 câu X, ID dẫn nguồn hợp lệ 100%; báo thêm độ hỗ trợ từng phát biểu và độ bao phủ nguồn, không suy ra hai chỉ số này từ ID hợp lệ. Nếu thiếu model thật, ghi `generation_chua_hoan_thanh`, tiếp tục phần kỹ thuật độc lập ở các tuần sau.
**Đổi bài:** thay 30 phút làm đẹp demo bằng nhờ người khác chạy theo hướng dẫn nếu sẵn có; không bắt buộc liên hệ dịch vụ hoặc người ngoài.

**Ngày thứ bảy — 1 giờ ôn:** 20 phút tự giải thích một trace dev, 20 phút đối chiếu R1–R3 với bằng chứng, 20 phút chọn lỗi sẽ xử lý ở phần agent/triển khai tiếp theo. Giữ nguyên T đến R6.

## Cách đọc kết quả ba mốc

Các ngưỡng R2/R3 là **mục tiêu giảng dạy**, chưa phải kết quả thực nghiệm hay cam kết chất lượng sản phẩm. Bộ dev 24 câu và corpus 24 tài liệu chỉ đủ cho bài học có thể kiểm tra; luôn báo số đếm, cấu hình, dữ liệu giả lập, việc đã dùng dev để chọn phương án và giới hạn mẫu nhỏ. Không điền sẵn điểm đạt trong báo cáo.

R1 chứng minh hợp đồng và cách xử lý lỗi; R2 chứng minh truy hồi có đo lường; R3 chứng minh hệ thống sinh đã được đánh giá bằng mô hình thật trên dev và có phiên bản tái lập. Kiểm tra độc lập trên T dành cho R6. Thiếu tài nguyên có thể để phần mô hình chờ và tiếp tục phần độc lập, nhưng không đánh dấu hoàn thành toàn bộ hướng bằng kết quả fake.
