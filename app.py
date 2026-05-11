import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="3D Studio Quote", page_icon="🎨")

# --- 2. PANEL DE ADMINISTRACIÓN (SIDEBAR) ---
# Definimos los valores base PRIMERO para que no den error abajo
costo_resina = 0.03
costo_hora_diseno = 11.0
costo_hora_pintura = 8.5
tasa_cambio = 4.10

with st.sidebar:
    st.header("🔐 Panel de Control")
    clave = st.text_input("Contraseña Admin", type="password")
    
    if clave == "admin123":
        st.success("Acceso Autorizado")
        costo_resina = st.number_input("Costo Resina x ml (€)", value=0.03, format="%.3f")
        costo_hora_diseno = st.number_input("Costo Hora Diseño (€)", value=11.0)
        costo_hora_pintura = st.number_input("Costo Hora Pintura (€)", value=8.5)
        tasa_cambio = st.number_input("Tasa Cambio (1€ = S/.)", value=4.10)

# --- 3. DICCIONARIO DE TRADUCCIONES ---
texts = {
    "Español": {
        "step1": "1️⃣ Datos del Proyecto",
        "step2": "2️⃣ Configuración",
        "step3": "3️⃣ Presupuesto",
        "wa_num": "51910034696",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "design_opts": ["Listo para imprimir (0€)", "Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "wa_btn": "📲 Enviar a WhatsApp Perú",
        "payment_note": "⚠️ El trabajo inicia tras confirmar el 50% de adelanto."
    },
    "English": {
        "step1": "1️⃣ Project Details",
        "step2": "2️⃣ Configuration",
        "step3": "3️⃣ Budget",
        "wa_num": "3934567890",
        "delivery": "🕒 Delivery: 1.5 weeks (After 50% deposit)",
        "design_opts": ["Ready to print (0€)", "Basic Fix (10€)", "Customization (25€)", "Premium (60€)"],
        "wa_btn": "📲 Send to WhatsApp Europe",
        "payment_note": "⚠️ Project starts after 50% deposit."
    },
    "Italiano": {
        "step1": "1️⃣ Dettagli Progetto",
        "step2": "2️⃣ Configurazione",
        "step3": "3️⃣ Preventivo",
        "wa_num": "3934567890",
        "delivery": "🕒 Consegna: 1.5 settimane (Dal acconto del 50%)",
        "design_opts": ["Pronto da stampare (0€)", "Base (10€)", "Personalizzato (25€)", "Premium (60€)"],
        "wa_btn": "📲 Invia a WhatsApp Italia",
        "payment_note": "⚠️ Il lavoro inizia dopo l'acconto del 50%."
    }
}

# --- 4. SELECTOR DE IDIOMA ---
idioma = st.selectbox("🌐 Selecciona Idioma", ["Español", "English", "Italiano"])
t = texts[idioma]

# --- 5. INTERFAZ PRINCIPAL ---
st.title("🚀 TU EMPRESA 3D")
st.write(f"**{t['delivery']}**")
st.divider()

# PASO 1
st.header(t["step1"])
c1, c2 = st.columns(2)
with c1:
    nombre_c = st.text_input("Tu Nombre", placeholder="Ej. Juan Perez")
    nombre_p = st.text_input("Nombre de la Figura", placeholder="Ej. Iron Man")
with c2:
    st.file_uploader("Sube una imagen de referencia", type=['png', 'jpg', 'jpeg'])

# PASO 2
st.header(t["step2"])
tab1, tab2, tab3 = st.tabs(["💧 Impresión", "🖌️ Pintura", "🧊 Diseño"])

with tab1:
    altura = st.number_input("Altura de la figura (cm)", 5, 100, 15)
    dif = st.select_slider("Complejidad de la pieza", options=["Simple", "Orgánico", "Épico"])
    vol = (altura ** 2.2) * 0.15
    extra_limpieza = {"Simple": 1.5, "Orgánico": 3.0, "Épico": 6.0}[dif]
    costo_imp = (vol * costo_resina) + extra_limpieza

with tab2:
    quiere_p = st.checkbox("¿Incluir Pintura Artística?")
    nv_p, costo_p = "No", 0.0
    if quiere_p:
        nv_p = st.select_slider("Nivel de acabado", options=["Básico", "Vitrina", "Museo"])
        mult = {"Básico": 1, "Vitrina": 2.5, "Museo": 5}
        horas_p = (altura/5) * mult[nv_p]
        costo_p = horas_p * costo_hora_pintura

with tab3:
    tipo_d = st.selectbox("Trabajo de edición digital", t["design_opts"])
    costo_d = {t["design_opts"][0]: 0.0, t["design_opts"][1]: 10.0, 
               t["design_opts"][2]: 25.0, t["design_opts"][3]: 60.0}[tipo_d]

# PASO 3
st.header(t["step3"])
total_eur = costo_imp + costo_p + costo_d
total_pen = total_eur * tasa_cambio

with st.container(border=True):
    st.title(f"€ {total_eur:.2f}")
    st.write(f"Precio en moneda local: **S/. {total_pen:.2f}**")
    st.write("---")
    st.write(f"📏 Altura: {altura}cm | 🎨 Pintura: {nv_p} | 🧊 Diseño: {tipo_d}")

# WHATSAPP
msg = (f"SOLICITUD DE COTIZACIÓN\n"
       f"----------------------\n"
       f"👤 Cliente: {nombre_c}\n"
       f"👾 Figura: {nombre_p}\n"
       f"📏 Altura: {altura} cm\n"
       f"🖌️ Pintura: {nv_p}\n"
       f"🧊 Diseño: {tipo_d}\n"
       f"💰 TOTAL: € {total_eur:.2f} (S/. {total_pen:.2f})\n"
       f"🕒 {t['delivery']}")

wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"

st.warning(t["payment_note"])

if nombre_c and nombre_p:
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
else:
    st.info("⚠️ Por favor completa tu nombre y el de la figura en el Paso 1 para enviar.")
