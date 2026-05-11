import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cotizador 3D - Oferta de Lanzamiento", page_icon="🎨")

st.title("🚀 Cotizador 3D: ¡Promoción de Apertura!")
st.info("🎁 Aprovecha nuestros precios especiales por inicio de operaciones. ¡Calidad premium a costo de taller!")

# --- SECCIÓN: PARÁMETROS DE COSTOS ---
# Precios de "mercado" para mostrar el ahorro
MERCADO_BLENDER = 20.0
MERCADO_PINTURA = 15.0

# Tus precios de lanzamiento (AJUSTADOS)
PRECIO_RESINA_ML = 0.03  # 30€ el litro
PRECIO_HORA_BLENDER = 11.0 
PRECIO_HORA_PINTURA = 8.5
TASA_CAMBIO_SOLS = 4.10 

with st.sidebar:
    st.header("⚙️ Configuración Interna")
    resina_base = st.number_input("Precio Resina por ml (€)", value=PRECIO_RESINA_ML, format="%.3f")
    hora_blender = st.number_input("Tu precio Blender (€/h)", value=PRECIO_HORA_BLENDER)
    hora_pintura = st.number_input("Tu precio Pintura (€/h)", value=PRECIO_HORA_PINTURA)
    
    st.divider()
    st.header("💱 Tasa de Cambio")
    tasa_soles = st.number_input("1 Euro (€) equivale a:", value=TASA_CAMBIO_SOLS)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["💧 Impresión (Resina ABS)", "🖌️ Pintura Artística", "🧊 Diseño/Blender"])

with tab1:
    st.header("Detalles de Impresión")
    st.caption("Usamos resina tipo ABS para mayor resistencia a impactos.")
    volumen = st.number_input("Volumen total (ml)", min_value=0.0, step=1.0)
    cantidad = st.number_input("Cantidad de copias", min_value=1, step=1)
    dificultad_imp = st.select_slider("Complejidad de la pieza", options=["Baja", "Media", "Alta"])
    
    extra_limpieza = {"Baja": 1.5, "Media": 3.0, "Alta": 6.0}
    costo_impresion_eur = (volumen * resina_base * cantidad) + extra_limpieza[dificultad_imp]

with tab2:
    st.header("Acabado y Pintura")
    quiere_pintura = st.checkbox("¿Deseas que pintemos tu figura?")
    horas_p = 0.0
    if quiere_pintura:
        horas_p = st.number_input("Horas de trabajo estimadas", min_value=0.0, step=0.5)
    costo_pintura_eur = horas_p * hora_pintura
    ahorro_pintura = horas_p * (MERCADO_PINTURA - PRECIO_HORA_PINTURA)

with tab3:
    st.header("Diseño y Ajustes en Blender")
    quiere_diseno = st.checkbox("¿Necesitas modelado o reparación de archivo?")
    horas_b = 0.0
    if quiere_diseno:
        horas_b = st.number_input("Horas de diseño", min_value=0.0, step=0.5)
    costo_diseno_eur = horas_b * hora_blender
    ahorro_blender = horas_b * (MERCADO_BLENDER - PRECIO_HORA_BLENDER)

# --- TOTALES Y EFECTO PSICOLÓGICO ---
st.divider()

total_eur = costo_impresion_eur + costo_pintura_eur + costo_diseno_eur
total_pen = total_eur * tasa_soles
ahorro_total_eur = ahorro_pintura + ahorro_blender

col1, col2 = st.columns(2)
col1.metric("PRECIO LANZAMIENTO", f"€ {total_eur:,.2f}", delta=f"S/. {total_pen:,.2f}", delta_color="normal")
if ahorro_total_eur > 0:
    col2.success(f"✨ ¡Te estás ahorrando € {ahorro_total_eur:,.2f} con esta oferta!")

st.subheader("📊 Comparativa de Inversión")
datos_tabla = [
    {"Servicio": "Impresión 3D ABS", "Euros (€)": f"{costo_impresion_eur:,.2f}", "Soles (S/.)": f"{costo_impresion_eur * tasa_soles:,.2f}"},
    {"Servicio": "Pintura (Oferta)", "Euros (€)": f"{costo_pintura_eur:,.2f}", "Soles (S/.)": f"{costo_pintura_eur * tasa_soles:,.2f}"},
    {"Servicio": "Blender (Oferta)", "Euros (€)": f"{costo_diseno_eur:,.2f}", "Soles (S/.)": f"{costo_diseno_eur * tasa_soles:,.2f}"},
]
st.table(datos_tabla)

if st.button("Generar Resumen para WhatsApp"):
    texto = (f"🔥 *COTIZACIÓN ESPECIAL LANZAMIENTO* 🔥\\n"
             f"------------------------------------\\n"
             f"✅ Total a pagar: € {total_eur:.2f} / S/. {total_pen:.2f}\\n"
             f"💰 Tu ahorro hoy: € {ahorro_total_eur:.2f}\\n"
             f"------------------------------------\\n"
             f"📦 Incluye lavado, curado y remoción de soportes.\\n"
             f"🛡️ Material: Resina ABS-Like de alta resistencia.")
    st.code(texto)
