import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cotizador 3D Resina Pro", page_icon="🎨")

st.title("🚀 Cotizador de Impresión 3D y Arte")
st.markdown("Calcula el costo de tu proyecto de resina, diseño y pintura al instante.")

# --- SECCIÓN: PARÁMETROS DE COSTOS PERMANENTES ---
# 30 euros el litro = 0.03 euros por ml
PRECIO_RESINA_ML = 0.03  
PRECIO_HORA_BLENDER = 20.0
PRECIO_HORA_PINTURA = 15.0
TASA_CAMBIO_SOLS = 4.10 # Puedes ajustar este valor según el día

with st.sidebar:
    st.header("⚙️ Configuración de Costos (€)")
    resina_base = st.number_input("Precio Resina por ml (€)", value=PRECIO_RESINA_ML, format="%.3f")
    hora_blender = st.number_input("Precio Hora Blender (€)", value=PRECIO_HORA_BLENDER)
    hora_pintura = st.number_input("Precio Hora Pintura (€)", value=PRECIO_HORA_PINTURA)
    
    st.divider()
    st.header("💱 Conversión a Soles")
    ver_en_soles = st.checkbox("Mostrar precios en Soles (S/.)")
    tasa_soles = st.number_input("Tasa de cambio (1€ a Soles)", value=TASA_CAMBIO_SOLS)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["💧 Impresión", "🖌️ Pintura", "🧊 Diseño Blender"])

with tab1:
    st.header("Detalles de Impresión")
    volumen = st.number_input("Volumen total de la pieza (ml) - Incluye soportes", min_value=0.0, step=1.0)
    cantidad = st.number_input("Cantidad de copias", min_value=1, step=1)
    dificultad_imp = st.select_slider("Complejidad de limpieza/curado", options=["Baja", "Media", "Alta"])
    
    # Extras por insumos (alcohol, guantes, etc.) en Euros
    extra_limpieza = {"Baja": 1.5, "Media": 3.0, "Alta": 6.0}
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
total_eur = costo_impresion + costo_pintura + costo_diseno

col1, col2 = st.columns(2)

if ver_en_soles:
    total_pen = total_eur * tasa_soles
    col1.metric("TOTAL ESTIMADO", f"S/. {total_pen:,.2f}")
    col2.write(f"**Desglose en Soles:**")
    col2.write(f"* Impresión: S/. {costo_impresion * tasa_soles:,.2f}")
    col2.write(f"* Pintura: S/. {costo_pintura * tasa_soles:,.2f}")
    col2.write(f"* Blender: S/. {costo_diseno * tasa_soles:,.2f}")
else:
    col1.metric("TOTAL ESTIMADO", f"€ {total_eur:,.2f}")
    col2.write(f"**Desglose en Euros:**")
    col2.write(f"* Impresión: € {costo_impresion:,.2f}")
    col2.write(f"* Pintura: € {costo_pintura:,.2f}")
    col2.write(f"* Blender: € {costo_diseno:,.2f}")

if st.button("Generar Resumen para WhatsApp"):
    moneda = "S/." if ver_en_soles else "€"
    valor = total_eur * tasa_soles if ver_en_soles else total_eur
    texto = f"Cotización 3D: Total {moneda} {valor:.2f} (Resina ABS, Pintura y Diseño)"
    st.code(texto)
