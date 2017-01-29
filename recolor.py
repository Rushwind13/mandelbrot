import png
from numpy import zeros

import palette

def recolor( filename ):
	reader = png.Reader(filename).read()
	w = reader[0]
	h = reader[1]
	planes = 3
	
	pixels_in = list( reader[2] ) # grayscale, r=g=b
	
	pal = palette.get_palette()
	num_colors = len(pal)
	
	values_out = []
	pixels_out = zeros((h,w,planes), 'uint8')
	pixel_black = [0,0,0]
	y = 0
	for line in pixels_in:
	    values_line = []
	    x = 0
	    for value in line[::3]: # just grab every third entry, R, G, B
	    	values_line.append(value)
	    	if value == 0 or value == 255:
	    		pixels_out[y][x] = pixel_black
	    	else:
	    		pixels_out[y][x] = pal[value % num_colors]	# apply the palette
	    	x = x + 1
	    values_out.append(values_line)
	    y = y + 1
	
	# then write out the new png
	file_out = open( "recolor_"+filename, "wb")
	
	writer = png.Writer( w, h, bitdepth = 8 )
	img = pixels_out.reshape(pixels_out.shape[0], pixels_out.shape[1]*pixels_out.shape[2])
	
	writer.write( file_out, img )
	
	file_out.close()
	
	
if __name__ == "__main__":
	import sys
	if len(sys.argv) == 1:
		print "Usage: <script> file1 file2 ... filen"
		sys.exit()

	for file in sys.argv[1:]:
		print "Working on %s..." % file
		recolor( file )
		print "done."
	sys.exit()
	