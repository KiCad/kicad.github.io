import json
from helpers import make_ascii

class ModelList:
    def __init__(self, lib_name, archive_size):
        self.name = lib_name
        self.archive_size = archive_size
        self.data = []

        self.count = 0

    def add_model(self, model_name, model_archive_size):
        data = {}
        data['name'] = make_ascii(model_name)
        data['size'] = model_archive_size

        self.data.append(data)
        self.count += 1

    # Ensure data are sorted by name
    def reorder(self):
        self.data = sorted(self.data, key=lambda item: item['name'].lower())

    def encode_json(self):
        json_data = {}
        json_data['model'] = self.name

        model_data = []

        for d in self.data:
            # Remove datasheet links (not needed for JSON output!)
            x = d
            x.pop('data')
            model_data.append(x)

        json_data['models'] = model_data

        return json_data

    def model_html(self, model):

        name = model['name']
        size = model['size']

        if not size:
            size = ''

        html = '<tr><td>{name}</td><td>{size}</td></tr>'.format(
            name = name,
            size = size)

        """
        html = '<tr><td>{name}</td><td><a href="/download/packages3d/{lib}.3dshapes/{model}.7z">{size}</a></td></tr>\n'.format(
            name = name,
            size = size,
            model = name,
            lib = self.name
        )
        """

        return html

    def encode_html(self):
        """
        Encode a html file to display all items in the library
        """

        html = "---\n"
        html += 'title: "{t}"\n'.format(t=self.name)
        html += 'modelcount: "{n}"\n'.format(n=self.count)
        html += 'layout: modellib\n'
        html += 'model: {t}\n'.format(t=self.name)

        if self.archive_size:
            html += 'archivesize: "{n}"\n'.format(n=self.archive_size)

        html += "---\n\n"

        html += "<table><tr>\n"
        html += "<th>Model</th>\n"
        html += "<th>Size</th>\n"
        html += "</tr>\n"

        for d in self.data:
            html += self.model_html(d) + "\n"

        return html
