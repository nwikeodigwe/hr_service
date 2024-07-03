from sqlalchemy import create_engine

# Replace with your actual connection string
db_uri = 'postgresql://postgres@pg:5432/postgres'

engine = create_engine(db_uri)
try:
    with engine.connect() as connection:
        result = connection.execute('SELECT 1')
        print(result.fetchone())
except Exception as e:
    print(f"Connection failed: {e}")
