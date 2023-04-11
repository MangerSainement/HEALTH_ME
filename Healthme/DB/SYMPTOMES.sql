create table SYMPTOMES
(
    CODES NUMBER generated as identity
        constraint SYMPTOMES_PK
            primary key,
    NOMS  NVARCHAR2(50)
)
/

