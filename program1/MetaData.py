class MetaData():
    self.working_directory = None
    self.files =None

    def __init__(working_dir, files):
        self.working_directory = working_dir
        self.files = files

class FileInfo():
        self.size = None
        self.name= None

        def __init__(self,name,size):
            self.size = size
            self.name = name

        def get_name(self):
            return self.name

        def get_size(self):
            return size


