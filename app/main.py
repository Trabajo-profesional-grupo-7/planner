from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes.plan import router

app = FastAPI(title="Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

app.include_router(router)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs")
