import os
from subprocess import call, Popen, PIPE
import re

def git_old_hash(hash_file):

    if os.path.exists(hash_file):
        with open(hash_file) as f:
            return f.read().strip()

    return None

def git_hash(path):

    os.chdir(path)

    cmd = ['git', 'rev-parse', 'HEAD']

    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()

    return output

def git_hash(path):

    os.chdir(path)

    cmd = ['git', 'rev-parse', 'HEAD']

    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()

    return output

def git_hashes(path):
    
    os.chdir(path)
    
    cmd = ['git', 'log', '--pretty=format:%H']
    
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    output, err = p.communicate()
    
    return output.split()


def git_deepen(path):
    
    os.chdir(path)
    
    cmd = ['git' 'fetch' '--deepen', '1']
    
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    output, err = p.communicate()


def git_diff(path, commit):
    
    os.chdir(path)
    
    hashes = git_hashes(path)
    
    while ( commit not in hashes ):
        git_deepen(path)
        hashes = git_hashes(path)

    cmd = ['git', 'diff', '--name-status', str(commit)]

    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()

    return output


def write_hash(hash_file, hash):

    with open(hash_file, 'w') as f:
        f.write(hash)


def make_ascii(text):
    return ''.join([c for c in str(text) if ord(c) < 127])


def read_lib_table(lib_table_file):

    entries = []

    s_name = r'\(name ([^"]*?)\)'
    s_descr = r'\(descr "([^"]*)"'

    def cleanse(txt):
        txt = txt.strip()

        ends = [',', '.']

        for e in ends:
            if txt.endswith(e):
                txt = txt[:-1]

        return txt

    with open(lib_table_file, 'r') as f:
        for line in f:

            f_name = re.search(s_name, line)
            f_descr = re.search(s_descr, line)


            if f_name and f_descr:
                name = cleanse(f_name.groups()[0])
                desc = cleanse(f_descr.groups()[0])

                entries.append({'name': name, 'desc': desc})

    return entries


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

def purge_old_folders(parent, dirnames):

    if not os.path.exists(parent) or not os.path.isdir(parent):
        return

    for d in os.listdir(parent):

        if d in dirnames:
            continue

        d = os.path.join(parent, d)

        if not os.path.exists(d) or not os.path.isdir(d):
            continue

        call(['rm', '-rf', d])

def purge_old_archives(directory, archives):
    """
    Purge old archive files from a directory
    """

    if not os.path.exists(directory) or not os.path.isdir(directory):
        return

    files = os.listdir(directory)

    for fn in files:

        f = os.path.join(directory, fn)

        if not os.path.exists(f) or os.path.isdir(f):
            continue

        if fn in archives:
            continue

        # Delete!
        path = os.path.join(directory, fn)

        print("Deleting outdated archive '{arc}'".format(arc=fn))

        call(['rm', path])
