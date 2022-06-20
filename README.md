# stream-snap-server
An HTTP server to capture screenshots from a video stream. Basic Authentication is supported. To grab the latest screenshot, default access is `http://localhost:8080/img`

## Usage
This script is a perfect companion to integrate your DIY security camera to [Homebridge](https://homebridge.io) or [Scrypted](https://github.com/koush/scrypted)

## Dependencies
`ffmpeg` is required to load the video stream and capture screenshot.

## Supported (Tested) streaming protocols
1. RTSP

## [Docker](https://hub.docker.com/r/donkeystudio/stream-snap-server)
Supported architectures: `linux/arm/v7`, `linux/arm64`, `linux/amd64`
```
docker run --rm --network=host donkeystudio/stream-snap-server
```

## Startup Configuration
```
python3 main.py --help
```

```
usage: main.py [-h] [-u USER] [-pwd PASSWORD] [-p PORT] stream_url

positional arguments:
  stream_url            Stream URL

optional arguments:
  -h,            --help                show this help message and exit
  -u USER,       --user USER           Username (default: None)
  -pwd PASSWORD, --password PASSWORD   Password (default: None)
  -p PORT,       --port PORT           Port (default: 8080)
  -f FRAMES,     --frames FRAMES       Number of frames to capture (default: 4)
```

## Example
```
python3 main.py -u user -pwd password -p 8888 -f 2 rtsp://192.168.0.10:8554/preview
```

## Notes
The program will load and capture 4 frames (instead of 1) to prevent packet/frame loss situations. It can be configured using `-f` or `--frames` argument
