create table ATTRIBUTER
(
    CODEA NUMBER
        references ALIMENTS,
    IDR   NUMBER
        references RECETTE,
    QTEA  NUMBER
)
/

