import subprocess
import io
import datetime
from PyQt6.QtGui import QImage

def get_preview():
    try:
        result = subprocess.run(
            ["gphoto2", "--capture-preview", "--stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        if result.returncode != 0:
            return None
        image = QImage.fromData(result.stdout)
        return image if not image.isNull() else None
    except Exception:
        return None

def capture_photo():
    filename = f"photos/photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    subprocess.run(["mkdir", "-p", "photos"])
    subprocess.run([
        "gphoto2",
        "--capture-image-and-download",
        f"--filename={filename}"
    ])
    return filename
