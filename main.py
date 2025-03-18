from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from containers import Container
from note.interface.controllers.note_controller import router as note_routers
from user.interface.controller.user_controller import router as user_routers

app = FastAPI()
app.container = Container()
app.include_router(user_routers)
app.include_router(note_routers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )
