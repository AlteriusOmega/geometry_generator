from geometry_generator import *
import svgwrite

triangle = Polygon(3, 10)

pentagon = Polygon(5, 40)

hexagon = Polygon(6,40)

fractal_polygon_radius = 70
fractal_polygon = Polygon(4, fractal_polygon_radius, [0, 0], drawing_global, 0)
shrinkage = .5

# fractal_points_1 = fractal_polygon.draw_fractal(shrinkage, 7, 360/16)

# print(fractal_polygon.draw_fractal(shrinkage, 7, 0))

# fractal_grid = Grid(fractal_polygon_radius*1,1, 6, fractal_polygon)
fractal_grid = GridIsometric(fractal_polygon_radius*(2+(1/8)),1, 6, fractal_polygon, True)
# fractal_grid.modify_polygons(lambda grid, polygon, i, j: polygon.draw_fractal(shrinkage, 4, 0))
# fractal_grid.draw_polygons()

# print(f"fractal_points is {fractal_points_1} ")
# drawing_global.add(drawing_global.polygon(fractal_points_1))

# mandala = Mandala(drawing_global, 20, 20, triangle)
# mandala.draw_polygons()

honeycomb_hexagon = Polygon(6, 6.0)
honeycomb = GridIsometric(12, 19, 67, honeycomb_hexagon)
# honeycomb.modify_polygons(radius_morph_polygon_center, magnitude = 0.3)
honeycomb.modify_polygons(circle_morph, magnitude = 0.75, decrease_out = True)
# honeycomb.modify_polygons(linear_gradient, magnitude = 1.0, angle = 30, decrease_out = True)
# honeycomb.draw_polygons()
# honeycomb.draw_outlines(5)

# for i in range(4):
#     honeycomb.modify_polygons(linear_gradient, magnitude = 0.7, angle = 45+10*i, decrease_out = True)
#     honeycomb.draw_polygons()

# honeycomb.polygon = honeycomb_hexagon
# honeycomb.modify_polygons(circle_morph, magnitude = 1.0, decrease_out = False)
# honeycomb.draw_polygons()

# honeycomb.polygon = honeycomb_hexagon
# honeycomb.modify_polygons(radius_morph, magnitude = -0.3)
# honeycomb.draw_polygons()

# for i in range(10):
#     hexagon = Polygon(drawing_global, [0, 0], i+5, 6)
#     temp_mandala = Mandala(drawing_global, (i+2)*10, 12, hexagon)
#     temp_mandala.draw_polygons()


pentagon.draw()

print(drawing_global.tostring())

drawing_global.save()