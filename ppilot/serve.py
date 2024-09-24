# -*- encoding: utf-8 -*-
'''
@File    :   serve.py
@Time    :   2024/07/13 22:03:03
@Contact :   small_dark@sina.com
@Brief   :   enable ppilot_serve cmd
'''

import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .cpu import get_cpu_model
from .disk import get_disk_usage
from .python_interpreter import python_interpreter
from .file_finder import find_file
from .certificate_utils import CERTIFICATE_PATH, SSL_KEY_PATH

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/cpu")
async def get_cpu_info():
    cpu_model = get_cpu_model()
    print("[API /cpu]", cpu_model)
    return cpu_model

@app.get("/disk")
async def get_disk_info():
    disk_usage = get_disk_usage()
    print("[API /disk]", disk_usage)
    return disk_usage

@app.post("/python_interpreter")
async def run_python_code(request: Request):
    form_data = await request.form()
    result = python_interpreter(form_data["input_code"])
    print("[API /python_interpreter]", result["status"])
    return JSONResponse(content=result)

@app.post("/file_finder")
async def run_file_finder(request: Request):
    form_data = await request.form()
    result = find_file(form_data["pattern"], form_data["src_dir"])
    print("[API /file_finder]", result)
    return result

@app.get("/manifest.json")
async def get_manifest():
    manifest = {
        "name": "System Info API",
        "version": "1.0.0",
        "description": "API to get CPU and disk information",
        "endpoints": [
            {"path": "/cpu", "description": "Get CPU usage"},
            {"path": "/disk", "description": "Get disk usage"},
            {"path": "/python_interpreter", "description": "Run python code with basic venv"},
            {"path": "/manifest.json", "description": "Get API manifest"}
        ]
    }
    return manifest

def main():
    import uvicorn
    os.environ['no_proxy'] = "localhost,127.0.0.*"
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=15260,
        ssl_certfile=CERTIFICATE_PATH,
        ssl_keyfile=SSL_KEY_PATH
    )

if __name__ == "__main__":
    main()