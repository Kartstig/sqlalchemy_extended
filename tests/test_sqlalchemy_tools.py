#!/usr/bin/env python

"""Tests for `sqlalchemy_extended` package."""

import pytest
from datetime import datetime
from faker import Faker
from random import randint, random
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_extended import BaseModel

fake = Faker()


@pytest.fixture
def model():
    """Fixture for an example model"""

    def build_model(**kwargs):
        Base = declarative_base(cls=BaseModel)

        class TestModel(Base):
            __restricted_columns__ = ("password",)
            __tablename__ = "tests"

            id = Column(Integer, primary_key=True)
            email = Column(String(400), nullable=False)
            password = Column(String(60), nullable=False)
            float = Column(Float, nullable=False)
            created_at = Column(DateTime, nullable=False)
            updated_at = Column(DateTime)

            def __init__(self, **data):
                self.id = data["id"]
                self.float = data.get("float")
                self.email = data["email"]
                self.password = data.get("password", "password")
                self.created_at = data["created_at"]
                self.updated_at = data.get("updated_at")

        return TestModel(
            id=kwargs.get("id", randint(1, 100)),
            email=kwargs.get("email", fake.email()),
            float=kwargs.get("float", random()),
            created_at=kwargs.get("created_at", datetime.now()),
            updated_at=kwargs.get("updated_at"),
        )

    return build_model


def test_BaseModel___repr___ok(model):
    """Ensure __repr__ works"""
    obj = model()
    assert obj.__repr__() == f"<{obj.__class__.__name__} {obj.id}>"


def test_BaseModel_dto_ok(model):
    """Ensure dto works"""
    obj = model()
    result = obj.dto()
    assert result["id"] == obj.id
    assert result["email"] == obj.email
    assert result["float"] == obj.float
    assert result["created_at"] == obj.created_at.isoformat()
    assert result["updated_at"] is None


def test_BaseModel_columns_ok(model):
    """Ensure columns works"""
    obj = model()
    result = tuple(obj.columns())

    assert len(result) == 6
    for k in ("id", "email", "password", "float", "created_at", "updated_at"):
        assert k in result


def test_BaseModel_safe_columns_ok(model):
    """Ensure columns works"""
    obj = model()
    result = tuple(obj.safe_columns())

    assert len(result) == 5
    for k in ("id", "email", "float", "created_at", "updated_at"):
        assert k in result


def test_BaseModel_update_ok(model):
    """Ensure update works"""
    now = datetime.utcnow()
    fake_email = fake.email()
    obj = model()
    old_email = obj.email
    obj.update(email=fake_email)

    assert obj.email == fake_email
    assert obj.email != old_email
    assert obj.updated_at > now


def test_BaseModel_update_id_ok(model):
    """Ensure update works"""
    fake_id = 123456789
    obj = model()
    old_id = obj.id
    obj.update(id=fake_id)

    assert obj.id != fake_id
    assert obj.id == old_id


def test_BaseModel_no_restricted_cols_ok():
    Base = declarative_base(cls=BaseModel)

    class TestModel(Base):
        __tablename__ = "tests"

        id = Column(Integer, primary_key=True)

        def __init__(self, **data):
            self.id = data["id"]

    result = tuple(TestModel(id=1).safe_columns())

    assert len(result) == 1
    assert result[0] == "id"


def test_BaseModel_eq_ok(model):
    obj1 = model()
    obj2 = model()

    assert obj1 != obj2

    obj2.update(**{col: getattr(obj1, col) for col in obj1.columns()})
    obj2.id = obj1.id  # The id is normally skipped

    assert obj1 == obj2
