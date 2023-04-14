import svgwrite
import math
import os
from typing import List

# This will be a SVG geometric pattern creator app

width = 100
height = 400
 
output_folder = "G:\My Drive\Design and 3D Printing Laser\Laser Cutting Engraving\Lightburn Inkscape Vector Graphics"
output_filename = "geometry_generator_output.svg"
output_path = os.path.join(output_folder, output_filename)
drawing = svgwrite.Drawing(output_path)

class Polygon:
    def __init__(self,  num_points, radius=5, center=[0,0], drawing=drawing, angle=0):
        self._num_points = num_points
        self._radius = radius
        self._center = center
        self.drawing = drawing
        self._angle = angle
        self.points = self.polygon()
        self.fractal_points = list(self.points)
        self.rotate = None
    
    def polygon(self):
        polygon_angle = 360 / self._num_points # In degrees
        points = []
        for i in range(self._num_points):
            current_angle = polygon_angle * i - 90 + self._angle
            x = self._center[0] + self._radius * math.cos(current_angle*(math.pi/180)) # Convert to rad for cos and sin
            y = self._center[1] + self._radius * math.sin(current_angle*(math.pi/180))
            points.append([x, y])
        return points
        
    def draw(self):
        drawing.add(drawing.polygon(self.points))

    def rotate(self, rotation_angle:float):
        self._angle += rotation_angle
        self.points = self.polygon()
                
    def draw_outline(self, outline_offset):
        outline_polygon = Polygon(self.num_points, self.radius + outline_offset, self.center, self.drawing, self.angle)
        self.drawing.add(drawing.polygon(outline_polygon.points))
        
    def draw_fractal(self, shrinkage:float, depth:int,  rotate = False, radius=None, first=True,):
        # print(f"self.fractal_points is {self.fractal_points}")
        if first: 
            radius = self.radius*shrinkage
            self.draw()
            self.rotate = rotate
        else: radius = radius*shrinkage
        if depth >= 1:
            current_fractal_points = []
            for point in self.fractal_points:
                fractal_polygon = Polygon(self.num_points, radius, point, self.drawing, rotate)
                fractal_polygon.draw()
                for fractal_point in fractal_polygon.points:
                    current_fractal_points.append(fractal_point)
            print(f"rotate is {rotate}")
            self.fractal_points = list(current_fractal_points)
            self.draw_fractal(shrinkage, depth-1, rotate+self.rotate, radius, False)
        else:
            return self.fractal_points
        
    @property
    def num_points(self):
        return self._num_points
    @num_points.setter
    def num_points(self, num_points:int):
        self._num_points = num_points
        self.points = self.polygon()
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, radius:float):
        self._radius = radius
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
    def angle(self):
        return self._angle
    @angle.setter
    def angle(self, angle:float):
        self._angle = angle
        self.points = self.polygon()
        
