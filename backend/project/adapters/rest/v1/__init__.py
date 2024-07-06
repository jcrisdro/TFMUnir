from fastapi import APIRouter

from project.adapters.rest.v1.run_models import RunModelsRestAdapter
from project.adapters.rest.v1.train_models import TrainModelsRestAdapter
from project.adapters.rest.v1.test_models import TestModelsRestAdapter

router = APIRouter()
router.include_router(RunModelsRestAdapter().router, prefix="/run/models", tags=["Models"])
router.include_router(TrainModelsRestAdapter().router, prefix="/train/models", tags=["Models"])
router.include_router(TestModelsRestAdapter().router, prefix="/test/models", tags=["Models"])
