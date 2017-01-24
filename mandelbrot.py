

class Mandelbrot():
    def __init__(self):
        self.mandx = ( -2.5, 1.0 )
        self.mandy = ( -1.0, 1.0 )

        self.julia_c = ( -0.79,  0.15 )
        #self.julia_c = (  0.3,  -0.01 )

        self.screenx = ( 0, 900 )
        self.screeny = ( 0, 600 )

        self.lerpx = self.lerp_scalar( self.screenx[1], self.screenx[0], self.mandx[1], self.mandx[0] )
        self.lerpy = self.lerp_scalar( self.screeny[1], self.screeny[0], self.mandy[1], self.mandy[0] )

        self.aspect = self.screeny[ 1 ] / self.screenx[ 1 ]

        self.iterations = 1000

        self.filename = "test.png"
    def lerp_scalar(self, a,b,c,d):
        return ( (d-c) / (b-a) )

    def interpolate(self, point, scalar, start_point):
        return start_point + ( point * scalar )

    def main_loop(self):
        return None

    def mandelbrot(self):
        output = {}
        for j in range(self.screeny[0], self.screeny[1]):
            y = self.interpolate( j, self.lerpy, self.mandy[0] )
            output[j] = {}
            for i in range( self.screenx[0], self.screenx[1] ):
                count = 0
                x = self.interpolate( i, self.lerpx, self.mandx[0] )

                while 4.000 > (x*x + y*y) and count < self.iterations:
                    temp = x*x - y*y
                    y = 2 * x * y
                    x = temp
                    count += 1

                if count > 1 and count != self.iterations: output[j][i] = count
            if not output[j]: del output[j]
        return output


    def julia(self):
        output = {}
        for j in range(self.screeny[0], self.screeny[1]):
            y = self.interpolate( j, self.lerpy, self.mandy[0] ) + self.julia_c[1]
            output[j] = {}
            for i in range( self.screenx[0], self.screenx[1] ):
                count = 0
                x = self.interpolate( i, self.lerpx, self.mandx[0] ) + self.julia_c[0]

                while 4.000 > (x*x + y*y) and count < self.iterations:
                    temp = x*x - y*y
                    y = 2 * x * y + self.julia_c[1]
                    x = temp + self.julia_c[0]
                    count += 1

                if count > 1:# and count != self.iterations:
                    output[j][i] = count
            if not output[j]: del output[j]
        return output



import sys

def main( argv ):
    m = Mandelbrot()
    # out = m.mandelbrot()
    out = m.julia()
    print out
    pass

if __name__ == "__main__":
        main( sys.argv )
