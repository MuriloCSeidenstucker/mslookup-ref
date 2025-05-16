CREATE DATABASE IF NOT EXISTS ms_database;

CREATE TABLE IF NOT EXISTS `ms_database`.`laboratories` (
    laboratory_id BIGINT NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    cnpj VARCHAR(14) NOT NULL,
    alt_names JSON NOT NULL,
    linked JSON,
    PRIMARY KEY (laboratory_id),
    UNIQUE (cnpj)
);

CREATE TABLE IF NOT EXISTS `ms_database`.`medicines` (
    medicine_id BIGINT NOT NULL,
    product VARCHAR(255) NOT NULL,
    substance VARCHAR(255) NOT NULL,
    presentation VARCHAR(255) NOT NULL,
    product_type VARCHAR(255) NOT NULL,
    ean BIGINT NOT NULL,
    laboratory_id BIGINT NOT NULL,
    PRIMARY KEY (medicine_id),
    FOREIGN KEY (laboratory_id) REFERENCES `ms_database`.`laboratories`(laboratory_id)
);