

class Container_creator:

    def __init__(self, filename):
        self.filename = filename

    def export_audio():
        os.system("ffmpeg -i {} -vn -acodec copy {}.mp3".format(self.filename, self.filename.split('.')[0]))
