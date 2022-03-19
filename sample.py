"""
From
https://www.programiz.com/python-programming/time/sleep
"""
import time


def sample(wait_time: float = 2.0):
    print("Printed immediately")
    time.sleep(wait_time)
    print(f"Printed after {wait_time} seconds")


if __name__ == "__main__":
    sample()
