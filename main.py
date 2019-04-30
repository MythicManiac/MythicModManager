import argparse

from manager.interface.app import Application as LegacyApplication
from manager.interface.wxapp import Application as WxApplication
from manager.utils.log import log_exception


parser = argparse.ArgumentParser(description="Run MythicModManager")
parser.add_argument(
    "--new-ui", default=False, action="store_true", help="Use the new UI"
)

args = parser.parse_args()


def main():
    args = parser.parse_args()
    application_cls = LegacyApplication
    if args.new_ui:
        application_cls = WxApplication
    application = application_cls()
    application.launch()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_exception(e)
