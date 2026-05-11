import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="3D Studio Quote", page_icon="🎨")

# --- 2. HEADER CON IDENTIDAD ---
col_logo, col_name = st.columns([1, 3])
with col_logo:
    # Reemplaza con tu logo real cuando lo subas a GitHub
    st.image("https://cdn-icons-png.flaticon.com/512/1720/1720516.png", width=100)
with col_name:
    st.markdown("# TU EMPRESA 3D")
    st.caption("Especialistas en Resina ABS-Like de Alta Definición")

# --- 3. DICCIONARIO DE TRADUCCIONES DETALLADO ---
texts = {
    "Español": {
        "step1": "1️⃣ Cuéntanos sobre tu proyecto",
        "step2": "2️⃣ Configura los detalles técnicos",
        "step3": "3️⃣ Revisa y envía tu pedido",
        "wa_num": "51910034696",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "p_name": "Tu nombre completo",
        "char_name": "Nombre del personaje / figura",
        "img_help": "Sube una foto o captura de lo que quieres imprimir",
        "paint_help": "Selecciona el nivel de pintura que deseas",
        "design_help": "Selecciona si el archivo necesita retoques",
        "total_label": "VALOR TOTAL ESTIMADO",
        "payment_note": "⚠️ El trabajo inicia tras confirmar el 50% de adelanto.",
        "wa_btn": "📲 Solicitar Pedido vía WhatsApp Perú",
        "detail_summary": "📝 Resumen de tu configuración:"
    },
    "English": {
        "step1": "1️⃣ Tell us about your project",
        "step2": "2️⃣ Technical configuration",
        "step3": "3️⃣ Review and send order",
        "wa_num": "3934567890", # Reemplazar con número de Italia
        "delivery": "🕒 Delivery: 1.5 weeks (After 50% deposit)",
        "p_name": "Your full name",
        "char_name": "Character / Figure name",
        "img_help": "Upload a screenshot of what you want to print",
        "paint_help": "Select your desired painting level",
        "design_help": "Select if the file needs adjustments",
        "total_label": "ESTIMATED TOTAL VALUE",
        "payment_note": "⚠️ Project starts after 50% down payment is confirmed.",
        "wa_btn": "📲 Send Order via WhatsApp Europe",
        "detail_summary": "📝 Configuration Summary:"
    },
    "Italiano": {
        "step1": "1️⃣ Raccontaci del tuo progetto",
        "step2": "2️⃣ Configurazione tecnica",
        "step3": "3️⃣ Revisione e invio ordine",
        "wa_num": "3934567890", # Reemplazar con número de Italia
        "delivery": "🕒 Consegna: 1.5 settimane (Dal deposito del 50%)",
        "p_name": "Il tuo nome completo",
        "char_name": "Nome del personaggio",
        "img_help": "Carica uno screenshot di ciò che vuoi stampare",
        "paint_help": "Seleziona il livello di pittura desiderato",
        "design_help": "Seleziona se il file necessita di modifiche",
        "total_label": "VALORE TOTALE ESTIMATO",
        "payment_note": "⚠️ Il lavoro inizia dopo la conferma dell'acconto del 50%.",
        "wa_btn": "📲 Invia Ordine via WhatsApp Italia",
        "detail_summary": "📝 Riepilogo configurazione:"
    }
}

idioma = st.selectbox("🌐 Selecciona tu idioma / Select Language / Seleziona Lingua", ["Español", "English", "Italiano"])
t = texts[idioma]
st.divider()

# --- 4. VALORES DE ADMINISTRACIÓN (OCULTOS) ---
PRECIO_RESINA_ML, PRECIO_HORA_BLENDER, PRECIO_HORA_PINTURA, TASA_CAMBIO_SOLS = 0.03, 11.0, 8.5, 4.10

# --- 5. PASO 1: DATOS ---
st.header(t["step1"])
c1, c2 = st.columns(2)
with c1:
    nombre_cliente = st.text_input(t["p_name"], placeholder="Ej: Mario Rossi")
    nombre_personaje = st.text_input(t["char_name"], placeholder="Ej: Seiya de Pegaso")
with c2:
    img = st.file_uploader(t["img_help"], type=['png', 'jpg', 'jpeg'])

