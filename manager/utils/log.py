import os
import traceback
from datetime import datetime


def log_exception(log_dir, exception):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    filename = log_dir / f"mmm-{timestamp}.error.log"
    if not log_dir.exists():
        os.makedirs(log_dir)
    with open(filename, "w") as f:
        traceback.print_exc(file=f)
