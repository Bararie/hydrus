#!/usr/bin/env python2

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

try:
    
    import locale
    
    try: locale.setlocale( locale.LC_ALL, '' )
    except: pass
    
    from include import HydrusExceptions
    from include import HydrusConstants as HC
    from include import HydrusData
    from include import HydrusPaths
    
    import os
    import sys
    import time
    
    from include import ServerController
    import threading
    from twisted.internet import reactor
    from include import HydrusGlobals
    from include import HydrusLogger
    import traceback
    
    import argparse
    
    argparser = argparse.ArgumentParser( description = 'hydrus network server' )
    
    argparser.add_argument( 'action', default = 'start', nargs = '?', choices = [ 'start', 'stop', 'restart' ], help = 'either start this server (default), or stop an existing server, or both' )
    argparser.add_argument( '-d', '--db_dir', help = 'set an external db location' )
    
    result = argparser.parse_args()
    
    if result.db_dir is None:
        
        db_dir = os.path.join( HC.BASE_DIR, 'db' )
        
    else:
        
        db_dir = result.db_dir
        
    
    try:
        
        HydrusPaths.MakeSureDirectoryExists( db_dir )
        
    except:
        
        raise Exception( 'Could not ensure db path ' + db_dir + ' exists! Check the location is correct and that you have permission to write to it!' )
        
    
    action = ServerController.ProcessStartingAction( db_dir, result.action )
    
    log_path = os.path.join( db_dir, 'server.log' )
    
    with HydrusLogger.HydrusLogger( log_path ) as logger:
        
        try:
            
            if action in ( 'stop', 'restart' ):
                
                ServerController.ShutdownSiblingInstance( db_dir )
                
            
            if action in ( 'start', 'restart' ):
                
                HydrusData.Print( 'Initialising controller...' )
                
                threading.Thread( target = reactor.run, kwargs = { 'installSignalHandlers' : 0 } ).start()
                
                controller = ServerController.Controller( db_dir )
                
                controller.Run()
                
            
        except HydrusExceptions.PermissionException as e:
            
            error = str( e )
            
            HydrusData.Print( error )
            
        except:
            
            error = traceback.format_exc()
            
            HydrusData.Print( 'Hydrus server failed' )
            
            HydrusData.Print( traceback.format_exc() )
            
        finally:
            
            HydrusGlobals.view_shutdown = True
            HydrusGlobals.model_shutdown = True
            
            try: controller.pubimmediate( 'wake_daemons' )
            except: pass
            
            reactor.callFromThread( reactor.stop )
            
        
    
except HydrusExceptions.PermissionException as e:
    
    HydrusData.Print( e )
    
except Exception as e:
    
    import traceback
    import os
    
    print( traceback.format_exc() )
    
    if 'db_dir' in locals() and os.path.exists( db_dir ):
        
        dest_path = os.path.join( db_dir, 'crash.log' )
        
        with open( dest_path, 'wb' ) as f:
            
            f.write( traceback.format_exc() )
            
        
        print( 'Critical error occured! Details written to crash.log!' )
        
    