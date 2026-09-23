"""End-to-end OTIO/OpenAssetIO/PostProject composition test."""

import os
from pathlib import Path

from postproject_otio_demo import run


def test_otio_reference_resolves_through_openassetio(tmp_path):
    result = run(tmp_path, Path(os.environ["POSTPROJECT_LIBRARY"]))
    assert result["entity_reference"].startswith("https://postproject.org/ref/v1/")
    assert result["resolved_url"].endswith("/camera.mov")
    assert result["rate"] == 24
    assert result["duration_frames"] == 48

