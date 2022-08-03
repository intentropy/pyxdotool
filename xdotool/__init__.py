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


    # Keyboard commands
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


    # Window Commands
    def search( 
        self,                   pattern,
        match_class = False,    match_classname = False,    match_name = False,
        match_all = False,      match_any = False,
        maxdepth = None,        pid = None,                 screen = None,
        desktop = None,         limit = None,               
        only_visible = False,   sync = False,
        ):
        """Search for windows.  Returns a list of window ids for all matches found"""
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "search"
        _options = []
        if match_class:
            _options.append( "--class" )
        if match_classname:
            _options.append( "--classname" )
        if match_name:
            _options.append( "--name" )
        if match_all:
            _options.append( f"--all" )
        if match_any:
            _options.append( f"--any" )
        if maxdepth is not None:
            _options.append( f"--maxdepth {maxdepth}" )
        if pid is not None:
            _options.append( f"--pid {pid}" )
        if screen is not None:
            _options.append( f"--screen {screen}" )
        if desktop is not None:
            _options.append( f"--desktop {desktop}" )
        if limit is not None:
            _options.append( f"--limit {limit}" )
        if only_visible:
            _options.append( "--onlyvisible" )
        if sync:
            _options.append( "--sync" )
        _xdotool_cmd[ "options "] = " ".join( _options )
        _xdotool_cmd[ "args" ] = pattern
        _cmd_ret =  _cmd_out(
            self.xdotool_cmd.format( **_xdotool_cmd ),
            stderr = False,
            ).split( "\n" )
        _ret = []
        for line in _cmd_ret:
            if line:
                _ret.append(
                    int( line )
                    )
        return _ret

    # Skipped Window commands
    """
        The following commands are currently being skipped:
            - selectwindow
            - behave
            - windowraise
            - windowparent
            - windowunmap
            - set_window

        These are being skipped because it does not fit my
        personal use case for this module.  They will eventually be added in
    """

    def get_window_pid( self , window ):
        """Return the pid for a windows process"""
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "getwindowpid"
        _xdotool_cmd[ "args" ] = window
        return int(
            _cmd_out(
                self.xdotool_cmd.format( **_xdotool_cmd ),
                stderr = False,
                )
            )

    def get_window_name( self , window ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "getwindowname"
        _xdotool_cmd[ "args" ] = window
        return _cmd_out(
            self.xdotool_cmd.format( **_xdotool_cmd ),
            stderr = False,
            )

    def get_window_geometry( self , window ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "getwindowgeometry"
        _xdotool_cmd[ "options" ] = "--shell"
        _xdotool_cmd[ "args" ] = window
        _cmd_ret = _cmd_out(
            self.xdotool_cmd.format( **_xdotool_cmd ),
            stderr = False,
            ).split( "\n" )
        _ret = {}
        for line in _cmd_ret:
            if line:
                _line_split = line.split( "=" )
                _ret[
                    _line_split[ 0 ].lower()
                    ] = _line_split[ 1 ]
        return _ret


    def get_window_focus( self , no_wm_class = False ):
        """Get the window ID of the current window in focus.
        no_wm_class will set the -f option.  See man XDOTOOL(1)"""
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "getwindowfocus"
        if no_wm_class:
            _xdotool_cmd[ "options" ] = "-f"
        return int(
            _cmd_out(
                self.xdotool_cmd.format( **_xdotool_cmd ),
                stderr = False,
                )
            )

    def window_size(
        self, 
        window,             width,          height, 
        use_hints = False,  sync = False,
        ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "windowsize"
        _options = []
        if use_hints:
            _options.append( "--usehints" )
        if sync:
            _options.append( "--sync" )
        _xdotool_cmd[ "options" ] = " ".join( _options )
        _xdotool_cmd[ "args" ] = f"{window} {width} {height}"
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def window_move(
        self,
        window,         x,                  y,
        sync = False,   relative = False,
        ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "windowmove"
        _options = []
        if sync:
            _options.append( "--sync" )
        if relative:
            _options.append( "--relative" )
        _xdotool_cmd[ "options" ] = " ".join( _options )
        _xdotool_cmd[ "args" ] = f"{window} {x} {y}"
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def window_focus(
        self, 
        window,
        sync = False,
        ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "windowfocus"
        if sync:
            _xdotool_cmd[ "options" ] = "--sync"
        _xdotool_cmd[ "args" ] = window
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def window_map(
        self, 
        window,
        sync = False,
        ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "windowmap"
        if sync:
            _xdotool_cmd[ "options" ] = "--sync"
        _xdotool_cmd[ "args" ] = window
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )

    def window_close( self , window ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "windowclose"
        _xdotool_cmd[ "args" ] = window
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )
    
    def window_kill( self , window ):
        _xdotool_cmd = deepcopy( self.xdotool_cmd_fmt )
        _xdotool_cmd[ "command" ] = "windowkill"
        _xdotool_cmd[ "args" ] = window
        return _cmd(
            self.xdotool_cmd.format( **_xdotool_cmd )
            )


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

        
