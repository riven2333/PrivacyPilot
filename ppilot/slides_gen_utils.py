import tempfile
from datetime import datetime
from pathlib import Path

# from aihub_slides_gen.md2pptx import convert_md_to_pptx as convert
import importlib.util
import sys

module_name = "md2pptx"
module_path = Path("ppilot/aihub-slides-gen") / f"{module_name}.py"
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
convert = module.convert_md_to_pptx

STATIC_DIR = Path("./data/generated_slides")
STATIC_DIR.mkdir(parents=True, exist_ok=True)

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
