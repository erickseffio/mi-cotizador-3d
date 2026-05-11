import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cotizador 3D Pro - Híbrido", page_icon="🎨")

st.title("🚀 Cotizador 3D: Presupuesto Instantáneo")
st.markdown("""
    *Usa esta calculadora para obtener un estimado. Para una cotización formal, 
    envíanos tu archivo .STL o .OBJ por WhatsApp.*
""")

# --- SECCIÓN: PARÁMETROS DE COSTOS (Precios de Lanzamiento) ---
PRECIO_RESINA_ML = 0.03  # Basado en 30€/litro
PRECIO_HORA_BLENDER = 11.0 
PRECIO_HORA_PINTURA = 8.5
TASA_CAMBIO_SOLS = 4.10 

with st.sidebar:
    st.header("⚙️ Configuración (Solo tú)")
    resina_base = st.number_input("Precio Resina por ml (€)", value=PRECIO_RESINA_ML, format="%.3f")
    hora_blender = st.number_input("Precio Blender (€/h)", value=PRECIO_HORA_BLENDER)
    hora_pintura = st.number_input("Precio Pintura (€/h)", value=PRECIO_HORA_PINTURA)
    tasa_soles = st.number_input("Tasa de cambio (1€ a S/.)", value=TASA_CAMBIO_SOLS)
    st.info("💡 Estos valores son internos. El cliente verá el resultado final basado en ellos.")

# --- INTERFAZ: GUÍA DE AYUDA ---
with st.expander("❓ ¿No sabes cuántos ml tiene tu figura? Mira esta guía"):
    st.write("""
    * **Miniatura (3-5 cm):** 5 a 12 ml aprox.
    * **Figura Mediana (10-12 cm):** 25 a 40 ml aprox.
    * **Busto o Figura Grande (18-20 cm):** 80 a 150 ml aprox.
    * *Nota: El volumen depende del grosor y si la pieza es hueca o sólida.*
    """)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["💧 Impresión 3D", "🖌️ Pintura Artística", "🧊 Diseño/Blender"])

with tab1:
    st.header("Detalles de Impresión")
    col_a, col_b = st.columns(2)
    with col_a:
        volumen = st.number_input("Volumen estimado (ml)", min_value=0.0, value=10.0, step=1.0)
    with col_b:
        cantidad = st.number_input("¿Cuántas copias?", min_value=1, value=1)
    
    dificultad_imp = st.select_slider("Complejidad de la pieza", options=["Baja", "Media", "Alta"])
    extra_limpieza = {"Baja": 1.5, "Media": 3.0, "Alta": 6.0}
    costo_impresion_eur = (volumen * resina_base * cantidad) + extra_limpieza[dificultad_imp]

with tab2:
    st.header("Acabado y Pintura")
    quiere_pintura = st.checkbox("¿Deseas servicio de pintura?")
    horas_p = 0.0
    if quiere_pintura:
        nivel = st.select_slider("Nivel de detalle", options=["Básico", "Avanzado", "Pro/Museo"])
        # Multiplicador de horas sugerido
        sugerencia_h = {"Básico": 1.0, "Avanzado": 3.0, "Pro/Museo": 6.0}
        horas_p = st.number_input(f"Horas estimadas (Sugerido para {nivel}: {sugerencia_h[nivel]}h)", min_value=0.0, value=sugerencia_h[nivel], step=0.5)
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

# Botón para el flujo híbrido
st.divider()
st.subheader("📲 Paso Final")
st.write("Si estás de acuerdo con este estimado, genera el resumen y envíanoslo para confirmar.")

if st.button("Generar Resumen para enviar por WhatsApp"):
    resumen = (f"👋 ¡Hola! He cotizado mi pieza en la web:\\n"
               f"------------------------------------\\n"
               f"📍 Detalle: {volumen}ml | Impresión: €{costo_impresion_eur:.2f}\\n"
               f"🖌️ Pintura: {horas_p}h | Diseño: {horas_b}h\\n"
               f"💰 TOTAL ESTIMADO: €{total_eur:.2f} / S/. {total_pen:.2f}\\n"
               f"------------------------------------\\n"
               f"¿Me confirman para enviarles el archivo?")
    st.code(resumen)
    st.success("Copia el texto de arriba y pégalo en nuestro chat de WhatsApp.")
