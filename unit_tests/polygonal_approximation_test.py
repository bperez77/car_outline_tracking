#!/usr/bin/env python3

"""
polygonal_approximation_test.py

Brandon Perez (bmperez)
Sohil Shah (sohils)

Wednesday, April 26, 2017 at 10:43:51 AM EDT

This file contains the unit tests for the polygonal_approximation module,
for the thick_polygonal_approximate function.
"""

# General Imports
import sys
import os
import numpy
import unittest
from matplotlib import pyplot

# Add the src directory to the PYTHONPATH
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '..',
        'src')))

# Local Imports
from polygonal_approximation import thick_polygonal_approximate

#-------------------------------------------------------------------------------
# Basic Unit Tests
#-------------------------------------------------------------------------------

class BasicUnitTests(unittest.TestCase):
    """A unit test subclass for performing basic unit tests for the
    thick_polygonal_approximate function."""

    # Change this true to show the plot of the original and approximated
    # polygons for the large point test.
    LARGE_POINT_SET_SHOW_PLOT = False

    def test_thin_curve(self):
        """Tests the function with a simple 4-point polyline with a min and max
        that are not thick enough to be considered dominant points."""

        # The parameters for the test, and the function call
        thickness = 40
        points = numpy.array([
            [20, 20],
            [30, 15],
            [40, 25],
            [50, 23],
        ])
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape, (2, 2))
        self.assertTrue(numpy.array_equal(dominant_points,
                [[20, 20], [50, 23]]))

    def test_thick_curve(self):
        """Tests the function with a simple 4-point polyline with a min and max
        that are thick enough, so all points are dominant."""

        # The parameters for the test, and the function call
        thickness = 40
        points = numpy.array([
            [20, 100],
            [30, 30],
            [40, 170],
            [50, 105],
        ])
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape, points.shape)
        self.assertTrue(numpy.array_equal(dominant_points, points))

    def test_reverse_order(self):
        """Tests that the function can also handle points in reverse order. This
        is the same test as the thick_curve_test, with the ordering of the
        points reversed."""

        # The parameters for the test, and the function call
        thickness = 40
        points = numpy.array([
            [50, 105],
            [40, 170],
            [30, 30],
            [20, 100],
        ])
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape, points.shape)
        self.assertTrue(numpy.array_equal(dominant_points, points))

    def test_horizontal_line(self):
        """Tests that the function can handle a horizontal regression line that
        passes through the endpoints. This is a thick line test."""

        # The parameters for the test, and the function call
        thickness = 40
        points = numpy.array([
            [20, 100],
            [30, 30],
            [40, 170],
            [50, 100],
        ])
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape, points.shape)
        self.assertTrue(numpy.array_equal(dominant_points, points))

    def test_vertical_line(self):
        """Tests that the function can handle a vertical regression line that
        passes through the endpoints. This is a thick line test"""

        # The parameters for the test, and the function call
        thickness = 40
        points = numpy.array([
            [100, 20],
            [30,  30],
            [170, 40],
            [100, 50],
        ])
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape, points.shape)
        self.assertTrue(numpy.array_equal(dominant_points, points))

    def test_no_maximum(self):
        """Tests that the function can handle when there is no maximum point,
        but there is a minimum. This is a thick line test."""

        # The parameters for the test, and the function call
        thickness = 40
        points = numpy.array([
            [20, 100],
            [30, 30],
            [40, 105],
        ])
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape, points.shape)
        self.assertTrue(numpy.array_equal(dominant_points, points))

    def test_no_minimum(self):
        """Tests that the function can handle when there is no minimum point,
        but there is a maximum."""

        # The parameters for the test, and the function call
        thickness = 40
        points = numpy.array([
            [20, 100],
            [30, 170],
            [40, 105],
        ])
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape, points.shape)
        self.assertTrue(numpy.array_equal(dominant_points, points))

    def test_large_point_set(self):
        """Tests the function with a larger, complete polygon point set, in this
        case, a circle."""

        # Generate the x points for a circle of radius 10, centered at (40, 100)
        radius = 10
        centerpoint = numpy.array([40, 100])
        circle_upper_xs = numpy.linspace(-radius, radius, num=10000)
        circle_lower_xs = numpy.flip(circle_upper_xs[1:-1], axis=0)

        # Generate the y points for the circle, and combine the x and y points.
        circle_upper_ys = numpy.sqrt(radius ** 2 - circle_upper_xs ** 2)
        circle_lower_ys = -numpy.sqrt(radius ** 2 - circle_lower_xs ** 2)
        circle_ys = numpy.concatenate([circle_upper_ys, circle_lower_ys])
        circle_xs = numpy.concatenate([circle_upper_xs, circle_lower_xs])
        points = numpy.column_stack([circle_xs, circle_ys]) + centerpoint

        # The thickness used, and the polygonal function call
        thickness = 0.01 * radius
        dominant_points = thick_polygonal_approximate(points, thickness)

        # Verify the format of the output
        self.assertIsInstance(dominant_points, numpy.ndarray)
        self.assertEqual(dominant_points.shape[1], 2)

        # Compare the original area to the new area, and the reduction in the
        # number of vertices.
        (original_vertices, _) = points.shape
        (new_vertices, _) = dominant_points.shape
        original_area = self._compute_area(points)
        new_area = self._compute_area(dominant_points)
        area_diff = (new_area - original_area) / original_area * 100
        vertex_diff = ((new_vertices - original_vertices) /
                original_vertices * 100)

        # Report the results to the user
        print("\nLarge Point Set Test Results:")
        print("\tOriginal Polygon Vertices:     {:<10}".format(
                original_vertices))
        print("\tOriginal Polygon Area:         {:<10.3f}".format(
                original_area))
        print("\tApproximated Polygon Vertices: {:<10} ({:0.3f}%)".format(
                new_vertices, vertex_diff))
        print("\tApproximated Polygon Area:     {:<10.3f} ({:0.3f}%)".format(
                new_area, area_diff))

        # If specified on the command line, show the plot
        if BasicUnitTests.LARGE_POINT_SET_SHOW_PLOT:
            pyplot.plot(points[:, 0], points[:, 1], 'r', color='r',
                    label='Original Polygon', linewidth=5)
            pyplot.plot(dominant_points[:, 0], dominant_points[:, 1], 'r',
                    color='b', label='Approximated Polygon', linewidth=3)
            pyplot.legend()
            pyplot.show()

    def _compute_area(self, points):
        """Computes the area of the polygon given by the specified points."""

        # Put each pair of vertices into a matrix, and stack them
        points_shifted = numpy.roll(points, -1, axis=0)
        vertex_pairs = numpy.stack([points, points_shifted], axis=2)

        # The signed area of the polygon is half of the sum of the determinants
        # of the vertex pairs.
        vertex_areas = numpy.linalg.det(vertex_pairs)
        return 1 / 2.0 * abs(numpy.sum(vertex_areas))

if __name__ == "__main__":
    unittest.main(verbosity=2)
