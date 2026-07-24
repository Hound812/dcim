-- ==========================================
-- Inventory System
-- Initial database schema
-- Version 1.0
-- ==========================================

CREATE SCHEMA IF NOT EXISTS inventory;


-- =========================
-- Клиенты
-- =========================

CREATE TABLE inventory.clients (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    comment TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================
-- Договоры
-- =========================

CREATE TABLE inventory.contracts (
    id BIGSERIAL PRIMARY KEY,

    client_id BIGINT NOT NULL,

    contract_number VARCHAR(100) NOT NULL,

    comment TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_contract_client
        FOREIGN KEY (client_id)
        REFERENCES inventory.clients(id)
        ON DELETE RESTRICT
);


CREATE INDEX idx_contract_client
ON inventory.contracts(client_id);


CREATE UNIQUE INDEX idx_contract_number
ON inventory.contracts(contract_number);



-- =========================
-- Серверные
-- =========================

CREATE TABLE inventory.rooms (

    id BIGSERIAL PRIMARY KEY,

    name VARCHAR(100) NOT NULL UNIQUE,

    comment TEXT

);



-- =========================
-- Стойки
-- =========================

CREATE TABLE inventory.racks (

    id BIGSERIAL PRIMARY KEY,

    room_id BIGINT NOT NULL,

    rack_number INTEGER NOT NULL,

    height_u INTEGER NOT NULL,


    comment TEXT,


    CONSTRAINT fk_rack_room
        FOREIGN KEY(room_id)
        REFERENCES inventory.rooms(id)
        ON DELETE RESTRICT,


    CONSTRAINT rack_height_check
        CHECK(height_u > 0)

);


CREATE UNIQUE INDEX idx_unique_rack
ON inventory.racks(room_id, rack_number);



-- =========================
-- Оборудование
-- =========================

CREATE TABLE inventory.equipment (

    id BIGSERIAL PRIMARY KEY,


    contract_id BIGINT NOT NULL,


    vendor VARCHAR(100) NOT NULL,

    model VARCHAR(150) NOT NULL,


    serial_number VARCHAR(200) NOT NULL UNIQUE,


    size_u INTEGER,


    placement_type VARCHAR(20),


    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_equipment_contract
        FOREIGN KEY(contract_id)
        REFERENCES inventory.contracts(id)
        ON DELETE RESTRICT,


    CONSTRAINT equipment_size_check
        CHECK(size_u IS NULL OR size_u > 0)

);



CREATE INDEX idx_equipment_serial
ON inventory.equipment(serial_number);


CREATE INDEX idx_equipment_model
ON inventory.equipment(model);


CREATE INDEX idx_equipment_vendor
ON inventory.equipment(vendor);



-- =========================
-- Размещение оборудования
-- =========================

CREATE TABLE inventory.equipment_location (

    id BIGSERIAL PRIMARY KEY,


    equipment_id BIGINT NOT NULL,


    rack_id BIGINT NOT NULL,


    unit_from INTEGER,

    unit_to INTEGER,


    placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    removed_at TIMESTAMP,


    CONSTRAINT fk_location_equipment
        FOREIGN KEY(equipment_id)
        REFERENCES inventory.equipment(id)
        ON DELETE CASCADE,


    CONSTRAINT fk_location_rack
        FOREIGN KEY(rack_id)
        REFERENCES inventory.racks(id)
        ON DELETE RESTRICT,


    CONSTRAINT unit_range_check
        CHECK(
            unit_from IS NULL
            OR unit_to IS NULL
            OR unit_to >= unit_from
        )

);



CREATE INDEX idx_location_equipment
ON inventory.equipment_location(equipment_id);


CREATE INDEX idx_location_rack
ON inventory.equipment_location(rack_id);



-- =========================
-- История операций
-- =========================

CREATE TABLE inventory.equipment_history (

    id BIGSERIAL PRIMARY KEY,


    equipment_id BIGINT NOT NULL,


    operation VARCHAR(50) NOT NULL,


    description TEXT,


    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_history_equipment
        FOREIGN KEY(equipment_id)
        REFERENCES inventory.equipment(id)
        ON DELETE CASCADE

);



CREATE INDEX idx_history_equipment
ON inventory.equipment_history(equipment_id);



-- =========================
-- Текущий вид оборудования
-- =========================

CREATE VIEW inventory.current_equipment_location AS

SELECT

    e.id AS equipment_id,

    e.serial_number,

    r.room_id,

    r.rack_number,

    el.unit_from,

    el.unit_to


FROM inventory.equipment e


JOIN inventory.equipment_location el

ON e.id = el.equipment_id


JOIN inventory.racks r

ON r.id = el.rack_id


WHERE el.removed_at IS NULL;
