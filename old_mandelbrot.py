#!/usr/bin/python
from __future__ import division
import sys

# Full set (maximum domain and range)
#mandx = (-2.5, 1)
#mandy = (-1, 1)
# mandx = (-0.25, 0.5)
# mandy = ( 0, -0.5)
# mandx = ( -1.5, -1.3125 )
# mandy = ( 0.125, 0 )
# mandx = ( -1.5, -1.3 )
# mandy = ( 0.03, 0.163 )
# 
# screenx = (0,900)
# screeny = (0,600)


screenx = (0,10000)
screeny = (0,10000)
screenx = (0,1000)
screeny = (0,1000)
mandx = ( -1.5, -1.3 )
mandy = ( 0.03, 0.23 )
mandx = ( -2.0, 2.0 )
mandy = ( -2.0, 2.0 )


# julia = ( -0.79,  0.15 )
# julia = ( 0.0,   0.65 )
# julia = ( -0.162, 1.04 )
# julia = (  0.3,  -0.01 )
julia = ( -0.726895347709114071439, 0.188887129043845954792 )
# julia = ( -0.75,  0.2 )
# julia = (  0.0,  -0.8 )
# julia = ( -1.25,  0.15 )
# julia = (  0.285, 0.01 )

tilesx = (0,9)
tilesy = (0,9)

max_iterations = 255

from numpy import *
def CreateImage( h, w, planes ):
	print "CreateImage"
	return zeros((h,w,planes), 'uint8')

import png
def SaveImage( image, filename, w,h ):
	print "Saving image...",
	#print image
	
	# add scipy to easily scale the data to uint8...
	# scipy.misc.bytescale( image )
	file = open( filename, 'wb' )
	
	writer = png.Writer( w, h, bitdepth=8)
	img = image.reshape(image.shape[0], image.shape[1]*image.shape[2])

	writer.write(file, img)
	
	file.close()
	print "saved."

def lerp_scalar( a,b, c,d ):
	return( (d-c) / ( b-a ) ) 

def lerp( base, curr, scalar ):
	return( base + ( curr * scalar ) )

def precalc_range( min, max, base, scalar ):
	retval = {}
	unit = min
	while unit < max:
		retval[unit] = lerp( base, unit, scalar )
		unit = unit + 1
	return retval

def mandelbrot( xcoords, ycoords, prex, prey, julia_set = False ):
	x0 = xcoords[0]
	y0 = ycoords[0]
	
	image = CreateImage( (ycoords[1]-ycoords[0])+1, (xcoords[1]-xcoords[0])+1, 3 )
	#image = {}
	iterations={}
	while y0 < ycoords[1]:
		while x0 < xcoords[1]:
			curr_iteration = 0
			if julia_set:
				x = prex[x0]
				y = prey[y0]
			else: # Mandelbrot set
				x = 0
				y = 0
			while (x*x + y*y) < 4.0 and curr_iteration < max_iterations:
				temp = x*x - y*y
				y = 2 * x * y
				x = temp
				if julia_set:
					x = x + julia[0]
					y = y + julia[1]
				else:
					x = x + prex[x0]
					y = y + prey[y0]
				#print x,y, " " ,
				curr_iteration = curr_iteration + 1
			#print x0,y0," ",curr_iteration,
			#print curr_iteration,
			#sys.stdout.flush()
			x0 = x0+1
			#image[y0 * xcoords[1] + x0] = curr_iteration
			if curr_iteration == max_iterations:
				image[y0][x0] = 0
			else:
				image[y0][x0] = curr_iteration
				
			if curr_iteration in  iterations:
				iterations[curr_iteration] += 1
			else:
				iterations[curr_iteration] = 1
		print y0," ",
		sys.stdout.flush()
		x0 = xcoords[0]
		y0 = y0+1
	print iterations
	#print image[13][13]
	SaveImage( image, "test.png", (xcoords[1]-xcoords[0])+1, (ycoords[1]-ycoords[0])+1 )
	print "done"

mosaic =  ( lerp_scalar( tilesx[0], tilesx[1], mandx[0], mandx[1] ), \
	lerp_scalar( tilesy[0], tilesy[1], mandy[0], mandy[1] ) )
print mosaic
#tilex = tilesx[0]
#tiley = tilesy[0]

#while tilex < tilesx[1]:
#	while tilex < tilesy[1]:

#lerp_scalars = (lerp_scalar( screenx[0], screenx[1], mandx[0], mandx[1] ), \
#	lerp_scalar( screeny[0], screeny[1], mandy[0], mandy[1] ) )
lerp_scalars = (lerp_scalar( screenx[0], screenx[1], mandx[0], mandx[1] ), \
	lerp_scalar( screeny[0], screeny[1], mandy[0], mandy[1] ) )


fx = precalc_range( screenx[0], screenx[1], mandx[0], lerp_scalars[0] )
fy = precalc_range( screeny[0], screeny[1], mandy[0], lerp_scalars[1] )
#print lerp_scalars

#fx={}
#fy={}
#x = screenx[0]
#y = screeny[0]
#
#while x < screenx[1]:
##	fx[x] = mandx[0] + x * lerp_scalars[0]
#	x = x+1

#print fx

#while y < screeny[1]:
#	fy[y] = mandy[0] + y * lerp_scalars[1]
#	y = y+1

#print fy

mandelbrot( screenx, screeny, fx, fy, julia_set = True )
