import json
import logging
import time
import uuid
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from .config import settings
from .db import get_db
from .models import Asset, Loan, now
from .schemas import AssetCreate, AssetOut, AssetUpdate, BorrowCreate, LoanOut
app = FastAPI(title=settings.app_name, version=settings.app_version)
logger = logging.getLogger("uvicorn.error")
Instrumentator(excluded_handlers=["/metrics", "/health", "/ready"]).instrument(app).expose(app)
@app.middleware("http")
async def request_log(request: Request, call_next):
    started = time.monotonic()
    request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)[:100]
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info(json.dumps({"event":"http_request", "method":request.method, "path":request.url.path,
                           "status":response.status_code, "duration_ms":round((time.monotonic()-started)*1000,2),
                           "request_id":request_id, "version":settings.app_version}))
    return response
@app.get("/")
def root():
    return {"service":settings.app_name, "version":settings.app_version, "docs":"/docs"}
@app.get("/health")
def health():
    return {"status":"UP", "version":settings.app_version}
@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1 FROM assets LIMIT 1"))
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database or schema unavailable") from None
    return {"status":"READY"}
@app.get("/api/assets", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return list(db.scalars(select(Asset).order_by(Asset.id)))
@app.get("/api/stats")
def stats(db: Session = Depends(get_db)):
    total, available = db.execute(select(func.coalesce(func.sum(Asset.total),0),func.coalesce(func.sum(Asset.available),0))).one()
    return {"assets":db.scalar(select(func.count(Asset.id))),"total":total,"available":available,
            "on_loan":total-available,"active_loans":db.scalar(select(func.count(Loan.id)).where(Loan.returned_at.is_(None)))}
def locked_asset(db, asset_id):
    asset = db.scalar(select(Asset).where(Asset.id==asset_id).with_for_update())
    if asset is None: raise HTTPException(status_code=404, detail="Asset not found")
    return asset
@app.get("/api/assets/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    return locked_asset(db,asset_id)
@app.post("/api/assets", response_model=AssetOut, status_code=201)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset=Asset(**payload.model_dump(), available=payload.total)
    db.add(asset)
    try: db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Asset tag already exists") from None
    db.refresh(asset)
    return asset
@app.put("/api/assets/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)):
    asset=locked_asset(db,asset_id)
    changes=payload.model_dump(exclude_unset=True)
    if "total" in changes:
        on_loan=asset.total-asset.available
        if changes["total"] < on_loan: raise HTTPException(status_code=409, detail="Stock cannot be lower than units on loan")
        asset.available += changes["total"]-asset.total
    for key,value in changes.items(): setattr(asset,key,value)
    db.commit(); db.refresh(asset)
    return asset
@app.delete("/api/assets/{asset_id}", status_code=204)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset=locked_asset(db,asset_id)
    if db.scalar(select(func.count(Loan.id)).where(Loan.asset_id==asset_id)):
        raise HTTPException(status_code=409, detail="Assets with lending history must be retained")
    db.delete(asset); db.commit()
    return Response(status_code=204)
@app.get("/api/loans", response_model=list[LoanOut])
def list_loans(db: Session = Depends(get_db)):
    return list(db.scalars(select(Loan).order_by(Loan.id.desc())))
@app.post("/api/loans", response_model=LoanOut, status_code=201)
def borrow(payload: BorrowCreate, db: Session = Depends(get_db)):
    asset=locked_asset(db,payload.asset_id)
    if payload.quantity > asset.available: raise HTTPException(status_code=409, detail="Not enough units available")
    asset.available -= payload.quantity
    loan=Loan(**payload.model_dump(),asset_name=asset.name)
    db.add(loan); db.commit(); db.refresh(loan)
    return loan
@app.put("/api/loans/{loan_id}/return", response_model=LoanOut)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    loan=db.scalar(select(Loan).where(Loan.id==loan_id).with_for_update())
    if loan is None: raise HTTPException(status_code=404, detail="Loan not found")
    if loan.returned_at is not None: raise HTTPException(status_code=409, detail="Loan already returned")
    asset=locked_asset(db,loan.asset_id)
    asset.available += loan.quantity
    loan.returned_at=now()
    db.commit(); db.refresh(loan)
    return loan
