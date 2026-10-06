"""Componentes visuais e preferências dos mascotes Orbit."""

import base64
from collections.abc import MutableMapping
from pathlib import Path
from textwrap import dedent
from typing import Any

import streamlit as st

from src.services.xano import (
    get_pet_for_screen,
    save_pet_preference,
)



def _html_block(value: str) -> str:
    """Normalize HTML so Streamlit Markdown never treats indentation as code."""
    return "\n".join(
        line.lstrip()
        for line in value.splitlines()
    ).strip()


PETS_DIR = Path(__file__).resolve().parents[2] / "assets" / "pets"

PETS = {
    "axolote": "axolote-mago.png",
    "raposa": "raposa-feiticeira.png",
    "lagosta": "lagosta-boxeadora.png",
    "caracol": "caracol-curandeiro.png",
}

PET_PROFILES = {
    "axolote": {
        "name": "Axalote Mago",
        "role": "Conhecimento e orientação",
        "description": "Ajuda a organizar estudos e encontrar caminhos.",
    },
    "raposa": {
        "name": "Raposa Feiticeira",
        "role": "Estratégia",
        "description": "Ajuda a planejar disciplinas e decisões acadêmicas.",
    },
    "lagosta": {
        "name": "Lagosta Boxeadora",
        "role": "Foco e execução",
        "description": "Ajuda a enfrentar tarefas, prazos e desafios.",
    },
    "caracol": {
        "name": "Caracol Curandeiro",
        "role": "Equilíbrio e constância",
        "description": "Ajuda a manter ritmo, rotina e progresso sustentável.",
    },
}

VALID_SCREEN_KEYS = {
    "home",
    "disciplinas",
    "tarefas",
    "agenda",
    "relatorios",
    "assistente",
    "perfil",
    "configuracoes",
}


def pet_data_uri(pet: str) -> str:
    """Converte a imagem do pet para uso dentro do HTML."""

    if pet not in PETS:
        raise ValueError(f"Mascote Orbit inválido: {pet}")

    path = PETS_DIR / PETS[pet]

    if not path.exists():
        raise FileNotFoundError(
            f"Imagem do Orbit Pet não encontrada: {path}"
        )

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return f"data:image/png;base64,{encoded}"


def render_orbit_pet_banner(
    pet: str,
    nome: str | None = None,
    funcao: str | None = None,
) -> None:
    """Renderiza o banner visual de um mascote Orbit."""

    if pet not in PETS:
        raise ValueError(f"Mascote Orbit inválido: {pet}")

    profile = PET_PROFILES[pet]

    nome = nome or profile["name"]
    funcao = funcao or profile["role"]

    dark = bool(
        st.session_state.get(
            "edutrack_dark_mode",
            False,
        )
    )

    theme_class = (
        " orbit-pet-banner-dark"
        if dark
        else ""
    )

    css = dedent(
        """
        <style>
        .orbit-pet-banner {
            margin: 12px 0 18px;
            min-height: 132px;
            padding: 14px 20px;

            border: 1px solid #e5e7eb;
            border-radius: 18px;

            background:
                linear-gradient(
                    135deg,
                    #ffffff 0%,
                    #f8f5ff 100%
                );

            display: flex;
            align-items: center;
            justify-content: space-between;

            gap: 18px;

            box-shadow:
                0 3px 10px rgba(15, 23, 87, 0.03);

            overflow: hidden;
        }

        .orbit-pet-banner-copy {
            min-width: 0;
            flex: 1;
        }

        .orbit-pet-banner-eyebrow {
            margin: 0 0 5px;

            color: #7c3aed;

            font-size: 11px;
            font-weight: 700;

            letter-spacing: 0.02em;
            text-transform: uppercase;
        }

        .orbit-pet-banner h3 {
            margin: 0 0 5px;

            color: #0f1757;

            font-size: 20px;
            line-height: 1.2;
        }

        .orbit-pet-banner p {
            margin: 0;

            color: #6b7280;

            font-size: 12px;
            line-height: 18px;
        }

        .orbit-pet-banner-art {
            width: 150px;
            height: 112px;

            flex: 0 0 150px;

            display: grid;
            place-items: center;

            border-radius: 16px;

            background: #f3efff;
        }

        .orbit-pet-banner-art img {
            width: 118px;
            height: 106px;

            object-fit: contain;
            display: block;
        }

        .orbit-pet-banner-dark {
            border-color: #343a55 !important;

            background:
                linear-gradient(
                    135deg,
                    #1a1d30 0%,
                    #211b36 100%
                ) !important;
        }

        .orbit-pet-banner-dark h3 {
            color: #f7f5ff !important;
        }

        .orbit-pet-banner-dark p {
            color: #a7aabd !important;
        }

        .orbit-pet-banner-dark
        .orbit-pet-banner-art {
            background: #171a2c !important;
        }
        </style>
        """
    ).strip()

    st.markdown(
        _html_block(css),
        unsafe_allow_html=True,
    )

    html = dedent(
        f"""
        <section
            class="orbit-pet-banner{theme_class}"
            aria-label="{nome}"
        >
            <div class="orbit-pet-banner-copy">

                <div class="orbit-pet-banner-eyebrow">
                    ✦ Orbit Pet
                </div>

                <h3>{nome}</h3>

                <p>{funcao}</p>

            </div>

            <div class="orbit-pet-banner-art">
                <img
                    src="{pet_data_uri(pet)}"
                    alt="{nome}"
                >
            </div>

        </section>
        """
    ).strip()

    st.markdown(
        _html_block(html),
        unsafe_allow_html=True,
    )


