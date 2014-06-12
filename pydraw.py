""" pydraw module: draw lines that can be modified via mouse click
"""
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

def draw_background(fig=None):
    """ background for drawing
    """
    if fig is None:
        fig = plt.figure()
    ax = fig.add_subplot(111)
    return ax

class InteractiveLine(object):
    """ class to plot a matplotlib 2-D line
    """ 
    def __init__(self, line):
        """
        """
        self.line = line
        self.line.set_picker(5) # 5 points tolerance
        #self.line.set_pickable(True) # line is pickable by mouse
        self.line.figure.canvas.mpl_connect('pick_event', self.on_pick)

    def on_pick(self, event):
        """ mouse pick of the line ==> modify the points
        """
        #i, xp, yp = find_closest_point(self.line.get_data(), \
                #(event.xdata, event.ydata))

        # line coordinates
        xl, yl = self.line.get_data()
        xp, yp = event.mouseevent.xdata, event.mouseevent.ydata

        # distance between points on the line and clicked point
        dist = (xp- np.asarray(xl))**2 + (yp - np.asarray(yl))**2

        # find minimum distance
        i = np.argmin(dist)

        return self.move_vertex(i)

    def move_vertex(self, i):
        """ move ith vertex of the line
        just offer the user to move the point and update the line
        """
        xl, yl = self.line.get_data()
    
        # display picked point
        pt, = self.line.axes.plot(xl[i], yl[i], 'ko') 

        # draw it
        self.draw()

        # user-input new location
        xy = self.line.figure.ginput(n=1, timeout=0)
        x, y = xy[0]

        # update line 
        xl[i] = x
        yl[i] = y
        self.line.set_data(xl, yl)

        # remove former point
        pt.remove()

        # draw
        self.draw()

    @classmethod
    def plot(cls, x, y, ax=None, **lineprops):
        """ plot a line
        """
        if ax is None:
            ax = plt.gca()

        line, = ax.plot(x, y, **lineprops)
        iline = cls(line)
        iline.draw()
        return iline

    @classmethod
    def ginput(cls, ax=None):
        """ draw a line
        """
        if ax is None:
            ax = plt.gca()

        # use input line
        print "draw a line"
        line = ax.figure.ginput(n=0, timeout=0)

        x, y = zip(*line)
        return cls.plot(x, y)

    def draw(self):
        self.line.figure.canvas.draw()

def main():
    ax = draw_background()
    line = InteractiveLine.ginput(ax=ax)
    return line

if __name__ == '__main__':
    line = main()

