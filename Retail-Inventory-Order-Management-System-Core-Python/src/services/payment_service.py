from typing import Optional
from src.dao.payment_dao import PaymentDAO
from src.dao.order_dao import OrderDAO

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self, payment_dao: PaymentDAO, order_dao: OrderDAO):
        self.dao = payment_dao
        self.order_dao = order_dao

    def process_payment(self, order_id: int, method: str) -> dict:
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise PaymentError("Order not found")
        payment = self.dao.get_payment_by_order(order_id)
        if not payment:
            payment = self.dao.create_payment(order_id, order["total_amount"])
        payment = self.dao.update_payment(payment["payment_id"], {"status": "PAID", "method": method})
        self.order_dao.update_order(order_id, {"status": "COMPLETED"})
        return payment

    def refund_payment(self, order_id: int) -> dict:
        payment = self.dao.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("Payment not found")
        self.dao.update_payment(payment["payment_id"], {"status": "REFUNDED"})
        self.order_dao.update_order(order_id, {"status": "CANCELLED"})
        return payment
