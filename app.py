import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cotizador 3D Pro - Altura", page_icon="🎨")

st.title("🚀 Cotizador 3D: Presupuesto por Tamaño")
st.info("🎁 ¡Precios de Lanzamiento activos! Todo se calcula en base a la altura de tu figura.")

# --- SECCIÓN: PARÁMETROS DE COSTOS ---
PRECIO_RESINA_ML = 0.03  
PRECIO_HORA_BLENDER = 11.0 
PRECIO_HORA_PINTURA = 8.5
TASA_CAMBIO_SOLS = 4.10 

with st.sidebar:
    st.header("⚙️ Configuración Interna")
    resina_base = st.number_input("Precio Resina por ml (€)", value=PRECIO_RESINA_ML, format="%.3f")
    hora_blender = st.number_input("Precio Blender (€/h)", value=PRECIO_HORA_BLENDER)
    hora_pintura = st.number_input("Precio Pintura (€/h)", value=PRECIO_HORA_PINTURA)
    tasa_soles = st.number_input("Tasa de cambio (1€ a S/.)", value=TASA_CAMBIO_SOLS)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["💧 Impresión 3D", "🖌️ Pintura Artística", "🧊 Diseño/Blender"])

with tab1:
    st.header("Detalles de Impresión")
    altura = st.number_input("Altura de la figura (cm)", min_value=1.0, value=10.0, step=1.0)
    cantidad = st.number_input("¿Cuántas copias?", min_value=1, value=1)
    
    # FÓRMULA AUTOMÁTICA DE VOLUMEN (Híbrida)
    # Estimamos volumen basado en altura para una figura humana estándar
    # Volumen aprox = (Altura^2.2) * 0.15 (Fórmula ajustada para miniaturas y figuras)
    volumen_estimado = (altura ** 2.2) * 0.15
    
    st.caption(f"📦 Volumen estimado para {altura}cm: ~{volumen_estimado:.1f} ml")
    
    dificultad_imp = st.select_slider("Complejidad de la pieza", options=["Baja", "Media", "Alta"])
    extra_limpieza = {"Baja": 1.5, "Media": 3.0, "Alta": 6.0}
    costo_impresion_eur = (volumen_estimado * resina_base * cantidad) + extra_limpieza[dificultad_imp]

with tab2:
    st.header("Acabado y Pintura")
    quiere_pintura = st.checkbox("¿Deseas servicio de pintura?")
    horas_p = 0.0
    if quiere_pintura:
        nivel = st.select_slider("Nivel de detalle deseado", options=["Básico", "Avanzado", "Pro/Museo"])
        # Sugerencia de horas basada en ALTURA y NIVEL
        base_h = (altura / 5) # Una figura de 10cm base son 2h
        mult_nivel = {"Básico": 1, "Avanzado": 2.5, "Pro/Museo": 5}
        sugerencia = base_h * mult_nivel[nivel]
        
        horas_p = st.number_input(f"Horas estimadas para {altura}cm ({nivel})", min_value=0.0, value=round(sugerencia, 1), step=0.5)
    costo_pintura_eur = horas_p * hora_pintura

with tab3:
    st.header("Diseño en Blender")
    quiere_diseno = st.checkbox("¿Necesitas ajustes de diseño?")
    horas_b = 0.0
    if quiere_diseno:
        horas_b = st.number_input("Horas de diseño/modelado", min_value=0.0, value=1.0, step=0.5)
    costo_diseno_eur = horas_b * hora_blender

# --- TOTALES ---
st.divider()
total_eur = costo_impresion_eur + costo_pintura_eur + costo_diseno_eur
total_pen = total_eur * tasa_soles

c1, c2 = st.columns(2)
c1.metric("PRECIO TOTAL (€)", f"€ {total_eur:,.2f}")
c2.metric("PRECIO TOTAL (S/.)", f"S/. {total_pen:,.2f}")

# Mensaje de acción
st.divider()
if st.button("Generar Resumen para WhatsApp"):
    resumen = (f"👋 ¡Hola! He cotizado una pieza de {altura}cm:\\n"
               f"------------------------------------\\n"
               f"📏 Altura: {altura}cm ({volumen_estimado:.1f}ml est.)\\n"
               f"🖌️ Pintura: {horas_p}h | Diseño: {horas_b}h\\n"
               f"💰 TOTAL ESTIMADO: €{total_eur:.2f} / S/. {total_pen:.2f}\\n"
               f"------------------------------------\\n"
               f"¿Me podrían dar una cotización final con mi archivo?")
    st.code(resumen)
    st.success("Copia este texto y envíanoslo por WhatsApp.")
