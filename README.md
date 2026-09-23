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

