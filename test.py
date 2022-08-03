#!/usr/bin/env python3
"""Test file for import
"""

from os             import system
from time           import sleep
from xdotool        import XDoTool
from xvfbwrapper    import Xvfb


if __name__ == '__main__':
    # Run the test in Xvfb with VNC to monitor
    with Xvfb() as xvfb , XDoTool() as xdt:
        # Start VNC and Window Manager
        system( f"x11vnc -display :{xvfb.new_display} -forever -bg 2>/dev/null" )
        system( "xfwm4 2>/dev/null &")
        system( "mousepad 2>/dev/null &" )
        print( f":{xvfb.new_display}" )

        # Input pause for run test
        input( "Press ENTER to start tests" )

        # Run xdotool test
        window = xdt.get_window_focus()
        sleep( 1 )
        xdt.window_close(window)



        # input pause for shutdown
        input( "Press ENTER to shutdown test" )