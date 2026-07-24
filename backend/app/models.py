from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database import Base


SCHEMA = "inventory"


# ---------------------------------------------------
# Clients
# ---------------------------------------------------

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True)

    name = Column(String(255), nullable=False)

    comment = Column(Text)

    created_at = Column(DateTime)

    contracts = relationship(
        "Contract",
        back_populates="client"
    )


# ---------------------------------------------------
# Contracts
# ---------------------------------------------------

class Contract(Base):
    __tablename__ = "contracts"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True)

    client_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.clients.id"),
        nullable=False
    )

    contract_number = Column(
        String(100),
        nullable=False,
        unique=True
    )

    comment = Column(Text)

    created_at = Column(DateTime)

    client = relationship(
        "Client",
        back_populates="contracts"
    )

    equipment = relationship(
        "Equipment",
        back_populates="contract"
    )


# ---------------------------------------------------
# Rooms
# ---------------------------------------------------

class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True)

    name = Column(String(100), nullable=False)

    comment = Column(Text)

    racks = relationship(
        "Rack",
        back_populates="room"
    )


# ---------------------------------------------------
# Racks
# ---------------------------------------------------

class Rack(Base):
    __tablename__ = "racks"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True)

    room_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.rooms.id"),
        nullable=False
    )

    rack_number = Column(
        Integer,
        nullable=False
    )

    height_u = Column(
        Integer,
        nullable=False
    )

    comment = Column(Text)

    room = relationship(
        "Room",
        back_populates="racks"
    )

    locations = relationship(
        "EquipmentLocation",
        back_populates="rack"
    )


# ---------------------------------------------------
# Equipment
# ---------------------------------------------------

class Equipment(Base):
    __tablename__ = "equipment"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True)

    contract_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.contracts.id"),
        nullable=False
    )

    vendor = Column(
        String(100),
        nullable=False
    )

    model = Column(
        String(150),
        nullable=False
    )

    serial_number = Column(
        String(200),
        nullable=False,
        unique=True
    )

    size_u = Column(Integer)

    placement_type = Column(String(20))

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    contract = relationship(
        "Contract",
        back_populates="equipment"
    )

    locations = relationship(
        "EquipmentLocation",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )

    history = relationship(
        "EquipmentHistory",
        back_populates="equipment",
        cascade="all, delete-orphan"
    )


# ---------------------------------------------------
# Equipment location
# ---------------------------------------------------

class EquipmentLocation(Base):
    __tablename__ = "equipment_location"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True)

    equipment_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.equipment.id"),
        nullable=False
    )

    rack_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.racks.id"),
        nullable=False
    )

    unit_from = Column(Integer)

    unit_to = Column(Integer)

    placed_at = Column(DateTime)

    removed_at = Column(DateTime)

    equipment = relationship(
        "Equipment",
        back_populates="locations"
    )

    rack = relationship(
        "Rack",
        back_populates="locations"
    )


# ---------------------------------------------------
# Equipment history
# ---------------------------------------------------

class EquipmentHistory(Base):
    __tablename__ = "equipment_history"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True)

    equipment_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.equipment.id"),
        nullable=False
    )

    operation = Column(
        String(50),
        nullable=False
    )

    description = Column(Text)

    created_at = Column(DateTime)

    equipment = relationship(
        "Equipment",
        back_populates="history"
    )
