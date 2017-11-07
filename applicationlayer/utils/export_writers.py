# -*- coding: utf-8 -*-

import csv
import json


try:
    import io
    from StringIO import StringIO # python 2
except ImportError:
    from io import StringIO  # python 3


class CSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        fout = io.BytesIO()
        data = ''
        if value:
            data = value.get('rows')
        if data and isinstance(data[0],list):
            writer = csv.writer(fout, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)

            rows = []
            headers = []

            for row in value.get('rows', []):
                utf8_row = []
                for item in row:
                    if item and isinstance(item, unicode):
                        try:
                            item = item.encode('utf-8')
                        except Exception as e:

                            pass
                    utf8_row.append(item)
                rows.append(utf8_row)

            for item in value.get('header', []):
                if item:
                    item = item.encode('utf-8', 'ignore')
                headers.append(item)
            writer.writerow(headers)
            for k in range(len(rows)):
                try:
                    writer.writerow(rows[k])
                except UnicodeEncodeError as uerror:
                    print uerror.message
                    print rows[k]
            return fout.getvalue()


        elif data and isinstance(data[0],dict):
            headers_config = value.get('header')
            headers = [header['name'] for header in headers_config]
            writer = csv.DictWriter(fout, fieldnames = headers, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            rows = []
            for row in value.get('rows', {}):
                utf8_row = {}
                for key,value in row.items():
                    key = key.encode('utf-8','ignore')
                    if value and isinstance(value, unicode):
                        try:
                            value = value.encode('utf-8')
                        except Exception as e:

                            pass
                    utf8_row.update({key:value})
                rows.append(utf8_row)
            display_headers = {}
            for header in headers_config:
                display_headers.update({header['name']: header['display_name']})
            writer.writerow(display_headers)
            for k in range(len(rows)):
                try:
                    writer.writerow(rows[k])
                except UnicodeEncodeError as uerror:
                    print uerror.message
                    print rows[k]
            return fout.getvalue()


        else:
            return json.dumps({'status': 'error', 'message': 'Not a valid list type requested or no data is available to export given the request.'}, 400)
