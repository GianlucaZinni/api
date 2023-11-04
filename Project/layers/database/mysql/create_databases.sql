-- Crear la base de datos Votechain

CREATE DATABASE IF NOT EXISTS Votechain;

-- Usar la base de datos Votechain

USE Votechain;

-- Tabla google_user

CREATE TABLE
    IF NOT EXISTS google_user (
        id_google VARCHAR(255) PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        verified_email TINYINT(1) NOT NULL,
        picture VARCHAR(255),
        UNIQUE KEY (email)
    );

-- Tabla votechain_user

CREATE TABLE
    IF NOT EXISTS votechain_user (
        DNI BIGINT PRIMARY KEY,
        id_google VARCHAR(255),
        nombre VARCHAR(255) NOT NULL,
        apellido VARCHAR(255) NOT NULL,
        telefono VARCHAR(15) NOT NULL,
        nro_tramite BIGINT,
        tries INT NOT NULL, 
        FOREIGN KEY (id_google) REFERENCES google_user(id_google),
        UNIQUE KEY (DNI)
    );

-- Tabla Email_Verification

CREATE TABLE
    IF NOT EXISTS Email_Verification (
        id_google VARCHAR(255),
        DNI BIGINT,
        code INT NOT NULL,
        expiration_time DATETIME NOT NULL,
        tries INT NOT NULL,
        FOREIGN KEY (id_google) REFERENCES google_user(id_google),
        FOREIGN KEY (DNI) REFERENCES votechain_user(DNI)
    );

-- Configurar el valor predeterminado para el campo 'expiration_time' en Email_Verification

ALTER TABLE
    Email_Verification MODIFY expiration_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- Tabla Auditory

CREATE TABLE
    IF NOT EXISTS Auditory (
        DNI BIGINT,
        enabled BOOLEAN,
        enabled_date DATETIME,
        vote BOOLEAN,
        vote_date DATETIME,
        FOREIGN KEY (DNI) REFERENCES votechain_user(DNI)
    );

-- Crear la base de datos RENAPER

CREATE DATABASE IF NOT EXISTS RENAPER;

-- Usar la base de datos RENAPER

USE RENAPER;

-- Tabla Padrón

CREATE TABLE
    IF NOT EXISTS Padron (
        DNI BIGINT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        apellido VARCHAR(255) NOT NULL,
        nro_tramite BIGINT NOT NULL,
        valid TINYINT(1) NOT NULL
    );