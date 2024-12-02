import threading
from queue import Queue
from typing import Any
import cv2
from app.cv.video_reader import VideoReader
from app.cv.detector import BirdDetector


def read_and_detect(path: str) -> dict[Any, Any]:
    lock = threading.Semaphore(0)
    SENTINEL = object()  # SENTINEL OBJECT
    SHARED_Q = Queue()
    res = dict[Any, Any]()
    birdsCascade = cv2.CascadeClassifier(
        "F:/Collage/4th year/Compilers Project/project/app/cv/birds1.xml"
    )
    reader = VideoReader(path=path, sentinel=SENTINEL, queue=SHARED_Q)

    detector = BirdDetector(
        lock=lock, sentinel=SENTINEL, queue=SHARED_Q, res=res, birdsCascade=birdsCascade
    )
    reader.start()
    detector.start()
    lock.acquire()
    return res
