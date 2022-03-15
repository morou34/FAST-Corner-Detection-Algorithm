## FAST: Features From Accelerated Segment Test
- This is a simple implementation of the FAST corner detection algorithm using python, this method does not use OpenCV functions.

- In general this is good for students or  anyone who is trying to write his own code instead of just using already builtins functions that comes with openCV or any other python libraries.


- FAST corner detector uses a circle of 16 pixels (a Bresenham circle of radius 3) to classify whether a candidate point p is actually a corner. Each pixel in the circle is labeled from integer number 1 to 16 clockwise. If a set of N contiguous pixels in the circle are all brighter than the intensity of candidate pixel p (denoted by Ip) plus a threshold value t or all darker than the intensity of candidate pixel p minus threshold value t, then p is classified as corner.

###Results:

#####Before 
![](https://raw.githubusercontent.com/iMouaad/FAST-Corner-Detection-Algorithm/main/FAST/assets/house4.jpg?token=GHSAT0AAAAAABR55AF6GVTU7YARSOH3DEHIYRRBTBQ)

#####After :
![](https://raw.githubusercontent.com/iMouaad/FAST-Corner-Detection-Algorithm/main/FAST/assets/House4_corners.png?token=GHSAT0AAAAAABR55AF7VQ2DP4NTLHBMMLWQYRRBSJA)
