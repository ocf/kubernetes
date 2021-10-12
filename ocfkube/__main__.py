import sys

import ocfkube

if __name__ == "__main__":
    # TODO: Make this more robust...
    if len(sys.argv) == 1:
        ocfkube.build_changed()
    elif len(sys.argv) == 2:
        print(ocfkube.build(sys.argv[1]))
    else:
        raise ValueError(f"usage: {sys.argv[0]} <application name>")
