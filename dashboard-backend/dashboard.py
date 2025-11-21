import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import requests

# ======================================
# CONFIG DA PÁGINA
# ======================================
st.set_page_config(
    page_title="Dashboard Futurion Hub",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Dashboard — Futurion Hub")
st.write("Dados sendo obtidos do FIWARE (simulado).")


# =====================================================
# CONFIGURAÇÃO DO FIWARE 
# =====================================================
ORION_URL = "http://9.234.176.2:1026/v2/entities"
HEADERS = {"Content-Type": "application/json"}


# =====================================================
# FUNÇÃO DE BUSCA DO FIWARE (SIMULAÇÃO + CÓDIGO REAL)
# =====================================================

def buscar_login_events():
    """Simula busca no FIWARE Orion"""
    try:
        # CHAMADA REAL (se servidor estivesse funcionando)
        response = requests.get(f"{ORION_URL}?type=LoginEvent", headers=HEADERS, timeout=1)

        # Como o FIWARE está instável: simulamos retorno
        raise Exception("Simulação ativada")

    except:
        # --- RETORNO SIMULADO, MAS REALISTA ---
        dados = [
            {"username": "Admin", "timestamp": "2025-11-20T09:15:00"},
            {"username": "Admin", "timestamp": "2025-11-20T10:32:00"},
            {"username": "User2", "timestamp": "2025-11-20T10:45:00"},
            {"username": "Admin", "timestamp": "2025-11-20T11:20:00"},
        ]

        df = pd.DataFrame(dados)
        df["hora"] = pd.to_datetime(df["timestamp"]).dt.hour
        return df


def buscar_mood_events():
    """Simula busca de humores do FIWARE"""
    try:
        response = requests.get(f"{ORION_URL}?type=MoodEvent", headers=HEADERS, timeout=1)

        raise Exception("Simulação ativada")

    except:
        dados = [
            {"username": "Admin", "mood": "bem", "timestamp": "2025-11-20T09:20:00"},
            {"username": "User2", "mood": "neutro", "timestamp": "2025-11-20T10:40:00"},
            {"username": "Admin", "mood": "mal", "timestamp": "2025-11-20T10:50:00"},
            {"username": "User2", "mood": "bem", "timestamp": "2025-11-20T11:10:00"},
            {"username": "Admin", "mood": "bem", "timestamp": "2025-11-20T12:00:00"},
        ]

        df = pd.DataFrame(dados)
        df["hora"] = pd.to_datetime(df["timestamp"]).dt.hour
        df["score"] = df["mood"].map({"mal": 1, "neutro": 2, "bem": 3})
        return df


# =====================================================
# BUSCA DOS DADOS (com botão)
# =====================================================
if st.button("🔄 Atualizar dados do FIWARE"):
    st.session_state.login_df = buscar_login_events()
    st.session_state.mood_df = buscar_mood_events()
    st.success("Dados atualizados com sucesso!")

# Caso ainda não tenha nada
if "login_df" not in st.session_state:
    st.session_state.login_df = buscar_login_events()

if "mood_df" not in st.session_state:
    st.session_state.mood_df = buscar_mood_events()

login_df = st.session_state.login_df
mood_df = st.session_state.mood_df


# =====================================================
# GRÁFICO 1 — LOGIN POR HORA
# =====================================================
st.header("🔐 Logins por hora (dados do FIWARE)")

login_por_hora = login_df["hora"].value_counts().sort_index()

fig1, ax1 = plt.subplots()
login_por_hora.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Hora do dia")
ax1.set_ylabel("Quantidade de logins")
ax1.set_title("Logins por hora (FIWARE)")
st.pyplot(fig1)


# =====================================================
# GRÁFICO 2 — DISTRIBUIÇÃO DE HUMOR
# =====================================================
st.header("💙 Distribuição de Humor (FIWARE)")

mood_counts = mood_df["mood"].value_counts()

fig2, ax2 = plt.subplots()
mood_counts.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Humor")
ax2.set_ylabel("Quantidade")
ax2.set_title("Distribuição dos tipos de humor")
st.pyplot(fig2)


# =====================================================
# GRÁFICO 3 — EVOLUÇÃO DO HUMOR
# =====================================================
st.header("📈 Evolução do humor ao longo do tempo")

fig3, ax3 = plt.subplots()
ax3.plot(mood_df["score"])
ax3.set_xlabel("Registros (antigo → recente)")
ax3.set_ylabel("Humor (1=Mal, 2=Neutro, 3=Bem)")
ax3.set_title("Evolução do Humor (FIWARE)")
st.pyplot(fig3)
