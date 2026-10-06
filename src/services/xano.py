"""HTTP client and authentication adapter for the EduTrack Xano API."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.services.demo_auth import AuthResult, DemoAuthService

XANO_BASE_URL_ENV = "XANO_API_BASE_URL"


class XanoError(RuntimeError):
    """Raised when Xano cannot complete an API request."""


@dataclass(frozen=True)
class XanoAuthResult:
    """Authentication result including the private session token."""

    result: AuthResult
    token: str | None = None


def configured_xano_base_url() -> str | None:
    """Read the Xano URL from the environment or Streamlit secrets."""
    value = os.getenv(XANO_BASE_URL_ENV, "").strip()
    if value:
        return value.rstrip("/")

    try:
        import streamlit as st

        value = str(st.secrets.get("xano_api_base_url", "")).strip()
    except (FileNotFoundError, KeyError):
        return None
    return value.rstrip("/") or None


class XanoClient:
    """Small JSON client for Xano endpoints."""

    def __init__(self, base_url: str, timeout: float = 15.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> Any:
        """Send a JSON request and return the decoded response."""
        headers = {"Accept": "application/json"}
        body = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(payload).encode("utf-8")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        request = Request(
            f"{self.base_url}/{path.lstrip('/')}",
            data=body,
            headers=headers,
            method=method.upper(),
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:  # noqa: S310
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except HTTPError as error:
            raw = error.read().decode("utf-8", errors="replace")
            try:
                details = json.loads(raw)
                message = details.get("message") or details.get("code") or raw
            except json.JSONDecodeError:
                message = raw
            raise XanoError(str(message or f"Erro HTTP {error.code} no Xano.")) from error
        except (URLError, TimeoutError) as error:
            raise XanoError("Não foi possível conectar ao Xano.") from error


class XanoAuthService:
    """Authenticate and register users through the Xano API."""

    def __init__(self, base_url: str) -> None:
        self.client = XanoClient(base_url)

    @staticmethod
    def _public_user(data: dict[str, Any]) -> dict[str, Any]:
        user = data.get("user", data)
        return {
            key: user[key] for key in ("id", "created_at", "name", "email", "role") if key in user
        }

    def _authenticated_result(self, data: Any, success_message: str) -> XanoAuthResult:
        if not isinstance(data, dict):
            return XanoAuthResult(AuthResult(False, "Resposta inválida recebida do Xano."))
        token = data.get("authToken") or data.get("auth_token")
        if not isinstance(token, str) or not token:
            return XanoAuthResult(AuthResult(False, "O Xano não retornou o token de acesso."))

        profile = self.client.request("GET", "auth/me", token=token)
        if not isinstance(profile, dict):
            return XanoAuthResult(AuthResult(False, "O Xano não retornou o perfil do usuário."))
        user = self._public_user(profile)
        return XanoAuthResult(AuthResult(True, success_message, user), token)

    def authenticate(self, email: str, password: str) -> XanoAuthResult:
        """Log in and validate the returned token using auth/me."""
        if not email.strip() or not password:
            return XanoAuthResult(AuthResult(False, "Informe e-mail e senha."))
        try:
            data = self.client.request(
                "POST", "auth/login", payload={"email": email.strip().lower(), "password": password}
            )
            return self._authenticated_result(data, "Login realizado com sucesso.")
        except XanoError:
            return XanoAuthResult(AuthResult(False, "E-mail ou senha inválidos."))

    def register(self, name: str, email: str, password: str, confirmation: str) -> XanoAuthResult:
        """Create an account and validate its returned authentication token."""
        error = DemoAuthService.validate_registration(name, email, password, confirmation)
        if error:
            return XanoAuthResult(AuthResult(False, error))
        try:
            data = self.client.request(
                "POST",
                "auth/signup",
                payload={
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "password": password,
                },
            )
            return self._authenticated_result(data, "Conta criada com sucesso.")
        except XanoError as error:
            return XanoAuthResult(AuthResult(False, str(error)))

def get_pet_preferences(
    token: str,
) -> list[dict[str, Any]]:
    """Retorna as preferências de mascote do usuário autenticado."""

    base_url = configured_xano_base_url()

    if not base_url:
        return []

    client = XanoClient(base_url)

    data = client.request(
        "GET",
        "profile/pets",
        token=token,
    )

    if not isinstance(data, list):
        return []

    return [
        item
        for item in data
        if isinstance(item, dict)
    ]


def get_pet_for_screen(
    token: str,
    screen_key: str,
) -> str | None:
    """Retorna o mascote salvo para uma tela específica."""

    preferences = get_pet_preferences(token)

    for preference in preferences:
        if preference.get("screen_key") != screen_key:
            continue

        pet_key = preference.get("pet_key")

        if isinstance(pet_key, str):
            return pet_key

    return None


def save_pet_preference(
    token: str,
    screen_key: str,
    pet_key: str,
) -> dict[str, Any]:
    """Cria ou atualiza a preferência de mascote no Xano."""

    base_url = configured_xano_base_url()

    if not base_url:
        raise XanoError("Xano não está configurado.")

    client = XanoClient(base_url)

    data = client.request(
        "POST",
        "profile/pet",
        token=token,
        payload={
            "screen_key": screen_key,
            "pet_key": pet_key,
        },
    )

    if not isinstance(data, dict):
        raise XanoError(
            "Resposta inválida ao salvar preferência de mascote."
        )

    return data