def pet_choice_key(
    user: dict[str, Any],
    screen_key: str,
) -> str:
    """Retorna a chave local da preferência do mascote por tela."""

    email = str(
        user.get(
            "email",
            "anonymous",
        )
    ).strip().lower()

    return f"orbit_pet_choice:{email}:{screen_key}"


def _auth_token(
    state: MutableMapping[str, Any],
) -> str | None:
    """Obtém o token Xano da sessão."""

    token = state.get("auth_token")

    if isinstance(token, str) and token.strip():
        return token.strip()

    return None


def load_pet_choice(
    state: MutableMapping[str, Any],
    user: dict[str, Any],
    screen_key: str = "home",
) -> str | None:
    """
    Carrega o mascote escolhido para uma tela.

    Tenta primeiro o Xano.
    Se não for possível, usa session_state como fallback.
    """

    if screen_key not in VALID_SCREEN_KEYS:
        raise ValueError(
            f"Tela Orbit inválida: {screen_key}"
        )

    local_key = pet_choice_key(
        user,
        screen_key,
    )

    token = _auth_token(state)

    if token:
        try:
            remote_pet = get_pet_for_screen(
                token=token,
                screen_key=screen_key,
            )

            if remote_pet in PETS:
                state[local_key] = remote_pet
                return remote_pet

        except Exception:
            pass

    local_pet = state.get(local_key)

    if local_pet in PETS:
        return str(local_pet)

    return None


def save_pet_choice(
    state: MutableMapping[str, Any],
    user: dict[str, Any],
    pet: str,
    screen_key: str = "home",
) -> str:
    """
    Salva a escolha do mascote para uma tela.

    Persiste no Xano quando houver autenticação
    e mantém uma cópia local na sessão.
    """

    if pet not in PETS:
        raise ValueError(
            "Mascote Orbit inválido."
        )

    if screen_key not in VALID_SCREEN_KEYS:
        raise ValueError(
            f"Tela Orbit inválida: {screen_key}"
        )

    local_key = pet_choice_key(
        user,
        screen_key,
    )

    token = _auth_token(state)

    if token:
        save_pet_preference(
            token=token,
            screen_key=screen_key,
            pet_key=pet,
        )

    state[local_key] = pet

    return pet


def render_saved_pet_for_screen(
    state: MutableMapping[str, Any],
    user: dict[str, Any],
    screen_key: str,
    default_pet: str = "axolote",
) -> str:
    """
    Carrega e renderiza o mascote definido para uma tela.

    Retorna a chave do mascote renderizado.
    """

    pet = load_pet_choice(
        state=state,
        user=user,
        screen_key=screen_key,
    )

    if pet not in PETS:
        pet = default_pet

    profile = PET_PROFILES[pet]

    render_orbit_pet_banner(
        pet=pet,
        nome=profile["name"],
        funcao=profile["role"],
    )

    return pet