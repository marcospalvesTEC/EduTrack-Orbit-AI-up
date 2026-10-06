"""Onboarding inicial do EduTrack Orbit AI."""

import streamlit as st

from src.core.auth_session import require_authenticated
from src.ui.pets import (
    PET_PROFILES,
    PETS,
    load_pet_choice,
    pet_data_uri,
    save_pet_choice,
)
from src.ui.theme import inject_custom_css


st.set_page_config(
    page_title="Boas-vindas - EduTrack Orbit AI",
    page_icon="✨",
    layout="wide",
)

inject_custom_css()

user = require_authenticated()

st.title("Bem-vindo ao EduTrack Orbit AI ✦")

st.write(
    """
    Organize suas disciplinas, acompanhe tarefas e prazos,
    planeje sua rotina acadêmica e conte com o Orbit AI
    para ajudar durante sua jornada.
    """
)

st.subheader("Escolha seu companheiro Orbit")

current = load_pet_choice(st.session_state, user)

columns = st.columns(4)

for column, pet_key in zip(columns, PETS.keys()):
    profile = PET_PROFILES[pet_key]

    with column:
        st.markdown(
            f"""
            <div style="
                min-height: 360px;
                padding: 18px;
                border: 1px solid #DDD6FE;
                border-radius: 18px;
                background: rgba(124, 58, 237, 0.06);
                text-align: center;
            ">
                <img
                    src="{pet_data_uri(pet_key)}"
                    alt="{profile['name']}"
                    style="
                        width: 150px;
                        height: 150px;
                        object-fit: contain;
                        margin-bottom: 10px;
                    "
                >

                <h3>{profile['name']}</h3>

                <p>
                    <strong>{profile['role']}</strong>
                </p>

                <p>{profile['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Escolher",
            key=f"choose_pet_{pet_key}",
            type="primary" if current == pet_key else "secondary",
            width="stretch",
        ):
            save_pet_choice(
                st.session_state,
                user,
                pet_key,
            )
            st.rerun()

selected = load_pet_choice(st.session_state, user)

if selected:
    pet = PET_PROFILES[selected]

    st.success(
        f'{pet["name"]} agora acompanhará sua jornada no Orbit.'
    )

    if st.button(
        "Entrar no EduTrack Orbit AI →",
        type="primary",
        width="stretch",
    ):
        st.session_state["orbit_onboarding_complete"] = True
        st.switch_page("app.py")
else:
    st.info("Escolha um mascote para continuar.")