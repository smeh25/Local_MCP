from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
from llm_handler import suggest_command_from_natural_language


app = FastAPI()

# Allow frontend or curl to access this API (important for dev/testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "CLI Map Assistant backend is running."}

@app.post("/run-command/")
async def run_command(request: Request):
    data = await request.json()
    command = data.get("command")

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return {"output": result}
    except subprocess.CalledProcessError as e:
        return {"error": e.output}
