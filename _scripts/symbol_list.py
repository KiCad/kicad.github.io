import json

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
        data['desc'] = doc.get('description', '')
        data['keys'] = doc.get('keywords', '')
        data['data'] = doc.get('datasheet', '')

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
        self.data = sorted(self.data, key=lambda item: item['name'].lower())

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

    def datasheet_link(self, ds):
        links = ['http', 'www', 'ftp']

        if not ds:
            ds = ''

        link = False

        if any([ds.startswith(i) for i in links]):
            link = True

        elif ds.endswith('.pdf') or '.htm' in ds:
            link = True

        if link:
            return "[{ds}]({ds})".format(ds=ds)
        else:
            return ds

    def symbol_md(self, symbol):
        md = "### {name}\n".format(name=symbol['name'])
        md += "{desc}\n".format(desc=symbol['desc'])
        md += "\n\nKeywords: *{keys}*".format(keys=symbol['keys'])

        ds = self.datasheet_link(symbol['data'])
        if len(ds) > 2:
            md += "\n\nDatasheet: *{data}*".format(data=ds)

        md += "\n"

        return md

    def encode_md(self):
        """
        Encode a markdown file to display all items in the library
        """

        md = "---\n"
        md += 'title: "{t}"\n'.format(t=self.name)
        md += 'descr: "{d}"\n'.format(d=self.description)
        md += 'symbolcount: "{n}"\n'.format(n=self.count)

        if self.archive_size:
            md += 'archivesize: "{n}"\n'.format(n=self.archive_size)

        md += "---\n\n"

        for d in self.data:
            md += self.symbol_md(d) + "\n"

        return md