class GridIsometric:
    def __init__(self, spacing, num_x, num_y, polygon, center=[0, 0], drawing=drawing):
        self._spacing = spacing
        self._num_x = num_x
        self._num_y = num_y
        self._polygon = polygon
        self._center = center
        self.drawing = drawing
        self.points = self._grid()
        self.polygons = self._generate_polygons()
        self.polygon_points = self._polygon_points()
        # print(f"In init, self.points is {self.points}, self.polygons is {self.polygons}")   
        
    def _grid(self):
        spacing_y = self._spacing * math.sin(60*(math.pi/180))
        grid = []
        for i in range(self._num_y):
            row = []
            for j in range(self._num_x):
                if i % 2 == 0:
                    x = self.center[0] + j * self._spacing
                else:
                    x = j * self._spacing + (self._spacing/2)
                y = self.center[1] + i * spacing_y
                row.append([x, y])
            grid.append(row)
        return grid
    
    def _generate_polygons(self):
        polygons = []
        for i, row in enumerate(self.points):
            polygon_row = []
            for j, coord in enumerate(row):
                polygon = Polygon(self._polygon.num_points, self._polygon.radius, coord, self.drawing, self._polygon.angle)
                polygon_row.append(polygon)
            polygons.append(polygon_row)
        self.polygons = polygons
        self.polygon_points = self._polygon_points()
        return polygons
    
    def _polygon_points(self):
        polygon_points = [] # Flat list of all points of all polygons in grid
        for i, row in enumerate(self.polygons):
            for j, polygon in enumerate(row):
                for point in polygon.points:
                    polygon_points.append(point)
        return polygon_points
    
    def modify_polygons(self, callback, **kwargs):
        if self.num_x == 1 and self.num_y == 1: 
            raise ValueError("Cannot modify grid of size 1 x 1")
        else:
            for i, row in enumerate(self.polygons):
                for j, polygon in enumerate(row):
                    callback(self, polygon, i, j, **kwargs)
                  
    def draw_polygons(self):
        self.modify_polygons(lambda self, polygon, i, j: self.drawing.add(self.drawing.polygon(polygon.points)))
        
    def center_polygon(self):
        center_i_j = self.center_i_j()
        return self.polygons[center_i_j[0]][center_i_j[1]]
    
    def center_geometric(self):
        center_x = (self.points[0][0][0] + self.points[1][-1][0]) / 2 # Center of length from first row first point to second row last point (it's isometric so second row is shifted over)
        center_y = (self.points[0][0][1] + self.points[-1][0][1]) / 2 # Top row y to bottom row y, colum doesn't matter
        print(f"center_x is {center_x} and is {center_y}")
        center = Polygon(3,1, [center_x, center_y])
        self.drawing.add(self.drawing.polygon(center.points))
        return [center_x, center_y]
    
    def center_i_j(self):
        center_polygon_j = round(self._num_x/2)-1
        center_polygon_i = round(self._num_y/2)-1
        print(f"{center_polygon_i} {center_polygon_j}")
        return [center_polygon_i, center_polygon_j]
    
    def distance(self, point_1:list, point_2:list):
        return math.sqrt( (point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2 )
        
    def draw_outlines(self, outline_offset):
        self.modify_polygons(lambda self, polygon, i, j: polygon.draw_outline(outline_offset))
    
    @property
    def spacing(self):
        return self._spacing
    
    @spacing.setter
    def spacing(self, spacing:float):
        self._spacing = spacing
        self.points = self._grid()
        
    @property
    def num_x(self):
        return self._num_x
    
    @num_x.setter
    def num_x(self, num_x:int):
        self._num_x = num_x
        self.points = self._grid()
        
    @property
    def num_y(self):
        return self._num_y
    
    @num_y.setter
    def num_y(self, num_y:int):
        self._num_y = num_y
        self.points = self._grid()
        
    @property
    def polygon(self):
        return self._polygon
    
    @polygon.setter
    def polygon(self, polygon):
        self._polygon = polygon
        self._generate_polygons()
        
    @property
    def center(self):
        return self._center
    
    @center.setter
    def center(self, center:List):
        self._center = center
        self.points = self._grid()
    
class Mandala:
    def __init__(self, drawing, mandala_radius:float, symmetry:int, polygon:Polygon, angle = 0, center = [0, 0]):
        self.drawing = drawing
        self._radius = mandala_radius
        self._symmetry = symmetry
        self._polygon = polygon
        self._angle = angle
        self._center = center
        self.points = self._mandala()
        self._polygons = self._generate_polygons()
    
    def _mandala(self):
        mandala_angle = 360 / self._symmetry # In degrees
        points = []
        for i in range(self._symmetry):
            current_angle = mandala_angle * i - 90 + self._angle
            x = self._center[0] + self._radius * math.cos(current_angle*(math.pi/180)) # Convert to rad for cos and sin
            y = self._center[1] + self._radius * math.sin(current_angle*(math.pi/180))
            points.append([x, y])
        return points
    
    def _generate_polygons(self):
        polygons = []
        mandala_angle = 360 / self._symmetry # In degrees
        for i, coord in enumerate(self.points):
            current_angle = mandala_angle * i + self._angle
            # print(f"in mandala _generate_polygons and i is {i}, mandala_angle is {mandala_angle} and current_angle is  {current_angle}")
            polygon = Polygon(self._polygon.num_points, self._polygon.radius, coord, self.drawing, current_angle)
            polygons.append(polygon)
        self._polygons = polygons
        return polygons
    
    def modify_polygons(self, callback, **kwargs):
        for i, polygon in enumerate(self._polygons):
            callback(self, polygon, i, **kwargs)
                  
    def draw_polygons(self):
        self.modify_polygons(lambda self, polygon, i: self.drawing.add(self.drawing.polygon(polygon.points))) 
        
    def draw_outlines(self, outline_offset):
        self.modify_polygons(lambda self, polygon, i: polygon.draw_outline(outline_offset))
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, radius:float):
        self._radius = radius
        self.points = self.points()
        
    @property
    def symmetry(self):
        return self._symmetry
    
    @symmetry.setter
    def radius(self, symmetry:float):
        self._symmetry = symmetry
        self.points = self.points()
        
    @property
    def polygon(self):
        return self._polygon
    
    @polygon.setter
    def polygon(self, polygon):
        self._polygon = polygon
        self._generate_polygons()
        
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, angle:float):
        self._angle = angle
        self.points = self.polygon()
        
    @property
    def center(self):
        return self._center
    
    @center.setter
    def center(self, center:List):
        self._center = center
        self.points = self.points()
        
