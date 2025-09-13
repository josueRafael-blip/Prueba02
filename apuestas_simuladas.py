import streamlit as st
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="🎯 Simulador de Apuestas Deportivas", layout="centered")

st.title("🎯 Simulador de Apuestas Deportivas (Ficticio)")

st.markdown("""
Este es un simulador **no real** de apuestas deportivas. Puedes seleccionar eventos, apostar de forma ficticia y generar una **boleta con tus apuestas**.
""")

# Eventos predefinidos (puedes ampliar esta lista)
eventos = [
    {"evento": "Real Madrid vs Barcelona", "cuotas": {"Local": 1.90, "Empate": 3.20, "Visitante": 2.10}},
    {"evento": "Manchester City vs Liverpool", "cuotas": {"Local": 2.00, "Empate": 3.00, "Visitante": 2.30}},
    {"evento": "Boca Juniors vs River Plate", "cuotas": {"Local": 2.10, "Empate": 3.10, "Visitante": 2.00}},
    {"evento": "PSG vs Bayern Munich", "cuotas": {"Local": 2.50, "Empate": 3.40, "Visitante": 1.90}},
    {"evento": "Inter Miami vs LA Galaxy", "cuotas": {"Local": 1.80, "Empate": 3.50, "Visitante": 2.50}},
]

# Inicializar sesión
if 'boleta' not in st.session_state:
    st.session_state['boleta'] = []

st.subheader("📋 Selecciona un evento y haz tu apuesta")

# Selección de evento
evento_idx = st.selectbox("Evento", options=range(len(eventos)), format_func=lambda i: eventos[i]["evento"])
evento = eventos[evento_idx]

# Mostrar cuotas
st.write("**Cuotas disponibles:**")
for resultado, cuota in evento["cuotas"].items():
    st.write(f"- {resultado}: {cuota}")

# Apuesta del usuario
opcion = st.radio("Selecciona tu apuesta", options=list(evento["cuotas"].keys()))
monto = st.number_input("Monto apostado (ficticio)", min_value=1.0, step=1.0, format="%.2f")

# Botón para apostar
if st.button("💸 Realizar Apuesta"):
    apuesta = {
        "evento": evento["evento"],
        "selección": opcion,
        "cuota": evento["cuotas"][opcion],
        "monto": monto,
        "ganancia_posible": round(monto * evento["cuotas"][opcion], 2),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state['boleta'].append(apuesta)
    st.success("✅ Apuesta registrada en tu boleta.")

# Mostrar boleta actual
st.subheader("🧾 Boleta de Apuestas")

if st.session_state['boleta']:
    df_boleta = pd.DataFrame(st.session_state['boleta'])
    st.dataframe(df_boleta, use_container_width=True)

    # Botón para generar imagen de la boleta
    if st.button("🖼️ Generar imagen de la boleta"):
        fig, ax = plt.subplots(figsize=(6, len(df_boleta) * 0.6 + 1))
        ax.axis('off')
        ax.set_title("🧾 Boleta de Apuestas", fontsize=14, fontweight='bold', loc='center')

        table_data = [["Evento", "Selección", "Cuota", "Monto", "Ganancia", "Fecha"]]
        for row in st.session_state['boleta']:
            table_data.append([
                row["evento"], row["selección"], row["cuota"],
                row["monto"], row["ganancia_posible"], row["fecha"]
            ])

        table = ax.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.2]*6)
        table.scale(1, 1.5)
        table.auto_set_font_size(False)
        table.set_fontsize(9)

        # Guardar imagen en memoria y mostrar
        buf = BytesIO()
        plt.savefig(buf, format="png")
        st.image(buf.getvalue(), caption="🖼️ Imagen generada de tu boleta")
else:
    st.info("Aún no has hecho ninguna apuesta.")
