"""Process-local model registry. Populated by TranslationWorker's
_load_models(); read by strategy classes via getters, never by direct
import of a module-level variable (which snapshots at import time and
goes stale — see worker GPU loading timeline)."""

_models = {
    "inpaint": None,
    "detection": None,
    "extraction": None,
    "device": None,
    "translation":None
}


def set_model(name: str, value):
    _models[name] = value


def get_model(name: str):
    value = _models[name]
    if value is None:
        raise RuntimeError(
            f"Model '{name}' not loaded yet in this process. "
            f"Was _load_models() called (via import-time CPU path or "
            f"worker_process_init for GPU)?"
        )
    return value