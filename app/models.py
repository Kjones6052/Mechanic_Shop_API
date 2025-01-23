# This file contains all the models for database tables

# Imports
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import List

# Create a base class for our models
class Base(DeclarativeBase):
    pass

# Instantiate your SQLAlchemy database and Marshmallow
db = SQLAlchemy(model_class = Base)

# Service Mechanics Link Table
service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

# Customers
class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    service_tickets: Mapped[List["Service_Ticket"]] = db.relationship(back_populates="customer", cascade="all, delete")

# Service Tickets
class Service_Ticket(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"), nullable=False)

    customer: Mapped["Customer"] = db.relationship(back_populates="service_tickets")
    mechanics: Mapped[List["Mechanic"]] = db.relationship(secondary=service_mechanics, back_populates="service_tickets")
    required_parts: Mapped[List["RequiredParts"]] = db.relationship(back_populates="service_ticket")

# Mechanics
class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[List["Service_Ticket"]] = db.relationship(secondary=service_mechanics)

# Parts (inventory)
class Part(Base):
    __tablename__ = "parts"

    # attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    required_parts: Mapped[List["RequiredParts"]] = db.relationship(back_populates="part")

# Required Parts
class RequiredParts(Base):
    __tablename__ = "required_parts"

    # attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey("service_tickets.id"), nullable=False)
    part_id: Mapped[int] = mapped_column(db.ForeignKey("parts.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)

    service_ticket: Mapped["Service_Ticket"] = db.relationship(back_populates="required_parts")
    part: Mapped["Part"] = db.relationship(back_populates="required_parts")