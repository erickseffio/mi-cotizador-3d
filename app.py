import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="3D Quote Pro", page_icon="🎨", initial_sidebar_state="collapsed")

# --- 2. DICCIONARIO DE TRADUCCIONES ---
texts = {
    "Español": {
        "title": "🚀 Cotizador 3D Pro",
        "info": "🎁 Calidad premium a precio de taller.",
        "admin_label": "🔐 Panel Admin",
        "project_data": "📝 Datos del Proyecto",
        "your_name": "Tu Nombre",
        "char_name": "Personaje",
        "upload_img": "Sube una imagen",
        "tabs": ["💧 Impresión", "🖌️ Pintura", "🧊 Blender"],
        "height": "Altura (cm)",
        "complexity": "Complejidad",
        "levels_opt": ["Baja", "Media", "Alta"],
        "paint_opt": ["Básico", "Vitrina", "Museo"],
        "design_opt": [
            "Ajuste Simple (Escalar, reparar, unir piezas)", 
            "Modificación Media (Añadir base, cortar, textos)", 
            "Diseño Complejo (Modelado desde cero)"
        ],
        "include_paint": "¿Incluir pintura?",
        "level": "Nivel de Acabado",
        "include_design": "¿Ajustes de diseño?",
        "total": "PRECIO FINAL (EUR)",
        "savings": "¡Ahorras!",
        "send_wa": "📲 Enviar por WhatsApp",
        "wa_msg": "¡Hola! Soy {name}. He cotizado a {char}. Total: {price}. ¿Cómo procedemos?"
    },
    "English": {
        "title": "🚀 3D Configurator Pro",
        "info": "🎁 Premium quality at workshop prices.",
        "admin_label": "🔐 Admin Panel",
        "project_data": "📝 Project Details",
        "your_name": "Your Name",
        "char_name": "Character Name",
        "upload_img": "Upload a reference image",
        "tabs": ["💧 Printing", "🖌️ Painting", "🧊 Blender"],
        "height": "Height (cm)",
        "complexity": "Complexity",
        "levels_opt": ["Low", "Medium", "High"],
        "paint_opt": ["Basic", "Display Case", "Museum Quality"],
        "design_opt": [
            "Simple Adjustment (Scale, repair, join parts)", 
            "Medium Modification (Add base, cut, texts)", 
            "Complex Design (Modeling from scratch)"
        ],
        "include_paint": "Include painting?",
        "level": "Finish Level",
        "include_design": "Design adjustments?",
        "total": "FINAL PRICE (EUR)",
        "savings": "You save!",
        "send_wa": "📲 Send via WhatsApp",
        "wa_msg": "Hi! I'm {name}. I quoted {char}. Total: {price}. How do we proceed?"
    },
    "Italiano": {
        "title": "🚀 Preventivo 3D Pro",
        "info": "🎁 Qualità premium a prezzi di bottega.",
        "admin_label": "🔐 Pannello Admin",
        "project_data": "📝 Dettagli del Progetto",
        "your_name": "Il tuo Nome",
        "char_name": "Nome del Personaggio",
        "upload_img": "Carica un'immagine",
        "tabs": ["💧 Stampa 3D", "🖌️ Pittura", "🧊 Blender"],
        "height": "Altezza (cm)",
        "complexity": "Complessità",
        "levels_opt": ["Bassa", "Media", "Alta"],
        "paint_opt": ["Base", "Vetrina", "Museo"],
        "design_opt": [
            "Regolazione Semplice (Scalare, riparare, unire pezzi)", 
            "Modifica Media (Aggiungere base, tagliare, testi)", 
            "Design Complesso (Modellazione da zero)"
        ],
        "include_paint": "Includere pittura?",
        "level": "Livello di Finitura",
        "include_design": "Modifiche di design?",
        "total": "PREZZO FINALE (EUR)",
        "savings": "Risparmi!",
        "send_wa": "📲 Invia su WhatsApp",
        "wa_msg": "Ciao! Sono {name}. Ho fatto un preventivo per {char}. Totale: {price}. Come procediamo?"
    }
}

# --- 3. SELECTOR DE IDIOMA ---
idioma = st.selectbox("🌐 Language / Idioma / Lingua", ["Español", "English", "Italiano"])
t = texts[idioma]

