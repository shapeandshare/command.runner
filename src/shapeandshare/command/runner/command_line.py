from pathlib import Path

from .manager import Manager


def main():
    Manager.parse_obj({"base_path": Path(".")}).main()
