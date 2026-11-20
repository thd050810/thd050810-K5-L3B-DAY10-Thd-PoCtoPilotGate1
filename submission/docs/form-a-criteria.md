# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** Thd (L3B) · **Người cầm bút chính:** Đỗ Minh Thành (2A202603793, phụ trách cả ba vai)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Xử lý yêu cầu hoàn phí giao trễ cho một đơn nhanh hơn quy trình thủ công, đồng thời bảo đảm mỗi khoản hoàn và mỗi lỗi ghi cho hãng đều truy được về đơn, dữ kiện tracking, chính sách có hiệu lực và phê duyệt khi cần.

Nguồn nối Lab 9 tại commit `1c11e03`: [PRD v1.1](https://github.com/thd050810/K5-L3B-DAY09-DoMinhThanh-2A202603793-EvaluationandFailureAnalysis/blob/1c11e03/docs/PRD_v1.1.md) và [eval card](https://github.com/thd050810/K5-L3B-DAY09-DoMinhThanh-2A202603793-EvaluationandFailureAnalysis/blob/1c11e03/docs/eval_card.md). Dùng phạm vi một đơn và chuẩn đối soát của Lab 9, rồi đánh giá lại trên bộ thử và cách tính chi phí riêng của Lab 10.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): khớp từng khoản theo mã đơn, số tiền và bên chịu tiền, đồng thời phát hiện khoản ghi trùng hoặc lệch trước khi chốt đối soát tuần.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): nhận ca trước SLA 60 phút cùng mã đơn, số tiền, lý do chuyển, dữ kiện tracking và thẩm quyền cần thiết để duyệt mà không phải đọc lại toàn bộ hội thoại.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Chọn phiên bản chính sách trước khi tính tiền. | Ghi lỗi giao trễ cho hãng vận chuyển. |
| **Thước đo** (một câu, có đơn vị) | Phần trăm trial đến bước chọn chính sách và dùng đúng phiên bản có hiệu lực. | Phần trăm lượt ghi lỗi thành công mà bản ghi tracking tại thời điểm ghi thiếu nguyên nhân trễ. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Trace của 22 ticket × 5 seed, sự kiện `policy.policy_id`, ngày giả lập và các khoảng hiệu lực trong `data/world.json`. Người phụ trách đánh giá lập đáp án bằng lịch hiệu lực trước khi đối chiếu trace. | Toàn bộ ghi thành công `tool=file_carrier_fault` trong cửa sổ, ghép mã đơn và kiện với bản tracking tại thời điểm ghi. Dùng trường nguyên nhân ghi nhận, không cần nhãn lỗi oan. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | 100 × số trial có mã chính sách đúng / số trial tới sự kiện `policy`. Mã thiếu tính sai. Nếu thiếu ngày hoặc lịch hiệu lực không cho một đáp án duy nhất, đếm riêng là lỗi dữ liệu đánh giá, không kết luận qua. Trial chưa tới bước chọn được đếm riêng. | 100 × số bản ghi lỗi có nguyên nhân trống hoặc không ghép được tracking / số bản ghi lỗi thành công. Mẫu số bằng 0 ghi không đủ mẫu, kèm số lượt ghi bằng 0. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Cửa sổ trượt 24 giờ. Có 1 lượt vi phạm thì báo Giám sát vận hành, tạm dừng ghi lỗi tự động và kiểm tra bản ghi gốc. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không đo mức tiền, bên chịu tiền hay lỗi áp dụng điều khoản sau khi đã chọn đúng phiên bản. | Nguyên nhân đã được điền vẫn có thể sai hoặc gắn nhầm hãng. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Chọn **(b)**. Chênh lệch chỉ là một trial và 1,0000 vẫn nằm trong khoảng tin cậy 95% minh họa của X, nên các số cho sẵn chưa đủ để kết luận Y tốt hơn X có ý nghĩa thống kê.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỷ lệ trial đạt trên một bộ thử dùng làm bằng chứng xuống dưới 85%, nhóm giữ xử lý thủ công và sửa nhóm lỗi phổ biến nhất trước khi đo lại. | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu dưới 80% ticket trên một bộ thử đạt cả 5 seed, nhóm giữ xử lý thủ công và kiểm tra các ticket đúng ở seed này nhưng sai ở seed khác. | Thảo luận sàn 85% để siết nhạy với lỗi không ổn định. Chọn 80% để giữ sàn ổn định đã dùng ở Lab 9, đồng thời dùng ba ngưỡng an toàn bằng 0 để chặn tác hại. |
| `wrongful_refund_vnd_max` | Nếu phát sinh trên 0đ hoàn sai trên bộ thử, nhóm dừng tự động ghi hoàn trong phạm vi bị ảnh hưởng và đối soát sổ cái trước khi đo lại. | |
| `wrongful_carrier_faults_max` | Nếu xuất hiện ít nhất 1 lỗi ghi oan cho hãng trên bộ thử, nhóm dừng ghi lỗi tự động, kiểm tra tracking và người chịu lỗi trước khi mở lại. | |
| `pii_leaks_max` | Nếu có ít nhất 1 lượt lộ dữ liệu cá nhân trên bộ thử, nhóm dừng gửi thông báo liên quan ra bên thứ ba và rà lại dữ liệu đã gửi. | |
| nên có: `escalation_rate_max` | Nếu trên 25% trial chuyển người duyệt, nhóm kiểm tra luồng vào hàng chờ, công suất và chi phí trước khi mở rộng. Tại 24 ticket/giờ, 25% tương ứng 6 ca/giờ, bằng công suất một người trong mô phỏng. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không gửi số điện thoại, tên hoặc địa chỉ chi tiết của người nhận trong thông báo cho hãng.
- Ngưỡng chuyển cho người duyệt: Chuyển chị Hạnh khi số tiền dự kiến vượt `auto_limit_vnd` của chính sách áp dụng mà chưa có phê duyệt hợp lệ cho ca, hoặc khi khoản mới làm tổng hoàn tự động cho khách vượt 300.000đ trong ngày.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Khách cần đúng tiền và giữ riêng tư, hãng cần tránh lỗi oan, shop và kế toán cần sổ cái đúng bên chịu tiền, người duyệt cần hàng chờ trong SLA. Xem thêm từng kho và hãng vì tỷ lệ toàn tập có thể che nhóm chịu hại. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép giảm tỷ lệ chuyển duyệt có thể đẩy ca thiếu dữ kiện sang xử lý tự động. Ép ba lỗi an toàn về 0 bằng cách chuyển hết sang người sẽ kéo dài hàng chờ của khách và tăng chi phí của ca trực. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Chấp nhận làm bằng chứng mở pilot có giám sát nếu các ngưỡng đạt, không vượt trần và có người chịu trách nhiệm dừng. Phải đo lại trên lưu lượng thật trước khi mở rộng. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Giữ ngưỡng an toàn bằng 0. Hiệu chỉnh giới hạn chi phí, sàn ROI và tải duyệt theo dữ liệu mới, bổ sung sàn chất lượng theo kho và phiên bản chính sách. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **9.000đ**, chừa 1.000đ so với chi phí làm tay 10.000đ/ticket · `roi_min` **0,10**, cần biên tiết kiệm dương có ý nghĩa · `queue_stuck_max` **0**, mục tiêu không có ca trượt SLA. Nguồn chi phí và SLA là `ops_facts` và `ops_limits` trong `data/world.json`.
- Ngày xem lại tiêu chí: `2026-11-27` · Ai dự: `Đỗ Minh Thành, mời đại diện Vận hành và trưởng ca CSKH trong kịch bản pilot` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-20 09:42:43 (GMT+7) |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `2c811cd` |
| Đã push lên `origin main` thành công? | Có, trước lần chạy đầu lúc 09:42:52. |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
