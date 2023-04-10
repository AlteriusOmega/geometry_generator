import svgwrite
import math

# This will be a SVG geometric pattern creator app

width = 100
height = 400


def regular_polygon(center, radius, num_points):
    angle = (math.pi * 2) / num_points
    points = []
    for i in range(num_points):
        current_angle = angle * i + (90*math.pi/180)
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
            print(f"polygon is {polygon}")
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

class polygon:
    def __init__(self, drawing, center, radius, num_points):
        self.drawing = drawing
        self.center = center
        self.radius = radius
        self.num_points = num_points
        self.points = regular_polygon(center, radius, num_points)
        
    
    def draw(self):
        drawing.add(drawing.polygon())
        

def print_polygon_center(polygon, center, i, j):
    print(center)
    
test_polygon = polygon(drawing, [0,0], 5, 6)
test_polygon.num_points = 5
print(test_polygon.num_points)
print(test_polygon.points)

hex_grid_1 = hex_grid(2, 5, 20, 100)

sine_gradient(hex_grid_1, 1, 1)

draw_grid(hex_grid_1, drawing)    

test_hex_grid = hex_grid(10, 20, 1, 1)

modify_grid(test_hex_grid, print_polygon_center)

drawing.save()