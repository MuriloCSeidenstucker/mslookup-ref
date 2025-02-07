CREATE DATABASE IF NOT EXISTS ms_database;

CREATE TABLE IF NOT EXISTS `ms_database`.`medicines` (
    id BIGINT NOT NULL,
    product VARCHAR(255) NOT NULL,
    substance VARCHAR(255) NOT NULL,
    presentation VARCHAR(255) NOT NULL,
    product_type VARCHAR(255) NOT NULL,
    ean BIGINT NOT NULL,
    cnpj BIGINT NOT NULL,
    laboratorie VARCHAR(255) NOT NULL,
    primary key (id)
);