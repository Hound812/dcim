from app.database import engine

try:
    connection = engine.connect()
    print("PostgreSQL OK")
    connection.close()

except Exception as e:
    print(e)
