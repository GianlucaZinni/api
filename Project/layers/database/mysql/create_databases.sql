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

-- Crear la base de datos Votechain

CREATE DATABASE IF NOT EXISTS Votechain;

-- Usar la base de datos Votechain

USE Votechain;

-- Verificar si la tabla CandidatosPresiVice ya existe y, si no existe, créala

CREATE TABLE
    IF NOT EXISTS CandidatosPresiVice (
        candidatos_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_presidente VARCHAR(255) NOT NULL,
        apellido_presidente VARCHAR(255) NOT NULL,
        nombre_vicepresidente VARCHAR(255),
        apellido_vicepresidente VARCHAR(255),
        foto_url VARCHAR(255)
    );

-- Insertar datos en la tabla CandidatosPresiVice si no existen registros

INSERT
    IGNORE INTO CandidatosPresiVice (
        candidatos_id,
        nombre_presidente,
        apellido_presidente,
        nombre_vicepresidente,
        apellido_vicepresidente,
        foto_url
    )
VALUES (
        1,
        'Javier',
        'Milei',
        'Victoria',
        'Villaruel',
        'milei_villaruel.jpg'
    ), (
        2,
        'Sergio',
        'Massa',
        'Agustín',
        'Rossi',
        'massa_rossi.jpg'
    );

-- Verificar si la tabla PartidosPoliticos ya existe y, si no existe, créala

CREATE TABLE
    IF NOT EXISTS PartidoPolitico (
        partido_id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        siglas VARCHAR(10),
        fundacion DATE,
        logo_url VARCHAR(255),
        candidatos_id INT,
        FOREIGN KEY (candidatos_id) REFERENCES CandidatosPresiVice(candidatos_id)
    );

-- Insertar datos en la tabla PartidosPoliticos si no existen registros

INSERT
    IGNORE INTO PartidoPolitico (
        partido_id,
        nombre,
        siglas,
        fundacion,
        logo_url,
        candidatos_id
    )
VALUES (
        1,
        'La Libertad Avanza',
        'LLA',
        '2021-01-01',
        'logo_lla.png',
        1
    ), (
        2,
        'Unión por la Patria',
        'UP',
        '2003-01-01',
        'logo_up.png',
        2
    );