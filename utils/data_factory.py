"""Test data generation. Unique values keep parallel runs from colliding."""

import uuid

from faker import Faker

fake = Faker()


def unique_id(length: int = 8) -> str:
    return uuid.uuid4().hex[:length]


def unique_email(domain: str = "example.com") -> str:
    return f"qa.{unique_id(10)}@{domain}"


def new_person() -> dict[str, str]:
    first, last = fake.first_name(), fake.last_name()
    return {
        "first_name": first,
        "last_name": last,
        "full_name": f"{first} {last}",
        "email": unique_email(),
        "password": f"Pw!{unique_id(10)}",
        "phone": fake.msisdn(),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zipcode": fake.postcode(),
        "country": "United States",
    }
