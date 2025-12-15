import streamlit as st
import google.generativeai as genai

# Título de tu aplicación
st.title("Generador de Marketing")

# Cuadro para que el usuario ponga su llave
api_key = st.text_input("Pega aquí tu API Key de Google:", type="password")

if api_key:
    # Configuración básica
    genai.configure(api_key=api_key)
    
    # AQUÍ PEGAS TUS INSTRUCCIONES DE AI STUDIO
    instrucciones = """
    Eres un experto en marketing digital y creación de catálogos de ropa.
    Ayudas a crear descripciones atractivas para ventas.
    """
    
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=instrucciones)

    # Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿Qué necesitas hoy?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        try:
            chat = model.start_chat(history=[{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages])
            response = chat.send_message(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
