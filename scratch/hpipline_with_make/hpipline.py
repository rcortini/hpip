from __future__ import print_function
import sys
import hpiplib

program_name = 'hpipline'

try :
    method_name = sys.argv[1]
    args = sys.argv[2:]
    try :
        method_to_call = getattr(hpiplib,method_name)
        method_to_call(args)
    except AttributeError :
        hpiplib.error_message(program_name,"Unrecognized method '%s'"%(method_name))
        sys.exit(1)
except IndexError :
    hpiplib.error_message(program_name,'Usage: python hpipline.py <method> [args ...]')
    sys.exit(1)
