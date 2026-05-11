import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Cotizador 3D Resina Pro", page_icon="🎨")

st.title("🚀 Cotizador de Impresión 3D y Arte")
st.markdown("Calcula el costo de tu proyecto de resina, diseño y pintura en Euros y Soles.")

# --- SECCIÓN: PARÁMETROS DE COSTOS PERMANENTES ---
# 30 euros el litro = 0.03 euros por ml
PRECIO_RESINA_ML = 0.03  
PRECIO_HORA_BLENDER = 20.0
PRECIO_HORA_PINTURA = 15.0
TASA_CAMBIO_SOLS = 4.10 

with st.sidebar:
    st.header("⚙️ Configuración de Costos (€)")
    resina_base = st.number_input("Precio Resina por ml (€)", value=PRECIO_RESINA_ML, format="%.3f")
    hora_blender = st.number_input("Precio Hora Blender (€)", value=PRECIO_HORA_BLENDER)
    hora_pintura = st.number_input("Precio Hora Pintura (€)", value=PRECIO_HORA_PINTURA)
    
    st.divider()
    st.header("💱 Tasa de Cambio")
    tasa_soles = st.number_input("1 Euro (€) equivale a:", value=TASA_CAMBIO_SOLS)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["💧 Impresión", "🖌️ Pintura", "🧊 Diseño Blender"])

with tab1:
    st.header("Detalles de Impresión")
    volumen = st.number_input("Volumen total de la pieza (ml) - Incluye soportes", min_value=0.0, step=1.0)
    cantidad = st.number_input("Cantidad de copias", min_value=1, step=1)
    dificultad_imp = st.select_slider("Complejidad de limpieza/curado", options=["Baja", "Media", "Alta"])
    
    extra_limpieza = {"Baja": 1.5, "Media": 3.0, "Alta": 6.0}
    costo_impresion_eur = (volumen * resina_base * cantidad) + extra_limpieza[dificultad_imp]

with tab2:
    st.header("Servicio de Pintura")
    quiere_pintura = st.checkbox("¿Requiere pintura?")
    horas_p = 0.0
    if quiere_pintura:
        horas_p = st.number_input("Estimación de horas de pintura", min_value=0.0, step=0.5)
    costo_pintura_eur = horas_p * hora_pintura

with tab3:
    st.header("Diseño en Blender")
    quiere_diseno = st.checkbox("¿Requiere modelado o ajustes en Blender?")
    horas_b = 0.0
    if quiere_diseno:
        horas_b = st.number_input("Horas estimadas de diseño/reparación", min_value=0.0, step=0.5)
    costo_diseno_eur = horas_b * hora_blender

# --- TOTALES Y COMPARATIVA ---
st.divider()
total_eur = costo_impresion_eur + costo_pintura_eur + costo_diseno_eur
total_pen = total_eur * tasa_soles

# Mostrar el total resaltado en ambas monedas
c1, c2 = st.columns(2)
c1.metric("TOTAL EN EUROS", f"€ {total_eur:,.2f}")
c2.metric("TOTAL EN SOLES", f"S/. {total_pen:,.2f}")

st.subheader("📊 Desglose Detallado")

# Crear una tabla comparativa
datos_tabla = [
    {"Concepto": "Impresión 3D", "Euros (€)": f"{costo_impresion_eur:,.2f}", "Soles (S/.)": f"{costo_impresion_eur * tasa_soles:,.2f}"},
    {"Concepto": "Pintura", "Euros (€)": f"{costo_pintura_eur:,.2f}", "Soles (S/.)": f"{costo_pintura_eur * tasa_soles:,.2f}"},
    {"Concepto": "Diseño Blender", "Euros (€)": f"{costo_diseno_eur:,.2f}", "Soles (S/.)": f"{costo_diseno_eur * tasa_soles:,.2f}"},
]

st.table(datos_tabla)

if st.button("Generar Resumen para WhatsApp"):
    texto = (f"Costo Total: € {total_eur:.2f} / S/. {total_pen:.2f}\\n"
             f"------------------------------\\n"
             f"- Impresión: € {costo_impresion_eur:.2f} (S/. {costo_impresion_eur * tasa_soles:.2f})\\n"
             f"- Pintura: € {costo_pintura_eur:.2f} (S/. {costo_pintura_eur * tasa_soles:.2f})\\n"
             f"- Blender: € {costo_diseno_eur:.2f} (S/. {costo_diseno_eur * tasa_soles:.2f})")
    st.code(texto)
