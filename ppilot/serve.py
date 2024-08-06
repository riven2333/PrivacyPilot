# -*- encoding: utf-8 -*-
'''
@File    :   serve.py
@Time    :   2024/07/13 22:03:03
@Contact :   small_dark@sina.com
@Brief   :   enable ppilot_serve cmd
'''

from fastapi import FastAPI, HTTPException, Request
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import os

from .cpu import get_cpu_model
from .disk import get_disk_usage
from .python_interpreter import python_interpreter
from .file_finder import find_file
from .slides_gen_utils import get_fixed_header, datetime, Path, tempfile, convert, STATIC_DIR 

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

@app.post("/file_finder")
async def run_file_finder(request: Request):
    form_data = await request.form()
    result = find_file(form_data["pattern"], form_data["src_dir"])
    print("[API /file_finder]", result)
    return result

app.mount("/data/generated_slides", StaticFiles(directory="data/generated_slides"), name="static")
@app.post("/slides_gen")
async def convert_md_to_pptx(request: Request):
    form_data = await request.form()
    markdown_content=form_data["markdown_content"]
    output_name=form_data["output_name"]
    save_input=form_data["save_input"]

    output_dir = STATIC_DIR
    input_dir = Path("./data/markdowns")
    input_dir.mkdir(parents=True, exist_ok=True)

    try:
        timestamp = datetime.now().strftime("%y%m%d-%H%M%S")
        output_base_name = output_name if not output_name.endswith(".pptx") else output_name[:-5]
        output_path = output_dir / f"{output_base_name}_{timestamp}.pptx"

        extended_markdown_content = get_fixed_header() + markdown_content
        if save_input:
            input_path = input_dir / f"{output_base_name}_{timestamp}.md"
            with open(input_path, "w", encoding="utf-8") as f:
                f.write(extended_markdown_content)
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp:
                tmp.write(markdown_content.encode("utf-8"))
                input_path = Path(tmp.name)

        convert(str(input_path), str(output_path))

        if not save_input:
            input_path.unlink()

        if not output_path.is_file():
            raise HTTPException(status_code=404, detail="File not found.")

        download_url = request.url_for("static", path=f"{output_path.name}")

        return JSONResponse(content={"download_url": str(download_url)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while converting: {e}")

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
            {"path": "/slides_gen", "description": "Convert markdown to pptx"},
            {"path": "/manifest.json", "description": "Get API manifest"}
        ]
    }
    return manifest

def main():
    import uvicorn
    os.environ['no_proxy'] = "localhost,127.0.0.*"
    uvicorn.run(app, host="0.0.0.0", port=15260)

if __name__ == "__main__":
    main()
