import os

def show_structure(root_dir, depth=3, level=0):
    if level >= depth:
        return
    try:
        for item in os.listdir(root_dir):
            path = os.path.join(root_dir, item)
            print("    " * level + "|-- " + item)
            if os.path.isdir(path):
                show_structure(path, depth, level + 1)
    except PermissionError:
        pass

if __name__ == "__main__":
    show_structure(".", depth=4)
