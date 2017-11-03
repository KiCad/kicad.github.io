import json
from helpers import datasheet_link, make_ascii

class SymbolList:
    def __init__(self, lib_name, lib_description, archive_size):
        self.name = lib_name
        self.description = lib_description
        self.archive_size = archive_size
        self.data = []

        self.count = 0

    def add_component(self, cmp, aliases=False):
        data = {}
        data['name'] = cmp.name

        doc = cmp.documentation

        keys = doc.keys()
        data['desc'] = make_ascii(doc.get('description', ''))
        data['keys'] = make_ascii(doc.get('keywords', ''))
        data['data'] = make_ascii(doc.get('datasheet', ''))

        self.data.append(data)
        self.count += 1

        # Any aliases?
        if aliases:
            for alias_name in cmp.aliases.keys():
                data = {}
                data['name'] = alias_name

                alias = cmp.aliases[alias_name]

                keys = alias.keys()

                data['desc'] = alias.get('description', '')
                data['keys'] = alias.get('keywords', '')
                data['data'] = alias.get('datasheet', '')
                self.data.append(data)

                self.count += 1

    # Ensure data are sorted by name
    def reorder(self):
        self.data = sorted(self.data, key=lambda item: str(item['name']).lower())

    def encode_json(self):
        json_data = {}
        json_data['lib'] = self.name

        symbol_data = []

        for d in self.data:
            # Remove datasheet links (not needed for JSON output!)
            x = d
            x.pop('data')
            symbol_data.append(x)

        json_data['symbols'] = symbol_data

        return json_data

    def symbol_html(self, symbol):

        desc = symbol['desc']
        keys = symbol['keys']
        ds = str(datasheet_link(symbol['data']))

        elements = []

        if desc:
            elements.append('Description: ' + desc)
        else:
            elements.append('<i>Description missing</i>')

        if keys:
            elements.append('Keys: ' + keys)

        if ds and len(ds) > 2:
            elements.append('Datasheet: ' + ds)

        html = "<tr>\n"
        html += "<td>{name}</td><td>{description}</td>\n".format(
            name = symbol['name'],
            description = '<br>'.join(elements))
        html += "</tr>\n"

        return html

    def encode_html(self):
        """
        Encode a markdown file to display all items in the library
        """

        html = "---\n"
        html += 'title: "{t}"\n'.format(t=self.name)
        html += 'descr: "{d}"\n'.format(d=self.description)
        html += 'symbolcount: "{n}"\n'.format(n=self.count)
        html += 'layout: symlib\n'

        if self.archive_size:
            html += 'archivesize: "{n}"\n'.format(n=self.archive_size)

        html += "---\n\n"

        html += "<table>\n"

        html += "<tr>\n"
        html += "<th>Symbol</th>\n"
        html += "<th>Description</th>\n"
        html += "</tr>\n"

        for d in self.data:
            html += self.symbol_html(d)

        html += "</table>\n"
        return html
