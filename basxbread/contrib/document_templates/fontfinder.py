import shutil
import subprocess  # nosec


def systemfonts():
    result = []
    for fontentry in (
        subprocess.run(
            [shutil.which("fc-list") or "false"], shell=False, capture_output=True
        )  # nosec
        .stdout.decode()
        .splitlines()
    ):
        result.extend(fontentry.split(":", 1)[1].split(":", 1)[0].split(","))
    return result
