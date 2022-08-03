#!/usr/bin/env python3
"""Test file for import
"""

from os             import system
from time           import sleep
from xdotool        import XDoTool
from xvfbwrapper    import Xvfb


if __name__ == '__main__':
    # Run the test in Xvfb with VNC to monitor
    _xvfb = {
        "width": 1280, 
        "height": 740, 
        "colordepth": 24,
        }
    with Xvfb( **_xvfb ) as xvfb , XDoTool() as xdt:
        # Start VNC and Window Manager
        system( "xfwm4 2>/dev/null &")
        #system( "xfdesktop" )
        #system( "xfsettingsd" )
        system( "mousepad 2>/dev/null &" )
        system( f"x11vnc -display :{xvfb.new_display} -forever -bg 2>/dev/null" )
        print( f":{xvfb.new_display}" )

        # Input pause for run test
        input( "Press ENTER to start tests" )

        # Run xdotool test
        window = xdt.get_active_window()
        xdt.window_move(
            window = window,
            x = 0, 
            y = 0, 
            )
        xdt.window_size(
            window = window,
            width = _xvfb.get( "width" ),
            height = _xvfb.get( "height" ),
            )
        xdt.type_strings( 
            "Write shit to this file", 
            "and dont for get to save it", 
            newlines = True,
            )
        xdt.mouse_move( 24 , 32 , sync = True )
        xdt.click( "Left" )
        xdt.mouse_move( 36 , 195 , sync = True )
        xdt.click( "left" )
        xdt.type_strings( "this_is_a_test.txt" )
        xdt.mouse_move( 1120 , 710 , sync = True )
        sleep( 1 )
        xdt.click( 1 )


        # input pause for shutdown
        input( "Press ENTER to shutdown test" )