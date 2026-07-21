"""Provider-neutral principal contract reserved for local auth and future OIDC."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class NormalizedPrincipal:
    """Stable provider subject before workspace membership is resolved."""

    provider: str
    subject: str
    email: str

    @classmethod
    def create(cls, *, provider: str, subject: str, email: str) -> NormalizedPrincipal:
        normalized_provider = provider.strip().casefold()
        normalized_subject = subject.strip()
        normalized_email = email.strip().casefold()
        if not normalized_provider or not normalized_subject:
            raise ValueError("provider and subject are required")
        if not normalized_email or "@" not in normalized_email:
            raise ValueError("normalized email is invalid")
        return cls(normalized_provider, normalized_subject, normalized_email)


class IdentityProvider(Protocol):
    """Port implemented by local auth now and an OIDC adapter only post-v1."""

    def authenticate(self, credential: object) -> NormalizedPrincipal:
        """Authenticate provider input and return a provider-neutral principal."""

        ...
