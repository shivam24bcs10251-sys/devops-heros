"""Wait for the single migration Job; app replicas do not race to migrate."""
import os,time
from sqlalchemy import create_engine,text
engine=create_engine(os.environ['DATABASE_URL'],pool_pre_ping=True)
for attempt in range(120):
    try:
        with engine.connect() as connection:
            connection.execute(text('SELECT 1 FROM assets LIMIT 1'))
        print('Database schema ready',flush=True)
        break
    except Exception:
        time.sleep(2)
else: raise SystemExit('Database schema did not become ready')
