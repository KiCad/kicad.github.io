"""
Functions for compressing files for distribution
"""

import os
from subprocess import call, Popen, PIPE

def file_md5(file):
    fn = os.path.abspath(file)

    if os.path.exists(file):
        p = Popen(['md5sum', file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()

        return output.split()[0]

    else:
        return None

def archive_7z(archive, files, silent=True):

    # Archive to a temp location first
    # Only copy to output path if it is different
    tmp_file = "/tmp/archive.7z"

    # Delete temp file
    if os.path.exists(tmp_file):
        call(['rm', tmp_file])

    # Add each file to the archive individually
    for f in files:
        args = ['7z', 'a', '-t7z', '-mx=9', os.path.abspath(tmp_file), f]
        if silent:
            args.append('>')
            args.append('/dev/null')
        call(args)

    p = Popen(['ls', '-lh', tmp_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()

    # Calculate archive size
    sz = output.split(' ')[4]

    copy = True

    if os.path.exists(archive):
        md5_archive = file_md5(archive)
        md5_tmp = file_md5(tmp_file)

        print("Comparing MD5:")
        print("Old: " + md5_archive)
        print("New: " + md5_tmp)

        if md5_tmp == md5_archive:
            print("No changes to archive {f} - skipping".format(f=os.path.basename(archive)))
            copy = False

    if copy:
        call(['mv', tmp_file, archive])

    return str(sz)
