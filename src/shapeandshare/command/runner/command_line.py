""" Command Line Tool Hook """
import logging

from .manager import Manager


def main():
    """Main entry point"""
    Manager().main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
