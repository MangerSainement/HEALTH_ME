create table CLIENT
(
    CODEC            NUMBER generated as identity
        constraint CLIENT_PK
            primary key,
    PSEUDO           NVARCHAR2(50),
    SEXE             NVARCHAR2(5)
        check (Sexe in ('H', 'F')),
    DATEANNIVERSAIEC DATE,
    EMAILC           NVARCHAR2(100),
    MOTDEPASSE       NVARCHAR2(100),
    STORED_SALT      NVARCHAR2(100)
)
/

INSERT INTO C##PH.CLIENT (CODEC, PSEUDO, SEXE, DATEANNIVERSAIEC, EMAILC, MOTDEPASSE, STORED_SALT) VALUES (11, 'PH', 'H', DATE '1999-02-09', 'panghanfr@gmail.com', '$2b$12$6m0hCMKrw7KMxoDXkPG8QenlR8CFnGljIu1CepGhNXhVob6dFmLT2', '$2b$12$6m0hCMKrw7KMxoDXkPG8Qe');
