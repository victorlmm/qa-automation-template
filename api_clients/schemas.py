"""Response contracts (pydantic). A missing or mistyped field fails the test,
which catches breaking API changes that a status check alone would miss."""

from pydantic import BaseModel, ConfigDict


class _Model(BaseModel):
    model_config = ConfigDict(extra="allow")  # new fields are fine, missing ones are not


class Category(_Model):
    category: str


class Product(_Model):
    id: int
    name: str
    price: str
    brand: str
    category: Category


class ProductsResponse(_Model):
    responseCode: int
    products: list[Product]
