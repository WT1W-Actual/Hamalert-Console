# HamAlert Client

A Python application that connects to [hamalert.org](https://hamalert.org) via telnet
(port 7300) and displays a live rolling feed of the 10 most recent DX spots in your
terminal.

## Features

- Connects to `hamalert.org:7300` using the DX-cluster telnet protocol
- Authenticates with your callsign and password
- Displays the 10 most recent spots, refreshing in place as new ones arrive
- No third-party dependencies — uses Python stdlib only

## Prerequisites

- Python 3.6 or higher
- An active HamAlert account (callsign + password)

## Installation

```bash
git clone <repository-url>
cd hamalert
bash install.sh
```

`install.sh` will:
1. Create a Python virtual environment (`hamalert_env/`)
2. Install the package
3. Prompt for your callsign and password
4. Write `~/.hamalert/config.json` (mode `600`)

## Manual configuration

If you prefer to configure by hand, create `~/.hamalert/config.json`:

```json
{
    "host": "hamalert.org",
    "port": 7300,
    "callsign": "YOURCALL",
    "password": "yourpassword",
    "timeout": 30
}
```

## Usage

```bash
source hamalert_env/bin/activate
python src/main.py
```

Or, if installed via `pip install -e .`:

```bash
hamalert
```

Press **Ctrl-C** to disconnect.

## License

This project is licensed under the MIT License.