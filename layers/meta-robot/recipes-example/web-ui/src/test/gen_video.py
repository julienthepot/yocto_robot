import argparse
import asyncio
import signal
import sys
import time
from threading import Event, Lock, Thread
import cv2  # type: ignore[import]
import websockets  # type: ignore[import]

#!/usr/bin/env python3
# Stream video from /dev/video0 to a WebSocket as JPEG frames.
# Usage: python3 gen_video.py --host 0.0.0.0 --port 8765 --device /dev/video0 --width 1280 --height 720 --fps 15 --quality 80


class CameraCapture(Thread):
  def __init__(self, device: str, width: int, height: int, fps: int, quality: int):
    super().__init__(daemon=True)
    self.device = device
    self.width = width
    self.height = height
    self.fps = fps
    self.quality = quality
    self.stop_event = Event()
    self.latest_jpeg = None  # type: bytes | None
    self._lock = Lock()

  def get_latest(self):
    with self._lock:
      return self.latest_jpeg

  def stop(self):
    self.stop_event.set()

  def run(self):
    cap = cv2.VideoCapture(self.device, cv2.CAP_V4L2)
    if not cap.isOpened():
      print(f"ERROR: Unable to open camera device {self.device}", file=sys.stderr)
      return

    # Try to configure camera
    if self.width:
      cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(self.width))
    if self.height:
      cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self.height))
    if self.fps:
      cap.set(cv2.CAP_PROP_FPS, float(self.fps))
    # Prefer MJPG from camera if available (faster)
    try:
      cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    except Exception:
      pass

    target_dt = 1.0 / max(self.fps, 1)
    enc_params = [int(cv2.IMWRITE_JPEG_QUALITY), int(self.quality)]

    print(f"[Camera] Streaming from {self.device} at {self.width}x{self.height}@{self.fps} q={self.quality}", file=sys.stderr)

    last = time.perf_counter()
    while not self.stop_event.is_set():
      ok, frame = cap.read()
      if not ok or frame is None:
        # Brief backoff on read failure
        time.sleep(0.01)
        continue

      # Encode to JPEG
      ok, buf = cv2.imencode(".jpg", frame, enc_params)
      if ok:
        data = buf.tobytes()
        with self._lock:
          self.latest_jpeg = data

      # Simple pacing
      now = time.perf_counter()
      elapsed = now - last
      if elapsed < target_dt:
        time.sleep(target_dt - elapsed)
      last = now

    cap.release()
    print("[Camera] Stopped", file=sys.stderr)


async def video_handler(websocket, path, cam: CameraCapture, send_fps: int):
  # Optional: restrict to a specific path
  if path not in ("/", "/video"):
    await websocket.close(code=1008, reason="Invalid path")
    return

  # Binary frames (JPEG)
  try:
    interval = 1.0 / max(send_fps, 1)
    # Informational text message (optional). Comment out if undesired.
    info = f'{{"type":"info","format":"jpeg","width":{cam.width},"height":{cam.height},"fps":{send_fps}}}'
    await websocket.send(info)

    print(f"[WS] Client connected", file=sys.stderr)

    while True:
      frame = cam.get_latest()
      if frame is not None:
        await websocket.send(frame)  # binary message
      await asyncio.sleep(interval)
  except (websockets.ConnectionClosedError, websockets.ConnectionClosedOK, websockets.ConnectionClosed):
    # Client disconnected
    return


async def main_async(args):
  cam = CameraCapture(device=args.device, width=args.width, height=args.height, fps=args.capture_fps, quality=args.quality)
  cam.start()

  stop_event = asyncio.Event()

  def on_signal():
    stop_event.set()

  loop = asyncio.get_running_loop()
  try:
    loop.add_signal_handler(signal.SIGINT, on_signal)
    loop.add_signal_handler(signal.SIGTERM, on_signal)
  except NotImplementedError:
    # Windows compatibility
    pass

  print(f"[WS] Serving WebSocket on ws://{args.host}:{args.port}/video (send_fps={args.send_fps})", file=sys.stderr)
  async with websockets.serve(
    lambda ws: video_handler(ws, getattr(ws, "path", "/video"), cam, args.send_fps),
    args.host,
    args.port,
    max_size=None,  # allow large frames
    ping_interval=20,
    ping_timeout=20,
  ):
    await stop_event.wait()

  cam.stop()
  cam.join(timeout=2.0)


def parse_args():
  p = argparse.ArgumentParser(description="Stream /dev/video0 as JPEG frames over WebSocket.")
  p.add_argument("--device", default="/dev/video0", help="Video device path (default: /dev/video0)")
  p.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
  p.add_argument("--port", type=int, default=8765, help="Bind port (default: 8765)")
  p.add_argument("--width", type=int, default=1280, help="Capture width (default: 1280)")
  p.add_argument("--height", type=int, default=720, help="Capture height (default: 720)")
  p.add_argument("--capture-fps", type=int, default=30, help="Camera capture FPS (default: 30)")
  p.add_argument("--send-fps", type=int, default=15, help="FPS to send to clients (default: 15)")
  p.add_argument("--quality", type=int, default=80, help="JPEG quality 1-100 (default: 80)")
  return p.parse_args()


if __name__ == "__main__":
  args = parse_args()
  try:
    asyncio.run(main_async(args))
  except KeyboardInterrupt:
    pass
