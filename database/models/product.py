from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    inn = Column(String(12))
    contact_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))

    products = relationship("Product", back_populates="supplier")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200))

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)

    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    unit = Column(String(50))
    quantity = Column(Numeric(10, 2))
    price = Column(Numeric(12, 2))
    status = Column(String(50), default="в наличии")
    expiry_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    supplier = relationship("Supplier", back_populates="products")
    category = relationship("Category", back_populates="products")
