import streamlit as st
import urllib.parse
from fpdf import FPDF
import tempfile
import re
import io

from fpdf import FPDF # fpdf2 usa el mismo nombre de importación

def generar_pdf(c_imp, c_dis, c_pin, tasa, total_final, t, logo_path, imagen_figura, descuento_val, simbolo):
    pdf = FPDF()
    pdf.add_page()
    
    color_primario = (44, 62, 80) 
    color_acento = (52, 152, 219)
    
    # 1. ESTA FUNCIÓN ES LA CLAVE: Maneja el Euro correctamente para el PDF
    def limpiar_formatear(texto, symb):
        limpio = str(texto).replace("€", "").replace("S/.", "").replace("$", "").strip()
        # Si el símbolo es Euro, usamos el código 128 que entiende el PDF
        s_pdf = chr(128) if "€" in symb else symb
        return f"{s_pdf} {limpio}"

    def formatear_texto(texto):
        # Aquí también nos aseguramos de que cualquier Euro en el texto se convierta
        return str(texto).replace("€", chr(128)).encode('latin-1', 'replace').decode('latin-1')

    # --- CABECERA (Tu código está perfecto aquí) ---
    if logo_path:
        try: pdf.image(logo_path, 12, 12, 32) 
        except: pass
    
    pdf.set_font("Helvetica", 'B', 18)
    pdf.set_text_color(*color_primario)
    pdf.set_y(20)
    pdf.cell(0, 10, formatear_texto(t.get("pdf_title", "PRESUPUESTO")).upper(), ln=True, align='R')
    
    pdf.set_draw_color(*color_acento)
    pdf.set_line_width(0.8)
    pdf.line(10, 52, 200, 52)
    pdf.ln(30)

    # --- CONTENIDO ---
    y_detalle = pdf.get_y()
    pdf.set_font("Helvetica", 'B', 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(90, 8, formatear_texto("DETALLES DEL PROYECTO"), ln=True)
    pdf.ln(2)

    def fila_estilizada(label, valor_texto):
        pdf.set_font("Helvetica", 'B', 10)
        pdf.set_text_color(*color_primario)
        pdf.cell(65, 9, formatear_texto(label), border='B')
        pdf.set_font("Helvetica", '', 10)
        # Aquí usamos la función de limpieza mejorada
        valor_final = limpiar_formatear(valor_texto, simbolo)
        pdf.cell(30, 9, formatear_texto(valor_final), border='B', ln=True, align='R')

    fila_estilizada(t.get('pdf_imp', 'Costo de Impresión'), c_imp)
    fila_estilizada(t.get('pdf_dis', 'Costo de Diseño'), c_dis)
    fila_estilizada(t.get('pdf_pin', 'Costo de Pintura'), c_pin)

    # --- 2. SECCIÓN DEL TOTAL (Asegúrate de tener esto al final) ---
    pdf.set_y(y_detalle + 70) 
    
    # Descuento dinámico
    if descuento_val > 0:
        pdf.set_font("Helvetica", 'I', 10)
        pdf.set_text_color(231, 76, 60)
        s_desc = chr(128) if "€" in simbolo else simbolo
        pdf.cell(100, 8, formatear_texto(f"{t.get('pdf_desc', 'Descuento')}: -{s_desc} {descuento_val:.2f}"), align='R', ln=True)

    # Bloque de Total dinámico
    pdf.set_fill_color(*color_primario)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", 'B', 14)
    
    s_total = chr(128) if "€" in simbolo else simbolo
    etiqueta_total = t.get('final_quote', 'Inversión Estimada')
    texto_total = f"{etiqueta_total}: {s_total} {total_final:.2f}"
    
    pdf.cell(100, 14, formatear_texto(texto_total), ln=True, align='C', fill=True)

    # --- PIE DE PÁGINA ---
    pdf.set_y(-25)
    pdf.set_font("Helvetica", 'I', 8)
    pdf.set_text_color(170, 170, 170)
    pdf.cell(0, 10, "MAKER 3D PERU - Arte y Tecnologia en cada detalle", align='C')

    return bytes(pdf.output())
    
# 1. Configuración de la página (ACTUALIZADO)
st.set_page_config(
    page_title="Maker3DPeru-Italia", 
    page_icon="Logo.jpg", 
    initial_sidebar_state="collapsed" # <-- Esto cierra el panel al inicio
)

# --- AJUSTE DE TAMAÑO Y LIMPIEZA DE INTERFAZ (CSS AGRESIVO) ---
st.markdown("""
    <style>
        /* 1. Mantenemos tu espacio superior para el contenido */
        .main .block-container {
            padding-top: 5rem !important;
        }

        /* 2. ELIMINACIÓN RADICAL DE LA BARRA SUPERIOR */
        /* Esto elimina la franja negra completa donde están Fork y GitHub */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            border-bottom: none !important;
        }

        /* Oculta todos los elementos de la derecha (Fork, GitHub, Menú) */
        [data-testid="stHeaderActionElements"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 3. BORRAR ICONOS INFERIORES (Logo Streamlit y Perfil) */
        [data-testid="stStatusWidget"], .stDeployButton, footer {
            display: none !important;
            visibility: hidden !important;
        }

        /* 4. EL BOTÓN MAESTRO (La flecha de la izquierda) */
        /* Forzamos que la flecha para tu panel de control sea lo único vivo */
        button[data-testid="stBaseButton-headerNoPadding"] {
            display: inline-flex !important;
            position: fixed !important;
            top: 10px !important;
            left: 10px !important;
            z-index: 999999 !important;
            opacity: 0.2; /* Casi invisible para que no estorbe el diseño */
        }
        
        button[data-testid="stBaseButton-headerNoPadding"]:hover {
            opacity: 1; /* Se ve claro cuando pasas el mouse */
        }

        /* Bloqueo extra para el texto "Fork" */
        .stActionButton, .stAppDeployButton {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.dialog("Vista de Obra - Maker 3D Perú", width="medium") # Volvemos al ancho que te gusta
def mostrar_imagen_grande(url, titulo, descripcion):
    # Añadimos espacio físico arriba antes de la imagen
    st.markdown("<br>", unsafe_allow_html=True) 
    
    # Mantén el use_container_width para recuperar el zoom potente
    st.image(url, use_container_width=True)
    
    st.subheader(titulo)
    st.write(descripcion)
    
    if st.button("Cerrar"):
        st.rerun()
        
# --- 2. VALORES ADMINISTRABLES ---
if 'resina' not in st.session_state: st.session_state.resina = 0.03
if 'blender' not in st.session_state: st.session_state.blender = 11.0
if 'pintura' not in st.session_state: st.session_state.pintura = 8.5
if 'tasa' not in st.session_state: st.session_state.tasa = 4.10

with st.sidebar:
    st.header("🔐 Panel de Control")
    clave = st.text_input("Contraseña Admin", type="password")
    
    # REEMPLAZO DE SEGURIDAD:
    if clave == st.secrets["admin_password"]:
        st.success("Acceso Autorizado")
        st.session_state.resina = st.number_input("Resina ml (€)", value=st.session_state.resina, format="%.3f")
        st.session_state.blender = st.number_input("Hora Diseño (€)", value=st.session_state.blender)
        st.session_state.pintura = st.number_input("Hora Pintura (€)", value=st.session_state.pintura)
        st.session_state.tasa = st.number_input("Tasa S/.", value=st.session_state.tasa)

# --- 3. DICCIONARIO DE TRADUCCIONES ---
texts = {
    texts = {
    "Español (Perú S/.)": {
        "simbolo": "S/.",
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Hiper-realismo en Resina: Del archivo digital a tu vitrina.",
        "delivery": "🕒 Entrega: 3 semanas (Desde el depósito del 50%)",
        "wa_num": "51977511500",
        "p_name_label": "Tu Nombre", "char_name_label": "Personaje", "ref_label": "Subir Referencia",
        "p_name_ph": "Ej: Juan Pérez", "char_name_ph": "Ej: Iron Man Mark 85",
        "step1": "1️⃣ Datos del Proyecto", "step2": "2️⃣ Configuración Artística", "step3": "3️⃣ Inversión Estimada",
        "pdf_title": "PRESUPUESTO DE IMPRESIÓN 3D",
        "pdf_imp": "Costo de Impresión", "final_quote": "Inversión Estimada",
        "pdf_dis": "Costo de Diseño", "pdf_pin": "Costo de Pintura",
        "tab_print": "💧 Estructura y Escala ", "tab_paint": "🖌️ Acabado Artístico", "tab_design": "🧊 Diseño",
        "height_label": "Altura (cm)", "height_help": "📏 Guía: Una lata de soda mide 12cm, una figura estándar 18cm.",
        "comp_label": "Complejidad", "comp_opts": ["Coleccionista", "Épico", "Obra Maestra"],
        "paint_check": "¿Incluir Pintura Profesional?", "paint_level": "Nivel de acabado", "paint_opts": ["Básico", "Vitrina", "Museo"],
        "design_label": "Edición Digital", "btn_download": "Descargar PDF con Foto",
        "pdf_desc": "DESCUENTO",
        "design_opts": ["Listo para imprimir", "Ajuste Básico", "Personalizado", "Premium"],
        "final_price_label": "PRECIO ESTIMADO", "saving_label": "Ahorro Aplicado",
        "savings_title": "✨ ¡Descuento de Taller Aplicado!", 
        "wa_btn": "📲 Enviar Pedido a WhatsApp", "note": "⚠️ El inicio de producción requiere el 50% de adelanto.",
        "wa_header": "*NUEVO PEDIDO DETALLADO*",
        "thanks": "✅ **¡Gracias por tu solicitud!** Al abrir WhatsApp, **no olvides adjuntar tu imagen de referencia**.",
        "social_title": "📱 ¡Síguenos en nuestras redes!",
        "social_proof": "Envíos seguros a todo el Perú y el extranjero 📦",
        "port_header": "✨ Portafolio Premium - Maker 3D Perú",
        "port_main_title": "Mi Portafolio", "port_tag": "GALERÍA DE TRABAJOS",
        "port_desc": "Explora nuestras últimas creaciones en resina y pintura artística.",
        "loading_img": "Procesando imagen...", "img_caption": "✅ Imagen cargada correctamente",
        "img_success": "¡Imagen lista para la cotización!", "img_info": "Sube una foto de tu modelo.",
        "warning_input": "⚠️ **Atención:** Ingresa tu Nombre y el Personaje arriba.",
        "footer_text": "Diseñado por Maker 3D Perú | Envíos nacionales e internacionales"
    },
    "Español (España €)": {
        "simbolo": "€",
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Hiper-realismo en Resina: Del archivo digital a tu vitrina.",
        "delivery": "🕒 Entrega: 2 semanas (Desde el depósito del 50%)",
        "wa_num": "393924043068",
        "p_name_label": "Tu Nombre", "char_name_label": "Personaje", "ref_label": "Subir Referencia",
        "p_name_ph": "Ej: Javier García", "char_name_ph": "Ej: Batman (Hush)",
        "step1": "1️⃣ Datos del Proyecto", "step2": "2️⃣ Configuración Artística", "step3": "3️⃣ Inversión Estimada",
        "pdf_title": "PRESUPUESTO DE IMPRESIÓN 3D",
        "pdf_imp": "Costo de Impresión", "final_quote": "Inversión Estimada",
        "pdf_dis": "Costo de Diseño", "pdf_pin": "Costo de Pintura",
        "tab_print": "💧 Estructura y Escala ", "tab_paint": "🖌️ Acabado Artístico", "tab_design": "🧊 Diseño",
        "height_label": "Altura (cm)", "height_help": "📏 Guía: Una lata de soda mide 12cm, una figura estándar 18cm.",
        "comp_label": "Complejidad", "comp_opts": ["Coleccionista", "Épico", "Obra Maestra"],
        "paint_check": "¿Incluir Pintura Profesional?", "paint_level": "Nivel de acabado", "paint_opts": ["Básico", "Vitrina", "Museo"],
        "design_label": "Edición Digital", "btn_download": "Descargar PDF con Foto",
        "pdf_desc": "DESCUENTO",
        "design_opts": ["Listo para imprimir", "Ajuste Básico", "Personalizado", "Premium"],
        "final_price_label": "PRECIO ESTIMADO", "saving_label": "Ahorro Aplicado",
        "savings_title": "✨ ¡Descuento de Taller Aplicado!", 
        "wa_btn": "📲 Enviar Pedido a WhatsApp", "note": "⚠️ El inicio de producción requiere el 50% de adelanto.",
        "wa_header": "*NUEVO PEDIDO DETALLADO*",
        "thanks": "✅ **¡Gracias!** Al abrir WhatsApp, adjunta tu imagen.",
        "social_title": "📱 ¡Síguenos!", "social_proof": "Envíos internacionales garantizados 📦",
        "port_header": "✨ Portafolio Premium - Maker 3D Perú",
        "port_main_title": "Mi Portafolio", "port_tag": "GALERÍA DE TRABAJOS",
        "port_desc": "Arte en resina y pintura artística.",
        "loading_img": "Procesando...", "img_caption": "✅ Imagen OK",
        "img_success": "¡Imagen lista!", "img_info": "Sube una foto.",
        "warning_input": "⚠️ **Atención:** Falta Nombre o Personaje.",
        "footer_text": "Maker 3D Perú | Calidad Profesional"
    },
    "English €": {
        "simbolo": "€",
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Hyper-realism in Resin: From digital file to display case.",
        "delivery": "🕒 Delivery: 3 weeks (After 50% deposit)",
        "wa_num": "393924043068",
        "p_name_label": "Your Name", "char_name_label": "Character", "ref_label": "Upload Reference",
        "p_name_ph": "e.g. John Doe", "char_name_ph": "e.g. Spider-Man",
        "step1": "1️⃣ Project Details", "step2": "2️⃣ Artistic Configuration", "step3": "3️⃣ Estimated Investment",
        "pdf_title": "3D PRINTING BUDGET",
        "pdf_imp": "Printing Cost", "final_quote": "Estimated Investment",
        "pdf_dis": "Design Cost", "pdf_pin": "Paint Cost",
        "tab_print": "💧 Structure and Scale", "tab_paint": "🖌️ Artistic Finish", "tab_design": "🧊 Design",
        "height_label": "Height (cm)", "height_help": "📏 Guide: A soda can is 12cm, a standard figure is 18cm.",
        "comp_label": "Complexity", "comp_opts": ["Collector's Item", "Epic", "Masterpiece"],
        "paint_check": "Include Professional Painting?", "paint_level": "Finish Level", "paint_opts": ["Basic", "Display", "Museum"],
        "design_label": "Digital Editing", "btn_download": "Download PDF with Photo",
        "pdf_desc": "DISCOUNT",
        "design_opts": ["Ready to print", "Basic Adjustment", "Customized", "Premium"],
        "final_price_label": "ESTIMATED PRICE", "saving_label": "Total Savings",
        "savings_title": "✨ Workshop Discount Applied!",
        "wa_btn": "📲 Send Order to WhatsApp", "note": "⚠️ Production starts after 50% deposit.",
        "wa_header": "*NEW DETAILED ORDER*",
        "thanks": "✅ **Thank you!** Please attach your image on WhatsApp.",
        "social_title": "📱 Follow us!", "social_proof": "Secure international shipping 📦",
        "port_header": "✨ Premium Portfolio - Maker 3D Perú",
        "port_main_title": "My portfolio", "port_tag": "WORK GALLERY",
        "port_desc": "Explore our resin creations.",
        "loading_img": "Processing...", "img_caption": "✅ Image uploaded",
        "img_success": "Image ready!", "img_info": "Upload a photo.",
        "warning_input": "⚠️ **Attention:** Enter Name and Character.",
        "footer_text": "Designed by Maker 3D Perú"
    },
    "Italiano €": {
        "simbolo": "€",
        "title": "Maker3DPeru-Italia",
        "slogan": "✨ Iperrealismo in resina: dal file digitale alla teca espositiva.",
        "delivery": "🕒 Consegna: 1 settimana (Dall'acconto del 50%)",
        "wa_num": "393924043068",
        "p_name_label": "Il tuo Nome", "char_name_label": "Personaggio", "ref_label": "Carica Riferimento",
        "p_name_ph": "es: Alessandro Rossi", "char_name_ph": "es: Darth Vader",
        "step1": "1️⃣ Dettagli Progetto", "step2": "2️⃣ Configurazione Artistica", "step3": "3️⃣ Investimento Stimato",
        "pdf_title": "PREVENTIVO DI STAMPA 3D",
        "pdf_it": "Costo di Stampa", "final_quote": "Investimento Stimato",
        "pdf_dis": "Costo del Design", "pdf_pin": "Costo di Pittura",
        "tab_print": "💧 Struttura e proporzioni", "tab_paint": "🖌️ finitura artistica", "tab_design": "🧊 Design",
        "height_label": "Altezza (cm)", "height_help": "📏 Guida: Una lattina misura 12cm, una figura standard 18cm.",
        "comp_label": "Complessità", "comp_opts": ["Oggetto da collezione", "epico", "capolavoro"],
        "paint_check": "Includere Pittura Professionale?", "paint_level": "Livello di finitura", "paint_opts": ["Base", "Vetrina", "Museo"],
        "design_label": "Modifica Digitale", "btn_download": "Scarica PDF con Foto",
        "pdf_desc": "SCONTO",
        "design_opts": ["Pronto per la stampa", "Regolazione Base", "Personalizzato", "Premium"],
        "final_price_label": "PREZZO STIMATO", "saving_label": "Risparmio Applicato",
        "savings_title": "✨ Sconto per il workshop applicato!",
        "wa_btn": "📲 Invia Ordine su WhatsApp", "note": "⚠️ Il lavoro inizia dopo l'acconto del 50%.",
        "wa_header": "*NUOVO ORDINE DETTAGLIATO*",
        "thanks": "✅ **Grazie!** Non dimenticare di allegare l'immagine.",
        "social_title": "📱 Seguici!", "social_proof": "Spedizioni sicure e garantite 📦",
        "port_header": "✨ Portfolio Premium - Maker 3D Perú",
        "port_main_title": "Il Mio Portfolio", "port_tag": "GALLERIA LAVORI",
        "port_desc": "Esplora le nostre ultime creazioni.",
        "loading_img": "Elaborazione...", "img_caption": "✅ Immagine caricata",
        "img_success": "Immagine pronta!", "img_info": "Carica una foto.",
        "warning_input": "⚠️ **Attenzione:** Inserisci Nome e Personaggio.",
        "footer_text": "Design di Maker 3D Perú"
    }
}
idioma = st.selectbox("🌐 Idioma", ["Español (Perú S/.)", "Español (España €)", "English €", "Italiano €"])
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
        # Cargador de archivos usando la etiqueta del idioma seleccionado
        archivo_reference = st.file_uploader(t["ref_label"], type=['png', 'jpg', 'jpeg'])

        if archivo_reference is not None:
            # st.spinner mostrará el mensaje en el idioma actual
            with st.spinner(t.get("loading_img", "Processing...")):
                try:
                    # Muestra la imagen con su descripción traducida
                    st.image(archivo_reference, caption=t.get("img_caption", "Uploaded image"), use_container_width=True)
                    # Cuadro verde de éxito traducido
                    st.success(t.get("img_success", "✅ Done!"))
                except Exception:
                    st.error("Error")
        else:
            # Mensaje informativo traducido cuando no hay archivo
            st.info(t.get("img_info", "Please upload an image."))

st.header(t["step2"])
tab1, tab2, tab3 = st.tabs([t["tab_print"], t["tab_paint"], t["tab_design"]])

# --- TAB 1: ESTRUCTURA Y ESCALA ---
with tab1:
    altura = st.number_input(t["height_label"], 5, 100, 15)
    st.caption(t["height_help"])
    
    # Creamos una 'key' única basada en el idioma seleccionado
    # Esto obliga al slider a reiniciarse sin errores al cambiar de idioma
    idioma_key = t["final_quote"].replace(" ", "_") 
    
    opciones_comp = t.get("comp_opts", ["Básico", "Medio", "Alto"])
    
    dif = st.select_slider(
        t["comp_label"], 
        options=opciones_comp,
        key=f"slider_comp_{idioma_key}" # <--- LA SOLUCIÓN ESTÁ AQUÍ
    )

    idx_comp = opciones_comp.index(dif)
    valores_extra = [1.5, 3.0, 6.0]
    extra = valores_extra[min(idx_comp, len(valores_extra)-1)]
    
    vol = (altura ** 2.2) * 0.15
    costo_imp = (vol * st.session_state.resina) + extra

# --- TAB 2: ACABADO ARTÍSTICO ---
with tab2:
    quiere_p = st.checkbox(t["paint_check"])
    nv_p, costo_p = "No", 0.0
    
    if quiere_p:
        opciones_p = t.get("paint_opts", ["Básico", "Vitrina", "Museo"])
        
        nv_p = st.select_slider(
            t["paint_level"], 
            options=opciones_p,
            key=f"slider_paint_{idioma_key}" # <--- LA SOLUCIÓN ESTÁ AQUÍ
        )
            
        idx_p = opciones_p.index(nv_p)
        multiplicadores = [1, 2.5, 5]
        mult = multiplicadores[min(idx_p, len(multiplicadores)-1)]
        
        horas_p = (altura / 5) * mult
        costo_p = horas_p * st.session_state.pintura
with tab3:
    st.subheader(t["design_label"])
    
    # El cliente ve la descripción completa sin el precio
    tipo_d = st.selectbox("Opciones de diseño:", t["design_opts"])
    
    # Obtenemos la posición de la opción elegida (0, 1, 2 o 3)
    idx = t["design_opts"].index(tipo_d)
    
    # Definimos los precios fijos en una lista que coincida con el orden de las opciones
    # 0 = Gratis, 1 = 10€, 2 = 25€, 3 = 60€
    precios = [0.0, 10.0, 25.0, 60.0]
    
    # Asignamos el costo basado en el índice
    costo_d = precios[idx]
    
  
        
# --- 6. PRESUPUESTO ---
st.header(t["step3"])
total_eur = costo_imp + costo_p + costo_d
total_pen = total_eur * st.session_state.tasa

# 1. Calculamos los ahorros primero para que las variables existan siempre
ahorro_est = (total_eur * 0.25)
ahorro_pen = ahorro_est * st.session_state.tasa

# 2. Definimos qué textos mostrar según el idioma
# IMPORTANTE: Revisa si tu idioma es "Español (Perú S/.)" o "Español (Perú)"
if "Perú" in idioma: 
    monto_principal = f"S/. {total_pen:.2f}"
    sub_ref = f"Ref: € {total_eur:.2f}"
    ahorro_texto = f"S/. {ahorro_pen:.2f}"
else:
    monto_principal = f"€ {total_eur:.2f}"
    sub_ref = f"Ref: S/. {total_pen:.2f}"
    ahorro_texto = f"€ {ahorro_est:.2f}"

# 3. Diseño visual
with st.container(border=True):
    col_res1, col_res2 = st.columns([1.5, 1])
    
    with col_res1:
        st.markdown(f"""
            <div style="padding:10px;">
                <p style="color:#808495; margin:0; text-transform:uppercase; font-size:0.8rem; font-weight:bold;">
                    {t["final_quote"]}
                </p>
                <h1 style="margin:0; color:white; font-size:3.5rem; line-height:1.2;">
                    {monto_principal}
                </h1>
                <p style="color:#808495; margin:0; font-size:0.9rem;">
                    {sub_ref}
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_res2:
        # Bloque de Ahorro tipo tarjeta verde
        st.markdown(f"""
            <div style="background-color:#142d1a; padding:20px; border-radius:10px; border: 1px solid #234d2c; margin-top:15px;">
                <p style="color:#4ecb71; margin:0; font-size:1rem; font-weight:bold;">
                        \u2728 {t['savings_title']}
                </p>
                <h2 style="margin:0; color:#4ecb71; font-size:1.8rem;">
                    {ahorro_texto}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
# --- 7. CIERRE Y ACCIONES (Versión Final Corregida) ---
st.warning(t["note"])
st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #fdf2d9; border-radius: 5px; border: 1px solid #f9e2af; color: #856404; margin: 15px 0;'>{t['social_proof']}</div>", unsafe_allow_html=True)

# Si el usuario NO ha puesto el nombre o el personaje
if not nombre_c or not nombre_p:
    st.info(t["warning_input"]) 
else:
    # 1. Definición de Monedas y Totales
    if "Perú" in idioma:
        moneda_wa = f"S/. {total_pen:.2f}"
        moneda_diseno = f"S/. {(costo_d * st.session_state.tasa):.2f}"
        ahorro_wsp_val = ahorro_pen 
        simbolo = "S/."
    else:
        moneda_wa = f"€ {total_eur:.2f}"
        moneda_diseno = f"€ {costo_d:.2f}"
        ahorro_wsp_val = ahorro_est 
        simbolo = "€"

    # 2. Generación del Mensaje de WhatsApp
    mapa_detalles = {}
    for lang in texts:
        opts = texts[lang]["design_opts"]
        details = texts[lang]["design_details"]
        for i in range(len(opts)):
            mapa_detalles[opts[i]] = details[i]
            
    msg = (f"{t['wa_header']}\n"
           f"--------------------------\n"
           f"👤 Cliente: {nombre_c}\n"
           f"👾 Figura: {nombre_p}\n"
           f"📏 Altura: {altura}cm\n"
           f"💧 Impresión: {dif}\n"
           f"🖌️ Pintura: {nv_p}\n"
           f"🧊 Diseño: {moneda_diseno}\n"
           f"📝 Detalle: {mapa_detalles[tipo_d]}\n"
           f"✨ DESCUENTO: {simbolo} {ahorro_wsp_val:.2f}\n"
           f"--------------------------\n"
           f"💎 {t['final_quote']}: {moneda_wa}")
    
    import urllib.parse
    wa_link = f"https://wa.me/{t['wa_num']}?text={urllib.parse.quote(msg)}"

    # 3. Bloques de Información Estética
    st.markdown("""
    <div style="background-color: #f0f2f6; border-left: 5px solid #ffa500; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        <small style="color: #31333F;">
            💡 <b>Nota del Experto:</b> Este presupuesto es una estimación base. El precio final se confirma tras revisar la complejidad del diseño 3D.
        </small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color: #1A1C24; border: 1px solid #FF4B2B; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 20px;">📲</span> 
        <strong style="color: #FF4B2B;">¿Los botones no funcionan?</strong><br>
        <p style="font-size: 0.8rem; color: white; margin-top: 5px;">
        Si vienes de TikTok, pulsa los <b>tres puntos (⋮)</b> y elige <b>'Abrir en navegador'</b> para descargar el PDF.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 4. BOTONES EN COLUMNAS (SOLUCIÓN DEFINITIVA DE CARGA)
st.write("---")

# Verificamos si hay un total calculado
hay_calculo = ('total_eur' in locals() and total_eur > 0) or ('total_pen' in locals() and total_pen > 0)

if hay_calculo:
    st.success(t.get("thanks", "¡Gracias por tu solicitud!"))
    col_pdf, col_wa = st.columns(2)

    with col_pdf:
        try:
            # 1. FORZAMOS EL SÍMBOLO DINÁMICO (Crucial)
            # Nos aseguramos de que 'simb' sea exactamente lo que el diccionario actual dice
            simb_pdf = t.get("simbolo", "€") 
            
            # 2. LIMPIEZA DE VARIABLES PARA EL PDF
            v_imp = f"{costo_imp:.2f}" if 'costo_imp' in locals() else "0.00"
            # Quitamos cualquier símbolo que se haya colado en el diseño
            v_dis = str(moneda_diseno).replace("€", "").replace("S/.", "").strip() if 'moneda_diseno' in locals() else "0.00"
            v_pin = f"{costo_p:.2f}" if 'costo_p' in locals() else "0.00"
            v_desc = ahorro_wsp_val if 'ahorro_wsp_val' in locals() else 0.0
            
            # 3. SELECCIÓN DEL TOTAL CORRECTO
            # Si el idioma elegido es "Español (Perú)", usamos total_pen, si no, total_eur
            t_pagar = total_pen if "Perú" in idioma else total_eur
    
            # 4. LLAMADA A LA FUNCIÓN (Fíjate en el último parámetro: simb_pdf)
            pdf_output = generar_pdf(
                v_imp, 
                v_dis, 
                v_pin, 
                st.session_state.tasa, 
                t_pagar, 
                t, 
                "Logo.jpg", 
                archivo_reference, 
                v_desc, 
                simb_pdf  # <--- AQUÍ LE PASAMOS EL SÍMBOLO QUE ACABAMOS DE CALCULAR
            )
            
            pdf_bytes = bytes(pdf_output)
    
            st.download_button(
                label=f"📥 {t.get('btn_download', 'Descargar PDF')}",
                data=pdf_bytes,
                file_name=f"Presupuesto_{nombre_p}.pdf",
                mime="application/pdf",
                key="download_pdf_btn",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error al generar el PDF: {e}")
    
    with col_wa:
        if 'wa_link' in locals() and wa_link:
            st.link_button(t["wa_btn"], wa_link, use_container_width=True, type="primary")
        else:
            st.info("Ingresa nombre y personaje arriba")
else:
    st.info("👋 Ingresa los datos para ver las opciones de presupuesto.")
    
# --- SECCIÓN PORTAFOLIO REFINADA ---
# --- SECCIÓN PORTAFOLIO RECUPERADA Y ADAPTABLE ---
st.markdown("""
<style>
    /* 1. Definición general de la tarjeta */
    .card {
        background: #1e1e1e;
        border-radius: 12px;
        border: 1px solid #333;
        overflow: hidden;
        height: 340px; 
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }
    
   .card-img {
        width: 100%;
        height: 160px; /* Aumentamos un poco el alto del contenedor */
        object-fit: contain; /* Esto evita que la imagen se corte o se estire */
        padding-top: 20px; /* <--- ESTO ES LO QUE BAJA LA FOTO */
        background-color: #1e1e1e; /* Asegura que el fondo combine con la tarjeta */
    }
    
    .card-text {
        padding: 15px;
        flex-grow: 1; 
    }
    
    .card-text h3 {
        color: #ff4b4b !important;
        font-size: 1.2rem !important;
        margin-bottom: 8px !important;
    }
    
    .card-text p {
        color: #ffffff !important; /* Blanco para mejor lectura */
        font-size: 1.05rem !important; /* Tamaño cómodo para celular y PC */
        line-height: 1.4 !important;
    }

    /* 2. Ajuste para pantallas pequeñas */
    @media (max-width: 768px) {
        .card {
            height: auto !important; /* En celular crece según el texto */
            min-height: 380px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Título de la sección (CORREGIDO PARA IDIOMAS)
st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <span style="font-size: 2.2rem; margin-right: 12px;">🎨</span>
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; color: #ffffff;">
            {t.get('port_main_title', 'Mi Portafolio')} <span style="color: #ff4b4b; font-size: 0.9rem; vertical-align: middle;">| Maker 3D Perú</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Función para renderizar cada obra (CORREGIDA)
def render_obra(col, img_url, title, description, key_btn):
    with col:
        st.markdown(f'''<div class="card">
            <img src="{img_url}" class="card-img">
            <div class="card-text">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
        </div>''', unsafe_allow_html=True)
        
        # Cambiamos "🔍 Detalles" por una f-string que usa el diccionario t
        label_boton = f"🔍 {t.get('btn_details', 'Detalles')}"
        
        if st.button(label_boton, key=key_btn, use_container_width=True):
            mostrar_imagen_grande(img_url, title, description)

# Llamadas a la función con tus datos
render_obra(col1, "https://i.postimg.cc/4NVvxmL4/20260502-113047.jpg", "Digimon", t['desc_digimon'], "btn_d_new")
render_obra(col2, "https://i.postimg.cc/tJC0CKyn/20260331-230329.jpg", "Hyoga", t['desc_hyoga'], "btn_h_new")
render_obra(col3, "https://i.postimg.cc/76wdmFCv/20250718-124326.jpg", "Albafica", t['desc_albafica'], "btn_a_new")
# --- 8. REDES SOCIALES ---
st.markdown(f"#### {t['social_title']}")
col_social = st.columns(4)
with col_social[0]: st.link_button("📸 Instagram", "https://www.instagram.com/maker_3d_peru_it", use_container_width=True)
with col_social[1]: st.link_button("🎬 TikTok", "https://www.tiktok.com/@maker3dperu.it", use_container_width=True)
with col_social[2]: st.link_button("📺 YouTube", "https://www.youtube.com/@Maker3dPeru.italia", use_container_width=True)
with col_social[3]: st.link_button("👤 Facebook", "https://www.facebook.com/Maker.3d.Peru", use_container_width=True)

st.write("")
st.markdown(f"""
    <div style="text-align: center; color: #888; padding: 20px; font-size: 0.9rem;">
        💗 {t['footer_text']}
    </div>
""", unsafe_allow_html=True)