st.title(t["title"])
st.info(t["info"])

# --- 4. VALORES INTERNOS ---
PRECIO_RESINA_ML, PRECIO_HORA_BLENDER, PRECIO_HORA_PINTURA, TASA_CAMBIO_SOLS = 0.03, 11.0, 8.5, 4.10

with st.sidebar:
    st.header(t["admin_label"])
    clave = st.text_input("Password", type="password")
    if clave == "admin123":
        resina_base = st.number_input("Resina ml (€)", value=PRECIO_RESINA_ML, format="%.3f")
        hora_blender = st.number_input("Blender (€/h)", value=PRECIO_HORA_BLENDER)
        hora_pintura = st.number_input("Pintura (€/h)", value=PRECIO_HORA_PINTURA)
        tasa_soles = st.number_input("Tasa S/.", value=TASA_CAMBIO_SOLS)
    else:
        resina_base, hora_blender, hora_pintura, tasa_soles = PRECIO_RESINA_ML, PRECIO_HORA_BLENDER, PRECIO_HORA_PINTURA, TASA_CAMBIO_SOLS

# --- 5. DATOS DEL PROYECTO ---
st.subheader(t["project_data"])
c_n1, c_n2 = st.columns(2)
with c_n1:
    nombre_cliente = st.text_input(t["your_name"])
    nombre_personaje = st.text_input(t["char_name"])
with c_n2:
    img = st.file_uploader(t["upload_img"], type=['png', 'jpg', 'jpeg'])

# --- 6. PESTAÑAS Y CÁLCULOS ---
tab1, tab2, tab3 = st.tabs(t["tabs"])

with tab1:
    altura = st.number_input(t["height"], min_value=0.0, value=10.0)
    vol = (altura ** 2.2) * 0.15 if altura > 0 else 0
    dif = st.select_slider(t["complexity"], options=t["levels_opt"])
    extra_cost = {t["levels_opt"][0]: 1.5, t["levels_opt"][1]: 3.0, t["levels_opt"][2]: 6.0}
    costo_imp = (vol * resina_base) + extra_cost[dif] if altura > 0 else 0

with tab2:
    quiere_p = st.checkbox(t["include_paint"])
    horas_p = 0.0
    if quiere_p:
        nv_p = st.select_slider(t["level"], options=t["paint_opt"], key="p")
        mult_p = {t["paint_opt"][0]: 1, t["paint_opt"][1]: 2.5, t["paint_opt"][2]: 5}
        horas_p = st.number_input("Hours", value=round((altura/5)*mult_p[nv_p], 1))
    costo_p = horas_p * hora_pintura

with tab3:
    quiere_b = st.checkbox(t["include_design"])
    horas_b = 0.0
    if quiere_b:
        tipo_b = st.selectbox("Type", t["design_opt"])
        # Mapeo de horas según la descripción seleccionada
        mapa_h = {t["design_opt"][0]: 1.0, t["design_opt"][1]: 3.0, t["design_opt"][2]: 8.0}
        horas_b = st.number_input("Design Hours", value=mapa_h[tipo_b])
    costo_b = horas_b * hora_blender

# --- 7. RESULTADOS ---
total_eur = costo_imp + costo_p + costo_b
total_pen = total_eur * tasa_soles
ahorro = (horas_p * (15 - hora_pintura)) + (horas_b * (20 - hora_blender))

st.divider()
c1, c2 = st.columns(2)
c1.metric(t["total"], f"€ {total_eur:,.2f}", f"S/. {total_pen:,.2f}", delta_color="normal")
if ahorro > 0: c2.success(f"✨ {t['savings']} € {ahorro:,.2f}")

# --- WHATSAPP ---
msg = t["wa_msg"].format(name=nombre_cliente, char=nombre_personaje, price=f"€ {total_eur:.2f} (S/. {total_pen:.2f})")
# RECUERDA CAMBIAR ESTE NÚMERO POR EL TUYO:
wa_link = f"https://wa.me/51999888777?text={urllib.parse.quote(msg)}"

st.link_button(t["send_wa"], wa_link)

with st.expander("Dettagli / Details / Detalles"):
    st.write(f"Impresión: € {costo_imp:.2f}")
    st.write(f"Pintura: € {costo_p:.2f}")
    st.write(f"Diseño: € {costo_b:.2f}")
