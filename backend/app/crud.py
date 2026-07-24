from sqlalchemy.orm import Session

from app import models, schemas


# =====================================================
# Equipment
# =====================================================

def create_equipment(
    db: Session,
    equipment: schemas.EquipmentCreate
):
    # Пользователь указывает верхний юнит
    top = equipment.top_unit
    bottom = top - equipment.size_u + 1

    try:
        # Создаем оборудование
        db_equipment = models.Equipment(
            contract_id=equipment.contract_id,
            vendor=equipment.vendor,
            model=equipment.model,
            serial_number=equipment.serial_number,
            size_u=equipment.size_u,
            placement_type=equipment.placement_type
        )

        db.add(db_equipment)
        db.flush()   # Получаем ID без commit

        # Создаем размещение
        db_location = models.EquipmentLocation(
            equipment_id=db_equipment.id,
            rack_id=equipment.rack_id,
            unit_from=bottom,
            unit_to=top
        )

        db.add(db_location)

        # Записываем историю
        db_history = models.EquipmentHistory(
            equipment_id=db_equipment.id,
            operation="CREATE",
            description=(
                f"Размещено в стойке {equipment.rack_id}, "
                f"U{top}-U{bottom}"
            )
        )

        db.add(db_history)

        # Всё сохраняется одной транзакцией
        db.commit()

        db.refresh(db_equipment)

        return db_equipment

    except Exception:
        db.rollback()
        raise


def get_equipment(
    db: Session,
    equipment_id: int
):
    return (
        db.query(models.Equipment)
        .filter(models.Equipment.id == equipment_id)
        .first()
    )


def get_equipment_by_serial(
    db: Session,
    serial_number: str
):
    return (
        db.query(models.Equipment)
        .filter(models.Equipment.serial_number == serial_number)
        .first()
    )


def get_all_equipment(db: Session):
    return (
        db.query(models.Equipment)
        .order_by(models.Equipment.id)
        .all()
    )


def update_equipment(
    db: Session,
    equipment_id: int,
    data: schemas.EquipmentUpdate
):
    equipment = get_equipment(db, equipment_id)

    if equipment is None:
        return None

    values = data.model_dump(exclude_unset=True)

    for key, value in values.items():
        setattr(equipment, key, value)

    db.commit()
    db.refresh(equipment)

    return equipment


def delete_equipment(
    db: Session,
    equipment_id: int
):
    equipment = get_equipment(db, equipment_id)

    if equipment is None:
        return False

    db.delete(equipment)
    db.commit()

    return True


# =====================================================
# Placement
# =====================================================

def place_equipment(
    db: Session,
    equipment_id: int,
    placement: schemas.PlacementCreate
):
    db_location = models.EquipmentLocation(
        equipment_id=equipment_id,
        rack_id=placement.rack_id,
        unit_from=placement.unit_from,
        unit_to=placement.unit_to
    )

    db.add(db_location)
    db.commit()
    db.refresh(db_location)

    return db_location


def get_rack_layout(
    db: Session,
    rack_id: int
):
    rack = (
        db.query(models.Rack)
        .filter(models.Rack.id == rack_id)
        .first()
    )

    if rack is None:
        return None

    layout = []

    locations = (
        db.query(
            models.EquipmentLocation,
            models.Equipment
        )
        .join(
            models.Equipment,
            models.Equipment.id == models.EquipmentLocation.equipment_id
        )
        .filter(
            models.EquipmentLocation.rack_id == rack_id,
            models.EquipmentLocation.removed_at.is_(None)
        )
        .all()
    )

    for unit in range(rack.height_u, 0, -1):

        entry = schemas.RackUnit(
            unit=unit
        )

        for location, equipment in locations:

            if location.unit_from <= unit <= location.unit_to:

                entry = schemas.RackUnit(
                    unit=unit,
                    equipment_id=equipment.id,
                    vendor=equipment.vendor,
                    model=equipment.model,
                    serial_number=equipment.serial_number
                )

                break

        layout.append(entry)

    return schemas.RackLayoutResponse(
        rack_id=rack.id,
        units=layout
    )
