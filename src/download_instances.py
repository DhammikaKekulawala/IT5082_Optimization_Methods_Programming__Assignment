"""Download the Nurse Rostering Benchmark Instances 1-24 into data/raw/.

Source: https://www.schedulingbenchmarks.org/nrp/  (Tim Curtois, University of Nottingham)

Usage (from the repository root, inside the conda environment 'seyon'):
    python src/download_instances.py            # download if data/raw is empty
    python src/download_instances.py --force    # download again
"""
import argparse
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

ZIP_URL = "https://www.schedulingbenchmarks.org/nrp/data/instances1_24.zip"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
EXPECTED_INSTANCES = 24


def download(force: bool = False) -> int:
    existing = sorted(RAW_DIR.glob("Instance*.txt"))
    if existing and not force:
        print(f"{len(existing)} instances already in {RAW_DIR} (use --force to download again)")
        return len(existing)

    print(f"Downloading {ZIP_URL}")
    with urllib.request.urlopen(ZIP_URL, timeout=60) as response:
        payload = response.read()
    print(f"Received {len(payload):,} bytes")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for member in archive.namelist():
            name = Path(member).name
            if name.lower().endswith((".txt", ".ros")):   # plain-text and XML versions of each instance
                (RAW_DIR / name).write_bytes(archive.read(member))

    count = len(list(RAW_DIR.glob("Instance*.txt")))
    if count != EXPECTED_INSTANCES:
        sys.exit(f"Expected {EXPECTED_INSTANCES} instances but found {count} in {RAW_DIR}")
    print(f"Extracted {count} instances to {RAW_DIR}")
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="download even if data/raw already has instances")
    download(parser.parse_args().force)
