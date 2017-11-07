import json
from helpers import datasheet_link, make_ascii

class FootprintList:
    def __init__(self, lib_name, archive_size):
        self.name = lib_name
        self.archive_size = archive_size
        self.data = []

        self.count = 0

    def add_footprint(self, fp):
        data = {}
        data['name'] = make_ascii(fp.name)

        data['tags'] = make_ascii(fp.tags)
        data['desc'] = make_ascii(fp.description)

        self.data.append(data)
        self.count += 1

    # Ensure data are sorted by name
    def reorder(self):
        self.data = sorted(self.data, key=lambda item: str(item['name']).lower())

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

    def footprint_html(self, fp):

        html = "<tr><td>{name}</td><td>{description}</td></tr>\n".format(
            name = fp['name'],
            description = datasheet_link(fp['desc'])
            )

        return html

    def encode_html(self):
        """
        Encode a html file to display all items in the library
        """

        html = "---\n"
        html += 'title: "' + self.name + '"\n'
        html += 'footprintcount: "{n}"\n'.format(n=self.count)
        html += 'layout: fplib\n'

        if self.archive_size:
            html += 'archivesize: "{n}"\n'.format(n=self.archive_size)

        html += "---\n\n"

        html += "<table>\n"
        html += "<tr>\n"
        html += "<th>Footprint</th>\n"
        html += "<th>Description</th>\n"
        html += "</tr>\n"

        for d in self.data:
            html += self.footprint_html(d)

        html += "</table>\n"
        return html
