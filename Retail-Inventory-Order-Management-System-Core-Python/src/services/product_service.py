# src/services/product_service.py
# from typing import List, Dict
# import src.dao.product_dao as product_dao
 
# class ProductError(Exception):
#     pass
#  # src/services/product_service.py
# from typing import Optional, Dict
# import src.dao.product_dao as product_dao

# def add_product(
#     name: str,
#     sku: str,
#     price: float,
#     stock: int = 0,
#     category: Optional[str] = None
# ) -> Optional[Dict]:
#     """
#     Validate inputs and create a product via the DAO.
#     Returns the inserted row (dict) or None.
#     Raises ValueError for validation/duplication errors.
#     """
#     # Basic validation
#     if not name or not name.strip():
#         raise ValueError("name is required")
#     if not sku or not sku.strip():
#         raise ValueError("sku is required")
#     if price < 0:
#         raise ValueError("price must be non-negative")
#     if stock < 0:
#         raise ValueError("stock must be non-negative")

#     # Ensure SKU is unique
#     existing = product_dao.get_product_by_sku(sku)
#     if existing:
#         raise ValueError(f"Product with sku '{sku}' already exists.")

#     # Delegate insertion to DAO
#     return product_dao.create_product(name=name, sku=sku, price=price, stock=stock, category=category)

 
# def restock_product(prod_id: int, delta: int) -> Dict:
#     if delta <= 0:
#         raise ProductError("Delta must be positive")
#     p = product_dao.get_product_by_id(prod_id)
#     if not p:
#         raise ProductError("Product not found")
#     new_stock = (p.get("stock") or 0) + delta
#     return product_dao.update_product(prod_id, {"stock": new_stock})
 
# def get_low_stock(threshold: int = 5) -> List[Dict]:
#     allp = product_dao.list_products(limit=1000)
#     return [p for p in allp if (p.get("stock") or 0) <= threshold]
 
 
#  using oops
from typing import Optional, Dict, List
from src.dao.product_dao import ProductDAO


class ProductError(Exception):
    pass


class ProductService:
    def __init__(self, dao: ProductDAO):
        self.dao = dao

    def add_product(
        self, name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None
    ) -> Optional[Dict]:
        if not name or not name.strip():
            raise ValueError("name is required")
        if not sku or not sku.strip():
            raise ValueError("sku is required")
        if price < 0:
            raise ValueError("price must be non-negative")
        if stock < 0:
            raise ValueError("stock must be non-negative")

        if self.dao.get_product_by_sku(sku):
            raise ValueError(f"Product with sku '{sku}' already exists.")

        return self.dao.create_product(name, sku, price, stock, category)

    def restock_product(self, prod_id: int, delta: int) -> Dict:
        if delta <= 0:
            raise ProductError("Delta must be positive")

        p = self.dao.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")

        new_stock = (p.get("stock") or 0) + delta
        return self.dao.update_product(prod_id, {"stock": new_stock})

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        allp = self.dao.list_products(limit=1000)
        return [p for p in allp if (p.get("stock") or 0) <= threshold]
