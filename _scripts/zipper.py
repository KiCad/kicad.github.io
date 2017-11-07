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

        return output.split(' ')[0]

    else:
        return None

def get_file_size(f):
    f = os.path.abspath(f)
    p = Popen(['ls', '-lh', f], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()

    return output.split(' ')[4]

def archive_7z(archive, files):

    if len(files) == 0:
        print("Empty archive - " + str(archive))
        return

    # Archive to a temp location first
    # Only copy to output path if it is different
    tmp_file = "/tmp/archive.7z"

    # Delete temp file
    if os.path.exists(tmp_file):
        call(['rm', tmp_file])

    args = ['7z', 'a', '-t7z', '-mx=9', os.path.abspath(tmp_file)] + files

    print("Creating archive '{name}'".format(name=os.path.basename(archive)))
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    sz = get_file_size(tmp_file)

    copy = True

    # If an archive already exists in the target location,
    # do not copy the temp file there if the MD5 sums are identical
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
        archive_dir = os.path.dirname(archive)
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        call(['mv', tmp_file, archive])

    return str(sz)
