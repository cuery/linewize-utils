from os import listdir, remove
from os.path import isfile, join, getsize


class LocalFileClient(object):

    def __init__(self, config):
        self.config = config

    def get_folder(self, folder_name):
        folder = LocalFolder(folder_name)
        return folder


class LocalFolder(object):
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def files(self, filter=""):
        files = [f for f in listdir(self.folder_name) if isfile(join(self.folder_name, f)) and f.startswith(filter)]
        return files

    def file(self, file_name):
        return LocalFile(join(self.folder_name, file_name))


class LocalFile(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_body(self):
        body = ""
        with open(self.file_path, 'r') as f:
            body = f.read()
        return body

    def set_body(self, file, public=False):
        with open(self.file_path, 'w+') as f:
            f.write(file)

    def delete(self):
        remove(self.file_path)

    def name(self):
        return self.file_path

    def size(self):
        return getsize(self.file_path)
