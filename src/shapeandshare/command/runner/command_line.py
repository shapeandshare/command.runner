import logging

from .manager import Manager


def main():
    Manager().main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
