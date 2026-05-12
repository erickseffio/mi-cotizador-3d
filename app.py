import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="Maker3DPeru-Italia", page_icon="Logo.jpg")

# --- 2. VALORES ADMINISTRABLES ---
if 'resina' not in st.session_state: st.session_state.resina = 0.03
if 'blender' not in st.session_state: st.session_state.blender = 11.0
if 'pintura' not in st.session_state: st.session_state.pintura = 8.5
if 'tasa' not in st.session_state: st.session_state.tasa = 4.10

with st.sidebar:
    st.header("🔐 Panel de Control")
    clave = st.text_input("Contraseña Admin", type="password")
    if clave == "02110510":
        st.success("Acceso Autorizado")
        st.session_state.resina = st.number_input("Resina ml (€)", value=st.session_state.resina, format="%.3f")
        st.session_state.blender = st.number_input("Hora Diseño (€)", value=st.session_state.blender)
        st.session_state.pintura = st.number_input("Hora Pintura (€)", value=st.session_state.pintura)
        st.session_state.tasa = st.number_input("Tasa S/.", value=st.session_state.tasa)

# --- 3. DICCIONARIO DE TRADUCCIONES ---
texts = {
    "Español (Perú)": {
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Hiper-realismo en Resina: Del archivo digital a tu vitrina.",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "wa_num": "51977511500",
        "p_name_label": "Tu Nombre", "char_name_label": "Personaje", "ref_label": "Subir Referencia",
        "p_name_ph": "Ej: Juan Pérez",
        "char_name_ph": "Ej: Iron Man Mark 85",
        "step1": "1️⃣ Datos del Proyecto", "step2": "2️⃣ Configuración Artística", "step3": "3️⃣ Presupuesto Final",
        "tab_print": "💧 Impresión", "tab_paint": "🖌️ Pintura", "tab_design": "🧊 Diseño",
        "height_label": "Altura (cm)", "comp_label": "Complejidad", "comp_opts": ["Simple", "Orgánico", "Épico"],
        "paint_check": "¿Incluir Pintura Profesional?", "paint_level": "Nivel de acabado", "paint_opts": ["Básico", "Vitrina", "Museo"],
        "design_label": "Edición Digital",
        "design_opts": ["Listo para imprimir (0€)", "Ajuste Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "final_price_label": "PRECIO ESTIMADO", "saving_label": "Ahorro Aplicado",
        "savings_title": "✨ ¡Descuento de Taller Aplicado!", 
        "wa_btn": "📲 Enviar Pedido a WhatsApp", "note": "⚠️ El inicio de producción requiere el 50% de adelanto.",
        "wa_header": "*NUEVO PEDIDO DETALLADO*",
        "thanks": "✅ **¡Gracias por tu solicitud!** Al abrir WhatsApp, **no olvides adjuntar tu imagen de referencia**.",
        "social_title": "📱 ¡Síguenos en nuestras redes!",
        "social_proof": "Envíos seguros a todo el Perú y el extranjero 📦",
        "height_help": "📏 Guía: Una lata de soda mide 12cm, una figura estándar 18cm.",
        "warning_input": "⚠️ **Atención:** Debes ingresar tu **Nombre** y el **Personaje** arriba para activar el botón de WhatsApp.",
        "quality_tag": "⭐ Calidad Garantizada | Envío Seguro | Resina ABS-Like"
    },
    "Español (España)": {
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Hiper-realismo en Resina: Del archivo digital a tu vitrina.",
        "delivery": "🕒 Entrega: 2 semanas (Desde el depósito del 50%)",
        "wa_num": "393924043068",
        "p_name_label": "Tu Nombre", "char_name_label": "Personaje", "ref_label": "Subir Referencia",
        "p_name_ph": "Ej: Javier García",
        "char_name_ph": "Ej: Batman (Hush)",
        "step1": "1️⃣ Datos del Proyecto", "step2": "2️⃣ Configuración Artística", "step3": "3️⃣ Presupuesto Final",
        "tab_print": "💧 Impresión", "tab_paint": "🖌️ Pintura", "tab_design": "🧊 Diseño",
        "height_label": "Altura (cm)", "comp_label": "Complejidad", "comp_opts": ["Simple", "Orgánico", "Épico"],
        "paint_check": "¿Incluir Pintura Profesional?", "paint_level": "Nivel de acabado", "paint_opts": ["Básico", "Vitrina", "Museo"],
        "design_label": "Edición Digital",
        "design_opts": ["Listo para imprimir (0€)", "Ajuste Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "final_price_label": "PRECIO ESTIMADO", "saving_label": "Ahorro Aplicado",
        "savings_title": "✨ ¡Descuento de Taller Aplicado!", 
        "wa_btn": "📲 Enviar Pedido a WhatsApp", "note": "⚠️ El inicio de producción requiere el 50% de adelanto.",
        "wa_header": "*NUEVO PEDIDO DETALLADO*",
        "thanks": "✅ **¡Gracias por tu solicitud!** Al abrir WhatsApp, **no olvides adjuntar tu imagen de referencia**.",
        "social_title": "📱 ¡Síguenos en nuestras redes!",
        "social_proof": "Envíos seguros a todo el Perú y el extranjero 📦",
        "height_help": "📏 Guía: Una lata de soda mide 12cm, una figura estándar 18cm.",
        "warning_input": "⚠️ **Atención:** Debes ingresar tu **Nombre** y el **Personaje** arriba para activar el botón de WhatsApp.",
        "quality_tag": "⭐ Calidad Garantizada | Envío Seguro | Resina ABS-Like"
    },
    "English": {
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Hyper-realism in Resin: From the digital file to your display case.",
        "delivery": "🕒 Delivery: 3 weeks (After 50% deposit)",
        "wa_num": "393924043068",
        "p_name_label": "Your Name", "char_name_label": "Character", "ref_label": "Upload Reference",
        "p_name_ph": "e.g. John Doe",
        "char_name_ph": "e.g. Spider-Man",
        "step1": "1️⃣ Project Details", "step2": "2️⃣ Artistic Configuration", "step3": "3️⃣ Final Budget",
        "tab_print": "💧 Printing", "tab_paint": "🖌️ Painting", "tab_design": "🧊 Design",
        "height_label": "Height (cm)", "comp_label": "Complexity", "comp_opts": ["Simple", "Organic", "Epic"],
        "paint_check": "Include Professional Painting?", "paint_level": "Finish Level", "paint_opts": ["Basic", "Display", "Museum"],
        "design_label": "Digital Editing",
        "design_opts": ["Ready to print (0€)", "Basic Fix (10€)", "Customization (25€)", "Premium (60€)"],
        "final_price_label": "ESTIMATED PRICE", "saving_label": "Total Savings",
        "savings_title": "✨ Workshop Discount Applied!",
        "wa_btn": "📲 Send Order to WhatsApp", "note": "⚠️ Production starts after 50% deposit.",
        "wa_header": "*NEW DETAILED ORDER*",
        "thanks": "✅ **Thank you!** When WhatsApp opens, **please attach your reference image**.",
        "social_title": "📱 Follow us!",
        "social_proof": "Secure shipping throughout Peru and abroad 📦",
        "height_help": "📏 Guide: A soda can is 12cm, a standard figure is 18cm.",
        "warning_input": "⚠️ **Attention:** Please enter your **Name** and **Character** above to enable the WhatsApp button.",
        "quality_tag": "⭐ Guaranteed Quality | Secure Shipping | ABS-Like Resin"
    },
    "Italiano": {
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Iperrealismo in resina: dal file digitale alla teca espositiva.",
        "delivery": "🕒 Consegna: 1.5 settimane (Dall'acconto del 50%)",
        "wa_num": "393924043068",
        "p_name_label": "Il tuo Nome", "char_name_label": "Personaggio", "ref_label": "Carica Riferimento",
        "p_name_ph": "es: Alessandro Rossi",
        "char_name_ph": "es: Darth Vader",
        "step1": "1️⃣ Dettagli Progetto", "step2": "2️⃣ Configurazione Artistica", "step3": "3️⃣ Preventivo Finale",
        "tab_print": "💧 Stampa", "tab_paint": "🖌️ Pittura", "tab_design": "🧊 Design",
        "height_label": "Altezza (cm)", "comp_label": "Complessità", "comp_opts": ["Semplice", "Organico", "Epico"],
        "paint_check": "Includere Pittura Professionale?", "paint_level": "Livello di finitura", "paint_opts": ["Base", "Vetrina", "Museo"],
        "design_label": "Modifica Digitale",
        "design_opts": ["Pronto da stampare (0€)", "Base (10€)", "Personalizzato (25€)", "Premium (60€)"],
        "final_price_label": "PREZZO STIMATO", "saving_label": "Risparmio Applicato",
        "savings_title": "✨ Sconto per il workshop applicato!",
        "wa_btn": "📲 Invia Ordine su WhatsApp", "note": "⚠️ Il lavoro inizia dopo l'acconto del 50%.",
        "wa_header": "*NUOVO ORDINE DETTAGLIATO*",
        "thanks": "✅ **Grazie!** Quando si apre WhatsApp, **non dimenticare di allegare l'immagine**.",
        "social_title": "📱 Seguici sui social!",
        "social_proof": "Spedizione sicura in tutto il Perù e all'estero 📦",
        "height_help": "📏 Guida: Una lattina misura 12cm, una figura standard 18cm.",
        "warning_input": "⚠️ **Attenzione:** Inserisci il tuo **Nome** e il **Personaggio** sopra per attivare il pulsante WhatsApp.",
        "quality_tag": "⭐ Qualità Garantita | Spedizione Sicura | Resina ABS-Like"
    }
}

idioma = st.selectbox("🌐 Idioma", ["Español (Perú)", "Español (España)", "English", "Italiano"])
t = texts[idioma]

# --- 4. HEADER ---
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.image("Logo.jpg", width=120)
with col_header2:
    st.markdown(f"<h1 style='margin-bottom: 0;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.write(f"{t['slogan']}")

st.info(t["delivery"])
st.divider()

# --- 5. PASOS 1 Y 2 ---
st.header(t["step1"])
c1, c2 = st.columns(2)
with c1:
    nombre_c = st.text_input(t["p_name_label"], placeholder=t["p_name_ph"])
    nombre_p = st.text_input(t["char_name_label"], placeholder=t["char_name_ph"])
with c2:
    st.file_uploader(t["ref_label"], type=['png', 'jpg', 'jpeg'])

st.header(t["step2"])
tab1, tab2, tab3 = st.tabs([t["tab_print"], t["tab_paint"], t["tab_design"]])

with tab1:
    altura = st.number_input(t["height_label"], 5, 100, 15)
    st.caption(t["height_help"])
    dif = st.select_slider(t["comp_label"], options=t["comp_opts"])
    vol = (altura ** 2.2) * 0.15
    extra = {t["comp_opts"][0]: 1.5, t["comp_opts"][1]: 3.0, t["comp_opts"][2]: 6.0}[dif]
    costo_imp = (vol * st.session_state.resina) + extra

with tab2:
    quiere_p = st.checkbox(t["paint_check"])
    nv_p, costo_p = "No", 0.0
    if quiere_p:
        nv_p = st.select_slider(t["paint_level"], options=t["paint_opts"])
        mult = {t["paint_opts"][0]: 1, t["paint_opts"][1]: 2.5, t["paint_opts"][2]: 5}
        horas_p = (altura/5) * mult[nv_p]
        costo_p = horas_p * st.session_state.pintura

with tab3:
    tipo_d = st.selectbox(t["design_label"], t["design_opts"])
    costo_d = {t["design_opts"][0]: 0.0, t["design_opts"][1]: 10.0, t["design_opts"][2]: 25.0, t["design_opts"][3]: 60.0}[tipo_d]

# --- 6. PRESUPUESTO ---
st.header(t["step3"])
total_eur = costo_imp + costo_p + costo_d
total_pen = total_eur * st.session_state.tasa

with st.container(border=True):
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        if idioma == "Español (Perú)":
            st.metric(label=t["final_price_label"], value=f"S/. {total_pen:.2f}")
            st.caption(f"Referencia: € {total_eur:.2f}")
        else:
            st.metric(label=t["final_price_label"], value=f"€ {total_eur:.2f}")
            st.caption(f"Ref: S/. {total_pen:.2f}")
    with col_res2:
        ahorro_est = (total_eur * 0.25)
        ahorro_pen = ahorro_est * st.session_state.tasa
        if idioma == "Español (Perú)":
            st.success(f"{t['savings_title']} **¡Ahorraste S/. {ahorro_pen:.2f}!**")
        else:
            st.success(f"{t['savings_title']} **Ahorro: € {ahorro_est:.2f}**")
            st.caption(f"Ref: S/. {ahorro_pen:.2f}")

# --- 7. CIERRE Y WHATSAPP (Lógica Corregida) ---
st.warning(t["note"])
# Agrégalo justo debajo de st.warning(t["note"])
st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #fdf2d9; border-radius: 5px; border: 1px solid #f9e2af; color: #856404; margin: 15px 0;'>{t['social_proof']}</div>", unsafe_allow_html=True)

# Si el usuario NO ha puesto el nombre o el personaje
if not nombre_c or not nombre_p:
    st.info(t["warning_input"]) # Aquí sale el aviso que pides
else:
        # Lógica para el TOTAL en WhatsApp
    moneda_wa = f"S/. {total_pen:.2f}" if idioma == "Español (Perú)" else f"€ {total_eur:.2f}"
        
        # Lógica para el DISEÑO en WhatsApp (¡Aquí estaba el detalle!)
        # Asumiendo que tienes una variable con el costo en soles o la calculas aquí
    diseno_pen = costo_d * st.session_state.tasa  
    moneda_diseno = f"S/. {diseno_pen:.2f}" if idioma == "Español (Perú)" else f"€ {costo_d:.2f}"

        # Generamos el mensaje usando la nueva variable 'moneda_diseno'
        # Generamos el mensaje limpio
    msg = (f"{t['wa_header']}\n"
               f"--------------------------\n"
               f"👤 Cliente: {nombre_c}\n"
               f"👾 Figura: {nombre_p}\n"
               f"📏 Altura: {altura}cm\n"
               f"💧 Impresión: {dif}\n"
               f"🖌️ Pintura: {nv_p}\n"
               f"🧊 Diseño: {moneda_diseno}\n"
               f"--------------------------\n"
               f"💰 TOTAL ESTIMADO {moneda_wa}")
    wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"
    st.markdown("""
    <div style="background-color: #f0f2f6; border-left: 5px solid #ffa500; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <small style="color: #31333F;">
            💡 <b>Nota del Experto:</b> Este presupuesto es una estimación base. 
            El precio final se confirma tras revisar la complejidad del diseño 3D. 
            ¡Envíame tu archivo y ajustamos los detalles!
        </small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #1A1C24; border: 2px solid #FF4B2B; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 20px;">📲</span> 
        <strong style="color: #FF4B2B;">¿Los botones no funcionan?</strong><br>
        <p style="font-size: 0.9rem; color: white; margin-top: 5px;">
        Si vienes de TikTok, pulsa los <b>tres puntos (⋮)</b> y elige <b>'Abrir en navegador externo'</b> para poder enviarnos tu pedido.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
    st.success(t["thanks"])
import streamlit.components.v1 as components

# --- SECCIÓN DEL PORTAFOLIO ---
st.divider() # Esto pone una línea divisoria estética
st.header("✨ Portafolio Premium - Maker 3D Perú")

# Aquí es donde pegas el código HTML largo que te envié antes
html_portafolio = """
<!DOCTYPE html>
<html lang="es">
<head>
    </head>
<body>
    </body>
</html>
"""

# Esta línea es la que hace la magia de mostrarlo en la web
components.html(html_portafolio, height=800, scrolling=True)
st.divider()

# --- 8. REDES SOCIALES ---
st.markdown(f"#### {t['social_title']}")
col_social = st.columns(4)
with col_social[0]: st.link_button("📸 Instagram", "https://www.instagram.com/maker_3d_peru_it", use_container_width=True)
with col_social[1]: st.link_button("🎬 TikTok", "https://www.tiktok.com/@maker3dperu.it", use_container_width=True)
with col_social[2]: st.link_button("📺 YouTube", "https://www.youtube.com/@Maker3dPeru.italia", use_container_width=True)
with col_social[3]: st.link_button("👤 Facebook", "https://www.facebook.com/Maker.3d.Peru", use_container_width=True)

st.write("")
st.markdown(f"<p style='text-align: center; color: #888888; font-size: 0.8rem;'>❤️ Diseñado por Maker 3D Perú | Envíos nacionales e internacionales</p>", unsafe_allow_html=True)