class EdgeMandala: # TODO figure this shit out
    # To determine orientation of line segment AB with respect to origin C, use dot product of AC and BC. I think you can also use the cross product
    # This function should have an initial seed polygon, then you can make layers from it. Each layer will be the full set of polygons connected to all outside edges from the previous layer
    def __init__(self,  seed_polygon):
        self._seed_polygon = seed_polygon
        self.layers = [[self.seed_polygon]] # Start layers list off with seed polygon as the first layer
        
    def generate_edge_polygon(self, edge, num_points):
        start = edge[0]
        end = edge[1]
        return get_polygon_vertices(start, end, num_points)
    
    def generate_layer(self):
        # Create 1 "layer" of polygons which is a full set of polygons connected to all the outside edges of the previous layer starting with the seed polygon
        last_layer = self.layers[-1]
    
    @property
    def seed_polygon(self):
        return self._seed_polygon
    
    @seed_polygon.setter
    def seed_polygon(self, polygon):
        self._seed_polygon = polygon
        
    
def get_polygon_vertices(start, end, num_vertices): # ChatGPT, this one doesn't know which side of the line to make the polygon on
    # Calculate the length of the line segment
    line_length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    
    # Calculate the angle between each vertex
    angle = 2 * math.pi / num_vertices
    
    # Calculate the x and y increments for each vertex
    x_increment = line_length * math.cos(angle)
    y_increment = line_length * math.sin(angle)
    
    # Calculate the slope and y-intercept of the line segment
    slope = (end[1] - start[1]) / (end[0] - start[0])
    y_intercept = start[1] - slope * start[0]
    
    # Initialize the starting x and y coordinates
    x = start[0] + line_length / 2
    y = slope * x + y_intercept
    
    # Initialize an empty list to store the vertex coordinates
    vertices = []
    
    # Iterate through each vertex, calculating its coordinates
    for i in range(num_vertices):
        vertices.append((x, y))
        # Rotate the line segment by the angle to get the coordinates of the next vertex
        x, y = (x * math.cos(angle) - y * math.sin(angle),
                x * math.sin(angle) + y * math.cos(angle))
        # Add the x and y increments to get the coordinates of the next vertex
        x += x_increment
        y += y_increment
    
    return vertices
    
def radius_morph_polygon_center(grid, polygon:Polygon, i:int, j:int, magnitude):
    center = grid.center_polygon().center
    difference_x = abs(center[0] - polygon.center[0])
    difference_y = abs(center[1] - polygon.center[1])
    
    polygon.radius -= (difference_x + difference_y)*magnitude/10
    
