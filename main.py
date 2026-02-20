import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Liberar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

class Lead(BaseModel):
    nome: str
    email: str
    telefone: str
    perfil: str
    investimento: str

# 👇 AQUI FAZ ABRIR O INDEX NO ROOT
@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.post("/cadastro")
def cadastrar_lead(lead: Lead):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO leads_workshop (nome, email, telefone, perfil, investimento)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            lead.nome,
            lead.email,
            lead.telefone,
            lead.perfil,
            lead.investimento
        ))

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "success"}

    except Exception as e:
        return {"status": "error", "message": str(e)}