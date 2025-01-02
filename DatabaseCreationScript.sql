/* Script di creazione del database in MySql */

DROP DATABASE SEGRETERIA;

CREATE DATABASE IF NOT EXISTS SEGRETERIA;

USE SEGRETERIA;

CREATE TABLE IF NOT EXISTS STUDENTI (
    MATRICOLA     CHAR(10)    PRIMARY KEY,
    PASSWORD      VARCHAR(256)   NOT NULL,
    CFUSTUDENTE   INT            NOT NULL,
    MEDIA         DECIMAL(4, 2)  NOT NULL,
    CONSTRAINT CHECK_MEDIA CHECK(MEDIA BETWEEN 18.0 AND 30.0)
);

INSERT INTO STUDENTI (MATRICOLA, PASSWORD, CFUSTUDENTE, MEDIA) VALUES ('0124002667', 'Vittoria_30', 104, 26.8);

CREATE TABLE IF NOT EXISTS ESAMI (
    NOMEESAME VARCHAR(30),
    CORSO     VARCHAR(30),
    CFUESAME  INT NOT NULL,
    PRIMARY KEY (NOMEESAME, CORSO),
    CONSTRAINT CHECK_CFU_ESAME CHECK(CFUESAME BETWEEN 3 AND 15)
);

INSERT INTO ESAMI (NOMEESAME, CORSO, CFUESAME) VALUES ('Algoritmi e Strutture Dati', 'Informatica', 12);

CREATE TABLE IF NOT EXISTS APPELLI (
    NOMEESAME VARCHAR(30),
    CORSO     VARCHAR(30),
    DATAESAME DATE NOT NULL,
    FOREIGN KEY (NOMEESAME, CORSO) REFERENCES ESAMI (NOMEESAME, CORSO)
);

INSERT INTO APPELLI (NOMEESAME, CORSO, DATAESAME) VALUES ('Algoritmi e Strutture Dati', 'Informatica', '2023-09-25');

CREATE TABLE IF NOT EXISTS PRENOTA (
    NOMEESAME        VARCHAR(30),
    CORSO            VARCHAR(30),
    MATRICOLA        CHAR(10),
    DATAPRENOTAZIONE DATE NOT NULL,
    PRIMARY KEY (NOMEESAME, CORSO, MATRICOLA),
    FOREIGN KEY (NOMEESAME, CORSO) REFERENCES APPELLI (NOMEESAME, CORSO),
    FOREIGN KEY (MATRICOLA)        REFERENCES STUDENTI (MATRICOLA)
);

CREATE TABLE IF NOT EXISTS SUPERA (
    NOMEESAME VARCHAR(30),
    CORSO     VARCHAR(30),
    MATRICOLA CHAR(10),
    VOTO INT NOT NULL,
    PRIMARY KEY (NOMEESAME, CORSO, MATRICOLA),
    FOREIGN KEY (NOMEESAME, CORSO) REFERENCES APPELLI (NOMEESAME, CORSO),
    FOREIGN KEY (MATRICOLA)        REFERENCES STUDENTI (MATRICOLA),
    CONSTRAINT CHECK_VOTO CHECK (VOTO BETWEEN 18.0 AND 30.0)
);

INSERT INTO SUPERA (NOMEESAME, CORSO, MATRICOLA, VOTO) VALUES ('Algoritmi e Strutture Dati', 'Informatica', '0124002667', 23);