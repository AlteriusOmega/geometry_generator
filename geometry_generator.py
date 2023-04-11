import svgwrite
import math
from typing import List

# This will be a SVG geometric pattern creator app

width = 100
height = 400
 
drawing = svgwrite.Drawing("test.svg")

class Polygon:
    def __init__(self, drawing, center, radius, num_points, angle=0):
        self.drawing = drawing
        self._center = center
        self._radius = radius
        self._num_points = num_points
        self._angle = angle
        self.points = self.polygon()
    
    def polygon(self):
        polygon_angle = (math.pi * 2) / self._num_points
        points = []
        for i in range(self._num_points):
            current_angle = polygon_angle * i - (90*math.pi/180) + self._angle*(math.pi/180)
            # print(f"self._center is {self._center}")
            x = self._center[0] + self._radius * math.cos(current_angle)
            y = self._center[1] + self._radius * math.sin(current_angle)
            # print(f" current_angle is {current_angle * (180/math.pi)},x is {x}, y is {y} ")
            points.append([x, y])
        return points
        
    def draw(self):
        drawing.add(drawing.polygon(self.points))

    def rotate(self, rotation_angle:float):
        self._angle += rotation_angle
        self.points = self.polygon()
        
    def draw_outline(self, outline_offset):
        outline_polygon = Polygon(self.drawing, self.center, self.radius + outline_offset, self.num_points, self.angle)
        self.drawing.add(drawing.polygon(outline_polygon.points))
        
    @property
    def center(self):
        return self._center
    @center.setter
    def center(self, center: List[float]):
        if len(center) == 2:
            self._center = center
            self.points = self.polygon()
        else:
            print(f"Center must be list of length 2, defining x and y coordinates") 
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, radius:float):
        self._radius = radius
        self.points = self.polygon()
    @property
    def num_points(self):
        return self._num_points
    @num_points.setter
    def num_points(self, num_points:int):
        self._num_points = num_points
        self.points = self.polygon()
    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, angle:float):
        self._angle = angle
        self.points = self.polygon()
        
class GridIsometric:
    def __init__(self, drawing, spacing, num_x, num_y, radius, num_points, angle=0):
        self.drawing = drawing
        self._spacing = spacing
        self._num_x = num_x
        self._num_y = num_y
        self._radius = radius
        self._num_points = num_points
        self._angle = angle
        self.points = self.grid()
        self.polygons = self.polygons()
        # print(f"In init, self.points is {self.points}, self.polygons is {self.polygons}")   
        
    def grid(self):
        spacing_y = self._spacing * math.sin(60*(math.pi/180))
        grid = []
        for i in range(self._num_y):
            row = []
            for j in range(self._num_x):
                if i % 2 == 0:
                    x = j * self._spacing
                else:
                    x = j * self._spacing + (self._spacing/2)
                y = i * spacing_y
                row.append([x, y])
            grid.append(row)
        # print(grid)
        return grid
    
    def polygons(self):
        polygons = []
        for i, row in enumerate(self.points):
            polygon_row = []
            for j, coord in enumerate(row):
                polygon = Polygon(self.drawing, coord, self._radius, self._num_points, self._angle)
                polygon_row.append(polygon)
            polygons.append(polygon_row)
        return polygons
    
    def modify_polygons(self, callback, **kwargs):
        polygons = []
        for i, row in enumerate(self.polygons):
            for j, polygon in enumerate(row):
                callback(polygon, i, j, self.num_x, self.num_y, **kwargs)
                  
    def draw_polygons(self):
        self.modify_polygons(lambda polygon, i, j, num_x, num_y: self.drawing.add(self.drawing.polygon(polygon.points)))
        
    def draw_outlines(self, outline_offset):
        self.modify_polygons(lambda polygon, i, j, num_x, num_y: polygon.draw_outline(outline_offset))
        
    @property
    def spacing(self):
        return self._spacing
    @spacing.setter
    def spacing(self, spacing:float):
        self._spacing = spacing
        self.points = self.grid()
    @property
    def num_x(self):
        return self._num_x
    @num_x.setter
    def spacing(self, num_x:int):
        self._num_x = num_x
        self.points = self.grid()
    @property
    def num_y(self):
        return self._num_y
    @num_y.setter
    def spacing(self, num_y:int):
        self._num_y = num_y
        self.points = self.grid()  
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, radius:float):
        self._radius = radius
        self.points = self.polygons()   
    @property
    def num_points(self):
        return self._num_points
    @num_points.setter
    def num_points(self, num_points:int):
        self._num_points = num_points
        self.points = self.polygons()
    @property
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, angle:float):
        self._angle = angle
        self.points = self.polygons()
    
class Mandala:
    def __init__(self, drawing, mandala_radius:float, symmetry:int):
        self.drawing = drawing
        self.mandala_radius = mandala_radius
        self.symmetry = symmetry
            
def print_polygon_center(polygon, center, i, j):
    print(center)
    
def radius_morph_1(polygon:Polygon, i:int, j:int, num_x:int, num_y:int):
    center_x = (num_x - 1)/2
    center_y = (num_y - 1)/2
    difference_x = abs(center_x - j)
    difference_y = abs(center_y - i)
    polygon.radius += (difference_x + difference_y)/10
    # polygon.rotate(i+j*5)

def radius_morph_2(polygon:Polygon, i:int, j:int, num_x:int, num_y:int):
    center_x = (num_x - 1)/2
    center_y = (num_y - 1)/2
    difference_x = abs(center_x - j)
    difference_y = abs(center_y - i)
    # print(f"i is {i}, j is {j}, center_x is {center_x}, difference_x is {difference_x}")
    polygon.radius -= (difference_x + difference_y)/10

def sine_morph(polygon:Polygon, i:int, j:int, num_x:int, num_y:int, num_waves=1, amplitude=None):
    amplitude = num_x/2
    frequency = num_waves / num_y
    sine_value = amplitude * math.sin(2 * math.pi * frequency * i) + (num_x/2)
    difference = abs(sine_value - j)
    # if j == 0: polygon.num_points = 4
    # if difference <= 2: polygon.num_points = 5
    polygon.radius += (difference/10)
    polygon.angle += difference*3 

test_grid = GridIsometric(drawing, spacing = 10, num_x = 21, num_y =  51, radius = 4, num_points = 3)
# test_grid.modify_polygons(radius_morph_1)
# test_grid.draw_polygons()
# test_grid.modify_polygons(radius_morph_2)
# test_grid.draw_polygons()
test_grid.modify_polygons(sine_morph, num_waves = 2)
test_grid.draw_polygons()
test_grid.draw_outlines(2)

drawing.save()