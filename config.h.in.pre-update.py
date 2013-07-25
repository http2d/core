#!/usr/bin/env python

import os, re, sys

## assert (len(sys.argv) == 2)

PATH_SRC = sys.argv[1]
PATH_BIN = sys.argv[2]

FILENAME_CMK = os.path.join (PATH_SRC, 'CMakeLists.txt')
FILENAME_PRE = os.path.join (PATH_SRC, 'config.h.in.pre')
FILENAME_NEW = os.path.join (PATH_BIN, 'config.h.in')

# Parse CMakeLists.txt
with open(FILENAME_CMK, 'r') as f:
    cont = f.read()

includes_t = ''
for h in re.findall (r'CHECK_INCLUDE_FILES *\(.+? *(\w+)\)', cont, re.IGNORECASE):
    includes_t += '#cmakedefine %s\n' %(h)

sizes_t = ''
for h in re.findall (r'CHECK_TYPE_SIZE *\(.+? *(\w+)\)', cont, re.IGNORECASE):
    sizes_t += '/* %s */\n' %(h.replace('SIZEOF_','').replace('_',' '))
    sizes_t += '#cmakedefine HAVE_%s\n' %(h)
    sizes_t += '@%s_CODE@\n' %(h)
    sizes_t += '#ifdef HAVE_%s\n' %(h)
    sizes_t += '# define HAVE_%s\n' %(h.replace('SIZEOF_',''))
    sizes_t += '#endif\n\n'

# Read .pre file
with open(FILENAME_PRE, 'r') as f:
    cont = f.read()

cont = cont.replace ("${{includes}}", includes_t)
cont = cont.replace ("${{sizes}}", sizes_t)

with open(FILENAME_NEW, 'w+') as f:
    f.write (cont)
