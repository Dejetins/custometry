"""Data-worker composition root."""

from apps.worker_data.vertical_slice import DataPipelineRunner, PipelineRunResult

__all__ = ["DataPipelineRunner", "PipelineRunResult"]
