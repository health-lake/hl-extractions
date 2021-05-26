import json
import os
import importlib.util
import sys


def main(source_path: str, source_args: list, source_class: str) -> None:
    source_name: str = source_path.split("/")[-1].replace(".py", "")
    spec: _frozen_importlib.ModuleSpec = importlib.util.spec_from_file_location(
        source_name, source_path
    )
    module: module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    extractor = getattr(module, source_class)(*source_args)

    extractor.download()


if __name__ == "__main__":
    config_file: str = "./config.json"

    # If there is a CLI arg with the script invocation, the default config_file location is overwritten by it:
    if len(sys.argv) > 1:
        config_file: str = sys.argv[1]

    with open(config_file) as f:
        config: dict = json.load(f)

    for source in config.keys():
        source_class: str = f"Extract{source}"
        main(config[source]["source_path"], config[source]["source_args"], source_class)
