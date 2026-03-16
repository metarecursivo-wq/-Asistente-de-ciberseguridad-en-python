from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv

load_dotenv(".env")

# Configurar la página de la app
st.set_page_config(page_title="Asistente de ciberseguridad en python", page_icon="🛡️")
st.title("🛡️ Asistente de ciberseguridad en python")
st.markdown("Este es un chatbot de ciberseguridad creado por el usuario de github @metarecursivo-wq, cuyo objetivo es detectar vulnerabilidades en código python.")

with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"])

    chat_model = ChatOpenAI(model=model_name, temperature=temperature)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


plantilla = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""
    Eres un analista de ciberseguridad experto en código seguro de python.
    Tu objetivo es analizar el código python y detectar vulnerabilidades, así cómo detectar fallas en la lógica del código.
    En caso de que el código no sea de python, responde que no es de python.
    Si el usuario te pregunta algo que no tiene que ver con ciberseguridad, responde que no es de tu competencia.
    Mejora la seguridad del código y sugiere cambios para mejorar la seguridad del código.
    Historial de conversación:
    {historial}

    Sugiere cambios para mejorar la seguridad del código: {mensaje}
    """)

if st.button("Otro script"):
    st.session_state.mensajes = []
    st.rerun()

codigo = st.chat_input("Introduce el código python a analizar")

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.code(msg["content"], language="python")
        else:
            st.markdown(msg["content"])

if codigo:
    st.session_state.mensajes.append({"role": "user", "content": codigo})
    with st.chat_message("user"):
        st.code(codigo, language="python")

    historial = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.mensajes[:-1]
    )

    prompt = plantilla.format(mensaje=codigo, historial=historial)

    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            respuesta = chat_model.invoke([HumanMessage(content=prompt)])
            st.markdown(respuesta.content)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta.content})