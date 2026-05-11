import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="Maker3DPeru-Italia", page_icon="🎨")

# --- 2. VALORES ADMINISTRABLES ---
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

# --- 3. DICCIONARIO DE TRADUCCIONES TOTAL ---
texts = {
    "Español": {
        "title": "Maker3DPeru-Italia",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "wa_num": "51910034696",
        "p_name_label": "Tu Nombre", 
        "char_name_label": "Personaje",
        "ref_label": "Referencia",
        "step1": "1️⃣ Datos del Proyecto",
        "step2": "2️⃣ Configuración",
        "step3": "3️⃣ Presupuesto Final",
        "tab_print": "💧 Impresión",
        "tab_paint": "🖌️ Pintura",
        "tab_design": "🧊 Diseño",
        "height_label": "Altura (cm)",
        "comp_label": "Complejidad",
        "comp_opts": ["Simple", "Orgánico", "Épico"],
        "paint_check": "¿Incluir Pintura Profesional?",
        "paint_level": "Nivel de acabado",
        "paint_opts": ["Básico", "Vitrina", "Museo"],
        "design_label": "Edición Digital",
        "design_opts": ["Listo para imprimir (0€)", "Ajuste Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "final_price": "PRECIO FINAL",
        "saving_label": "Tu Ahorro",
        "savings_title": "✨ Ahorro por Tarifa de Taller",
        "savings_desc": "Comparado con precios de estudios de arte estándar.",
        "wa_btn": "📲 Solicitar Pedido (WhatsApp Perú)",
        "note": "⚠️ El trabajo inicia tras confirmar el 50% de adelanto."
    },
    "English": {
        "title": "Maker3DPeru-Italia",
        "delivery": "🕒 Delivery: 1.5 weeks (After 50% deposit)",
        "wa_num": "3934567890",
        "p_name_label": "Your Name", 
        "char_name_label": "Character",
        "ref_label": "Reference",
        "step1": "1️⃣ Project Details",
        "step2": "2️⃣ Configuration",
        "step3": "3️⃣ Final Budget",
        "tab_print": "💧 Printing",
        "tab_paint": "🖌️ Painting",
        "tab_design": "🧊 Design",
        "height_label": "Height (cm)",
        "comp_label": "Complexity",
        "comp_opts": ["Simple", "Organic", "Epic"],
        "paint_check": "Include Professional Painting?",
        "paint_level": "Finish Level",
        "paint_opts": ["Basic", "Display", "Museum"],
        "design_label": "Digital Editing",
        "design_opts": ["Ready to print (0€)", "Basic Fix (10€)", "Customization (25€)", "Premium (60€)"],
        "final_price": "FINAL PRICE",
        "saving_label": "Your Savings",
        "savings_title": "✨ Workshop Rate Savings",
        "savings_desc": "Compared to standard art studio prices.",
        "wa_btn": "📲 Send Order (WhatsApp Europe)",
        "note": "⚠️ Project starts after 50% deposit."
    },
    "Italiano": {
        "title": "Maker3DPeru-Italia",
        "delivery": "🕒 Consegna: 1.5 settimane (Dal acconto del 50%)",
        "wa_num": "3934567890",
        "p_name_label": "Il tuo Nome", 
        "char_name_label": "Personaggio",
        "ref_label": "Riferimento",
        "step1": "1️⃣ Dettagli Progetto",
        "step2": "2️⃣ Configurazione",
        "step3": "3️⃣ Preventivo Finale",
        "tab_print": "💧 Stampa",
        "tab_paint": "🖌️ Pittura",
        "tab_design": "🧊 Design",
        "height_label": "Altezza (cm)",
        "comp_label": "Complessità",
        "comp_opts": ["Semplice", "Organico", "Epico"],
        "paint_check": "Includere Pittura Professionale?",
        "paint_level": "Livello di finitura",
        "paint_opts": ["Base", "Vetrina", "Museo"],
        "design_label": "Modifica Digitale",
        "design_opts": ["Pronto da stampare (0€)", "Base (10€)", "Personalizzato (25€)", "Premium (60€)"],
        "final_price": "PREZZO FINALE",
        "saving_label": "Il tuo Risparmio",
        "savings_title": "✨ Risparmio Tariffa Bottega",
        "savings_desc": "Rispetto ai prezzi standard degli studi d'arte.",
        "wa_btn": "📲 Invia Ordine (WhatsApp Italia)",
        "note": "⚠️ Il lavoro inizia dopo l'acconto del 50%."
    }
}

idioma = st.selectbox("🌐 Idioma / Language", ["Español", "English", "Italiano"])
t = texts[idioma]

# --- 4. HEADER ---
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.image("Logo.jpg", width=90) # <-- Pon el nombre exacto del archivo
with col_header2:
    st.markdown(f"<h1 style='margin-bottom: 0;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.write("✨ *Arte en Resina ABS-Like & Pintura Profesional*")

st.info(t["delivery"])
st.divider()

# --- 5. PASO 1: DATOS (TRADUCIDO) ---
st.header(t["step1"])
c1, c2 = st.columns(2)
with c1:
    nombre_c = st.text_input(t["p_name_label"])
    nombre_p = st.text_input(t["char_name_label"])
with c2:
    st.file_uploader(t["ref_label"], type=['png', 'jpg', 'jpeg'])

# --- 6. PASO 2: CONFIGURACIÓN (TABS TRADUCIDOS) ---
st.header(t["step2"])
tab1, tab2, tab3 = st.tabs([t["tab_print"], t["tab_paint"], t["tab_design"]])

with tab1:
    altura = st.number_input(t["height_label"], 5, 100, 15)
    dif = st.select_slider(t["comp_label"], options=t["comp_opts"])
    vol = (altura ** 2.2) * 0.15
    extra = {t["comp_opts"][0]: 1.5, t["comp_opts"][1]: 3.0, t["comp_opts"][2]: 6.0}[dif]
    costo_imp = (vol * st.session_state.resina) + extra

with tab2:
    quiere_p = st.checkbox(t["paint_check"])
    nv_p, costo_p, horas_p = "No", 0.0, 0.0
    if quiere_p:
        nv_p = st.select_slider(t["paint_level"], options=t["paint_opts"])
        mult = {t["paint_opts"][0]: 1, t["paint_opts"][1]: 2.5, t["paint_opts"][2]: 5}
        horas_p = (altura/5) * mult[nv_p]
        costo_p = horas_p * st.session_state.pintura

with tab3:
    tipo_d = st.selectbox(t["design_label"], t["design_opts"])
    costo_d = {t["design_opts"][0]: 0.0, t["design_opts"][1]: 10.0, t["design_opts"][2]: 25.0, t["design_opts"][3]: 60.0}[tipo_d]
    horas_d = {t["design_opts"][0]: 0, t["design_opts"][1]: 1, t["design_opts"][2]: 3, t["design_opts"][3]: 8}[tipo_d]

# --- 7. PASO 3: PRESUPUESTO (ETIQUETAS TRADUCIDAS) ---
st.header(t["step3"])
total_eur = costo_imp + costo_p + costo_d
total_pen = total_eur * st.session_state.tasa

ahorro_p = horas_p * (18 - st.session_state.pintura)
ahorro_d = horas_d * (30 - st.session_state.blender)
total_ahorro = ahorro_p + ahorro_d

with st.container(border=True):
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(label=t["final_price"], value=f"€ {total_eur:.2f}")
        st.write(f"S/. {total_pen:.2f}")
    
    with col_res2:
        if total_ahorro > 0:
            st.success(f"{t['savings_title']}")
            st.write(f"{t['saving_label']}: **€ {total_ahorro:.2f}**")
            st.caption(t["savings_desc"])

# --- 8. WHATSAPP ---
st.warning(t["note"])
msg = f"*COTIZACIÓN {t['title']}*\nCliente: {nombre_c}\nFigura: {nombre_p}\nAltura: {altura}cm\nTOTAL: €{total_eur:.2f}"
wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"

if nombre_c and nombre_p:
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
else:
    st.info("⚠️ Completa tus datos para enviar.")
