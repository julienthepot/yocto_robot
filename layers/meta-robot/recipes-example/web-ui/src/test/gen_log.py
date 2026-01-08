import argparse
import random
import time
from datetime import datetime
import requests

#!/usr/bin/env python3



def generate_random_log():
  """Generate a random log entry."""
  levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
  messages = [
    "System started successfully",
    "Connection established",
    "Processing request",
    "Database query executed",
    "Cache updated",
    "User authenticated",
    "File uploaded",
    "Configuration loaded",
    "Service health check passed",
    "Network timeout occurred",
    "Invalid input detected",
    "Retry attempt failed",
    "Resource not found",
    "Permission denied",
    "Memory usage high",
    "CPU load increased",
    "Disk space low",
    "Temperature sensor reading: OK",
    "Motor speed adjusted",
    "Battery level: 85%",
  ]
  
  level = random.choice(levels)
  message = random.choice(messages)
  created = datetime.now().isoformat()
  
  return {
    "level": level,
    "message": message,
    "created": created,
  }


def send_log(url: str, log_data: dict):
  """Send log data to the server."""
  try:
    response = requests.post(url, data=log_data, timeout=5)
    if response.status_code == 200:
      print(f"[{log_data['created']}] {log_data['level']}: {log_data['message']} -> OK")
    else:
      print(f"Failed to send log: HTTP {response.status_code}")
  except requests.exceptions.RequestException as e:
    print(f"Error sending log: {e}")


def main():
  parser = argparse.ArgumentParser(description="Send random logs to a server.")
  parser.add_argument("--url", default="http://localhost:5000/log/add", help="Target URL (default: http://localhost:5000/log/add)")
  parser.add_argument("--interval", type=float, default=2.0, help="Interval between logs in seconds (default: 2.0)")
  parser.add_argument("--count", type=int, default=0, help="Number of logs to send (0 = infinite, default: 0)")
  
  args = parser.parse_args()
  
  print(f"Sending logs to {args.url} every {args.interval}s")
  print("Press Ctrl+C to stop\n")
  
  sent = 0
  try:
    while args.count == 0 or sent < args.count:
      log_data = generate_random_log()
      send_log(args.url, log_data)
      sent += 1
      time.sleep(args.interval)
  except KeyboardInterrupt:
    print(f"\nStopped. Sent {sent} logs.")


if __name__ == "__main__":
  main()