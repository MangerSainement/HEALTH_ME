import cx_Oracle
from translate import Translator

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

# symptome = 'Mal de tête'
#
# query_CodeS = f"""
#                 select CodeS
#                 from SYMPTOMES
#                 where NOMS = '{symptome}'
#             """
#
# CodeS = execute_query(query_CodeS)
# CodeS = CodeS[0][0]
# print(CodeS)
#
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

translator = Translator(from_lang='french', to_lang='english')
translation = translator.translate("Bonjour")
print(translation)
