from direct.showbase.ShowBase import ShowBase
from TimCam import TimCam
from pandac.PandaModules import NodePath, TextNode, TransparencyAttrib, GeomNode
from panda3d.core import LineSegs

import random
import voronoi
import math

class point:
    xcoord = 0
    ycoord = 0
    town_name = ""

    def name(self):
        return self.name

    def x(self):
        return self.xcoord

    def y(self):
        return self.ycoord

class MapGen(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()
        cam = TimCam()
        self.map_width = 1000
        self.map_height = 500
        self.point_number = 100
        self.draw_border((0,0,0))
        self.points = self.create_points()
        self.calc_voronoi(self.points)
        self.calc_delaunay(self.points)

    def draw_border(self,col):
        self.draw_line((0,0,self.map_width,0),col)
        self.draw_line((self.map_width,0,self.map_width,self.map_height),col)
        self.draw_line((self.map_width,self.map_height,0,self.map_height),col)
        self.draw_line((0,0,0,self.map_height),col)

    def create_town(self,text,x,y):
        scale = 4
        town_node = NodePath("town")
        town = loader.loadModel("models/infantry_counter.egg")
        town.setScale(scale,scale,scale)
        town.reparentTo(town_node)
        text_node = TextNode("town_text_node")
        text_node.setText(text)
        text_node_path = town.attachNewNode(text_node)
        text_node_path.setPos(1,0,0)
        text_node_path.setHpr(0,-90,0)
        text_node_path.setScale(scale/2)
        text_node_path.setTransparency(TransparencyAttrib.MAlpha)
        text_node.setTextColor(0.8, 0.1, 0.1, 1)
        text_node.setAlign(TextNode.ALeft)
        town_node.reparentTo(render)
        town_node.setPos(x,y,0)
        print "Town Made",x,y

    def create_points(self):
        number = self.point_number
        points = []
        for i in range(number):
            p = point()
            p.xcoord = random.randrange(self.map_width)
            p.ycoord = random.randrange(self.map_height)
            p.town_name = str(i)
            points.append(p)
            self.create_town(str(i),p.xcoord,p.ycoord)
        return(points)

    def calc_voronoi(self,points):
        v = voronoi.computeVoronoiDiagram(points)
        for l in v[2]:
            c = (v[0][l[1]][0], v[0][l[1]][1], v[0][l[2]][0], v[0][l[2]][1])
            if c[0] > 0 and c[0] < self.map_width and c[1] > 0 and c[1] < self.map_height and c[2] > 0 and c[2] < self.map_width and c[3] > 0 and c[3] < self.map_height:
                self.draw_line(c,(0,0,0))

    def calc_delaunay(self,points):
        d = voronoi.computeDelaunayTriangulation(points)
        col = (255,0,0)
        for t in range(len(d)):
            tri = d[t]
            l1 = (points[tri[0]].x(),points[tri[0]].y(),points[tri[1]].x(),points[tri[1]].y())
            self.draw_line(l1,col)
            l2 = (points[tri[1]].x(),points[tri[1]].y(),points[tri[2]].x(),points[tri[2]].y())
            self.draw_line(l2,col)
            l3 = (points[tri[2]].x(),points[tri[2]].y(),points[tri[0]].x(),points[tri[0]].y())
            self.draw_line(l3,col)


    def draw_line(self,p,col):
        line = LineSegs()
        line.setColor(col[0],col[1],col[2], 1)
        line.setThickness(2)
        line.moveTo(p[0],p[1],0)
        line.drawTo(p[2],p[3],0)
        line_node = line.create()
        node_path = NodePath(line_node)
        node_path.reparentTo(render)

app = MapGen()
app.setFrameRateMeter(True)
app.run()