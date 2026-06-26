"""
Simple console logger for extraction scripts.
"""


def log_start(source):
    print(f"\nStarting {source} extraction...")


def log_success(message):
    print(f"  {message}")


def log_error(message):
    print(f"  ERROR: {message}")


def log_complete(source, output_path, successful_pages=None, errors=None):
    print(f"\n{source} extraction completed: {output_path}")

    if successful_pages is not None:
        print(f"Successful pages: {successful_pages}")

    if errors is not None:
        print(f"Errors: {errors}")