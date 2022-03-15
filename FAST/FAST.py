import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def FindCorners(img, seuil):
	height, width, _ = img.shape
	coins = []
	sommeValues = [] # coins + vsomme
	# +3: Pour s'assurer que notre circle de R=3, est toujours à l'interieur de l'image.
	#  8: image border
	#the image i was using has a border of 8 pixels, change it to 0 or adapt it to your own case
	bordure = 0 # 8
	xDebut = bordure + 3 
	xFin   = width - (bordure + 3) 
	yDebut = bordure + 3
	yFin   = height - (bordure + 3) 

	for i in range(yDebut, yFin):
		for j in range(xDebut, xFin):

			centre = [i, j]
			# Loops the circle offsets to read the pixel value for the sixteen surrounding pixels.
			is_coin, sommeV = detection_coin_FAST(img, centre, seuil)
			if is_coin:
				coins.append([j,i])
				sommeValues.append(sommeV);
				j += 3
	return (coins, sommeValues)

def detection_coin_FAST(image, centre, seuil):
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	points_circle = circle_itensity(centre, gray)
	#intensité de centre
	x, y = centre
	p = int(gray[x][y])
	is_fast_corner, sommeV = isCorner(p, points_circle, seuil)
	
	return (is_fast_corner,sommeV)

def isCorner(p, circlePixels, threshold):
	if is_Candidate(circlePixels, p, threshold):
		return (False, 0)

	for x in range(16):
		darker = True
		brighter = True
		maxim_dark = 0
		maxim_bright = 0
		# Pour s'assurer d'avoir 12 points continue sur l'arc sombre ou lumineux
		for y in range(12):
			circlePixel = circlePixels[(x+y)&15]

			if not isBrighter(p, circlePixel, threshold):
				brighter = False
				if not darker:
					break
			else: 
				maxim_bright+= circlePixel
				

			if not isDarker(p, circlePixel, threshold):
				darker = False
				if not brighter:
					break
			else:
				maxim_dark+= circlePixel

		if brighter or darker:
			return (True,max(abs(maxim_dark-p*12), abs(maxim_bright-p*12)))
	return (False, 0)

# Tester si le pixel peut etre un candidat de test FAST.
# Test des points 1, 9, 5 et 13
# Test prend en considération: si l'arc est sombre ou lumineux 
def is_Candidate(circle_points, p, threshold):
	count = 0
	circleTop    = circle_points[1]
	circleBottom = circle_points[9]
	circleRight  = circle_points[5]
	circleLeft   = circle_points[13]

	if isBrighter(circleTop, p, threshold):
		count+=1
	if isBrighter(circleRight, p, threshold):
		count+=1
	if isBrighter(circleBottom, p, threshold):
		count+=1
	if isBrighter(circleLeft, p, threshold):
		count+=1

	if count < 3:
		count = 0
		if isDarker(circleTop, p, threshold):
			count+=1
		if isDarker(circleRight, p, threshold):
			count+=1
		if isDarker(circleBottom, p, threshold):
			count+=1
		if isDarker(circleLeft, p, threshold):
			count+=1
		if count < 3:
			return True

	return False

#Vérifie si le pixel du cercle est plus lumineux que le pixel candidat p.
def	isBrighter(circlePixel, p , threshold):
	return circlePixel-p > threshold

#Vérifie si le pixel du cercle est plus sombre que le pixel candidat p.
def isDarker(circlePixel, p, threshold):
	return p-circlePixel > threshold

# Les points autour de circle 
def circle_itensity(center, img):
	x, y = center
	circle = []

	pt1 = int(img[x][y-3])
	pt2 = int(img[x+1][y-3])
	pt3 = int(img[x+2][y-2])
	pt4 = int(img[x+3][y-1])
	pt5 = int(img[x+3][y])
	pt6 = int(img[x+3][y+1])
	pt7 = int(img[x+2][y+2])
	pt8 = int(img[x+1][y+3])
	pt9 = int(img[x][y+3])
	pt10 = int(img[x-1][y+3])
	pt11 = int(img[x-2][y+2])
	pt12 = int(img[x-3][y+1])
	pt13 = int(img[x-3][y])
	pt14 = int(img[x-3][y-1])
	pt15 = int(img[x-2][y-2])
	pt16 = int(img[x-1][y-3])
	
	circle.append(pt1)
	circle.append(pt2)
	circle.append(pt3)
	circle.append(pt4)
	circle.append(pt5)
	circle.append(pt6)
	circle.append(pt7)
	circle.append(pt8)
	circle.append(pt9)
	circle.append(pt10)
	circle.append(pt11)
	circle.append(pt12)
	circle.append(pt13)
	circle.append(pt14)
	circle.append(pt15)
	circle.append(pt16)

	return circle

def sort_best_corners(corners, sumValues):
	best_corners = []
	for coordinate, sum_value in zip(corners, sumValues):
		corner = {}
		corner['pixel'] = coordinate
		corner['sumValue'] = sum_value
		best_corners.append(corner)

	sorted_best_corners = sorted(best_corners, key = lambda k: k['sumValue'], reverse=True)
	_range = int(0.1*len(sorted_best_corners))
	return sorted_best_corners[:_range]
#_____________________________________________________________

if __name__ == "__main__":
	image = cv.imread('assets/house4.jpg')
	nmb_pixels= cv.cvtColor(image, cv.COLOR_RGB2GRAY)

	#initialisation: 
	x = 110 
	y = 111
	centre = [x,y]
	seuil = 10 #threshold

	# Test if a specific corner is a corner 
	is_coin, intensite_coin= detection_coin_FAST(image, centre, seuil)
	print(f"Point: {centre}\nFAST: {is_coin}\nVsomme: {intensite_coin}")

	# Searching for corners
	print("\nSearching For Corners... ")
	gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	data = FindCorners(image, seuil)
	corners = data[0]
	sumValues= data[1] 
	corners_percentage = len(corners) / (len(nmb_pixels) * len(nmb_pixels[0])) * 100
	
	print("Corners Found:", len(corners))
	print(f"Pourcentage of corners in the image: {round(corners_percentage,2)}")
	
	# Draw all corners
	# print("Drawing Corners ...")
	# implot = plt.imshow(gray, cmap='gray')
	# for point in coins:
	#     plt.scatter(point[0], point[1], color = "red", s=5)
	# plt.show()

	# sorting the corners based on sumvalue
	# returns a list of dictionaries [{'pixel': [44, 44], 'sumValue': 50}, {}, {}]  
	sorted_best_corners = sort_best_corners(corners, sumValues)
	print("Number of best 5% corners Found:", len(sorted_best_corners))


	# Draw best corners based on sumValue
	print("Drawing Best Corners ...")
	implot = plt.imshow(gray, cmap='gray')
	for item in sorted_best_corners:
		point = item['pixel']
		plt.scatter(point[0], point[1], color = "red", s=3)
	plt.show()

	# #Plot Histogramme
	# _ = plt.hist(sommeValues, bins = 256)
	# _ = plt.xlabel('Intensity')
	# _ = plt.ylabel('Nomber of corners')
	# plt.show()
	
