"""Proof-only fresh production API process with computation/source ports disabled."""
from fastapi import FastAPI
from packages.contracts.analytics import AnalyticsFailure
import uvicorn
from packages.analytics_core.application.service import AnalyticsService
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository


def unavailable(*args: object, **kwargs: object) -> object:
    raise AnalyticsFailure('S03_PROOF_COMPUTATION_AND_SOURCE_DISABLED')


AnalyticsService.run_sales_report = unavailable
PostgresSalesSemanticRepository.sales_projection = unavailable
from custometry_api.main import create_app
app = FastAPI()
app.mount('/api', create_app())
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=58103, log_level='error', access_log=False)
