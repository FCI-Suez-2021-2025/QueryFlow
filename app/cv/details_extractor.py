from threading import Thread


class DetailsExtractor(Thread):
    def __init__(self, queue, sentinel, lock, res):
        super().__init__()
        self.queue = queue
        self.sentinel = sentinel
        self.lock = lock
        self.res = res

    def extract(self):
        image = self.queue.get()
        while image is not self.sentinel:
            head_pose, leg_pose, wing_pose, tail_pose = image.split("_")
            image = self.queue.get()
            self.res.append(
                {
                    "HEAD": head_pose.split(".")[1],
                    "LEG": leg_pose.split(".")[1],
                    "WING": wing_pose.split(".")[1],
                    "TAIL": tail_pose.split(".")[1],
                }
            )
        self.lock.release()

    def run(self):
        self.extract()
