import os

IGNORE = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules"
}

def tree(path, prefix=""):
    items = [
        x for x in os.listdir(path)
        if x not in IGNORE
    ]

    for index, item in enumerate(items):
        full = os.path.join(path, item)

        connector = "└── " if index == len(items)-1 else "├── "

        print(prefix + connector + item)

        if os.path.isdir(full):
            extension = "    " if index == len(items)-1 else "│   "
            tree(full, prefix + extension)

tree("app")
