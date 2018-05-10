from __future__ import print_function
import sys

try :
    method_name = sys.argv[1]
    args = sys.argv[2:]
    # method_to_call = getattr(hpiplib,method_name)
    # method_to_call(*sys.argv[2:])
    print('%s %s'%(method_name,' '.join([a for a in args])))

except IndexError :
    print('Usage: python hpipline.py <method> [args ...]', file=sys.stderr)
    sys.exit(1)
