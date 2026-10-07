import os
os.environ["DATABASE_URL"]="sqlite://"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base,get_db
from app.main import app
@pytest.fixture()
def client():
    engine=create_engine("sqlite://",connect_args={"check_same_thread":False},poolclass=StaticPool)
    Base.metadata.create_all(engine)
    sessions=sessionmaker(bind=engine)
    def override():
        with sessions() as db: yield db
    app.dependency_overrides[get_db]=override
    with TestClient(app) as test_client: yield test_client
    app.dependency_overrides.clear()
    engine.dispose()
@pytest.fixture()
def asset(client):
    return client.post("/api/assets",json={"asset_tag":"LAB-001","name":"Arduino starter kit","category":"Electronics","total":3}).json()
