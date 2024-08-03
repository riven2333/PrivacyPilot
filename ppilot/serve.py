# -*- encoding: utf-8 -*-
"""
@File    :   serve.py
@Time    :   2024/07/13 22:03:03
@Contact :   small_dark@sina.com
@Brief   :   enable ppilot_serve cmd
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .cpu import get_cpu_model
from .disk import get_disk_usage
from .file_finder import find_file
from .local_rag import RAGRequest, RAGResponse, clear_local_rag_cache, get_rag_engine
from .python_interpreter import python_interpreter


@asynccontextmanager
async def lifespan(_: FastAPI):
    rag = get_rag_engine()
    await rag.process_files()
    yield
    clear_local_rag_cache()


app = FastAPI(lifespan=lifespan)


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


@app.post("/local_rag", response_model=RAGResponse)
async def run_local_rag(request: RAGRequest):
    rag = get_rag_engine()
    if not rag.processed:
        return RAGResponse(
            status="processing",
            message="LocalRAG not finished pre-processing yet, please retry later",
            results=[],
        )
    else:
        results = await rag.query(request.query)
        print("[API /local_rag]", results)
        return RAGResponse(
            status="success",
            message="RAG query finished",
            results=results,
        )


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
            {
                "path": "/python_interpreter",
                "description": "Run python code with basic venv",
            },
            {
                "path": "/local_rag",
                "description": "Retrieval Augmented Generation (RAG) query on local files",
            },
            {"path": "/manifest.json", "description": "Get API manifest"},
        ],
    }
    return manifest


def main():
    import uvicorn

    os.environ["no_proxy"] = "localhost,127.0.0.*"
    uvicorn.run(app, host="0.0.0.0", port=15260)


if __name__ == "__main__":
    main()
