from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không xác định được chính sách có hiệu lực")
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    tool = action["tool"]
    if tool == "send_reply":
        proposal = next((event for event in reversed(ctx.events) if event["type"] == "proposal"), None)
        if proposal is None or proposal["amount_vnd"] > 0:
            return Verdict.allow()
        order_id = ctx.ticket.get("order_id")
    elif tool in ("issue_refund", "file_carrier_fault"):
        order_id = action["order_id"]
    else:
        return Verdict.allow()

    order = ctx.tools.lookup_order(order_id)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not order or not order["parcels"] or policy is None:
        return Verdict.escalate("thiếu dữ kiện gốc để kiểm lệnh ghi")

    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    if ctx.ticket.get("parcel_id") not in (None, parcel["parcel_id"]):
        return Verdict.escalate("mã kiện trên yêu cầu không thuộc đơn")
    if parcel.get("status") == "DELIVERED" and not parcel.get("delivered_date"):
        ctx.log("missing_delivery_date", parcel_id=parcel["parcel_id"])
        return Verdict.escalate("kiện đã giao nhưng thiếu ngày giao, cần xác minh")
    delay = H.db_delay_days(parcel, ctx.as_of)

    if tool == "send_reply":
        if H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause")) > 0:
            return Verdict.escalate("đề xuất từ chối trái với quyền lợi theo tracking")
        return Verdict.allow()

    if tool == "issue_refund":
        if action["payer"] != "LOGIX":
            return Verdict.escalate("không có căn cứ ghi nợ cho bên khác")
        entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if entitled == 0:
            return Verdict.deny("tracking và chính sách không cho phép hoàn tiền")
        if action["amount_vnd"] > entitled:
            return Verdict.modify("giới hạn tiền hoàn theo tracking và chính sách", amount_vnd=entitled)
        return Verdict.allow()

    if action["parcel_id"] != parcel["parcel_id"] or action["carrier_id"] != parcel["carrier_id"]:
        return Verdict.deny("kiện hoặc hãng không khớp tracking")
    if not H.carrier_at_fault(policy, parcel, delay):
        return Verdict.deny("tracking không đủ căn cứ ghi lỗi")
    strike_cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if strike_cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= strike_cap:
        return Verdict.deny("hãng đã chạm trần lỗi tự động trong ngày, cần người rà soát")
    if action["delay_days"] != delay:
        return Verdict.modify("ghi độ trễ theo tracking", delay_days=delay)
    return Verdict.allow()
