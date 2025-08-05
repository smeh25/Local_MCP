from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


from llm_handler import suggest_command_from_natural_language


from modules import file_tools

#enabling the html page
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Allow frontend or curl to access this API (important for dev/testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@app.get("/")
#def read_root():
#    return {"message": "CLI Map Assistant backend is running."}


@app.post("/suggest-command/")
async def suggest_command(request: Request):
    data = await request.json()
    query = data.get("query")

    try:
        command = suggest_command_from_natural_language(query)
        return {"suggested_command": command}
    except Exception as e:
        return {"error": str(e)}

@app.post("/file-action/")
async def file_action(request: Request):
    data = await request.json()
    action = data.get("action")
    target = data.get("target", ".")

    if action == "list":
        return {"output": file_tools.list_files(target)}
    elif action == "create_dir":
        return {"output": file_tools.create_dir(target)}
    elif action == "delete_file":
        return {"output": file_tools.delete_file(target)}
    else:
        return {"error": "Unknown action"}



#enabling the html page


@app.get("/", response_class=HTMLResponse)
async def get_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


##Update main.py With One Unified Endpoint

from llm_handler import suggest_command_from_natural_language
import subprocess

@app.post("/suggest-and-run/")
async def suggest_and_run(request: Request):
    data = await request.json()
    query = data.get("query")

    try:
        # Get suggested shell command from LLM
        shell_command = suggest_command_from_natural_language(query)

        # Run it
        result = subprocess.check_output(shell_command, shell=True, stderr=subprocess.STDOUT, text=True)

        return {
            "query": query,
            "suggested_command": shell_command,
            "output": result
        }

    except subprocess.CalledProcessError as e:
        return {"error": e.output}
    except Exception as e:
        return {"error": str(e)}
