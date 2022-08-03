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
        system( "xfwm4 2>/dev/null &")
        system( "xfdesktop" )
        system( "xfsettingsd" )
        system( "mousepad 2>/dev/null &" )
        system( f"x11vnc -display :{xvfb.new_display} -forever -bg 2>/dev/null" )
        print( f":{xvfb.new_display}" )

        # Input pause for run test
        input( "Press ENTER to start tests" )

        # Run xdotool test
        xdt.mouse_move( 10 , 10 , sync = True )
        sleep( 1 )
        #xdt.mouse_restore( sync = True )
        sleep( 1 )
        xdt.mouse_move( 100 , 100 , sync = True )
        sleep( 1 )


        # input pause for shutdown
        input( "Press ENTER to shutdown test" )