import tempfile
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from md2pptx import convert_md_to_pptx as convert

app = FastAPI()

STATIC_DIR = Path("./data/generated_slides")
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/data/generated_slides", StaticFiles(directory="data/generated_slides"), name="static")


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_fixed_header():
    return f"""<!-- title: "Slides Title"
author: "Your Name"
date: "{get_date()}" -->
template: Intel Template.pptx
presTitleSize: 60
sectionTitleSize: 40
sectionSubtitleSize: 36
pageTitleSize: 30
monoFont: IntelOne Text
marginBase: 0.5
tableMargin: 0.5
cardlayout: horizontal
CardTitleSize: 16
CardColour: BACKGROUND 2
CardBorderWidth: 0
CardTitlePosition: inside
cardshadow: yes
cardshape: rounded

"""


@app.post("/convert")
async def convert_md_to_pptx(
    request: Request,
    markdown_content: str,
    output_name: str,
    save_input: bool = False,
):
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
def manifest(request: Request):
    server_url = request.base_url
    manifest_dict = {
        "api": [],
        "openapi": f"{server_url}openapi.json",
        "author": "HYD",
        "createdAt": "2024-06-17",
        "identifier": "slides-gen",
        "meta": {
            "avatar": "🎥",
            "tags": ["slides-gen"],
            "title": "Slides Generator",
            "description": "This is a slides generator.",
        },
        "version": "1",
    }
    manifest_dict["openapi"] = manifest_dict["openapi"].format(server_url=server_url)
    print(manifest_dict)
    return manifest_dict


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=12345, reload=True)
