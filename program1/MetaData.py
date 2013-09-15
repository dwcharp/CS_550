class MetaData():

    def __init__(self,working_dir, files):
        self.working_directory = working_dir
        self.files = files

class FileInfo():
        def __init__(self,name,size):
            self.size = size
            self.name = name

        def get_name(self):
            return self.name

        def get_size(self):
            return size


