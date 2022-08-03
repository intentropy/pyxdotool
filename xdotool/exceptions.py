#!/usr/bin/env python3
"""Exception classes for xdotool module"""

class NoXDoTool( Exception ):
    """xdotool is not installed on the system"""
    pass

class NonExistantMouseButton( Exception ):
    """The mouse button used for a mouse click does not exist"""
    pass