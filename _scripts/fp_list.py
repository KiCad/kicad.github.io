import json

class FootprintList:
    def __init__(self, lib_name, lib_description, archive_size):
        self.name = lib_name
        self.description = lib_description
        self.archive_size = archive_size
        self.data = []

        self.count = 0

    def add_footprint(self, fp):
        data = {}
        data['name'] = fp.name

        data['tags'] = fp.tags
        data['desc'] = fp.description

        self.data.append(data)
        self.count += 1

    # Ensure data are sorted by name
    def reorder(self):
        self.data = sorted(self.data, key=lambda item: item['name'].lower())

    def encode_json(self):
        json_data = {}
        json_data['lib'] = self.name

        fp_data = []

        for d in self.data:
            # Remove datasheet links (not needed for JSON output!)
            x = d
            x.pop('data')
            fp_data.append(x)

        json_data['footprints'] = fp_data

        return json_data

    def datasheet_link(self, ds):

        output = []

        for el in ds.split():

            links = ['http', 'www', 'ftp']

            if not el:
                el = ''

            link = False

            if any([el.startswith(i) for i in links]):
                link = True

            elif el.endswith('.pdf') or '.htm' in el:
                link = True

            if link:
                el = "[{ds}]({ds})".format(ds=el)

            output.append(el)

        return " ".join(output)

    def footprint_md(self, fp):
        md = "### {name}\n".format(name=fp['name'])

        desc = self.datasheet_link(fp['desc'])

        md += "{desc}\n".format(desc=desc)

        #md += "{desc}\n".format(desc=fp['desc'])
        md += "\n\nTags: *{tags}*".format(tags=fp['tags'])

        md += "\n"

        return md

    def encode_md(self):
        """
        Encode a markdown file to display all items in the library
        """

        md = "---\n"
        md += 'title: "' + self.name + '"\n'
        md += 'descr: "' + self.description + '"\n'
        md += 'footprintcount: "{n}"\n'.format(n=self.count)

        if self.archive_size:
            md += 'archivesize: "{n}"\n'.format(n=self.archive_size)

        md += "---\n\n"

        for d in self.data:
            md += self.footprint_md(d) + "\n"

        return md
