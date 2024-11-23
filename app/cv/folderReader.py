from threading import Thread
import os

class FolderReader(Thread):
    def __init__(self,path,queue, sentinel):
        super().__init__()
        self.path = path
        self.queue = queue
        self.sentinel = sentinel

    def read(self):
        directory = self.path
        for image in os.listdir(directory):
            if image.endswith(".jpg"):
                # img_num = image[:4]
                img_name = image[4:-4]
                self.queue.put(img_name)
        self.queue.put(self.sentinel)

    def run(self):
        self.read()
