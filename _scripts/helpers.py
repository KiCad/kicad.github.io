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

        el = element

        # Strip quote characters
        start = ['"', "'", "[", "(", "{", ":"]
        end = ['"', "'", "]", ")", "}", ".", ","]

        for s in start:
            if el.startswith(s):
                el = el[1:]

        for e in end:
            if el.endswith(e):
                el = el[:-1]

        if any([el.lower().startswith(i) for i in links]):
            link = True

        elif el.endswith('.pdf') or '.htm' in el:
            link = True

        if link:
            element = '<a href="{link}">{text}</a>'.format(link=el, text=element)

        out.append(element)

    return make_ascii(' '.join(out))

def purge_old_archives(directory, archives):
    """
    Purge old archive files from a directory
    """

    if not os.path.exists(directory) or not os.path.isdir(directory):
        return

    files = os.listdir(directory)

    for fn in files:

        if fn in archives:
            continue

        # Delete!
        path = os.path.join(directory, fn)

        print("Deleting outdated archive '{arc}'".format(arc=fn))

        call(['rm', path])
