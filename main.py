# FastAPI giriş noktası
from fastapi import FastAPI, Request, Header, HTTPException, Depends
from db import get_db, create_tables, add_log, get_logs, get_log_by_id, add_news, get_stored_news
from models import LogCreate, Log, News, NewsStored
from utils import fetch_cryptopanic_news
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ATLAS_KEY = os.getenv("ATLAS_KEY")

# Güvenlik kontrolü
def verify_key(x_atlas_key: str = Header(...)):
    if x_atlas_key != ATLAS_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "Atlas Trader API'ye hoş geldiniz!"}

@app.get("/about")
def about():
    return {"project": "Atlas Trader", "description": "Log ve CryptoPanic haber API'si"}

@app.post("/logs", dependencies=[Depends(verify_key)])
def create_log(log: LogCreate):
    log_id = add_log(log)
    return {"id": log_id, "message": "Log kaydedildi."}

@app.get("/logs", response_model=list[Log], dependencies=[Depends(verify_key)])
def list_logs():
    return get_logs()

@app.get("/logs/{id}", response_model=Log, dependencies=[Depends(verify_key)])
def get_log(id: int):
    log = get_log_by_id(id)
    if not log:
        raise HTTPException(status_code=404, detail="Log bulunamadı.")
    return log

@app.get("/news", dependencies=[Depends(verify_key)])
def fetch_news():
    news_list = fetch_cryptopanic_news()
    add_news(news_list)
    return {"count": len(news_list), "message": "Haberler çekildi ve kaydedildi."}

@app.get("/news/stored", response_model=list[NewsStored], dependencies=[Depends(verify_key)])
def stored_news():
    return get_stored_news()
