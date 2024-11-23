import threading
from queue import Queue
import cv2
from app.cv.Reader import VideoReader
from app.cv.detector import BirdDetector

def readAndDetect(path):
    lock = threading.Semaphore(0)
    SENTINEL = object()  #SENTINEL OBJECT
    SHARED_Q = Queue()
    res = dict()
    birdsCascade = cv2.CascadeClassifier("F:\Collage\\4th year\Compilers Project\project\\app\cv\\birds1.xml")

    reader = VideoReader(path=path , sentinel=SENTINEL ,queue=SHARED_Q)

    detector = BirdDetector( lock=lock, sentinel=SENTINEL, queue=SHARED_Q , res=res ,birdsCascade = birdsCascade)
    reader.start()
    data = detector.start()
    lock.acquire()
    return str(res['MaxBirds'])

