from ocfkube.utils.secrets import convert_secret


def postprocess(obj: dict, dev: bool = True):
    """Run all postprocessing steps (right now just secret processing)."""
    if obj["kind"] == "Secret" and not dev:
        return convert_secret(obj)

    return obj
