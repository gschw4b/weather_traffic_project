CREATE DATABASE IF NOT EXISTS zebrinha_azul;

USE zebrinha_azul;

CREATE TABLE IF NOT EXISTS clima (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cidade VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    temperatura FLOAT,
    sensacao_termica FLOAT,
    temperatura_min FLOAT,
    temperatura_max FLOAT,
    `date` DATETIME
);

CREATE TABLE IF NOT EXISTS trafego (
    id INT PRIMARY KEY AUTO_INCREMENT,
    endereco_origem VARCHAR(100),
    origem_lat DECIMAL(9,6),
    origem_lon DECIMAL(9,6),
    endereco_destino VARCHAR(100),
    destino_lat DECIMAL(9,6),
    destino_lon DECIMAL(9,6),
    distancia_km INT,
    duracao VARCHAR(40)
);