def radius_morph_normalize(grid, polygon:Polygon, i:int, j:int, magnitude):
    # Magnitude will be 0 to 1, 1 being where the radius becomes 0 at the smallest
    # Use i and j
    center = grid.center_polygon().center
    # max_difference_x = abs(center[0] - grid.num_x)
    # max_difference_y = abs(center[0] - grid.num_y)
    # difference_x = abs(center[0] - grid.points[i][j][0])
    # difference_y = abs(center[1] - grid.points[i][j][1])
    # normalize_x = polygon.radius/max_difference_x
    # normalize_y = polygon.radius/max_difference_y
    # print(polygon.radius - max_difference_x*normalize_x)
    
    # Just calculate the actual line segment length and normalize that
    # max_difference = max(grid.)
    # difference = math.sqrt( (center[0] - polygon.center[0])**2 + (center[1] - polygon.center[1])**2 )
    # polygon.radius -= (difference_x*normalize_x + difference_y*normalize_y)*magnitude/2
    
def circle_morph(grid:GridIsometric, polygon:Polygon, i:int, j:int, magnitude:float, decrease_out:bool = True):
    center = grid.center_polygon().center
    # Try every distance from center to each corner and get max
    max_difference = max (grid.distance(center, grid.points[0][0]),
                        grid.distance(center, grid.points[0][-1]),
                        grid.distance(center, grid.points[-1][0]),
                        grid.distance(center, grid.points[-1][-1]))
    normalize = polygon.radius/max_difference
    difference = math.sqrt( (center[0] - polygon.center[0])**2 + (center[1] - polygon.center[1])**2 )
    if decrease_out:
        polygon.radius -= difference*normalize*magnitude
    else:
        polygon.radius = 0
        polygon.radius += difference*normalize*magnitude
        
def radius_morph_2(grid, polygon:Polygon, i:int, j:int):
    center_x = (grid.num_x - 1)/2
    center_y = (grid.num_y - 1)/2
    difference_x = abs(center_x - j)
    difference_y = abs(center_y - i)
    # print(f"i is {i}, j is {j}, center_x is {center_x}, difference_x is {difference_x}")
    polygon.radius -= (difference_x + difference_y)/4

def sine_morph(grid, polygon:Polygon, i:int, j:int, num_waves=1, amplitude=None):
    if not amplitude: amplitude = grid.num_x/2
    frequency = num_waves / grid.num_y
    sine_value = amplitude * math.sin(2 * math.pi * frequency * i) + (grid.num_x/2)
    difference = abs(sine_value - j)
    # if j == 0: polygon.num_points = 4
    # if difference <= 2: polygon.num_points = 5
    polygon.radius += (difference/10)
    polygon.angle += difference*3 
    

triangle = Polygon(3, 10)

pentagon = Polygon(5, 40)

hexagon = Polygon(6,40)

# fractal_polygon = Polygon(4, 50, [0, 0], drawing, 0)
# shrinkage = .25
# fractal_shape.draw_polygons()
# fractal_points = fractal_polygon.draw_fractal(shrinkage, 8, 360/16)
# print(f"fractal_points is {fractal_points} and fractal_polygon.fractal_points in {fractal_polygon.fractal_points}")
# drawing.add(drawing.polygon(*fractal_points))

# mandala = Mandala(drawing, 20, 20, triangle)
# mandala.draw_polygons()

honeycomb_hexagon = Polygon(6, 4.0)
honeycomb = GridIsometric(8, 1, 1, honeycomb_hexagon)
# honeycomb.modify_polygons(radius_morph_polygon_center, magnitude = 0.3)
honeycomb.modify_polygons(circle_morph, magnitude = 1.0, decrease_out = True)
honeycomb.draw_polygons()
# honeycomb.polygon = honeycomb_hexagon
# honeycomb.modify_polygons(circle_morph, magnitude = 1.0, decrease_out = False)
# honeycomb.draw_polygons()

# honeycomb.polygon = honeycomb_hexagon
# honeycomb.modify_polygons(radius_morph, magnitude = -0.3)
# honeycomb.draw_polygons()

# for i in range(10):
#     hexagon = Polygon(drawing, [0, 0], i+5, 6)
#     temp_mandala = Mandala(drawing, (i+2)*10, 12, hexagon)
#     temp_mandala.draw_polygons()

drawing.save()