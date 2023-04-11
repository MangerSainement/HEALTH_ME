create table CONTENIR
(
    CODEA NUMBER
        references ALIMENTS,
    CODEM NUMBER
        references MINERAUX,
    QTEM  FLOAT
)
/

