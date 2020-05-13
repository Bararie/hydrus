import os
import traceback
import collections.abc

class HydrusException( Exception ):
    
    def __str__( self ):
        
        s = []
        
        if isinstance( self.args, collections.abc.Iterable ):
            
            for arg in self.args:
                
                try:
                    
                    s.append( str( arg ) )
                    
                except:
                    
                    s.append( repr( arg ) )
                    
                
            
        else:
            
            s = [ repr( self.args ) ]
            
        
        return os.linesep.join( s )
        
    
class CantRenderWithCVException( HydrusException ): pass
class DataMissing( HydrusException ): pass

class DBException( HydrusException ): pass
class DBAccessException( HydrusException ): pass
class DBCredentialsException( HydrusException ): pass
class FileMissingException( HydrusException ): pass
class DirectoryMissingException( HydrusException ): pass
class SerialisationException( HydrusException ): pass
class NameException( HydrusException ): pass
class ShutdownException( HydrusException ): pass
class QtDeadWindowException(HydrusException): pass

class VetoException( HydrusException ): pass
class CancelledException( VetoException ): pass
class MimeException( VetoException ): pass
class SizeException( VetoException ): pass
class DecompressionBombException( SizeException ): pass

class ParseException( HydrusException ): pass
class StringConvertException( ParseException ): pass
class StringMatchException( ParseException ): pass
class URLClassException( ParseException ): pass
class GUGException( ParseException ): pass

class NetworkException( HydrusException ): pass

class NetworkInfrastructureException( NetworkException ): pass
class ConnectionException( NetworkInfrastructureException ): pass
class FirewallException( NetworkInfrastructureException ): pass
class CloudFlareException( NetworkInfrastructureException ): pass
class BandwidthException( NetworkInfrastructureException ): pass
class ServerException( NetworkInfrastructureException ): pass
class ServerBusyException( NetworkInfrastructureException ): pass

class StreamTimeoutException( NetworkException ): pass

class NetworkVersionException( NetworkException ): pass
class NoContentException( NetworkException ): pass
class NotFoundException( NetworkException ): pass
class NotModifiedException( NetworkException ): pass
class BadRequestException( NetworkException ): pass
class ConflictException( NetworkException ): pass
class MissingCredentialsException( NetworkException ): pass
class DoesNotSupportCORSException( NetworkException ): pass
class InsufficientCredentialsException( NetworkException ): pass
class RedirectionException( NetworkException ): pass
class SessionException( NetworkException ): pass
class WrongServiceTypeException( NetworkException ): pass
class ValidationException( NetworkException ): pass
class ShouldReattemptNetworkException( NetworkException ): pass