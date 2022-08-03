#!/usr/bin/env python3
"""xdotool module

This is a rebuild of the older module I made
"""

# Imports
from .exceptions    import *

from copy       import deepcopy
from shlex      import split    as slxsplit
from shutil     import which
from subprocess import check_output , DEVNULL, STDOUT
from os         import system



# Constants
SPECIAL_CHARS = {
        '@': 'at',
        '&': 'ampersand',
        '^': 'asciicircum', # Caret
        '~': 'asciitilde',
        '*': 'asterisk',
        '\\': 'backslash',
        '\b': 'BackSpace',
        '|': 'bar',         # Pipe
        '{': 'braceleft',
        '}': 'braceright',
        '[': 'bracketleft',
        ']': 'bracketright',
        ',': 'comma',
        ':': 'colon',
        '$': 'dollar',
        '=': 'equal',
        '!': 'exclam',
        '>': 'greater',
        '<': 'less',
        '-': 'minus',
        '#': 'numbersign',
        '(': 'parenleft',
        ')': 'parenright',
        '%': 'percent',
        '.': 'period',
        '+': 'plus',
        '?': 'question',
        '\"': 'quotedbl',
        '\'': 'quoteright',
        '`': 'quoteleft',   # Backtick
        '\n': 'Return',
        ';': 'semicolon',
        '/': 'slash',
        ' ': 'space',
        '\t': 'Tab',
        '_': 'underscore',
        }

SPECIAL_KEYS = {
        'Alt': 'alt',
        'Ctrl': 'ctrl',
        'Delete': 'Delete',
        'Down': 'Down',
        'End': 'End',
        'Enter': 'Return',
        'Home': 'Home',
        'Left': 'Left',
        'Meta': 'meta',
        'Right': 'Right',
        'Super': 'super',
        'Up': 'Up',
        }



# Internal Commands
def _cmd( command ):
    """Run command and return True or Flase based on error codes"""
    return bool(
        not(
            system( command )
            )
        )

def _cmd_out( command , stderr = None ):
    """Run a command and grab output
    stderr can be None, True, or False
        - None: Default behaviour
        - True: stderr to stdout
        - False: stderr to devnull
    """
    _stderr = {
        True: STDOUT,
        False: DEVNULL,
        }
    _check_output = {}
    if stderr is not None:
        _check_output[ "stderr" ] = _stderr.get( stderr )
    return check_output( 
        slxsplit( command ), 
        **_check_output 
        ).decode()
    


# XDoTool class
class XDoTool():
    def __init__( self ):
        # Test for xdotool being installed, raise early if missing
        if not which( "xdotool" ):
            raise NoXDoTool( "xdotool is not installed on the system" )

        # Assing CONSTANTS as attributes
        self.SPECIAL_KEYS = SPECIAL_KEYS
        self.SPECIAL_CHARS = SPECIAL_CHARS

        # Command base string
        self.xdotool_cmd = "xdotool {command} {options} {args}"
        self.xdotool_cmd_fmt = { "command": "" , "options": "" , "args": "" }

        # Key options
        self.key_opts = {
            "window": None,
            "clearmodifiers": None,
            "delay": None,
            }

    def __enter__( self ):
        return self

    def __exit__( self , *exception ):
        return

    # testing functions
    def cmd_out( self , command , stderr = None ):
        print( 
            _cmd_out( command , stderr )
            )

    # Key commands
    """
        *args is a list of keys or strings to use for the command
        key up and down will hold or release all of the keys in args
    """
    def _key_opts( self ):
        """Create the options string from self.key_opts"""
        _ret = []
        if self.key_opts.get( "clearmodifiers" ):
            _ret.append( "--clearmodifiers" )
        _window = self.key_opts.get( "window" )
        if _window:
            _ret.append( f"--window {_window}")
        _delay = self.key_opts.get( "delay" )
        if _delay:
            _ret.append( f"--delay {_delay}" )
        return " ".join( _ret )

    def _key_arg_stirng( self , keys ):
        """Take a list of Keys and create an argument string
        for this key combination.
        Check for an alias for the key in SPECIAL_KEYS and SPECIAL_CHARS
        """
        _ret = []
        for key in keys:
            if key in self.SPECIAL_KEYS:
                _ret.append(
                    self.SPECIAL_KEYS.get( key )
                    )
            elif key in self.SPECIAL_CHARS:
                _ret.append(
                    self.SPECIAL_CHARS.get( key )
                    )
            else:
                _ret.append( key )
        return "+".join( _ret )


    def key( self , *args ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "key"
        _xdotool_cmd[ "options" ] = self._key_opts()
        _xdotool_cmd[ "args" ] = self._key_arg_stirng( args )
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def key_down( self , *args ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "keydown"
        _xdotool_cmd[ "options" ] = self._key_opts()
        _xdotool_cmd[ "args" ] = self._key_arg_stirng( args )
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def key_up( self , args ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "keyup"
        _xdotool_cmd[ "args" ] = self._key_arg_stirng( args )
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def type_strings( self, *args , newlines = False ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "type"
        _xdotool_cmd[ "options" ] = self._key_opts()
        for arg in args:
            _xdotool_cmd[ "args" ] = arg
            _cmd(
                self.xdotool_cmd.format( **_xdotool_cmd )
                )
            if newlines:
                self.key( "\n" )

    # Mouse Commands


    # Desktop and Window Commands
    def window_activate( self , window , sync = True ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "windowactivate"
        if sync:
            _xdotool_cmd[ "options" ] = "--sync"
        _xdotool_cmd[ "args" ] = window_id
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )
        
    def get_active_window( self ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "getactivewindow"
        return int(
            _cmd_out(
                self.xdotool_cmd.format( **_xdotool_cmd )
                )
            )

    def set_num_desktops( self , desktops ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "set_num_desktops"
        _xdotool_cmd[ "args" ] = desktops
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def get_num_desktops( self ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "get_num_desktops"
        return int(
            _cmd_out(
                self.xdotool_cmd.format( **_xdotool_cmd )
                )
            )

    def get_desktop_viewport( self ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "get_desktop_viewport"
        _cmd_ret = _cmd_out(
                self.xdotool_cmd.format( **_xdotool_cmd ),
                stderr = False,
                ).split()
        _ret = {
            "x": _cmd_ret[ 0 ],
            "y": _cmd_ret[ 1 ],
            }
        return _ret

    def set_desktop_viewport( self , x , y ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "set_desktop_viewport"
        _xdotool_cmd[ "args" ] = f"{x} {y}"
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def set_desktop( self , desktop ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "set_desktop"
        _xdotool_cmd[ "args" ] = desktop
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def get_desktop( self ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "get_desktop"
        return int(
            _cmd_out(
                self.xdotool_cmd.format( **_xdotool_cmd )
                )
            )

    def set_desktop_for_window( self , window , desktop ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "set_desktop_for_window"
        _xdotool_cmd[ "args" ] = f"{window} {desktop}"
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def get_desktop_for_window( self , window ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "get_desktop_for_window"
        _xdotool_cmd[ "args" ] = window
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    # Miscellaneous Commands 

        