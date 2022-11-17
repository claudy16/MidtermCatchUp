#20192164 Claudia
import numpy as np
import cv2
import math
import datetime

# Canvas size information
COLORS = {'black': (0,0,0)}
RADIUS = 260
CENTER = (320,320)
CANVAS_SIZE = (640,640,3)

#Code to define the ticks of the clock
def get_ticks():
	hours_init = []
	hours_dest = []

	for i in range(0,360,6):
		x_coord = int(CENTER[0] + RADIUS * math.cos(i * math.pi / 180))
		y_coord = int(CENTER[1] + RADIUS * math.sin(i * math.pi / 180))
		hours_init.append((x_coord,y_coord))

	for i in range(0,360,6):
		x_coord = int(CENTER[0] + (RADIUS-20) * math.cos(i * math.pi / 180))
		y_coord = int(CENTER[1] + (RADIUS-20) * math.sin(i * math.pi / 180))
		hours_dest.append((x_coord,y_coord))

	return hours_init, hours_dest

#Representation of the time in our clock
def getTime(h,m,s):
	time = ""
	hour = ""
	minute = ""
	second = ""
	if(h<10):
		hour = "0{}:".format(h)
	else:
		hour = "{}:".format(h)
	if(m<10):
		minute = "0{}:".format(m)
	else:
		minute = "{}:".format(m)
	if(s<10):
		second = "0{}".format(s)
	else:
		second = "{}".format(s)
	time = hour+minute+second
	return time

#Drawing the time on the clock
def draw_time(image):
	time_now = datetime.datetime.now().time() #getting the time from time module (Can you make the clock synchrozed with your computer clock?)
	hour = math.fmod(time_now.hour, 12)
	minute = time_now.minute
	second = time_now.second

	second_angle = math.fmod(second * 6 + 270, 360)
	minute_angle = math.fmod(minute * 6 + 270, 360)
	hour_angle = math.fmod((hour*30) + (minute/2) + 270, 360)

	minute_x = int(CENTER[0] + (RADIUS-60) * math.cos(minute_angle * math.pi / 180))
	minute_y = int(CENTER[1] + (RADIUS-60) * math.sin(minute_angle * math.pi / 180))
	cv2.line(image, CENTER, (minute_x, minute_y), COLORS['black'], 3)

	hour_x = int(CENTER[0] + (RADIUS-100) * math.cos(hour_angle * math.pi / 180))
	hour_y = int(CENTER[1] + (RADIUS-100) * math.sin(hour_angle * math.pi / 180))
	cv2.line(image, CENTER, (hour_x, hour_y), COLORS['black'], 7)

	cv2.circle(image, CENTER, 5, COLORS['black'], -1)
	time = getTime(int(hour),minute,second)

	return image
#

def main():
    #Canvas
    image = np.zeros(CANVAS_SIZE, dtype=np.uint8)
    image[:] = [255,255,255]

    #get the starting and ending points of ticks in the watch
    hours_init, hours_dest = get_ticks()

    #Draw
    for i in range(len(hours_init)):
        if i % 5 == 0:
            cv2.line(image, hours_init[i], hours_dest[i], COLORS['black'], 3)

    #Draw circle watch
    cv2.circle(image, (320,320), RADIUS+10, COLORS['black'], 2)

    while True:
        image_original = image.copy()
        #Use draw time to make clock hands on the canvas
        clock_face = draw_time(image_original)
        #Show the watch
        cv2.imshow('clock', image_original)
        if(cv2.waitKey(1)==ord('q')):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()