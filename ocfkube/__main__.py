import sys
import ocfkube

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError(f"usage: {sys.argv[0]} <application name>")
    application_name = sys.argv[1]
    print(ocfkube.build(application_name))
