import svgwrite
import math
from typing import List

# This will be a SVG geometric pattern creator app

width = 100
height = 400


def regular_polygon(center, radius, num_points):
    angle = (math.pi * 2) / num_points
    points = []
    for i in range(num_points):
        current_angle = angle * i - (90*math.pi/180)
        x = center[0] + radius * math.cos(current_angle)
        y = center[1] + radius * math.sin(current_angle)
        # print(f" current_angle is {current_angle * (180/math.pi)},x is {x}, y is {y} ")
        points.append([x, y])
    return points

def isometric_grid(spacing, num_x, num_y):
    spacing_y = spacing * math.sin(60*(math.pi/180))
    grid = []
    for i in range(num_y):
        row = []
        for j in range(num_x):
            if i % 2 == 0:
                x = j * spacing
            else:
                x = j * spacing + (spacing/2)
            y = i * spacing_y
            row.append([x, y])
        grid.append(row)
    return grid
            
drawing = svgwrite.Drawing("test.svg")
# drawing.add(drawing.polygon(regular_polygon((0, 0), 5, 6)))
# drawing.add(drawing.polygon(regular_polygon((5, 5), 5, 3)))
# print(isometric_grid(5, 4, 8))

isometric_grid_1 = isometric_grid(4, 10, 50)

# for i, row in enumerate(isometric_grid_1):
#     for j, point in enumerate(row):
#         drawing.add(drawing.polygon(regular_polygon(point, (i/30), 6)))

def hex_grid(radius, spacing, num_x, num_y):
    spacing_y = spacing * math.sin(60*(math.pi/180))
    hex_grid = []
    for i in range(num_y):
        row = []
        for j in range(num_x):
            if i % 2 == 0:
                x = j * spacing
            else:
                x = j * spacing + (spacing/2)
            y = i * spacing_y
            row.append(regular_polygon([x, y], radius, 6))
        hex_grid.append(row)
    return hex_grid

def draw_grid(grid, drawing):
    for i, row in enumerate(grid):
        for j, points in enumerate(row):
            drawing.add(drawing.polygon(points))

def sine_gradient(hex_grid, max_difference, num_waves):
    amplitude = max_difference
    frequency = num_waves / len(hex_grid)
    # Calculate the value of the sine wave at a given time t
    for i, row in enumerate(hex_grid):
        for j, hexagon in enumerate(row):
            sine_value = amplitude * math.sin(2 * math.pi * frequency * i)
            # print(f"sine_value is {sine_value}")
            center = [x - y for x, y in zip(hexagon[0], hexagon[3])]
            for point in hexagon:
                # print(point)
                # TODO calculate difference difference_x = 
                point[0] += sine_value*10
                point[1] += sine_value*10
                # print(point)

def modify_grid(grid, callback):
    for i, row in enumerate(grid):
        for j, polygon in enumerate(row):
            # print(f"polygon is {polygon}")
            num_points = len(polygon)
            if num_points % 2 == 0: # Even number of sides
                middle = int(num_points/2)
                center = [(x + y)/2 for x, y in zip (polygon[0], polygon[middle])]
            else:
                edge_point_1 = math.floor(num_points/2)
                edge_point_2 = math.ceiling(num_points/2)
                edge_center = edge_point_2 - edge_point_1
                center = [polygon[0] - edge_center]
            callback(polygon, center, i, j)

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
    
    def modify_polygons(self, callback):
        polygons = []
        for i, row in enumerate(self.polygons):
            for j, polygon in enumerate(row):
                # print(f"in modify_polygons and polygon is {polygon}")
                callback(polygon, i, j, self.num_x, self.num_y)
                  
    def draw_polygons(self):
        # print(f"draw_polygons was called")
        self.modify_polygons(lambda polygon, i, j, num_x, num_y: self.drawing.add(self.drawing.polygon(polygon.points)))
        
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
        
def print_polygon_center(polygon, center, i, j):
    print(center)
    
    
def radius_morph_1(polygon:Polygon, i:int, j:int, num_x:int, num_y:int):
    center_x = (num_x - 1)/2
    center_y = (num_y - 1)/2
    difference_x = abs(center_x - j)
    difference_y = abs(center_y - i)
    # print(f"i is {i}, j is {j}, center_x is {center_x}, difference_x is {difference_x}")
    polygon.radius += (difference_x + difference_y)/10
    # polygon.rotate(i+j*5)

def radius_morph_2(polygon:Polygon, i:int, j:int, num_x:int, num_y:int):
    center_x = (num_x - 1)/2
    center_y = (num_y - 1)/2
    difference_x = abs(center_x - j)
    difference_y = abs(center_y - i)
    # print(f"i is {i}, j is {j}, center_x is {center_x}, difference_x is {difference_x}")
    polygon.radius -= (difference_x + difference_y)/10
    
test_polygon = Polygon(drawing, [0,0], 5, 6)
# test_polygon._num_points = 5
test_polygon.center = [0.0, 0]
# print(test_polygon._num_points)
# print(test_polygon.points)

test_polygon.draw()

test_polygon.num_points = 3
test_polygon.center = [50, -20]
test_polygon.rotate(10)
test_polygon.draw()

test_grid = GridIsometric(drawing, 10, 21, 51, 2, 6)
test_grid.modify_polygons(radius_morph_1)
test_grid.draw_polygons()
test_grid.modify_polygons(radius_morph_2)
test_grid.draw_polygons()

# hex_grid_1 = hex_grid(2, 5, 20, 100)
# sine_gradient(hex_grid_1, 1, 1)
# draw_grid(hex_grid_1, drawing)    
# test_hex_grid = hex_grid(10, 20, 1, 1)
# modify_grid(test_hex_grid, print_polygon_center)

drawing.save()