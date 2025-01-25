"""
LegendsVPN - A Python-based VPN management tool
"""

from .core import ProxyManager
from .cli import VpnCLI

__version__ = "0.1.0"
__all__ = ['ProxyManager', 'VpnCLI']
