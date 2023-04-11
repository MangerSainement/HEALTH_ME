create table AVOIR
(
    CODEC NUMBER
        references CLIENT,
    CODES NUMBER
        references SYMPTOMES
)
/

