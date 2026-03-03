#!/usr/bin/env python3
"""
HamAlert Client - Connects to hamalert.org via telnet (port 7300),
logs in with callsign and password, then streams incoming spot data.
"""

import socket
import sys
import os
from collections import deque
from datetime import datetime

# Allow running directly from the src/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import load_config


class HamAlertClient:
    """Telnet client for hamalert.org:7300 (DX-cluster protocol)."""

    def __init__(self):
        cfg = load_config()
        self.host = cfg["host"]
        self.port = cfg["port"]
        self.callsign = cfg["callsign"].upper()
        self.password = cfg["password"]
        self.timeout = cfg["timeout"]
        self._sock = None

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _recv_for(self, seconds: float = 2.0) -> bytes:
        """Read everything the server sends within *seconds* seconds."""
        self._sock.settimeout(seconds)
        buf = b""
        try:
            while True:
                chunk = self._sock.recv(4096)
                if not chunk:
                    break
                buf += chunk
        except socket.timeout:
            pass
        return buf

    def _send(self, text: str) -> None:
        self._sock.sendall((text + "\r\n").encode())

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def connect(self) -> None:
        """Open the TCP connection and authenticate."""
        print(f"Connecting to {self.host}:{self.port} ...")
        self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)

        # Read the server greeting / login prompt
        banner = self._recv_for(3.0)
        if banner:
            print(banner.decode(errors="replace").strip())

        # Send callsign; DX cluster nodes expect just the callsign first
        self._send(self.callsign)

        # Read whatever the server sends back (may be a password prompt or MOTD)
        response = self._recv_for(3.0)
        if response:
            print(response.decode(errors="replace").strip())

        # If a password prompt was detected, send the password
        lower = response.lower()
        if b"password" in lower or b"pass" in lower:
            self._send(self.password)
            motd = self._recv_for(3.0)
            if motd:
                print(motd.decode(errors="replace").strip())

        print(f"\nConnected as {self.callsign}. Waiting for spots...\n")

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    DISPLAY_ROWS = 10
    WIDTH = 78

    def _render(self, spots: deque, last_updated: str, first_draw: bool) -> None:
        """Redraw the rolling 10-spot display in place."""
        header  = f" WT1W @ {self.host}:{self.port}   last updated: {last_updated}"
        sep     = "\u2500" * self.WIDTH
        footer  = " Ctrl-C to quit"

        total_lines = 3 + self.DISPLAY_ROWS  # header + sep + spots + sep (footer on same last line)

        if not first_draw:
            # Move cursor back up to overwrite previous draw
            print(f"\033[{total_lines}A", end="")

        print(f"\033[2K{header[:self.WIDTH]}")
        print(f"\033[2K{sep}")
        for i, spot in enumerate(spots):
            label = f"{i + 1:>2}  "
            line  = (label + spot)[: self.WIDTH]
            print(f"\033[2K{line}")
        # Blank out any unfilled rows when fewer than 10 spots have arrived
        for _ in range(self.DISPLAY_ROWS - len(spots)):
            print(f"\033[2K")
        print(f"\033[2K{sep}")
        print(f"\033[2K{footer}", end="\r\n", flush=True)

    def stream(self) -> None:
        """Maintain a rolling display of the 10 most recent spots."""
        self._sock.settimeout(None)  # block indefinitely
        spots: deque = deque(maxlen=self.DISPLAY_ROWS)
        buf = b""
        first_draw = True
        try:
            while True:
                chunk = self._sock.recv(4096)
                if not chunk:
                    print("\nConnection closed by server.")
                    break
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    text = line.decode(errors="replace").rstrip()
                    if text:
                        spots.appendleft(text)
                        self._render(spots, datetime.now().strftime("%H:%M:%S"), first_draw)
                        first_draw = False
        except KeyboardInterrupt:
            print("\nDisconnected by user.")

    def disconnect(self) -> None:
        if self._sock:
            try:
                self._send("BYE")
            except OSError:
                pass
            self._sock.close()
            self._sock = None


def main():
    client = HamAlertClient()
    try:
        client.connect()
        client.stream()
    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except (OSError, ConnectionError) as e:
        print(f"Connection error: {e}")
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
