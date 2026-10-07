import pytest
def test_health(client):
    assert client.get("/health").json()["status"]=="UP"
def test_service_identity(client):
    assert client.get("/").json()["service"]=="LabLedger API"
def test_ready_checks_schema(client):
    assert client.get("/ready").status_code==200
def test_metrics(client):
    client.get("/api/assets")
    assert "http_requests_total" in client.get("/metrics").text
def test_asset_create_and_read(client,asset):
    assert asset["available"]==3
    assert client.get(f'/api/assets/{asset["id"]}').json()["name"]=="Arduino starter kit"
    assert len(client.get("/api/assets").json())==1
def test_duplicate_tag(client,asset):
    assert client.post("/api/assets",json={"asset_tag":"LAB-001","name":"Duplicate","category":"Electronics","total":1}).status_code==409
@pytest.mark.parametrize("change",[{"total":0},{"asset_tag":"invalid tag"},{"name":""}])
def test_invalid_asset(client,change):
    payload={"asset_tag":"LAB-002","name":"Kit","category":"Tools","total":1,**change}
    assert client.post("/api/assets",json=payload).status_code==422
def test_borrow_reduces_stock(client,asset):
    loan=client.post("/api/loans",json={"asset_id":asset["id"],"borrower":"Demo Student","quantity":2})
    assert loan.status_code==201
    assert client.get(f'/api/assets/{asset["id"]}').json()["available"]==1
    assert client.get("/api/stats").json()["on_loan"]==2
def test_over_borrow_is_rejected(client,asset):
    assert client.post("/api/loans",json={"asset_id":asset["id"],"borrower":"Demo","quantity":4}).status_code==409
    assert client.get(f'/api/assets/{asset["id"]}').json()["available"]==3
def test_return_restores_stock_once(client,asset):
    loan=client.post("/api/loans",json={"asset_id":asset["id"],"borrower":"Demo","quantity":2}).json()
    assert client.put(f'/api/loans/{loan["id"]}/return').status_code==200
    assert client.put(f'/api/loans/{loan["id"]}/return').status_code==409
    assert client.get(f'/api/assets/{asset["id"]}').json()["available"]==3
    assert client.get("/api/loans").json()[0]["returned_at"] is not None
def test_stock_edit_preserves_outstanding_loans(client,asset):
    client.post("/api/loans",json={"asset_id":asset["id"],"borrower":"Demo","quantity":2})
    path=f'/api/assets/{asset["id"]}'
    assert client.put(path,json={"total":1}).status_code==409
    assert client.put(path,json={"total":5,"name":"Updated kit"}).json()["available"]==3
def test_explicit_null_rejected(client,asset):
    assert client.put(f'/api/assets/{asset["id"]}',json={"name":None}).status_code==422
def test_delete_unused_asset(client,asset):
    assert client.delete(f'/api/assets/{asset["id"]}').status_code==204
    assert client.get(f'/api/assets/{asset["id"]}').status_code==404
def test_lending_history_cannot_be_deleted(client,asset):
    loan=client.post("/api/loans",json={"asset_id":asset["id"],"borrower":"Demo"}).json()
    client.put(f'/api/loans/{loan["id"]}/return')
    assert client.delete(f'/api/assets/{asset["id"]}').status_code==409
@pytest.mark.parametrize("method,path",[("get","/api/assets/999"),("put","/api/loans/999/return"),("delete","/api/assets/999")])
def test_missing_records(client,method,path):
    assert getattr(client,method)(path).status_code==404
def test_request_correlation(client):
    assert client.get("/health",headers={"X-Request-ID":"test-request-21"}).headers["X-Request-ID"]=="test-request-21"
