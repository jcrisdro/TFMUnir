from fastapi import APIRouter, HTTPException

class Run:

    def __init__(self) -> None:
        self.router = APIRouter()
        self.routes()
    
    def routes(self):

        @self.router.post("/v1/run")
        async def run():
            try:
                return "run model"
            except Exception as e:
                return f"Exception: {e}"
