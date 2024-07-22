# -*- encoding: utf-8 -*-
'''
@File    :   serve.py
@Time    :   2024/07/13 22:03:03
@Author  :   Haoyu Wang 
@Contact :   small_dark@sina.com
@Brief   :   enable ppilot_serve cmd
'''

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .cpu import get_cpu_model
from .disk import get_disk_usage
from .python_interpreter import python_interpreter


app = FastAPI()

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

@app.get("/manifest.json")
async def get_manifest():
    # TODO: adjust for lobe-chat & coze
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
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
