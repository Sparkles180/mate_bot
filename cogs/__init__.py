import os

__all__ = []

for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
    if file.endswith("cog.py") and file != "base_cog.py":
        __all__.append(str(file)[:-3])

