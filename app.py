import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cotizador 3D Resina", page_icon="🎨")

st.title("🚀 Cotizador de Impresión 3D y Arte")
st.markdown("Calcula el costo de tu proyecto de resina, diseño y pintura al instante.")

# --- SECCIÓN: PARÁMETROS DE COSTOS (Puedes editarlos aquí) ---
PRECIO_RESINA_ML = 0.15  # Ejemplo: $0.15 por ml
PRECIO_HORA_BLENDER = 20.0
PRECIO_HORA_PINTURA = 15.0

with st.sidebar:
    st.header("Configuración de Precios")
    resina_base = st.number_input("Precio Resina por ml ($)", value=PRECIO_RESINA_ML)
    hora_blender = st.number_input("Precio Hora Blender ($)", value=PRECIO_HORA_BLENDER)
    hora_pintura = st.number_input("Precio Hora Pintura ($)", value=PRECIO_HORA_PINTURA)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["💧 Impresión", "🖌️ Pintura", "🧊 Diseño Blender"])

with tab1:
    st.header("Detalles de Impresión")
    volumen = st.number_input("Volumen total de la pieza (ml) - Incluye soportes", min_value=0.0, step=1.0)
    cantidad = st.number_input("Cantidad de copias", min_value=1, step=1)
    dificultad_imp = st.select_slider("Complejidad de limpieza/curado", options=["Baja", "Media", "Alta"])
    
    extra_limpieza = {"Baja": 2.0, "Media": 5.0, "Alta": 10.0}
    costo_impresion = (volumen * resina_base * cantidad) + extra_limpieza[dificultad_imp]

with tab2:
    st.header("Servicio de Pintura")
    quiere_pintura = st.checkbox("¿Requiere pintura?")
    horas_p = 0.0
    if quiere_pintura:
        nivel = st.selectbox("Nivel de acabado", ["Base (1 color)", "Tabletop (Detalle medio)", "Coleccionista (Detalle alto)"])
        horas_p = st.number_input("Estimación de horas de pintura", min_value=0.0, step=0.5)
    
    costo_pintura = horas_p * hora_pintura

with tab3:
    st.header("Diseño en Blender")
    quiere_diseno = st.checkbox("¿Requiere modelado o ajustes en Blender?")
    horas_b = 0.0
    if quiere_diseno:
        horas_b = st.number_input("Horas estimadas de diseño/reparación", min_value=0.0, step=0.5)
    
    costo_diseno = horas_b * hora_blender

# --- TOTALES ---
st.divider()
total_final = costo_impresion + costo_pintura + costo_diseno

col1, col2 = st.columns(2)
col1.metric("TOTAL ESTIMADO", f"${total_final:,.2f}")
col2.write(f"""
**Desglose:**
* Impresión: ${costo_impresion:,.2f}
* Pintura: ${costo_pintura:,.2f}
* Blender: ${costo_diseno:,.2f}
""")

if st.button("Generar Resumen para WhatsApp"):
    texto = f"Cotización 3D: Total ${total_final:.2f} (Imp: ${costo_impresion:.2f}, Pint: ${costo_pintura:.2f}, Blender: ${costo_diseno:.2f})"
    st.code(texto) # El usuario puede copiar y pegar esto