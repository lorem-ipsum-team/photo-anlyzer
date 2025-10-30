import os
import re
import sys
import time

from app.pkg.tf.universal_sentence_encoder import TextProcessor


def main(*argv):
    if len(argv) < 2:
        print(f"Usage: main.py path/to/dir", file=sys.stderr)
        return 1

    txtdir = argv[1]
    files: list[str] = []

    for file in (f for f in os.listdir(txtdir) if re.match(r".*\.txt", f)):
        full_path = f"{txtdir}/{file}"
        with open(full_path, 'r') as txt:
            files.append(txt.read())

    processor = TextProcessor()
    start_time = time.time()

    for file in files:
        processor.process_text(file)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"Processed {len(files)} sentences in {elapsed:.2f} seconds")


if __name__ == '__main__':
    ecode = main(*sys.argv)
    exit(ecode)