# --- 6. PASO 2: CONFIGURACIÓN ---
st.header(t["step2"])
tab1, tab2, tab3 = st.tabs(["💧 Impresión (ABS)", "🖌️ Pintura Artística", "🧊 Ajustes Blender"])

with tab1:
    altura = st.number_input("Altura de la figura (cm)", min_value=5.0, max_value=100.0, value=15.0)
    # Lista de opciones de complejidad para evitar errores de traducción
    opts_comp = ["Simple", "Orgánico", "Épico"] if idioma == "Español" else (["Simple", "Organic", "Epic"] if idioma == "English" else ["Semplice", "Organico", "Epico"])
    dif = st.select_slider("Nivel de detalle de la pieza", options=opts_comp)
    
    vol = (altura ** 2.2) * 0.15
    extra = {opts_comp[0]: 1.5, opts_comp[1]: 3.0, opts_comp[2]: 6.0}
    costo_imp = (vol * PRECIO_RESINA_ML) + extra[dif]

with tab2:
    st.write(t["paint_help"])
    quiere_p = st.checkbox("¿Deseas que la pintemos a mano?")
    nv_p, costo_p = "No", 0.0
    if quiere_p:
        opts_p = ["Básico", "Vitrina", "Museo"] if idioma == "Español" else (["Basic", "Display", "Museum"] if idioma == "English" else ["Base", "Vetrina", "Museo"])
        nv_p = st.select_slider("Calidad del acabado", options=opts_p)
        mult = {opts_p[0]: 1, opts_p[1]: 2.5, opts_p[2]: 5}
        horas_p = (altura/5) * mult[nv_p]
        costo_p = horas_p * PRECIO_HORA_PINTURA

with tab3:
    st.write(t["design_help"])
    quiere_b = st.checkbox("¿El archivo necesita modificaciones?")
    tipo_b, costo_b = "No", 0.0
    if quiere_b:
        opts_b = ["Simple", "Medio", "Complejo"] if idioma == "Español" else (["Simple", "Medium", "Complex"] if idioma == "English" else ["Semplice", "Medio", "Complesso"])
        tipo_b = st.selectbox("Tipo de intervención", opts_b)
        horas_b = {opts_b[0]: 1.0, opts_b[1]: 3.0, opts_b[2]: 8.0}
        costo_b = horas_b[tipo_b] * PRECIO_HORA_BLENDER

# --- 7. PASO 3: RESUMEN Y ENVÍO ---
st.header(t["step3"])
total_eur = costo_imp + costo_p + costo_b
total_pen = total_eur * TASA_CAMBIO_SOLS

with st.container(border=True):
    st.subheader(t["total_label"])
    st.title(f"€ {total_eur:.2f}")
    st.write(f"Equivalente aproximado: **S/. {total_pen:.2f}**")
    st.caption(t["delivery"])

    # Resumen visual para que el cliente confirme antes de irse
    st.write(t["detail_summary"])
    col_res1, col_res2 = st.columns(2)
    col_res1.write(f"- Altura: {altura}cm")
    col_res1.write(f"- Detalle: {dif}")
    col_res2.write(f"- Pintura: {nv_p}")
    col_res2.write(f"- Diseño: {tipo_b}")

# --- BOTÓN DE WHATSAPP ---
msg = (
    f"🚀 *SOLICITUD DE PEDIDO 3D*\n"
    f"------------------------------------\n"
    f"👤 *Cliente:* {nombre_cliente}\n"
    f"👾 *Figura:* {nombre_personaje}\n"
    f"📏 *Tamaño:* {altura} cm\n"
    f"🧪 *Material:* Resina ABS-Like\n"
    f"⚙️ *Detalle:* {dif}\n"
    f"🖌️ *Pintura:* {nv_p}\n"
    f"🧊 *Diseño:* {tipo_b}\n"
    f"------------------------------------\n"
    f"💰 *PRECIO TOTAL: € {total_eur:.2f}*\n"
    f"🕒 *TIEMPO:* {t['delivery']}\n"
    f"------------------------------------\n"
    f"✅ El cliente confirma conocimiento del adelanto del 50%."
)

st.warning(t["payment_note"])
wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"

if nombre_cliente and nombre_personaje:
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
else:
    st.error("⚠️ Por favor, escribe tu nombre y el del personaje en el Paso 1 para habilitar el envío.")
