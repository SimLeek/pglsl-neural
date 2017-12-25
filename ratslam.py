import cv2, pubsub
import cv_pubsubs.cv_webcam_pub as cv_cam_pub

if False:
    from typing import List

cvWindows = []
frameDict={}

def cv_win_sub(*,
               names,  # type: List[str]
               inputVidGlobalNames  # type: List[str]
               ):
    global cvWindows
    for name in names:
        cvWindows.append(name)
        cv2.namedWindow(name)

    global frameDict
    while True:
        #global camImg
        for i in range(len(inputVidGlobalNames)):
            if inputVidGlobalNames[i] in frameDict and frameDict[inputVidGlobalNames[i]] is not None:
                cv2.imshow(names[i%len(names)], frameDict[inputVidGlobalNames[i]])
            if cv2.waitKey(1)& 0xFF==ord('q'):
                for name in names:
                    cv2.destroyWindow(name)
                return


camImg = None
if __name__ == '__main__':

    def camHandler(frame, camId):
        frameDict[str(camId)+"Frame"]= frame

    t = cv_cam_pub.init_cv_cam_pub_handler(0, camHandler)

    cv_win_sub(names=['cammy', 'cammy2'], inputVidGlobalNames=[str(0)+"Frame"])

    pubsub.publish("cvcamhandlers.0.cmd", 'q')
    t.join()



