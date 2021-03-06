import requests
import zlib
import os
import tempfile

from ponyexpress.api.lib.providers import Provider


class AptRepository(Provider):
    _repo_url = None

    _key_list = ['SHA256', 'Package', 'Version', 'Filename', 'Description', 'Architecture']

    def __init__(self, url):
        self._repo_url = url

    def set_url(self, url):
        self._repo_url = url

    def fetch_metadata(self):
        if self._repo_url is None:
            return None

        chunk_size = 1024 * 8

        r = requests.get(self._repo_url, stream=True)

        if r.status_code == 200:
            tmpfd = tempfile.TemporaryFile(mode='w+b')

            d = zlib.decompressobj(16 + zlib.MAX_WBITS)
            for chunk in r.iter_content(chunk_size):
                # write decompressed data
                tmpfd.write(d.decompress(chunk))

            # flush out file contents before reading
            tmpfd.flush()

            return self._parse_packages(tmpfd)
        else:
            return None

    #private
    def _parse_packages(self, filehandle):
        filehandle.seek(0)  # reset file pointer

        # Package blocks are separated by empty lines
        # Once we find such a line we read all the metadata for one Package
        # We use that data to process the package information
        metadata = {}

        # read until we find an empty line
        package_metadata = {}
        for line in filehandle:
            line = line.decode('utf-8')
            if line == "\n" or line == "\r\n":
                key = package_metadata.get('sha256')
                if key is not None:
                    metadata[key] = package_metadata

                package_metadata = {}
            else:
                key, value = self._parse_metadata(line)
                if key is not None or value is not None:
                    package_metadata[key] = value

        # remember to close the filehandle
        filehandle.close()

        return metadata

    def _parse_metadata(self, package_metadata):
        # split line into key => value pair
        try:
            k, v = package_metadata.split(':', 1)

            v = v.rstrip('\n').lstrip()
            k = k.rstrip('\n').lstrip()

            # Check if key => value is required
            if k in self._key_list:
                return k.lower(), v
        except ValueError:
            return None, None

        return None, None
