#20192164
import numpy as np
import cv2
import time


def getLine(x0, y0, x1, y1):
    points = []
    if abs(x1-x0) >= abs(y1-y0):
        if x0 >= x1:
            for x in range(x0, x1-1, -1):
                y = (x-x0)*(y1-y0)/(x1-x0) + y0
                points.append((x, int(y)))
        else:
            for x in range(x0, x1+1):
                y = (x-x0)*(y1-y0)/(x1-x0) + y0
                points.append((x, int(y)))
    else:
        if y0 >= y1:
            for y in range(y0, y1-1, -1):
                x = (x1-x0)*(y-y0)/(y1-y0) + x0
                points.append((int(x), y))
        else:
            for y in range(y0, y1):
                x = (x1-x0)*(y-y0)/(y1-y0) + x0
                points.append((int(x), y))
    return points


def drawLine(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    if True:
        xys = getLine(x0, y0, x1, y1)
        for xy in xys:
            x, y = xy
            canvas[y, x, :] = color
    return


def deg2rad(deg):
    rad = deg * np.pi / 180.
    return rad


def getRegularNGon(ngon):
    delta = 360. / ngon
    points = []
    for i in range(ngon):
        degree = i * delta
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        points.append((x, y, 1))
    #
    points = np.array(points)
    return points


def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return


def drawPolygon(canvas, pts, color, axis=False):
    for k in range(pts.shape[0]-1):
        drawLine(canvas, pts[k, 0], pts[k, 1],
                 pts[k+1, 0], pts[k+1, 1], color)
    drawLinePQ(canvas, pts[-1], pts[0], color)

    if axis == True:  # center - pts[0]
        center = np.array([0., 0, 0])
        for p in pts:
            center += p
        center = center / pts.shape[0]
        center = center.astype('int')
        print(center)
        drawLinePQ(canvas, center, pts[0], color=(255, 128, 128))
    #
    return

def makeT(a, b):
    T = np.eye(3, 3)
    T[0, 2] = a
    T[1, 2] = b
    return T


def makeR(deg):
    rad = deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.eye(3, 3)
    R[0, 0] = c
    R[0, 1] = -s
    R[1, 0] = s
    R[1, 1] = c
    return R

def drawStar(canvas, pts, color, axis=False):
    drawLine(canvas, pts[0, 0], pts[0, 1], pts[2, 0], pts[2, 1], color)
    drawLine(canvas, pts[0, 0], pts[0, 1], pts[3, 0], pts[3, 1], color)
    drawLine(canvas, pts[1, 0], pts[1, 1], pts[3, 0], pts[3, 1], color)
    drawLine(canvas, pts[1, 0], pts[1, 1], pts[4, 0], pts[4, 1], color)
    drawLine(canvas, pts[2, 0], pts[2, 1], pts[4, 0], pts[4, 1], color)
    return


def erasePolygon(canvas, pts, color=(0, 0, 0), axis=False):
    for k in range(pts.shape[0]-1):
        drawLine(canvas, pts[k, 0], pts[k, 1],
                 pts[k+1, 0], pts[k+1, 1], color)
    drawLinePQ(canvas, pts[-1], pts[0], color)

    if axis == True:  # center - pts[0]
        center = np.array([0., 0, 0])
        for p in pts:
            center += p
        center = center / pts.shape[0]
        center = center.astype('int')
        print(center)
        drawLinePQ(canvas, center, pts[0], color)
    return


def eraseStar(canvas, pts, color=(0, 0, 0), axis=False):
    drawLine(canvas, pts[0, 0], pts[0, 1], pts[2, 0], pts[2, 1], color)
    drawLine(canvas, pts[0, 0], pts[0, 1], pts[3, 0], pts[3, 1], color)
    drawLine(canvas, pts[1, 0], pts[1, 1], pts[3, 0], pts[3, 1], color)
    drawLine(canvas, pts[1, 0], pts[1, 1], pts[4, 0], pts[4, 1], color)
    drawLine(canvas, pts[2, 0], pts[2, 1], pts[4, 0], pts[4, 1], color)
    return


def rotatePoints(degree, points):
    R = makeR(30)
    qT = R @ points.T
    points = qT.T
    return points


def main():
    width, height = 1400, 1000
    canvas = np.zeros((height, width, 3), dtype='uint8')

    while True:
        star1Pts = getRegularNGon(5)
        star2Pts = getRegularNGon(5)
        star3Pts = getRegularNGon(5)
        star4Pts = getRegularNGon(5)

        star1Pts *= 40
        star1Pts[:, 2] /= 40

        star1x = np.random.randint(100, 1200)
        star1y = np.random.randint(100, 700)
        Tc = makeT(star1x, star1y)
        star1Pts = (Tc @ star1Pts.T).T
        star1Pts = star1Pts.astype('int')
        drawStar(canvas, star1Pts, np.random.randint(0, 256, size=3), axis=False)

        star2Pts *= 20
        star2Pts[:, 2] /= 20

        star2x = np.random.randint(100, 1200)
        star2y = np.random.randint(100, 700)
        Tc = makeT(star2x, star2y)
        star2Pts = (Tc @ star2Pts.T).T
        star2Pts = star2Pts.astype('int')
        drawStar(canvas, star2Pts, np.random.randint(0, 256, size=3), axis=False)

        star3Pts *= 10
        star3Pts[:, 2] /= 10

        star3x = np.random.randint(100, 1200)
        star3y = np.random.randint(100, 700)
        Tc = makeT(star3x, star3y)
        star3Pts = (Tc @ star3Pts.T).T
        star3Pts = star3Pts.astype('int')
        drawStar(canvas, star3Pts, np.random.randint(0, 256, size=3), axis=False)

        star4Pts *= 50
        star4Pts[:, 2] /= 50

        star4x = np.random.randint(100, 1200)
        star4y = np.random.randint(100, 700)
        Tc = makeT(star4x, star4y)
        star4Pts = (Tc @ star4Pts.T).T
        star4Pts = star4Pts.astype('int')
        drawStar(canvas, star4Pts, np.random.randint(0, 256, size=3), axis=False)

        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27:
            break

        drawStar(canvas, star1Pts, (0, 0, 0), axis=False)
        drawStar(canvas, star2Pts, (0, 0, 0), axis=False)
        drawStar(canvas, star3Pts, (0, 0, 0), axis=False)
        drawStar(canvas, star4Pts, (0, 0, 0), axis=False)

        time.sleep(0.3)
    #
#


if __name__ == "__main__":  # __
    main()
