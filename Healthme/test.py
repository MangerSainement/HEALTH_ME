import bcrypt
import cx_Oracle


# from translate import Translator


def connect_to_db():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
    conn = cx_Oracle.connect(user='C##PH', password='123456', dsn=dsn_tns)
    print('Connecting to database')
    return conn


def execute_query(query):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute(query)
    res = c.fetchall()
    conn.commit()
    conn.close()
    print('Executing query')
    return res


def execute_insert(query):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    print('insert!')


# query_GetCodeA = f"""
#                 select CodeA
#                 from ALIMENTS
#                 where NOMA = {allergie}
#             """
#
# CodeA = execute_query(query_GetCodeA)

# symptome = 'Fatigue'
#
# query_CodeS = f"""
#                 select CodeS
#                 from SYMPTOMES
#                 where NOMS = '{symptome}'
#             """
#
# CodeS = execute_query(query_CodeS)
# print(CodeS)
# CodeS = CodeS[0][0]
# print(CodeS)
# #
# email = 'panghanfr@gmail.com'
# query_GetCodeC = f"""
#                 select CodeC
#                 from client
#                 where EMAILC = '{email}'
#             """
#
# CodeC = execute_query(query_GetCodeC)
# CodeC = CodeC[0][0]
#
# query_Avoir = f"""
#                 insert into AVOIR(CodeC, CodeS)
#                 values ({CodeC}, {CodeS})
#             """
#
# execute_insert(query_Avoir)

# translator = Translator(from_lang='french', to_lang='english')
# translation = translator.translate("Bonjour")
# print(translation)

# CodeS = 10
# query_MinerauxSoulager = f"""
#             select MINERAUX.CODEM
#             from SOULAGER, MINERAUX
#             where SOULAGER.CODEM = MINERAUX.CODEM
#             and CodeS = {CodeS}
# """
#
# res1 = execute_query(query_MinerauxSoulager)
#
# print(res1)
#
# symptome = 'Fatigue'
# query_MinerauxSoulager = f'''
#                    select MINERAUX.CODEM, MINERAUX.NOMM
#                    from SOULAGER, MINERAUX, SYMPTOMES
#                    where SOULAGER.CODEM = MINERAUX.CODEM
#                    and SYMPTOMES.CODES = SOULAGER.CODES
#                    and NomS = '{symptome}'
#                '''
#
# res3 = execute_query(query_MinerauxSoulager)
#
# print(res3)
#
# CodeM = 18
# query2 = f"""
#     SELECT ALIMENTS.CodeA, NOMA, QTEM
#     FROM MINERAUX, CONTENIR, ALIMENTS
#     WHERE MINERAUX.CODEM = CONTENIR.CODEM
#     AND CONTENIR.CODEA = ALIMENTS.CODEA
#     AND MINERAUX.CODEM = {CodeM}
#     AND ROWNUM <= 10
#     ORDER BY QTEM DESC
# """
#
# res111 = execute_query(query2)
# print(res111[0][1])

# email = 'superf@gmail.com'
# query_infoCLi = f"""
#        select CODEC, PSEUDO, SEXE, DATEANNIVERSAIEC, EMAILC
#        from CLIENT
#        where EMAILC = '{email}'
#    """
#
# infoCli = execute_query(query_infoCLi)
# infoCli = infoCli[0]
#
# infoCLI_dict = {
#     "CodeCli": infoCli[0],
#     "Pseudo": infoCli[1],
#     "gendre": infoCli[2],
#     "DtNaissance": infoCli[3].strftime('%d-%m-%Y'),  # 格式化日期
#     "email": infoCli[4],
# }
#
# print(infoCLI_dict)

# nouveau_pseudo = 'PH007'
# email = 'dssdfsdf@gmail.com'
# query_pseudo_changement = f"""
#                 update CLIENT
#                 set PSEUDO = '{nouveau_pseudo}'
#                 where EMAILC = '{email}'
#              """
#
# execute_insert(query_pseudo_changement)
#
# query_pseudo_verification = f"""
#                 select PSEUDO
#                 from CLIENT
#                 where EMAILC = '{email}'
#             """
#
# res_verification = execute_query(query_pseudo_verification)
#
# print(res_verification)

nouveau_mdp = '123456'
email = '123456@gmail.com'

# creer "salt"
salt = bcrypt.gensalt()

# crypter le mot de passe
hashed_password = bcrypt.hashpw(nouveau_mdp.encode('utf-8'), salt)

# Conversion de chaînes binaires en chaînes
hashed_password = hashed_password.decode('utf-8')
salt = salt.decode('utf-8')

# Update password
query_MDP_changement = f"""
    update CLIENT
    set MOTDEPASSE = '{hashed_password}', STORED_SALT = '{salt}'
    where EMAILC = '{email}'  
"""

execute_insert(query_MDP_changement)

# verification MDP
query_MDP_verification = f"""
    select MOTDEPASSE
    from CLIENT
    where EMAILC = '{email}'
"""

res_MDP_verification = execute_query(query_MDP_verification)
if res_MDP_verification[0][0] == hashed_password:
    message_MDP = 'Votre mot de pass a été modifié !'
else:
    message_MDP = 'Veuillez réessayer de changer mot de pass !'

print(message_MDP)