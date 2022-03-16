CREATE TABLE Bruker (
    Epost VARCHAR(64) NOT NULL,
    Passord VARCHAR(64) NOT NULL,
    Fornavn VARCHAR(30) NOT NULL,
    Etternavn VARCHAR(30) NOT NULL,
    CONSTRAINT Bruker_PK PRIMARY KEY (Epost)
);

CREATE TABLE FerdigbrentKaffe (
    ID INTEGER NOT NULL,
    Navn VARCHAR(30) NOT NULL,
    Dato DATE NOT NULL,
    Beskrivelse TEXT,
    Brenningsgrad VARCHAR(30),
    Kilopris FLOAT(24),
    KaffepartiID INTEGER NOT NULL,
    KaffebrenneriID INTEGER NOT NULL,
    CONSTRAINT FerdigbrentKaffe_PK PRIMARY KEY (ID),
    CONSTRAINT FerdigbrentKaffe_FK1 FOREIGN KEY (KaffepartiID) REFERENCES Kaffeparti(ID),
    CONSTRAINT FerdigbrentKaffe_FK2 FOREIGN KEY (KaffebrenneriID) REFERENCES Kaffebrenneri(ID)
);

CREATE TABLE Kaffesmaking (
    BrukerEpost VARCHAR(64) NOT NULL,
    FerdigbrentKaffeID INTEGER NOT NULL,
    Smaksnotater TEXT,
    AntallPoeng SMALLINT NOT NULL,
    Smaksdato DATE NOT NULL,
    CONSTRAINT Kaffesmaking_PK PRIMARY KEY (BrukerEpost, FerdigbrentKaffeID),
    CONSTRAINT Kaffesmaking_FK1 FOREIGN KEY (BrukerEpost) REFERENCES Bruker(Epost)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT Kaffesmaking_FK2 FOREIGN KEY (FerdigbrentKaffeID) REFERENCES FerdigbrentKaffe(ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Kaffebrenneri (
    ID INTEGER NOT NULL,
    Navn VARCHAR(30) NOT NULL,
    Lokasjon VARCHAR(30)  NOT NULL,
    CONSTRAINT Kaffebrenneri_PK PRIMARY KEY (ID)
);

CREATE TABLE Kaffeparti (
    ID INTEGER NOT NULL,
    Innhøstingsår YEAR,
    Betalt FLOAT(24),
    GårdID INTEGER NOT NULL,
    ForedlingsmetodeNavn VARCHAR(30) NOT NULL,
    CONSTRAINT Kaffeparti_PK PRIMARY KEY (ID),
    CONSTRAINT Kaffeparti_FK1 FOREIGN KEY (GårdID) REFERENCES Gård(ID),
    CONSTRAINT Kafeparti_FK2 FOREIGN KEY (ForedlingsmetodeNavn) REFERENCES Foredlingsmetode(Navn)
);

CREATE TABLE Foredlingsmetode (
    Navn VARCHAR(30) NOT NULL,
    Beskrivelse TEXT,
    CONSTRAINT Foredlingsmetode_PK PRIMARY KEY (Navn)
);

CREATE TABLE Gård (
    ID INTEGER NOT NULL,
    Navn VARCHAR(30),
    HøydeOverHavet FLOAT(24) NOT NULL,
    Region VARCHAR(30) NOT NULL,
    Land VARCHAR(30) NOT NULL,
    CONSTRAINT Gård_PK PRIMARY KEY (ID)
);

CREATE TABLE Kaffebønne (
    Art VARCHAR(30) NOT NULL,
    Navn VARCHAR(30),
    CONSTRAINT Kaffebønne_PK PRIMARY KEY (Art)
);

CREATE TABLE DyrketKaffebønne (
    Art VARCHAR(30) NOT NULL,
    GårdID INTEGER NOT NULL,
    KaffepartiID INTEGER NOT NULL,
    CONSTRAINT DyrketKaffebønne_PK PRIMARY KEY (Art, GårdID, KaffepartiID),
    CONSTRAINT DyrketKaffebønne_FK1 FOREIGN KEY (Art) REFERENCES Kaffebønne(Art)
    CONSTRAINT DyrketKaffebønne_FK2 FOREIGN KEY (GårdID) REFERENCES Gård(ID)
    CONSTRAINT DyrketKaffebønne_FK3 FOREIGN KEY (KaffepartiID) REFERENCES Kaffeparti(ID)
);

/*Brukerhistorie 1*/
INSERT INTO Kaffebønne (Art,Navn)
VALUES ("Coffea Arabica", "Bourbon"),
("Coffea Robusta", "Robusta"),
("Coffea Liberica", "Liberica");

INSERT INTO Foredlingsmetode (Navn, Beskrivelse)
VALUES ("Bærtørket", "Hele Kaffebæret tørkes. 
Med denne prosesseringen fjernes verken skallet eller fruktkjøttet før tørking. 
Denne prosesseringen gir ofte mer fyldige kaffe med stor munnfølelse. Denne prosesseringen kalles også for Natural.");

INSERT INTO Gård (Navn, HøydeOverHavet, Region, Land)
Values ("Nombre de Dios", 1500, "Santa Ana", "El Salvador");

INSERT INTO Kaffeparti(Innhøstingsår, Betalt, GårdID, ForedlingsmetodeNavn)
VALUES (2021, 8, (SELECT ID from Gård WHERE Navn='Nombre de Dios') , "Bærtørket");

INSERT INTO DyrketKaffebønne (Art, GårdID, KaffepartiID)
VALUES ("Coffea Arabica",
(SELECT ID from Gård WHERE Navn='Nombre de Dios'),
(SELECT ID from Kaffeparti  WHERE (Innhøstingsår=2021 and Betalt=8)));

INSERT INTO Kaffebrenneri(Navn, Lokasjon)
VALUES ("Jacobsen & Svart", "Trondheim");

INSERT INTO FerdigbrentKaffe(Navn, Dato, Beskrivelse, Brenningsgrad, Kilopris, KaffepartiID, KaffebrenneriID)
VALUES ("Vinterkaffe 2022", "2022-01-20", "En velsmakende og kompleks kaffe for mørketiden", "Lys", 600, 
(SELECT ID from Kaffeparti WHERE (Innhøstingsår=2021 and Betalt=8)),
(SELECT ID from Kaffebrenneri WHERE (Navn="Jacobsen & Svart" and Lokasjon="Trondheim")));