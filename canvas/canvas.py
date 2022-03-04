import cv2
import mediapipe as mp
import numpy as np
import time

class handDetector():

	def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
		self.mode = mode
		self.maxHands = maxHands
		self.detectionCon = detectionCon
		self.trackCon = trackCon

		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode, self.maxHands)#, self.detectionCon, self.trackCon)
		self.mpDraw = mp.solutions.drawing_utils


	def findHands(self, img, drawIndex=False):
		img = cv2.flip(img, 1)
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)

		hands = False

		if self.results.multi_hand_landmarks:
			hands = True
			for handLms in self.results.multi_hand_landmarks:
				if drawIndex:
					self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

		return hands, img
					

	def findPosition(self, img, handNo=0, draw=True):
		lmList = []
		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks
			for id, lm in enumerate(myHand[0].landmark):
				h, w, c = img.shape
				cx, cy = int(lm.x*w), int(lm.y*h)
				lmList.append([id, cx, cy])

		return lmList


def main():
	pTime = 0
	cTime = 0
	handDet = handDetector()
	cap = cv2.VideoCapture(0)

	drawIndex = False

	points = []
	points.append([])
	while True:
		success, img = cap.read()

		if not success:
			break

		hands, img = handDet.findHands(img, drawIndex)

		if hands:
			lmList = handDet.findPosition(img)

			if len(lmList)>0:
				hyp = np.hypot(lmList[4][1]-lmList[8][1], lmList[4][2]-lmList[8][2])
				if hyp<40:
					midX, midY = int( (lmList[4][1]+lmList[8][1])/2 ), int( (lmList[4][2]+lmList[8][2])/2 )
					img = cv2.circle(img, (midX, midY), 4, (0, 255, 255), -1)
					if len(points[-1])>0:
						dist = np.hypot(points[-1][-1][0]-midX, points[-1][-1][1]-midY) 
						if dist>5:
							points[-1].append((midX, midY))
					else:
						points[-1].append((midX, midY))

				else:
					if len(points[-1])==1:
						points = points[:-1]
					if len(points[-1])>1:
						points.append([])
			

		for fig in points:
			if len(fig)>1:
				for i in range(len(fig)-1):
					img = cv2.line(img, fig[i], fig[i+1], (255,0,0), 2)


		cTime = time.time()
		fps = 1/(cTime-pTime)
		pTime = cTime

		cv2.putText(img, str(int(fps)), (30, 30), cv2.FONT_HERSHEY_PLAIN,
						 3, (0, 0, 255), 3)
		cv2.imshow("Image", img)
		
		key = cv2.waitKey(1) & 0xFF 
		if key == ord('q'):
			break
		elif key == ord('t'):
			drawIndex = not drawIndex
		elif key == ord('c'):
			points = []
			points.append([])


	cv2.destroyAllWindows()

	print(len(points))

	print("---------------")
	for fig in points:
		print(len(fig))


if __name__ == "__main__":
	main()