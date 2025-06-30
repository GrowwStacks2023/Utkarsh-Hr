import PyMySQL
import ssl
import os

CA_CERT_PATH = os.path.abspath("BaltimoreCyberTrustRoot.crt.pem")
try:
    conn = PyMySQL.connect(
        host='gfydwceabn.mysql.database.azure.com',
        user='mfexyzjecv@gfydwceabn',
        password='shubham_10',
        database='hr-database',
        port=3306,
        ssl={'ca': CA_CERT_PATH}  
    )
    print("✅ Connection successful")
    with conn.cursor() as cursor:
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()
        print("Current Time:", result[0])
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
