from fastapi import APIRouter, HTTPException

class Training:

    def __init__(self) -> None:
        self.router = APIRouter()
        self.routes()
    
    def routes(self):

        @self.router.post("/v1/training/cav1")
        async def cav1():
            try:
                return "load file"
            except Exception as e:
                return f"Exception: {e}"


        @self.router.post("/v1/training/cvv1")
        async def cvv1():
            try:
                return "load file"
            except Exception as e:
                return f"Exception: {e}"
