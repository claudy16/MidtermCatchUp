#20192164
import numpy as np
import cv2

width, height = 1600, 1000  #canvas size
canvas = np.zeros((height, width, 3), dtype=np.uint8)


def getline(x0, y0, x1, y1):
    points = []
    if (y0>y1):
        bigY = y0
        smallY = y1
    else:
        bigY = y1
        smallY = y0
    if (x0>x1):
        bigX = x0
        smallX = x1
    else: 
        bigX = x1
        smallX = x0
    if (x0==x1):
        for i in range(smallY, bigY+1):
            points.append((x0,i))
        return points
    slope = (y1-y0)/(x1-x0)
    if(slope*slope<=1):
        for i in range(smallX, bigX+1):
            y = slope*(i-x0)+y0
            yint = int(y)
            points.append((i, yint))
        return points
    else:
        for i in range(smallY, bigY+1):
            x = (i-y0)/slope+x0
            xint = int(x)
            points.append((xint, i))
        return points
    


def drawline(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    #draw the lines
    xys = getline(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color

def radom_lines(canvas):
    x0 = np.random.randint(0, canvas.shape[1])
    y0 = np.random.randint(0, canvas.shape[0])
    x1 = np.random.randint(0, canvas.shape[1])
    y1 = np.random.randint(0, canvas.shape[0])
    color = np.random.randint(0, 256, size = 3)
    drawline(canvas, x0, y0, x1, y1, color)

def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad


def drawlinepq(canvas, p, q, color):
    drawline(canvas, p[0], p[1], q[0], q[1], color)
    return

def drawpolygon(canvas, pts, color, axis=False, star=False):

    if star ==True:
        drawlinepq(canvas, pts[0], pts[2], color)
        drawlinepq(canvas, pts[1], pts[3], color)
        drawlinepq(canvas, pts[2], pts[4], color)
        drawlinepq(canvas, pts[3], pts[0], color)
        drawlinepq(canvas, pts[4], pts[1], color)
        return

    for k in range(pts.shape[0]-2):
        drawline(canvas, pts[k, 0], pts[k, 1], pts[k+1,0], pts[k+1,1], color)
    drawlinepq(canvas, pts[-1], pts[0], color)

    if axis == True:
        drawlinepq(canvas, pts[-1], pts[0], color=(255, 128, 128))

    
def clearcanvas(canvas):
    canvas.fill(0)

def makeTmat(a,b):
    T = np.eye(3, 3)
    T[0,2] = a
    T[1,2] = b
    return T

def makeRmat(degree):
    r = deg2rad(degree)
    c = np.cos(r)
    s = np.sin(r)
    R = np.eye(3,3)
    R[0, 0] = c
    R[0, 1] = -s
    R[1, 0] = s
    R[1, 1] = c
    return R

def makepointmat(points):
    ones = np.ones(points.shape[0])
    points = np.c_[points, ones]
    return points

def rotatelimit(limit, rotate, speed):
    #set a limit to the rotation of the rectangles
    if (rotate>limit and speed>0) or (rotate<-limit and speed<0):
        speed = -speed
    rotate += speed
    return rotate, speed

def main():
    width, height = 1600, 1000
    canvas = np.zeros( (height, width, 3), dtype='uint8')
    color = np.random.randint(0, 256, size=3)

    #size of the rectangles
    r_height = 20
    r_width = 50
    rectangle1= [(0,0), (0,r_height), (r_width,r_height), (r_width,0), (r_width/2,r_height/2)]
    rectangle1 = np.array(rectangle1)
    rectangle1 = makepointmat(rectangle1)

    #rotation and rotation speed of the rectangles
    R2 = 0
    R2_s = 3
    R3 = 0
    R3_s = 2
    R4 = 0
    R4_s = -4
    R5 = 0
    R5_s = 3

    while True: #rectangles
        Q1 = makeTmat(width/2, height/2)@makeRmat(-90)
        qT = Q1@rectangle1.T
        arm1 = qT.T 
        arm1 = arm1.astype('int')

        Q2 = Q1@makeTmat(r_width,0)@makeTmat(0,r_height/2)@makeRmat(R2)@makeTmat(0,-r_height/2)
        qT = Q2@rectangle1.T
        arm2 = qT.T
        arm2 = arm2.astype('int')

        Q3 = Q2@makeTmat(r_width,0)@makeTmat(0,r_height/2)@makeRmat(R3)@makeTmat(0,-r_height/2)
        qT = Q3@rectangle1.T
        arm3 = qT.T
        arm3 = arm3.astype('int')

        Q4 = Q3@makeTmat(r_width,0)@makeTmat(0,r_height/2)@makeRmat(R4)@makeTmat(0,-r_height/2)
        qT = Q4@rectangle1.T
        arm4 = qT.T
        arm4 = arm4.astype('int')

        Q5 = Q4@makeTmat(r_width,0)@makeTmat(0,r_height/2)@makeRmat(R5)@makeTmat(0,-r_height/2)
        qT = Q5@rectangle1.T
        arm5 = qT.T
        arm5 = arm5.astype('int')

        drawpolygon(canvas, arm1, color)
        drawpolygon(canvas, arm2, color)
        drawpolygon(canvas, arm3, color)
        drawpolygon(canvas, arm4, color)
        drawpolygon(canvas, arm5, color)

        #setting the limit for each rectangle
        R2,R2_s = rotatelimit(30,R2,R2_s)
        R3,R3_s = rotatelimit(50,R3,R3_s)
        R4,R4_s = rotatelimit(70,R4,R4_s)
        R5,R5_s = rotatelimit(20,R5,R5_s)

        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27: break
        clearcanvas(canvas)

if __name__ == "__main__":  # __
    main()

