import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Cotizador 3D - Oferta Lanzamiento", 
    page_icon="🎨", 
    initial_sidebar_state="collapsed" # Esto la mantiene cerrada al inicio
)

st.title("🚀 Cotizador 3D: ¡Promoción de Apertura!")
st.info("🎁 Calidad premium a precio de taller. ¡Aprovecha nuestros descuentos de inauguración!")

# --- SECCIÓN: PARÁMETROS DE COSTOS ---
MERCADO_BLENDER = 20.0
MERCADO_PINTURA = 15.0

PRECIO_RESINA_ML = 0.03  
PRECIO_HORA_BLENDER = 11.0 
PRECIO_HORA_PINTURA = 8.5
TASA_CAMBIO_SOLS = 4.10 

with st.sidebar:
    st.header("⚙️ Configuración Interna")
    resina_base = st.number_input("Precio Resina por ml (€)", value=PRECIO_RESINA_ML, format="%.3f")
    hora_blender = st.number_input("Tu precio Blender (€/h)", value=PRECIO_HORA_BLENDER)
    hora_pintura = st.number_input("Tu precio Pintura (€/h)", value=PRECIO_HORA_PINTURA)
    tasa_soles = st.number_input("Tasa de cambio (1€ a S/.)", value=TASA_CAMBIO_SOLS)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["💧 Impresión 3D (ABS)", "🖌️ Pintura Artística", "🧊 Diseño/Blender"])

with tab1:
    st.header("Detalles de Impresión")
    st.write("*(Deja en 0 si solo deseas diseño o pintura)*")
    # CAMBIO AQUÍ: Ahora el mínimo es 0.0
    altura = st.number_input("Altura de la figura (cm)", min_value=0.0, value=10.0, step=1.0)
    cantidad = st.number_input("Cantidad de copias", min_value=1, value=1)
    
    if altura > 0:
        volumen_estimado = (altura ** 2.2) * 0.15
        st.caption(f"📦 Volumen estimado: ~{volumen_estimado:.1f} ml (Resina ABS-Like)")
        dificultad_imp = st.select_slider("Complejidad de la pieza", options=["Baja", "Media", "Alta"])
        extra_limpieza = {"Baja": 1.5, "Media": 3.0, "Alta": 6.0}
        costo_impresion_eur = (volumen_estimado * resina_base * cantidad) + extra_limpieza[dificultad_imp]
    else:
        costo_impresion_eur = 0.0
        st.write("⚠️ No se ha incluido servicio de impresión.")

with tab2:
    st.header("Servicio de Pintura")
    quiere_pintura = st.checkbox("¿Deseas incluir pintura?")
    horas_p = 0.0
    ahorro_pintura = 0.0
    if quiere_pintura:
        nivel_p = st.select_slider("Nivel de acabado", options=["Básico", "Avanzado", "Pro/Museo"], key="pintura")
        # Si la altura es 0, usamos una base de 5cm para el cálculo o permitimos manual
        h_referencia = altura if altura > 0 else 5.0
        base_h = (h_referencia / 5)
        mult_nivel_p = {"Básico": 1, "Avanzado": 2.5, "Pro/Museo": 5}
        sugerencia_p = base_h * mult_nivel_p[nivel_p]
        horas_p = st.number_input(f"Horas estimadas de pintura", min_value=0.0, value=round(sugerencia_p, 1), step=0.5)
        costo_pintura_eur = horas_p * hora_pintura
        ahorro_pintura = horas_p * (MERCADO_PINTURA - PRECIO_HORA_PINTURA)
    else:
        costo_pintura_eur = 0.0

with tab3:
    st.header("Diseño en Blender")
    quiere_diseno = st.checkbox("¿Necesitas ajustes de diseño?")
    horas_b = 0.0
    ahorro_blender = 0.0
    tipo_diseno = "N/A"
    if quiere_diseno:
        tipo_diseno = st.selectbox("¿Qué necesitas hacer?", 
                                 ["Ajuste Simple (Escalar, reparar archivo, unir piezas)", 
                                  "Modificación Media (Añadir base, cortar para impresión, textos)", 
                                  "Diseño Complejo (Modelado desde cero, esculpido orgánico)"])
        
        mapa_horas = {
            "Ajuste Simple (Escalar, reparar archivo, unir piezas)": 1.0,
            "Modificación Media (Añadir base, cortar para impresión, textos)": 3.0,
            "Diseño Complejo (Modelado desde cero, esculpido orgánico)": 8.0
        }
        
        horas_b = st.number_input("Horas de diseño", min_value=0.0, value=mapa_horas[tipo_diseno], step=0.5)
        costo_diseno_eur = horas_b * hora_blender
        ahorro_blender = horas_b * (MERCADO_BLENDER - PRECIO_HORA_BLENDER)
    else:
        costo_diseno_eur = 0.0

# --- TOTALES Y AHORRO ---
st.divider()
total_eur = costo_impresion_eur + costo_pintura_eur + costo_diseno_eur
total_pen = total_eur * tasa_soles
ahorro_total_eur = ahorro_pintura + ahorro_blender

col1, col2 = st.columns(2)
col1.metric("PRECIO FINAL", f"€ {total_eur:,.2f}", delta=f"S/. {total_pen:,.2f}", delta_color="normal")

if ahorro_total_eur > 0:
    col2.success(f"✨ ¡Ahorras € {ahorro_total_eur:,.2f}!")

# --- EL CUADRO DESGLOSADO ---
st.subheader("📊 Desglose del Servicio")
datos_tabla = [
    {"Servicio": "Impresión 3D (ABS)", "Euros (€)": f"{costo_impresion_eur:,.2f}", "Soles (S/.)": f"{costo_impresion_eur * tasa_soles:,.2f}"},
    {"Servicio": "Pintura Artística", "Euros (€)": f"{costo_pintura_eur:,.2f}", "Soles (S/.)": f"{costo_pintura_eur * tasa_soles:,.2f}"},
    {"Servicio": "Diseño en Blender", "Euros (€)": f"{costo_diseno_eur:,.2f}", "Soles (S/.)": f"{costo_diseno_eur * tasa_soles:,.2f}"},
]
st.table(datos_tabla)

# --- RESUMEN WHATSAPP DINÁMICO ---
if st.button("Generar Resumen para WhatsApp"):
    if altura == 0 and costo_diseno_eur > 0:
        titulo = "🖥️ *COTIZACIÓN DE DISEÑO DIGITAL*"
        detalle = f"✅ Servicio: {tipo_diseno}\\n⏳ Tiempo estimado: {horas_b}h"
    else:
        titulo = "🔥 *COTIZACIÓN ESPECIAL LANZAMIENTO*"
        detalle = f"📏 Tamaño: {altura}cm\\n📦 Servicio de Impresión incluido"

    texto = (f"{titulo}\\n"
             f"------------------------------------\\n"
             f"{detalle}\\n"
             f"💰 Precio: € {total_eur:.2f} / S/. {total_pen:.2f}\\n"
             f"✨ Tu ahorro: € {ahorro_total_eur:.2f}\\n"
             f"------------------------------------\\n"
             f"¿Cómo podemos proceder?")
    st.code(texto)
