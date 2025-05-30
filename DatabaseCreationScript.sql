/* Script di creazione del database in MySql */

DROP DATABASE SEGRETERIA;

CREATE DATABASE IF NOT EXISTS SEGRETERIA;

USE SEGRETERIA;

CREATE TABLE IF NOT EXISTS STUDENTI (
    MATRICOLA       CHAR(10)       PRIMARY KEY,
    PASSWORD        VARCHAR(256)   NOT NULL,
    EMAIL           VARCHAR(50)    NOT NULL,
    NOMESTUDENTE    VARCHAR(30)    NOT NULL,
    COGNOMESTUDENTE VARCHAR(30)    NOT NULL,
    CFUSTUDENTE     INT            NOT NULL,
    DATANASCITA     DATE           NOT NULL,
    MEDIA           DECIMAL(4, 2)  NOT NULL,
    CORSOSTUDENTE   VARCHAR(30)    NOT NULL,
    CONSTRAINT CHECK_CFU            CHECK(CFUSTUDENTE >= 0),
    CONSTRAINT CHECK_MEDIA          CHECK(MEDIA BETWEEN 18.0 AND 30.0),
    CONSTRAINT CHECK_CORSO_STUDENTE CHECK(LOWER(CORSOSTUDENTE) IN ('informatica', 'economia', 'giurisprudenza', 'biologia', 'ingegneria')),
    CONSTRAINT CHECK_EMAIL          CHECK(EMAIL REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    CONSTRAINT CHECK_NOME           CHECK(NOMESTUDENTE REGEXP '^[A-Za-z]+$'),
    CONSTRAINT CHECK_COGNOME        CHECK(COGNOMESTUDENTE REGEXP '^[A-Za-z ]+$'),
    CONSTRAINT CHECK_MATRICOLA      CHECK(MATRICOLA REGEXP '^[0-9]+$')
);

INSERT INTO STUDENTI (MATRICOLA, PASSWORD, EMAIL, NOMESTUDENTE, COGNOMESTUDENTE, DATANASCITA, CFUSTUDENTE, MEDIA, CORSOSTUDENTE)
VALUES ('0124002667', 'Vittoria_30', 'gaetano.romeo001@studenti.uniparthenope.it', 'Gaetano', 'Romeo', '2003-01-22', 104, 26.8, 'Informatica');

CREATE TABLE IF NOT EXISTS CORSI (
    NOMECORSO     VARCHAR(30) PRIMARY KEY,
    NUMEROESAMI   INT NOT NULL,
    NUMEROCREDITI INT NOT NULL,
    DURATAINANNI  INT NOT NULL,
    CONSTRAINT CHECK_CORSO_ESAME    CHECK(LOWER(NOMECORSO) IN ('informatica', 'economia', 'giurisprudenza', 'machine learning', 'ingegneria')),
    CONSTRAINT CHECK_NUMERO_ESAMI   CHECK(NUMEROESAMI BETWEEN 12 AND 21),
    CONSTRAINT CHECK_NUMERO_CREDITI CHECK(NUMEROCREDITI BETWEEN 120 AND 180),
    CONSTRAINT CHECK_DURATA         CHECK(DURATAINANNI BETWEEN 2 AND 3)
);

INSERT INTO CORSI (NOMECORSO, NUMEROESAMI, NUMEROCREDITI, DURATAINANNI) VALUES ('Informatica', 21, 180, 3);
INSERT INTO CORSI (NOMECORSO, NUMEROESAMI, NUMEROCREDITI, DURATAINANNI) VALUES ('Machine Learning', 12, 120, 2);

CREATE TABLE IF NOT EXISTS ESAMI (
    NOMEESAME  VARCHAR(30),
    NOMECORSO  VARCHAR(30),
    CFUESAME   INT NOT NULL,
    PRIMARY KEY (NOMEESAME, NOMECORSO),
    FOREIGN KEY (NOMECORSO) REFERENCES CORSI (NOMECORSO),
    CONSTRAINT CHECK_CFU_ESAME   CHECK(CFUESAME BETWEEN 3 AND 15)
);

INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Algoritmi e Strutture Dati', 'Informatica', 12);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Sistemi Operativi', 'Informatica', 12);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Architettura dei Calcolatori', 'Informatica', 12);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Programmazione 1', 'Informatica', 12);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Programmazione 2', 'Informatica', 9);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Programmazione 3', 'Informatica', 6);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Matematica 1', 'Informatica', 12);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Matematica 2', 'Informatica', 9);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Economia', 'Informatica', 9);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Ingegneria del Software', 'Informatica', 9);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Reti di Calcolatori', 'Informatica', 9);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Database', 'Informatica', 9);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Calcolo Numerico', 'Informatica', 6);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Calcolo Parallelo', 'Informatica', 9);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Fisica', 'Informatica', 6);
INSERT INTO ESAMI (NOMEESAME, NOMECORSO, CFUESAME) VALUES ('Elaborazione delle Immagini', 'Informatica', 6);

CREATE TABLE IF NOT EXISTS APPELLI (
    NOMEESAME   VARCHAR(30),
    NOMECORSO   VARCHAR(30),
    DATAESAME   DATE NOT NULL,
    FOREIGN KEY (NOMEESAME, NOMECORSO) REFERENCES ESAMI (NOMEESAME, NOMECORSO)
);

INSERT INTO APPELLI (NOMEESAME, NOMECORSO, DATAESAME) VALUES ('Algoritmi e Strutture Dati', 'Informatica', '2023-09-25');
INSERT INTO APPELLI (NOMEESAME, NOMECORSO, DATAESAME) VALUES ('Algoritmi e Strutture Dati', 'Informatica', '2025-09-25');
INSERT INTO APPELLI (NOMEESAME, NOMECORSO, DATAESAME) VALUES ('Sistemi Operativi', 'Informatica', '2025-11-25');

CREATE TABLE IF NOT EXISTS PRENOTA (
    NOMEESAME        VARCHAR(30),
    NOMECORSO        VARCHAR(30),
    MATRICOLA        CHAR(10),
    DATAPRENOTAZIONE DATE NOT NULL,
    PRIMARY KEY (NOMEESAME, NOMECORSO, MATRICOLA),
    FOREIGN KEY (NOMEESAME, NOMECORSO) REFERENCES APPELLI  (NOMEESAME, NOMECORSO),
    FOREIGN KEY (MATRICOLA)            REFERENCES STUDENTI (MATRICOLA)
);

INSERT INTO PRENOTA (NOMEESAME, NOMECORSO, MATRICOLA, DATAPRENOTAZIONE) VALUES ('Algoritmi e Strutture Dati', 'Informatica', '0124002667', '2023-09-01');

CREATE TABLE IF NOT EXISTS SUPERA (
    NOMEESAME  VARCHAR(30),
    NOMECORSO  VARCHAR(30),
    MATRICOLA  CHAR(10),
    VOTO       INT NOT NULL,
    PRIMARY KEY (NOMEESAME, NOMECORSO, MATRICOLA),
    FOREIGN KEY (NOMEESAME, NOMECORSO) REFERENCES APPELLI  (NOMEESAME, NOMECORSO),
    FOREIGN KEY (MATRICOLA)            REFERENCES STUDENTI (MATRICOLA),
    CONSTRAINT CHECK_VOTO CHECK (VOTO BETWEEN 18 AND 30)
);

INSERT INTO SUPERA (NOMEESAME, NOMECORSO, MATRICOLA, VOTO) VALUES ('Algoritmi e Strutture Dati', 'Informatica', '0124002667', 23);