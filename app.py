import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="3D Studio Quote Pro", page_icon="🎨")

# --- 2. VALORES ADMINISTRABLES (Inicialización segura) ---
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

# --- 3. DICCIONARIO DE TRADUCCIONES (Completo para evitar KeyErrors) ---
texts = {
    "Español": {
        "title": "EMPRESA 3D",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "wa_num": "51910034696",
        "p_name": "Tu Nombre", "char_name": "Personaje",
        "design_label": "Edición Digital",
        "design_opts": ["Listo para imprimir (0€)", "Ajuste Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "wa_btn": "📲 Solicitar Pedido (WhatsApp Perú)",
        "note": "⚠️ El trabajo inicia tras confirmar el 50% de adelanto.",
        "savings_title": "✨ Ahorro por Tarifa de Taller",
        "savings_desc": "Comparado con precios de estudios de arte estándar."
    },
    "English": {
        "title": "3D STUDIO",
        "delivery": "🕒 Delivery: 1.5 weeks (After 50% deposit)",
        "wa_num": "3934567890",
        "p_name": "Your Name", "char_name": "Character",
        "design_label": "Digital Editing",
        "design_opts": ["Ready to print (0€)", "Basic Fix (10€)", "Customization (25€)", "Premium (60€)"],
        "wa_btn": "📲 Send Order (WhatsApp Europe)",
        "note": "⚠️ Project starts after 50% deposit.",
        "savings_title": "✨ Workshop Rate Savings",
        "savings_desc": "Compared to standard art studio prices."
    },
    "Italiano": {
        "title": "STUDIO 3D",
        "delivery": "🕒 Consegna: 1.5 settimane (Dal acconto del 50%)",
        "wa_num": "3934567890",
        "p_name": "Il tuo Nome", "char_name": "Personaggio",
        "design_label": "Modifica Digitale",
        "design_opts": ["Pronto da stampare (0€)", "Base (10€)", "Personalizzato (25€)", "Premium (60€)"],
        "wa_btn": "📲 Invia Ordine (WhatsApp Italia)",
        "note": "⚠️ Il lavoro inizia dopo l'acconto del 50%.",
        "savings_title": "✨ Risparmio Tariffa Bottega",
        "savings_desc": "Rispetto ai prezzi standard degli studi d'arte."
    }
}

idioma = st.selectbox("🌐 Idioma / Language", ["Español", "English", "Italiano"])
t = texts[idioma]

# --- 4. HEADER: LOGO Y NOMBRE ---
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.image("https://cdn-icons-png.flaticon.com/512/1720/1720516.png", width=90)
with col_header2:
    st.markdown(f"<h1 style='margin-bottom: 0;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.write("✨ *Arte en Resina ABS-Like & Pintura Profesional*")

st.info(t["delivery"])
st.divider()

# --- 5. PASOS DE DATOS Y CONFIGURACIÓN ---
st.header("1️⃣ Datos del Proyecto")
col1, col2 = st.columns(2)
with col1:
    nombre_c = st.text_input(t["p_name"], key="user_name")
    nombre_p = st.text_input(t["char_name"], key="char_name")
with col2:
    st.file_uploader("Subir referencia", type=['png', 'jpg', 'jpeg'])

st.header("2️⃣ Configuración Técnica")
tab1, tab2, tab3 = st.tabs(["💧 Impresión", "🖌️ Pintura", "🧊 Diseño"])

with tab1:
    altura = st.number_input("Altura (cm)", 5, 100, 15)
    dif = st.select_slider("Complejidad", options=["Pieza Simple", "Detalle Orgánico", "Complejidad Épica"])
    vol = (altura ** 2.2) * 0.15
    extra = {"Pieza Simple": 1.5, "Detalle Orgánico": 3.0, "Complejidad Épica": 6.0}[dif]
    costo_imp = (vol * st.session_state.resina) + extra

with tab2:
    quiere_p = st.checkbox("¿Incluir Pintura Profesional?")
    nv_p, costo_p, horas_p = "No", 0.0, 0.0
    if quiere_p:
        nv_p = st.select_slider("Nivel de acabado", options=["Básico", "Vitrina", "Museo"])
        mult = {"Básico": 1, "Vitrina": 2.5, "Museo": 5}
        horas_p = (altura/5) * mult[nv_p]
        costo_p = horas_p * st.session_state.pintura

with tab3:
    tipo_d = st.selectbox(t["design_label"], t["design_opts"])
    costo_d = {t["design_opts"][0]: 0.0, t["design_opts"][1]: 10.0, t["design_opts"][2]: 25.0, t["design_opts"][3]: 60.0}[tipo_d]
    horas_d = {t["design_opts"][0]: 0, t["design_opts"][1]: 1, t["design_opts"][2]: 3, t["design_opts"][3]: 8}[tipo_d]

# --- 6. PRESUPUESTO Y AHORRO (El cuadro de abajo) ---
st.header("3️⃣ Presupuesto Final")
total_eur = costo_imp + costo_p + costo_d
total_pen = total_eur * st.session_state.tasa

# Cálculo del ahorro (Precios mercado: Pintura €18/h | Diseño €30/h)
ahorro_p = horas_p * (18 - st.session_state.pintura)
ahorro_d = horas_d * (30 - st.session_state.blender)
total_ahorro = ahorro_p + ahorro_d

# Dibujamos el cuadro de resultados
with st.container(border=True):
    c_res1, c_res2 = st.columns(2)
    with c_res1:
        st.metric("PRECIO TOTAL", f"€ {total_eur:.2f}")
        st.write(f"Conversión aprox: **S/. {total_pen:.2f}**")
    
    with c_res2:
        if total_ahorro > 0:
            st.success(f"{t['savings_title']}")
            st.write(f"💰 Ahorras: **€ {total_ahorro:.2f}**")
            st.caption(t["savings_desc"])

# --- 7. BOTÓN WHATSAPP ---
st.warning(t["note"])

msg = (f"*SOLICITUD DE COTIZACIÓN*\n"
       f"----------------------\n"
       f"👤 Cliente: {nombre_c}\n"
       f"👾 Figura: {nombre_p}\n"
       f"📏 Altura: {altura}cm\n"
       f"🖌️ Pintura: {nv_p}\n"
       f"🧊 Edición: {tipo_d}\n"
       f"----------------------\n"
       f"💰 TOTAL: €{total_eur:.2f}\n"
       f"🕒 {t['delivery']}")

wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"

if nombre_c and nombre_p:
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
else:
    st.info("⚠️ Completa tu nombre y el del personaje en el Paso 1 para activar el envío.")
