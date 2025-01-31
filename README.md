# LegendsVpn

A Python-based VPN management tool that fetches and manages proxy servers with a rich terminal interface.

## Features

- Automatic proxy fetching from multiple sources:
  - proxy-list.download
  - spys.me
  - free-proxy-list.net
- Smart proxy testing and selection
- Finds the fastest working proxy
- Beautiful terminal interface with ASCII art logo
- Rich text formatting with colors and tables
- Error handling and graceful degradation

## Installation

### From Source
1. Clone or download this repository
2. Navigate to the project directory
3. Install in development mode:
```bash
pip install -e .
```

### Using pip (when published)
```bash
pip install legendsvpn
```

## Usage

After installation, you can run LegendsVpn in two ways:

1. Using the command-line tool:
```bash
legendsvpn
```

2. Using Python:
```python
from legendsvpn import ProxyManager, VpnCLI

# Use the CLI
cli = VpnCLI()
cli.run()

# Or use the ProxyManager directly
proxy_manager = ProxyManager()
working_proxies = proxy_manager.find_working_proxies(min_working=3)
```

### Menu Options

1. **Fetch new proxies**: Downloads and updates the proxy list from multiple sources
2. **Connect to fastest proxy**: Tests multiple proxies and connects to the fastest one
3. **Exit**: Closes the program

## Package Structure

```
LegendsVpn/
├── legendsvpn/
│   ├── __init__.py      # Package initialization
│   ├── core.py          # Core proxy management functionality
│   └── cli.py           # Command-line interface
├── data/
│   └── proxies.txt      # Stored proxy lists
├── setup.py             # Package setup configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Proxy Testing Strategy

The program uses a smart proxy testing strategy:
1. Tests proxies continuously until finding working ones
2. Keeps testing additional proxies after finding the first working one
3. Maintains a list of working proxies sorted by speed
4. Only stops when either:
   - Found at least 3 working proxies
   - Or tested all available proxies

## Error Handling

The program includes error handling for:
- Network connectivity issues
- File system operations
- Invalid proxy formats
- Missing proxy lists
- Connection timeouts

## Note

This tool uses real proxies and will actually route your traffic through them. Make sure you understand the implications of using proxy servers before connecting to one.
