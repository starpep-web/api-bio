import os


def get_model_path(model_name: str) -> str:
    project_root = os.path.dirname(os.path.dirname(__file__))
    models_path = os.path.join(project_root, 'models')
    return os.path.join(models_path, model_name)
