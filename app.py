import streamlit as st
import urllib.parse

# 1. Configurazione della pagina
st.set_page_config(page_title="3D Studio Quote Pro", page_icon="🎨")

# --- 2. VALORI AMMINISTRATIVI (Admin Panel) ---
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

# --- 3. DIZIONARIO DELLE TRADUZIONI (Español, English, Italiano) ---
texts = {
    "Español": {
        "title": "EMPRESA 3D",
        "slogan": "✨ Hacemos tus sueños realidad",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "wa_num": "51910034696",
        "p_name_label": "Tu Nombre", "char_name_label": "Personaje", "ref_label": "Subir Referencia",
        "step1": "1️⃣ Datos del Proyecto", "step2": "2️⃣ Configuración Artística", "step3": "3️⃣ Presupuesto Final",
        "tab_print": "💧 Impresión", "tab_paint": "🖌️ Pintura", "tab_design": "🧊 Diseño",
        "height_label": "Altura (cm)", "comp_label": "Complejidad de la pieza", "comp_opts": ["Simple", "Orgánico", "Épico"],
        "paint_check": "¿Incluir Pintura Profesional?", "paint_level": "Nivel de acabado", "paint_opts": ["Básico", "Vitrina", "Museo"],
        "design_label": "Edición Digital / Modelado",
        "design_opts": ["Listo para imprimir (0€)", "Ajuste Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "final_price_label": "PRECIO ESTIMADO", "saving_label": "Ahorro Aplicado",
        "savings_title": "✨ Beneficio por Tarifa de Taller", "savings_desc": "Precio optimizado por fabricación directa.",
        "wa_btn": "📲 Enviar Pedido a WhatsApp", "note": "⚠️ El inicio de producción requiere el 50% de adelanto.",
        "wa_header": "*NUEVO PEDIDO DETALLADO*",
        "thanks": "✅ **¡Gracias por tu solicitud!** Al abrir WhatsApp, **no olvides adjuntar tu imagen de referencia** para procesar tu pedido de inmediato.",
        "quality_tag": "⭐ Calidad Garantizada | Envío Seguro | Resina ABS-Like"
    },
    "English": {
        "title": "3D STUDIO",
        "slogan": "✨ We make your dreams come true",
        "delivery": "🕒 Delivery: 1.5 weeks (After 50% deposit)",
        "wa_num": "3934567890",
        "p_name_label": "Your Name", "char_name_label": "Character", "ref_label": "Upload Reference",
        "step1": "1️⃣ Project Details", "step2": "2️⃣ Artistic Configuration", "step3": "3️⃣ Final Budget",
        "tab_print": "💧 Printing", "tab_paint": "🖌️ Painting", "tab_design": "🧊 Design",
        "height_label": "Height (cm)", "comp_label": "Piece Complexity", "comp_opts": ["Simple", "Organic", "Epic"],
        "paint_check": "Include Professional Painting?", "paint_level": "Finish Level", "paint_opts": ["Basic", "Display", "Museum"],
        "design_label": "Digital Editing / Modeling",
        "design_opts": ["Ready to print (0€)", "Basic Fix (10€)", "Customization (25€)", "Premium (60€)"],
        "final_price_label": "ESTIMATED PRICE", "saving_label": "Total Savings",
        "savings_title": "✨ Workshop Rate Benefit", "savings_desc": "Optimized price for direct manufacturing.",
        "wa_btn": "📲 Send Order to WhatsApp", "note": "⚠️ Production starts after 50% deposit.",
        "wa_header": "*NEW DETAILED ORDER*",
        "thanks": "✅ **Thank you for your request!** When WhatsApp opens, **please attach your reference image** to process your order faster.",
        "quality_tag": "⭐ Guaranteed Quality | Secure Shipping | ABS-Like Resin"
    },
    "Italiano": {
        "title": "STUDIO 3D",
        "slogan": "✨ Rendiamo i tuoi sogni realtà",
        "delivery": "🕒 Consegna: 1.5 settimane (Dall'acconto del 50%)",
        "wa_num": "3934567890",
        "p_name_label": "Il tuo Nome", "char_name_label": "Personaggio", "ref_label": "Carica Riferimento",
        "step1": "1️⃣ Dettagli Progetto", "step2": "2️⃣ Configurazione Artistica", "step3": "3️⃣ Preventivo Finale",
        "tab_print": "💧 Stampa", "tab_paint": "🖌️ Pittura", "tab_design": "🧊 Design",
        "height_label": "Altezza (cm)", "comp_label": "Complessità", "comp_opts": ["Semplice", "Organico", "Epico"],
        "paint_check": "Includere Pittura Professionale?", "paint_level": "Livello di finitura", "paint_opts": ["Base", "Vetrina", "Museo"],
        "design_label": "Modifica Digitale / Modellazione",
        "design_opts": ["Pronto da stampare (0€)", "Base (10€)", "Personalizzato (25€)", "Premium (60€)"],
        "final_price_label": "PREZZO STIMATO", "saving_label": "Risparmio Applicato",
        "savings_title": "✨ Vantaggio Tariffa Bottega", "savings_desc": "Prezzo ottimizzato per produzione diretta.",
        "wa_btn": "📲 Invia Ordine su WhatsApp", "note": "⚠️ Il lavoro inizia dopo l'acconto del 50%.",
        "wa_header": "*NUOVO ORDINE DETTAGLIATO*",
        "thanks": "✅ **Grazie per la tua richiesta!** Quando si apre WhatsApp, **non dimenticare di allegare l'immagine di riferimento** per elaborare il tuo ordine più velocemente.",
        "quality_tag": "⭐ Qualità Garantita | Spedizione Sicura | Resina ABS-Like"
    }
}

idioma = st.selectbox("🌐 Selecciona Idioma / Select Language / Lingua", ["Español", "English", "Italiano"])
t = texts[idioma]

# --- 4. HEADER ---
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.image("https://cdn-icons-png.flaticon.com/512/1720/1720516.png", width=90)
with col_header2:
    st.markdown(f"<h1 style='margin-bottom: 0;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.write(f"{t['slogan']}")

st.info(t["delivery"])
st.divider()

# --- 5. PASOS ---
st.header(t["step1"])
c1, c2 = st.columns(2)
with c1:
    nombre_c = st.text_input(t["p_name_label"])
    nombre_p = st.text_input(t["char_name_label"])
with c2:
    st.file_uploader(t["ref_label"], type=['png', 'jpg', 'jpeg'])

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

# --- 6. BUDGET FINALE ---
st.header(t["step3"])
total_eur = costo_imp + costo_p + costo_d
total_pen = total_eur * st.session_state.tasa

with st.container(border=True):
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        if idioma == "Español":
            st.metric(label=t["final_price_label"], value=f"S/. {total_pen:.2f}")
            st.caption(f"Equivalente a: € {total_eur:.2f}")
        else:
            st.metric(label=t["final_price_label"], value=f"€ {total_eur:.2f}")
            st.caption(f"Ref: S/. {total_pen:.2f}")
    
    with col_res2:
        # Cálculo de ahorro simplificado para mostrar profesionalismo
        ahorro_est = (total_eur * 0.25) 
        st.success(f"{t['savings_title']}")
        if idioma == "Español":
            st.write(f"{t['saving_label']}: **S/. {ahorro_est * st.session_state.tasa:.2f}**")
        else:
            st.write(f"{t['saving_label']}: **€ {ahorro_est:.2f}**")

# --- 7. INVIO WHATSAPP ---
st.warning(t["note"])

msg = (f"{t['wa_header']}\n--------------------------\n"
       f"👤 Cliente: {nombre_c}\n👾 Figura: {nombre_p}\n📏 Altura: {altura}cm\n"
       f"💧 Impressione: {dif}\n🖌️ Pittura: {nv_p}\n🧊 Edit: {tipo_d}\n"
       f"--------------------------\n💰 TOTAL: €{total_eur:.2f} / S/. {total_pen:.2f}")

wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"

if nombre_c and nombre_p:
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
    st.success(t["thanks"])
else:
    st.info("⚠️ Info: " + t["p_name_label"] + " & " + t["char_name_label"])

st.divider()
st.markdown(f"<p style='text-align: center; color: gray;'>{t['quality_tag']}</p>", unsafe_allow_html=True)
