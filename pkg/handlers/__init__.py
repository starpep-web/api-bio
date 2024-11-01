from fastapi import APIRouter
import os
import glob
import importlib


router = APIRouter()


def load_controllers() -> None:
    current_dir = os.path.dirname(__file__)
    controller_files = glob.glob(os.path.join(current_dir, "*/controller.py"))

    for file in controller_files:
        module_path = file.replace(current_dir, 'pkg.handlers').replace('/', '.').replace('\\', '.').replace('.py', '')
        importlib.import_module(module_path)
