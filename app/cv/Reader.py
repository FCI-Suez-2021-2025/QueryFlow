from threading import Thread

import cv2


class VideoReader(Thread):
    def __init__(self, path, queue, sentinel):
        super().__init__()
        self.queue = queue
        self.path = path
        self.sentinel = sentinel
    def run(self):
        cap = cv2.VideoCapture(self.path)
        ret, frame = cap.read()
        while ret:
            self.queue.put(frame)
            ret, frame = cap.read()
        self.queue.put(self.sentinel)
        cap.release()
