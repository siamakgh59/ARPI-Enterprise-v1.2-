import os

def tree(path, prefix=""):
    files = os.listdir(path)

    for index, file in enumerate(files):
        full = os.path.join(path, file)

        connector = "└── " if index == len(files)-1 else "├── "

        print(prefix + connector + file)

        if os.path.isdir(full):
            extension = "    " if index == len(files)-1 else "│   "
            tree(full, prefix + extension)

tree(".")
