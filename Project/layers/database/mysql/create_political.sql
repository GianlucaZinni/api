-- Crear la base de datos Votechain

CREATE DATABASE IF NOT EXISTS Votechain;

-- Usar la base de datos Votechain

USE Votechain;

-- Verificar si la tabla PartidosPoliticos ya existe y, si no existe, créala

CREATE TABLE
    IF NOT EXISTS PartidosPoliticos (
        id INT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        siglas VARCHAR(10),
        fundacion DATE,
        logo_url VARCHAR(255)
    );

-- Insertar datos en la tabla PartidosPoliticos si no existen registros

INSERT
    IGNORE INTO PartidosPoliticos (
        id,
        nombre,
        siglas,
        fundacion,
        logo_url
    )
VALUES (
        1,
        'La Libertad Avanza',
        'LLA',
        '2021-01-01',
        'logo_lla.png'
    ),
    (
        1,
        'Unión por la Patria',
        'UP',
        '2003-01-01',
        'logo_up.png'
    );

-- Verificar si la tabla CandidatosPresiVice ya existe y, si no existe, créala

CREATE TABLE
    IF NOT EXISTS CandidatosPresiVice (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_presidente VARCHAR(255) NOT NULL,
        apellido_presidente VARCHAR(255) NOT NULL,
        nombre_vicepresidente VARCHAR(255),
        apellido_vicepresidente VARCHAR(255),
        partido_id INT,
        foto_url VARCHAR(255),
        FOREIGN KEY (partido_id) REFERENCES PartidosPoliticos(id)
    );

-- Insertar datos en la tabla CandidatosPresiVice si no existen registros

INSERT
    IGNORE INTO CandidatosPresiVice (
        nombre_presidente,
        apellido_presidente,
        nombre_vicepresidente,
        apellido_vicepresidente,
        partido_id,
        foto_url
    )
VALUES (
        'Javier',
        'Milei',
        'Victoria',
        'Villaruel',
        1,
        'milei_villaruel.jpg'
    );

INSERT
    IGNORE INTO CandidatosPresiVice (
        nombre_presidente,
        apellido_presidente,
        nombre_vicepresidente,
        apellido_vicepresidente,
        partido_id,
        foto_url
    )
VALUES (
        'Sergio',
        'Massa',
        'Agustín',
        'Rossi',
        2,
        'massa_rossi.jpg'
    );

-- Verificar si la tabla ListasCandidatos ya existe y, si no existe, créala

CREATE TABLE
    IF NOT EXISTS ListasCandidatos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_lista VARCHAR(255) NOT NULL,
        partido_id INT,
        candidato_presidente_id INT,
        candidato_vicepresidente_id INT,
        FOREIGN KEY (partido_id) REFERENCES PartidosPoliticos(id),
        FOREIGN KEY (candidato_presidente_id) REFERENCES CandidatosPresiVice(id),
        FOREIGN KEY (candidato_vicepresidente_id) REFERENCES CandidatosPresiVice(id)
    );

-- Insertar datos en la tabla ListasCandidatos si no existen registros

INSERT
    IGNORE INTO ListasCandidatos (
        nombre_lista,
        partido_id,
        candidato_presidente_id,
        candidato_vicepresidente_id
    )
VALUES ('135A', 1, 1, 1);

INSERT
    IGNORE INTO ListasCandidatos (
        nombre_lista,
        partido_id,
        candidato_presidente_id,
        candidato_vicepresidente_id
    )
VALUES ('134', 2, 2, 2);