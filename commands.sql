-- Oszlopok atnevezese
ALTER TABLE "adagok"
RENAME COLUMN "ADAGSZÁM" TO "adagszam";
ALTER TABLE "adagok"
RENAME COLUMN "ADAGIDŐ" TO "adagido";
ALTER TABLE "adagok"
RENAME COLUMN "Kezdet" TO "kezdet";
ALTER TABLE "adagok"
RENAME COLUMN "Vége" TO "vege";
ALTER TABLE "adagok"
RENAME COLUMN "Adagkozi_ido" TO "adagkozi_ido";

-- Elsodleges kulcs hozzaadasa
CREATE TABLE "new_adagok" (
"adagszam" INTEGER PRIMARY KEY,
  "adagido" REAL,
  "kezdet" TIMESTAMP,
  "vege" TIMESTAMP,
  "adagkozi_ido" REAL
);
INSERT INTO "new_adagok" (adagszam, adagido, kezdet, vege, adagkozi_ido)
SELECT adagszam, adagido, kezdet, vege, adagkozi_ido FROM adagok;
DROP TABLE adagok;
ALTER TABLE "new_adagok" RENAME TO "adagok";

-- Idegen kulcs hozzaadas
CREATE TABLE "new_panel1" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel1" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel1";
DROP TABLE "panel1";
ALTER TABLE "new_panel1" RENAME TO "panel1";

CREATE TABLE "new_panel2" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel2" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel2";
DROP TABLE "panel2";
ALTER TABLE "new_panel2" RENAME TO "panel2";

CREATE TABLE "new_panel3" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel3" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel3";
DROP TABLE "panel3";
ALTER TABLE "new_panel3" RENAME TO "panel3";

CREATE TABLE "new_panel4" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel4" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel4";
DROP TABLE "panel4";
ALTER TABLE "new_panel4" RENAME TO "panel4";

CREATE TABLE "new_panel5" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel5" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel5";
DROP TABLE "panel5";
ALTER TABLE "new_panel5" RENAME TO "panel5";

CREATE TABLE "new_panel6" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel6" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel6";
DROP TABLE "panel6";
ALTER TABLE "new_panel6" RENAME TO "panel6";

CREATE TABLE "new_panel7" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel7" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel7";
DROP TABLE "panel7";
ALTER TABLE "new_panel7" RENAME TO "panel7";

CREATE TABLE "new_panel8" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel8" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel8";
DROP TABLE "panel8";
ALTER TABLE "new_panel8" RENAME TO "panel8";

CREATE TABLE "new_panel9" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel9" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel9";
DROP TABLE "panel9";
ALTER TABLE "new_panel9" RENAME TO "panel9";

CREATE TABLE "new_panel10" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel10" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel10";
DROP TABLE "panel10";
ALTER TABLE "new_panel10" RENAME TO "panel10";

CREATE TABLE "new_panel11" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel11" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel11";
DROP TABLE "panel11";
ALTER TABLE "new_panel11" RENAME TO "panel11";

CREATE TABLE "new_panel12" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel12" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel12";
DROP TABLE "panel12";
ALTER TABLE "new_panel12" RENAME TO "panel12";

CREATE TABLE "new_panel13" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel13" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel13";
DROP TABLE "panel13";
ALTER TABLE "new_panel13" RENAME TO "panel13";

CREATE TABLE "new_panel14" (
    "time" TIMESTAMP,
    "value" REAL,
    "adagszam" INTEGER,
    FOREIGN KEY ("adagszam") REFERENCES "adagok"("adagszam")
);
INSERT INTO "new_panel14" (time, value, adagszam)
SELECT time, value, adagszam FROM "panel14";
DROP TABLE "panel14";
ALTER TABLE "new_panel14" RENAME TO "panel14";

-- This is the adatb_init.db file


-- Szeretnenk latni 10 olyan merest az 1. panel es a 2. panel mereseibol,
-- ami a 13-as adagbol szarmazik. Kivancsiak vagyunk a kezdet es veg idokre,
-- hogy ellenorizzuk, megfelelo volt az adagszam hozzarendeles
SELECT 
    p1.time AS time1, p1.value AS value1, p1.adagszam,
    p2.time AS time2, p2.value AS value2,
    a.adagido, a.kezdet, a.vege, a.adagszam
FROM 
    panel1 p1
JOIN 
    panel2 p2 ON p1.adagszam = p2.adagszam
JOIN 
    adagok a ON p1.adagszam = a.adagszam
WHERE 
    a.adagszam = 13
ORDER BY 
    p1.time
LIMIT 10;

-- Indexek

CREATE INDEX idx_adagok_adagszam ON adagok (adagszam);
CREATE INDEX idx_panel1_adagszam ON panel1 (adagszam);
CREATE INDEX idx_panel2_adagszam ON panel2 (adagszam);
-- Ezek gyorsaitjak a joinokat 
CREATE INDEX idx_panel1_time ON panel1 (time);
CREATE INDEX idx_panel2_time ON panel2 (time);
-- Ezek gyorsitjak az ido alapu szureseket
CREATE INDEX idx_panel1_time_adagszam ON panel1 (time, adagszam);
CREATE INDEX idx_panel2_time_adagszam ON panel2 (time, adagszam);
-- Ha olyan lekerdezesek vannak, ahol az ido es az adagszam egyszerre szerepel
CREATE INDEX idx_adagok_adagido ON adagok (adagido);
CREATE INDEX idx_adagok_kezdet ON adagok (kezdet);
CREATE INDEX idx_adagok_vege ON adagok (vege);

-- Allekerdezesek
-- Keressuk a panel1 meresek kozul a legnagyobb erteket azok kozul a meresek kozul,
-- aminek adagideje nagyobb mint 100
SELECT max(value)
FROM panel1
WHERE adagszam IN (SELECT adagszam FROM adagok WHERE adagido > 100);

-- JOIN
SELECT p1.time, p1.value, p1.adagszam
FROM panel1 p1
WHERE p1.time = (
    SELECT MAX(p2.time)
    FROM panel1 p2
    WHERE p2.adagszam = p1.adagszam
);

-- UNION

-- INSERT + elozo lekerdezesek

