import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="3D Studio Quote", page_icon="🎨")

# --- 2. VALORES BASE (Administrables) ---
if 'resina' not in st.session_state: st.session_state.resina = 0.03
if 'blender' not in st.session_state: st.session_state.blender = 11.0
if 'pintura' not in st.session_state: st.session_state.pintura = 8.5
if 'tasa' not in st.session_state: st.session_state.tasa = 4.10

with st.sidebar:
    st.header("🔐 Panel de Control")
    clave = st.text_input("Contraseña Admin", type="password")
    if clave == "admin123":
        st.success("Acceso Autorizado")
        st.session_state.resina = st.number_input("Resina ml (€)", value=st.session_state.resina, format="%.3f")
        st.session_state.blender = st.number_input("Hora Diseño (€)", value=st.session_state.blender)
        st.session_state.pintura = st.number_input("Hora Pintura (€)", value=st.session_state.pintura)
        st.session_state.tasa = st.number_input("Tasa S/.", value=st.session_state.tasa)

# --- 3. DICCIONARIO DE TRADUCCIONES ---
texts = {
    "Español": {
        "title": "🚀 TU EMPRESA 3D",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "wa_num": "51910034696",
        "p_name": "Tu Nombre", "char_name": "Personaje",
        "design_label": "Edición Digital",
        "design_opts": ["Listo para imprimir (0€)", "Ajuste Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "wa_btn": "📲 Solicitar Pedido (WhatsApp Perú)",
        "note": "⚠️ El trabajo inicia tras confirmar el 50% de adelanto.",
        "savings": "¡Estás ahorrando!"
    },
    "English": {
        "title": "🚀 3D STUDIO QUOTE",
        "delivery": "🕒 Delivery: 1.5 weeks (After 50% deposit)",
        "wa_num": "3934567890",
        "p_name": "Your Name", "char_name": "Character",
        "design_label": "Digital Editing",
        "design_opts": ["Ready to print (0€)", "Basic Fix (10€)", "Customization (25€)", "Premium (60€)"],
        "wa_btn": "📲 Send Order (WhatsApp Europe)",
        "note": "⚠️ Project starts after 50% deposit.",
        "savings": "You are saving!"
    },
    "Italiano": {
        "title": "🚀 PREVENTIVO 3D",
        "delivery": "🕒 Consegna: 1.5 settimane (Dal acconto del 50%)",
        "wa_num": "3934567890",
        "p_name": "Il tuo Nome", "char_name": "Personaggio",
        "design_label": "Modifica Digitale",
        "design_opts": ["Pronto da stampare (0€)", "Base (10€)", "Personalizzato (25€)", "Premium (60€)"],
        "wa_btn": "📲 Invia Ordine (WhatsApp Italia)",
        "note": "⚠️ Il lavoro inizia dopo l'acconto del 50%.",
        "savings": "Stai risparmiando!"
    }
}

idioma = st.selectbox("🌐 Idioma / Language", ["Español", "English", "Italiano"])
t = texts[idioma]

st.title(t["title"])
st.info(t["delivery"])
st.divider()

# --- 4. PASO 1: DATOS ---
st.header("1️⃣ Datos")
c1, c2 = st.columns(2)
with c1:
    nombre_c = st.text_input(t["p_name"])
    nombre_p = st.text_input(t["char_name"])
with c2:
    st.file_uploader("Referencia", type=['png', 'jpg', 'jpeg'])

# --- 5. PASO 2: CONFIGURACIÓN ---
st.header("2️⃣ Configuración")
tab1, tab2, tab3 = st.tabs(["💧 Impresión", "🖌️ Pintura", "🧊 Diseño"])

with tab1:
    altura = st.number_input("Altura (cm)", 5, 100, 15)
    dif = st.select_slider("Detalle", options=["Pieza Simple", "Detalle Orgánico", "Complejidad Épica"])
    vol = (altura ** 2.2) * 0.15
    extra = {"Pieza Simple": 1.5, "Detalle Orgánico": 3.0, "Complejidad Épica": 6.0}[dif]
    costo_imp = (vol * st.session_state.resina) + extra

with tab2:
    quiere_p = st.checkbox("¿Incluir Pintura?")
    nv_p, costo_p, horas_p = "No", 0.0, 0.0
    if quiere_p:
        nv_p = st.select_slider("Nivel", options=["Básico", "Vitrina", "Museo"])
        mult = {"Básico": 1, "Vitrina": 2.5, "Museo": 5}
        horas_p = (altura/5) * mult[nv_p]
        costo_p = horas_p * st.session_state.pintura

with tab3:
    tipo_d = st.selectbox(t["design_label"], t["design_opts"])
    costos_d_map = {t["design_opts"][0]: 0.0, t["design_opts"][1]: 10.0, 
                    t["design_opts"][2]: 25.0, t["design_opts"][3]: 60.0}
    costo_d = costos_d_map[tipo_d]
    # Estimación de horas para el cálculo de ahorro
    horas_d = {t["design_opts"][0]: 0, t["design_opts"][1]: 1, 
               t["design_opts"][2]: 3, t["design_opts"][3]: 8}[tipo_d]

# --- 6. PASO 3: TOTALES Y AHORRO ---
st.header("3️⃣ Presupuesto")
total_eur = costo_imp + costo_p + costo_d
total_pen = total_eur * st.session_state.tasa

# Cálculo del ahorro (Diferencia vs mercado estándar)
# Mercado: Pintura €15/h | Diseño €25/h
ahorro_p = horas_p * (15 - st.session_state.pintura)
ahorro_d = horas_d * (25 - st.session_state.blender)
total_ahorro = ahorro_p + ahorro_d

col_res1, col_res2 = st.columns(2)

with col_res1:
    st.metric(label="TOTAL (EUR)", value=f"€ {total_eur:.2f}")
    st.write(f"S/. {total_pen:.2f}")

with col_res2:
    if total_ahorro > 0:
        st.success(f"✨ {t['savings']}")
        st.write(f"**€ {total_ahorro:.2f}**")

with st.expander("Ver desglose del pedido"):
    st.write(f"📏 Altura: {altura}cm")
    st.write(f"🧪 Impresión Resina ABS: €{costo_imp:.2f}")
    st.write(f"🖌️ Pintura ({nv_p}): €{costo_p:.2f}")
    st.write(f"🧊 Edición Digital: €{costo_d:.2f}")

# --- 7. WHATSAPP ---
msg = (f"*SOLICITUD COTIZACIÓN*\n"
       f"Cliente: {nombre_c}\nFigura: {nombre_p}\n"
       f"Altura: {altura}cm\nMaterial: Resina ABS\n"
       f"Pintura: {nv_p}\nDiseño: {tipo_d}\n"
       f"TOTAL: €{total_eur:.2f}\n"
       f"Adelanto 50% aceptado.")

wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"
st.warning(t["note"])

if nombre_c and nombre_p:
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
else:
    st.info("Completa nombre y personaje para activar el botón.")
