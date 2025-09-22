class ReportService:
    def __init__(self, dao):
        self.dao = dao

    def top_products(self, limit: int = 5):
        return self.dao.top_products(limit=limit)

    def total_revenue_last_month(self):
        return self.dao.total_revenue_last_month()

    def customer_order_count(self):
        return self.dao.customer_order_counts()

    def frequent_customers(self, min_orders: int = 2):
        return [c for c in self.dao.customer_order_counts() if c["order_count"] > min_orders]
