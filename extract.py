import os
import sys
import json
import importlib.util
from typing import Union


def main(source_path: str, source_args: Union[list, str], source_class: str) -> None:
    """
    Dynamically imports the specified module and executes the module's `.download()` method.

        Parameters:
            source_path (str): Relative path to the module;
            source_args (list, str): List/string containing the arguments to that specific module (if any);
            source_class (str): Class name referring the class that will be executing the `.download()` method.
    """

    source_name: str = source_path.split("/")[-1].replace(".py", "")
    spec: _frozen_importlib.ModuleSpec = importlib.util.spec_from_file_location(
        source_name, source_path
    )
    module: module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    extractor = getattr(module, source_class)(*source_args)

    extractor.download()


if __name__ == "__main__":
    config_file: str = "./config/config.json"

    # Getting environmental variable from docker
    extraction = sys.argv[1]
 
    # If there is a CLI arg with the script invocation, the default config_file location is overwritten by it:
    if extraction != None:

        with open(config_file) as f:
            config_file: dict = json.load(f)

        # "Filtering" the ./config.json to return only the key-value for the argument provided
        config = dict()
        for (key, value) in config_file.items():
            if key == extraction.upper():
                config[key] = value
    else:
        print(extraction)
        with open(config_file) as f:
            config: dict = json.load(f)

    for source in config.keys():
        source_class: str = f"Extract{source}"
        main(config[source]["source_path"], config[source]["source_args"], source_class)
