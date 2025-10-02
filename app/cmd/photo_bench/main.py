from io import FileIO
import os
import re
import sys
import time
from PIL import Image

from app.pkg.pytorch.facenet import FacenetProcessor


def main(*argv):
    if len(argv) < 2:
        print(f"Usage: main.py path/to/dir", file=sys.stderr)
        return 1

    imgdir = argv[1]
    images: list[Image.Image] = []
    img = None

    try:
        for file in (f for f in os.listdir(imgdir) if re.match(r".*\.(jpg|png)", f)):
            full_path = f"{imgdir}/{file}"
            img = Image.open(FileIO(full_path)).convert("RGB")
            images.append(img)
            img = None

        processor = FacenetProcessor()
        start_time = time.time()

        for image in images:
            processor.process_image(image)

        end_time = time.time()
        elapsed = end_time - start_time
        print(f"Processed {len(images)} images in {elapsed:.2f} seconds")

    finally:
        for image in images:
            image.close()

        if img is not None:
            img.close()


if __name__ == '__main__':
    ecode = main(*sys.argv)
    exit(ecode)
