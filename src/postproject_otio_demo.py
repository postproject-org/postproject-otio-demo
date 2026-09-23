"""Resolve an OTIO media reference through OpenAssetIO and PostProject."""

import argparse
import json
from pathlib import Path

import opentimelineio as otio
from postproject import Production


def build_timeline(entity_reference: str) -> otio.schema.Timeline:
    """Create a one-clip timeline carrying an OpenAssetIO entity reference."""
    clip = otio.schema.Clip(
        name="Camera A",
        media_reference=otio.schema.ExternalReference(target_url=entity_reference),
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, 24),
            duration=otio.opentime.RationalTime(48, 24),
        ),
    )
    timeline = otio.schema.Timeline(name="PostProject OpenAssetIO demo")
    timeline.tracks.append(otio.schema.Track(children=[clip]))
    return timeline


def resolve_timeline(
    timeline: otio.schema.Timeline,
    production_path: Path,
    library_path: Path,
) -> otio.schema.Timeline:
    """Round-trip through OTIO's established OpenAssetIO media linker."""
    encoded = otio.adapters.write_to_string(timeline, adapter_name="otio_json")
    return otio.adapters.read_from_string(
        encoded,
        adapter_name="otio_json",
        media_linker_name="openassetio_media_linker",
        media_linker_argument_map={
            "identifier": "org.postproject.manager",
            "settings": {
                "production_path": str(production_path),
                "library_path": str(library_path),
            },
        },
    )


def run(work_directory: Path, library_path: Path) -> dict[str, object]:
    """Create a production and prove standards-composed reference resolution."""
    work_directory.mkdir(parents=True, exist_ok=True)
    media = work_directory / "camera.mov"
    media.write_bytes(b"PostProject OTIO demonstration media")
    production_path = work_directory / "demo.pproj"
    with Production.create(production_path, library_path=library_path) as production:
        with production.transaction() as transaction:
            asset_id = transaction.import_media(media, "Camera A")
        representation = production.representations[asset_id][0]
        entity_reference = production.host_bindings[representation.id]

    linked = resolve_timeline(
        build_timeline(entity_reference), production_path, library_path
    )
    clip = linked.find_clips()[0]
    resolved_url = clip.media_reference.target_url
    expected_url = media.resolve().as_uri()
    if resolved_url != expected_url:
        raise RuntimeError(f"expected {expected_url}, resolved {resolved_url}")
    return {
        "entity_reference": entity_reference,
        "resolved_url": resolved_url,
        "rate": clip.source_range.duration.rate,
        "duration_frames": clip.source_range.duration.value,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("work_directory", type=Path)
    parser.add_argument("--library", type=Path, required=True)
    arguments = parser.parse_args()
    print(json.dumps(run(arguments.work_directory, arguments.library), indent=2))


if __name__ == "__main__":
    main()
