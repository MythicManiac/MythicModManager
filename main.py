import argparse

from manager.interface.wxapp import Application
from manager.utils.log import log_exception


parser = argparse.ArgumentParser(description="Run MythicModManager")


def main():
    application = Application()
    application.launch()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_exception(e)
