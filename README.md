# PostProject OTIO through OpenAssetIO

This runnable demonstration stores a PostProject representation reference in an
OpenTimelineIO `ExternalReference`, then asks the existing
[`otio-openassetio`](https://github.com/OpenAssetIO/otio-openassetio) media
linker to resolve it through the PostProject OpenAssetIO Manager. The resulting
OTIO reference is the local media URI; PostProject-specific linking code is not
added to OTIO.

```sh
postproject-otio-demo /tmp/postproject-otio --library /opt/postproject/lib/libpostproject.so
```

The test also verifies that OTIO's rational duration remains `48@24` through
the round trip.

The development SDK creates host bindings from `RepresentationRef(id)`.
The stored HTTPS reference remains compatible; use matching SDK and Manager
builds when testing the development tree.

## Install with PostProject 0.7

Download the native archive and Python wheel from the
[PostProject 0.7 release](https://github.com/postproject-org/postproject/releases/tag/v0.7.0-alpha.1).
From this demo checkout, with the current Manager checkout in
`../postproject-openassetio-manager`, build the compatible wheels and install
the pinned upstream linker:

```sh
python -m pip wheel --no-deps ../postproject-openassetio-manager . --wheel-dir dist
python -m pip install postproject-0.7.0a1-py3-none-any.whl \
  dist/postproject_openassetio_manager-0.4.0-py3-none-any.whl \
  dist/postproject_otio_demo-0.2.0-py3-none-any.whl
python -m pip install \
  git+https://github.com/OpenAssetIO/otio-openassetio.git@ee762d7d24670f84c30baa6149123b6d252a9969
```

The demo also needs the native library from the matching PostProject archive;
pass its absolute path with `--library`.
The older published Manager/demo wheels require earlier PostProject SDKs.
