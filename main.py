from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# ⚠️ CONFIRA SE A PORTA É 6543 NO SEU SUPABASE
DATABASE_URL = "postgresql://postgres.fkpnzuygmqdbfsrxhmdg:Alme%24202510M**--@aws-1-sa-east-1.pooler.supabase.com:54332/postgres"

# 🔓 LIBERAR CORS (IMPORTANTE PARA FUNCIONAR NO FRONTEND)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois podemos restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lead(BaseModel):
    nome: str
    email: str
    telefone: str
    perfil: str
    investimento: str

@app.get("/")
def home():
    return {"status": "API rodando"}

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