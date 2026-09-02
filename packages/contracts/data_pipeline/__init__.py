"""Stable cross-context envelopes for the W15 data-pipeline slice."""


class DataPipelineFailure(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code

    def __str__(self) -> str:
        return self.code


class InjectedCrash(DataPipelineFailure):
    """A deterministic test-only crash at a declared commit checkpoint."""


__all__ = ["DataPipelineFailure", "InjectedCrash"]
