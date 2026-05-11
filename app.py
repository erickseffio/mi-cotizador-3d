import streamlit as st
import urllib.parse

# 1. Configuración de la página
st.set_page_config(page_title="3D Studio Quote", page_icon="🎨")

# --- 2. VALORES POR DEFECTO (Si no eres admin) ---
# Estos valores se usan si no se entra al panel de control
default_resina = 0.03
default_blender = 11.0
default_pintura = 8.5
default_tasa = 4.10

# --- 3. PANEL DE ADMINISTRACIÓN (SIDEBAR) ---
with st.sidebar:
    st.header("🔐 Panel de Control")
    clave = st.text_input("Contraseña Admin", type="password")
    
    if clave == "admin123":
        st.success("Acceso Autorizado")
        # Estos inputs sobreescriben los valores por defecto
        costo_resina = st.number_input("Costo Resina x ml (€)", value=default_resina, format="%.3f")
        costo_hora_diseno = st.number_input("Costo Hora Diseño (€)", value=default_blender)
        costo_hora_pintura = st.number_input("Costo Hora Pintura (€)", value=default_pintura)
        tasa_cambio = st.number_input("Tasa Cambio (1€ = S/.)", value=default_tasa)
    else:
        # Si no hay clave, usamos los valores por defecto
        costo_resina = default_resina
        costo_hora_diseno = default_blender
        costo_hora_pintura = default_pintura
        tasa_cambio = default_tasa
        if clave != "":
            st.error("Contraseña incorrecta")

# --- 4. DICCIONARIO DE TRADUCCIONES ---
texts = {
    "Español": {
        "step1": "1️⃣ Datos del Proyecto",
        "step2": "2️⃣ Configuración",
        "step3": "3️⃣ Presupuesto",
        "wa_num": "51910034696",
        "delivery": "3 semanas (Desde el 50% de adelanto)",
        "design_help": "Selecciona el nivel de edición digital",
        "design_opts": ["Listo para imprimir (0€)", "Básico (10€)", "Personalizado (25€)", "Premium (60€)"],
        "wa_btn": "📲 Enviar a WhatsApp Perú"
    },
    "English": {
        "step1": "1️⃣ Project Details",
        "step2": "2️⃣ Configuration",
        "step3": "3️⃣ Budget",
        "wa_num": "3934567890",
        "delivery": "1.5 weeks (After 50% deposit)",
        "design_help": "Select digital editing level",
        "design_opts": ["Ready to print (0€)", "Basic Fix (10€)", "Customization (25€)", "Premium (60€)"],
        "wa_btn": "📲 Send to WhatsApp Italy"
    },
    "Italiano": {
        "step1": "1️⃣ Dettagli Progetto",
        "step2": "2️⃣ Configurazione",
        "step3": "3️⃣ Preventivo",
        "wa_num": "3934567890",
        "delivery": "1.5 settimane (Dal deposito del 50%)",
        "design_help": "Seleziona il livello di editing digitale",
        "design_opts": ["Pronto da stampare (0€)", "Base (10€)", "Personalizzato (25€)", "Premium (60€)"],
        "wa_btn": "📲 Invia a WhatsApp Italia"
    }
}

idioma = st.selectbox("🌐 Idioma", ["Español", "English", "Italiano"])
t = texts[idioma]

# --- 5. INTERFAZ DE USUARIO ---
st.title("🚀 TU EMPRESA 3D")
