import os
from subprocess import call

def make_ascii(text):
    return ''.join([c for c in str(text) if ord(c) < 127])

def datasheet_link(text):
    links = ['http', 'www', 'ftp']

    if not text:
        text = ''


    out = []

    for element in text.split():
        link = False

        el = element.lower()

        if any([el.startswith(i) for i in links]):
            link = True

        elif el.endswith('.pdf') or '.htm' in el:
            link = True

        if link:
            element = '<a href="{el}">{el}</a>'.format(el=element)

        out.append(element)

    return make_ascii(' '.join(out))

def purge_old_archives(directory, names):
    """
    Purge old archive files from a directory
    """

    if not os.path.exists(directory) or not os.path.isdir(directory):
        return

    files = os.listdir(directory)

    for fn in files:

        f = fn
        if f.endswith('.7z'):
            f = f[:-3]
        else:
            continue

        if f in names:
            continue

        # Delete!
        path = os.path.join(directory, fn)

        print("Deleting outdated archive '{arc}'".format(arc=fn))

        call(['rm', path])
