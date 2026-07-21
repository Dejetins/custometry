import pytest

from packages.contracts.identity.provider import NormalizedPrincipal


def test_normalized_principal_is_provider_neutral_and_locale_independent() -> None:
    principal = NormalizedPrincipal.create(
        provider="LOCAL",
        subject="local:01HXYZ",
        email="Owner@Example.TEST",
    )

    assert principal.provider == "local"
    assert principal.subject == "local:01HXYZ"
    assert principal.email == "owner@example.test"


@pytest.mark.parametrize(
    ("provider", "subject", "email"),
    [("", "subject", "a@example.test"), ("local", "", "a@example.test"), ("local", "x", "bad")],
)
def test_normalized_principal_rejects_incomplete_identity(
    provider: str, subject: str, email: str
) -> None:
    with pytest.raises(ValueError):
        NormalizedPrincipal.create(provider=provider, subject=subject, email=email)
