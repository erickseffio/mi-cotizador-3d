import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="3D Studio Quote", page_icon="🎨")

# --- 2. HEADER ---
col_logo, col_name = st.columns([1, 3])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/1720/1720516.png", width=100)
with col_name:
    st.markdown("# TU EMPRESA 3D")
    st.caption("Resina ABS-Like de Alta Definición")

# --- 3. DICCIONARIO (SECCIÓN DE DISEÑO ACTUALIZADA) ---
texts = {
    "Español": {
        "step1": "1️⃣ Cuéntanos sobre tu proyecto",
        "step2": "2️⃣ Configura los detalles técnicos",
        "step3": "3️⃣ Revisa y envía tu pedido",
        "wa_num": "51910034696",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "p_name": "Tu nombre", "char_name": "Nombre de la figura",
        "img_help": "Sube una imagen de referencia",
        "tab_design": "🧊 Ajustes de Diseño", # <--- CAMBIO AQUÍ
        "design_help": "Selecciona si tu archivo necesita trabajo de edición digital",
        "design_opt": [
            "Listo para imprimir (No requiere ajustes)",
            "Ajuste Básico (Escalar, reparar archivo, unir piezas)",
            "Personalización (Añadir nombre, base especial, cortes)",
            "Diseño Premium (Modelado o cambios estructurales)"
        ],
        "total_label": "VALOR TOTAL ESTIMADO",
        "payment_note": "⚠️ El trabajo inicia tras confirmar el 50% de adelanto.",
        "wa_btn": "📲 Solicitar Pedido vía WhatsApp Perú",
        "detail_summary": "📝 Resumen de tu configuración:"
    },
    "English": {
        "step1": "1️⃣ Project details",
        "step2": "2️⃣ Technical configuration",
        "step3": "3️⃣ Review & Send",
        "wa_num": "3934567890",
        "delivery": "🕒 Delivery: 1.5 weeks (After 50% deposit)",
        "p_name": "Your name", "char_name": "Character name",
        "img_help": "Upload reference image",
        "tab_design": "🧊 Design Adjustments", # <--- CAMBIO AQUÍ
        "design_help": "Select if your file needs digital editing",
        "design_opt": [
            "Ready to print (No adjustments needed)",
            "Basic Fix (Scaling, repairing, joining parts)",
            "Customization (Add name, special base, cuts)",
            "Premium Design (Structural changes or modeling)"
        ],
        "total_label": "ESTIMATED TOTAL",
        "payment_note": "⚠️ Project starts after 50% deposit.",
        "wa_btn": "📲 Send Order via WhatsApp Europe",
        "detail_summary": "📝 Summary:"
    },
    "Italiano": {
        "step1": "1️⃣ Dettagli del progetto",
        "step2": "2️⃣ Configurazione tecnica",
        "step3": "3️⃣ Revisione e invio",
        "wa_num": "3934567890",
        "delivery": "🕒 Consegna: 1.5 settimane (Dal deposito del 50%)",
        "p_name": "Il tuo nome", "char_name": "Nome del personaggio",
        "img_help": "Carica immagine",
        "tab_design": "🧊 Modifiche Digitali", # <--- CAMBIO AQUÍ
        "design_help": "Seleziona se il file necessita di editing digitale",
        "design_opt": [
            "Pronto da stampare (Nessuna modifica)",
            "Regolazione Base (Scalare, riparare, unire pezzi)",
            "Personalizzazione (Aggiungere nome, base, tagli)",
            "Design Premium (Modellazione o modifiche strutturali)"
        ],
        "total_label": "TOTALE STIMATO",
        "payment_note": "⚠️ Il lavoro inizia dopo l'acconto del 50%.",
        "wa_btn": "📲 Invia Ordine via WhatsApp Italia",
        "detail_summary": "📝 Riepilogo:"
    }
}

idioma = st.selectbox("🌐 Idioma / Language", ["Español", "English", "Italiano"])
t = texts[idioma]

# --- 4. PASO 1: DATOS ---
st.header(t["step1"])
c1, c2 = st.columns(2)
with c1:
    nombre_cliente = st.text_input(t["p_name"])
    nombre_personaje = st.text_input(t["char_name"])
with c2:
    img = st.file_uploader(t["img_help"], type=['png', 'jpg', 'jpeg'])

# --- 5. PASO 2: CONFIGURACIÓN ---
st.header(t["step2"])
tab1, tab2, tab3 = st.tabs(["💧 Impresión", "🖌️ Pintura", t["tab_design"]])

# ... (Cálculos de Impresión y Pintura se mantienen igual) ...
with tab1:
    altura = st.number_input("Altura (cm)", 5.0, 100.0, 15.0)
    opts_comp = ["Simple", "Orgánico", "Épico"]
    dif = st.select_slider("Complejidad", options=opts_comp)
    costo_imp = ((altura ** 2.2) * 0.0045) + (3.0 if dif != "Simple" else 1.5)

with tab2:
    quiere_p = st.checkbox("¿Deseas pintura?")
    nv_p, costo_p = "No", 0.0
    if quiere_p:
        opts_p = ["Básico", "Vitrina", "Museo"]
        nv_p = st.select_slider("Nivel de acabado", options=opts_p)
        costo_p = (altura/5) * (8.5 if nv_p == "Museo" else 4.5)

with tab3:
    st.write(t["design_help"])
    # El selector ahora usa las nuevas descripciones
    tipo_b = st.selectbox("Tipo de trabajo digital", t["design_opt"])
    
    # Mapeo de costos basado en la opción elegida
    costos_b = {t["design_opt"][0]: 0.0, t["design_opt"][1]: 10.0, t["design_opt"][2]: 25.0, t["design_opt"][3]: 60.0}
    costo_b = costos_b[tipo_b]

# --- 6. RESUMEN Y WHATSAPP ---
total_eur = costo_imp + costo_p + costo_b
total_pen = total_eur * 4.10

st.header(t["step3"])
with st.container(border=True):
    st.subheader(t["total_label"])
    st.title(f"€ {total_eur:.2f}")
    st.write(f"S/. {total_pen:.2f}")
    
    st.write(t["detail_summary"])
    st.write(f"- {altura}cm | {dif} | Pintura: {nv_p} | Edición: {tipo_b}")

msg = (f"SOLICITUD: {nombre_personaje}\n"
       f"Cliente: {nombre_cliente}\n"
       f"Altura: {altura}cm\n"
       f"Edición Digital: {tipo_b}\n"
       f"Pintura: {nv_p}\n"
       f"TOTAL: € {total_eur:.2f}\n"
       f"Nota: Entrega en {t['delivery']}")

wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"
st.warning(t["payment_note"])

if nombre_cliente and nombre_personaje:
    st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
