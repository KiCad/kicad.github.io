import os
from subprocess import call

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

    return ' '.join(out)

def purge_old_archives(directory, names):
    """
    Purge old archive files from a directory
    """

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
