from src.config import get_supabase

class ReportDAO:
    def __init__(self):
        self.sb = get_supabase()

    def top_products(self, limit: int = 5):
        resp = self.sb.table("order_items").select("prod_id, sum(quantity) as total_qty").group("prod_id").order("total_qty", desc=True).limit(limit).execute()
        return resp.data or []

    def total_revenue_last_month(self):
        import datetime
        now = datetime.datetime.now()
        first_day = datetime.datetime(now.year, now.month, 1)
        last_month = first_day - datetime.timedelta(days=1)
        first_day_last_month = datetime.datetime(last_month.year, last_month.month, 1)
        resp = self.sb.table("orders").select("sum(total_amount)").gte("created_at", first_day_last_month.isoformat()).lte("created_at", last_month.isoformat()).execute()
        return resp.data[0]["sum"] if resp.data else 0

    def customer_order_counts(self):
        resp = self.sb.table("orders").select("customer_id, count(order_id) as order_count").group("customer_id").execute()
        return resp.data or []
