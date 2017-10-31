"""
Functions for compressing files for distribution
"""

import os
from subprocess import call, Popen, PIPE

def archive_7z(archive, files, **kwargs):

    # Add each file to the archive individually
    for f in files:
        args = ['7z', 'a', '-t7z', '-mx=9', os.path.abspath(archive), f]
        call(args)


    p = Popen(['ls', '-lh', archive], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()

    sz = output.split(' ')[4]

    return str(sz)
