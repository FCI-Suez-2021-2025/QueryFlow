import cv2

class DetectBirds(object):
    def __init__(self, camera_url):
        self.cap = cv2.VideoCapture(camera_url)
        self.birdsCascade = cv2.CascadeClassifier("F:\\Collage\\4th year\\Compilers Project\\project\\app\cv\\birds1.xml")
        self.MAX_BIRDS = 0
        self.running = True

    def detect(self):
        while self.running:
            # Capture frame-by-frame from a video
            ret, frame = self.cap.read()
            if ret:
                # convert the frame into gray scale for better analysis
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Detect birds in the gray scale image
                birds = self.birdsCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.4,
                    minNeighbors=5,
                    #minSize=(10, 10),
                    maxSize=(30, 30),
                    flags = cv2.CASCADE_SCALE_IMAGE
                )
                if (len(birds)>self.MAX_BIRDS):
                    self.MAX_BIRDS = len(birds)
            else:
                self.running = False
        self.cap.release()
        print(self.MAX_BIRDS)
        return self.MAX_BIRDS

if __name__ == "__main__":
    D = DetectBirds("birds-test.mp4")
    D.detect()