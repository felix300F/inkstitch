from math import atan2, copysign,pi
from random import (random,uniform)

import numpy as np
import shapely.prepared
from shapely import geometry as shgeo
from shapely.affinity import translate
from shapely.ops import linemerge, nearest_points, unary_union

from ..debug import debug
from ..stitch_plan import Stitch
from ..utils.geometry import Point as InkstitchPoint
from ..utils.geometry import (ensure_geometry_collection,
                              ensure_multi_line_string, reverse_line_string)
from .auto_fill import (auto_fill, build_fill_stitch_graph, build_travel_graph,
                        collapse_sequential_outline_edges, find_stitch_path,
                        graph_is_valid, travel)


def guided_fill(shape,
                guideline,
                angle,
                row_spacing,
                num_staggers,
                max_stitch_length,
                running_stitch_length,
                running_stitch_tolerance,
                skip_last,
                starting_point,
                ending_point,
                underpath,
                strategy,
                length_decrease=0,
                length_increase=0,
                angle_variation=0,
                row_spacing_randomness=0
                ):
    segments = intersect_region_with_grating_guideline(shape, guideline, row_spacing, num_staggers, max_stitch_length, strategy,length_decrease, length_increase,angle_variation,row_spacing_randomness)
    if not segments:
        return fallback(shape, guideline, row_spacing, max_stitch_length, running_stitch_length, running_stitch_tolerance,
                        num_staggers, skip_last, starting_point, ending_point, underpath)

    fill_stitch_graph = build_fill_stitch_graph(shape, segments, starting_point, ending_point)

    if not graph_is_valid(fill_stitch_graph, shape, max_stitch_length):
        return fallback(shape, guideline, row_spacing, max_stitch_length, running_stitch_length, running_stitch_tolerance,
                        num_staggers, skip_last, starting_point, ending_point, underpath)

    travel_graph = build_travel_graph(fill_stitch_graph, shape, angle, underpath)
    path = find_stitch_path(fill_stitch_graph, travel_graph, starting_point, ending_point)
    result = path_to_stitches(path, travel_graph, fill_stitch_graph, max_stitch_length, running_stitch_length, running_stitch_tolerance, skip_last )

    return result


def fallback(shape, guideline, row_spacing, max_stitch_length, running_stitch_length, running_stitch_tolerance,
             num_staggers, skip_last, starting_point, ending_point, underpath):
    # fall back to normal auto-fill with an angle that matches the guideline (sorta)
    guide_start, guide_end = [guideline.coords[0], guideline.coords[-1]]
    angle = atan2(guide_end[1] - guide_start[1], guide_end[0] - guide_start[0]) * -1
    return auto_fill(shape, angle, row_spacing, None, max_stitch_length, running_stitch_length, running_stitch_tolerance,
                     num_staggers, skip_last, starting_point, ending_point, underpath)


def path_to_stitches(path, travel_graph, fill_stitch_graph, stitch_length, running_stitch_length, running_stitch_tolerance, skip_last):
    path = collapse_sequential_outline_edges(path)

    stitches = []

    # If the very first stitch is travel, we'll omit it in travel(), so add it here.
    if not path[0].is_segment():
        stitches.append(Stitch(*path[0].nodes[0]))

    for edge in path:
        if edge.is_segment():
            current_edge = fill_stitch_graph[edge[0]][edge[-1]]['segment']
            path_geometry = current_edge['geometry']

            if edge[0] != path_geometry.coords[0]:
                path_geometry = reverse_line_string(path_geometry)

            new_stitches = [Stitch(*point) for point in path_geometry.coords]

            # need to tag stitches

            if skip_last:
                del new_stitches[-1]

            stitches.extend(new_stitches)

            travel_graph.remove_edges_from(fill_stitch_graph[edge[0]][edge[1]]['segment'].get('underpath_edges', []))
        else:
            stitches.extend(travel(travel_graph, edge[0], edge[1], running_stitch_length, running_stitch_tolerance, skip_last))

    return stitches


def extend_line(line, shape):
    (minx, miny, maxx, maxy) = shape.bounds

    upper_left = InkstitchPoint(minx, miny)
    lower_right = InkstitchPoint(maxx, maxy)
    length = (upper_left - lower_right).length()

    start_point = InkstitchPoint.from_tuple(line.coords[0])
    end_point = InkstitchPoint.from_tuple(line.coords[-1])
    direction = (end_point - start_point).unit()

    new_start_point = start_point - direction * length
    new_end_point = end_point + direction * length

    # without this, we seem especially likely to run into this libgeos bug:
    #   https://github.com/shapely/shapely/issues/820
    new_start_point += InkstitchPoint(random() * 0.01, random() * 0.01)
    new_end_point += InkstitchPoint(random() * 0.01, random() * 0.01)

    return shgeo.LineString((new_start_point, *line.coords, new_end_point))


def repair_multiple_parallel_offset_curves(multi_line):
    lines = ensure_multi_line_string(linemerge(multi_line))
    longest_line = max(lines.geoms, key=lambda line: line.length)

    # need simplify to avoid doubled points caused by linemerge
    return longest_line.simplify(0.01, False)


def repair_non_simple_line(line):
    repaired = unary_union(line)
    counter = 0
    # Do several iterations since we might have several concatenated selfcrossings
    while repaired.geom_type != 'LineString' and counter < 4:
        line_segments = []
        for line_seg in repaired.geoms:
            if not line_seg.is_ring:
                line_segments.append(line_seg)

        repaired = unary_union(linemerge(line_segments))
        counter += 1
    if repaired.geom_type != 'LineString':
        # They gave us a line with complicated self-intersections.  Use a fallback.
        return shgeo.LineString((line.coords[0], line.coords[-1]))
    else:
        return repaired


def take_only_line_strings(thing):
    things = ensure_geometry_collection(thing)
    line_strings = [line for line in things.geoms if isinstance(line, shgeo.LineString)]

    return shgeo.MultiLineString(line_strings)


def apply_stitches(line, max_stitch_length, num_staggers, row_spacing, row_num,length_decrease=0, length_increase=0,angle_variation=0,row_spacing_randomness=0):

    start = (float(row_num % num_staggers) / num_staggers) * max_stitch_length

   
    if length_decrease or length_increase:
        projections=[start]
        position=start
        while position<line.length-max_stitch_length:
            length_perturbation=uniform(-length_decrease/100,length_increase/100)
            position+=max_stitch_length*(1+length_perturbation)
            projections+=[position]

        projections+=[line.length]
    else:
        projections = np.arange(start, line.length, max_stitch_length)

    points = np.array([line.interpolate(projection).coords[0] for projection in projections])
   
    if angle_variation:
        for i,(point1, point0)in enumerate (zip( points[1:] , points[0:])):
      
            beg = Stitch(*point1)
            end = Stitch(*point0)

            line_direction = (end - beg)#.unit()
          
            normal=line_direction.rotate(pi/2)
            angle_perturbation=uniform(-angle_variation/100,angle_variation/100)
            points[i]+=angle_perturbation*normal
    
      
    stitched_line = shgeo.LineString(points)

    # stitched_line may round corners, which will look terrible.  This finds the
    # corners.
    threshold = row_spacing / 2.0
    simplified_line = line.simplify(row_spacing / 2.0, False)
    simplified_points = [shgeo.Point(x, y) for x, y in simplified_line.coords]

    extra_points = []
    extra_point_projections = []
    for point in simplified_points:
        if point.distance(stitched_line) > threshold:
            extra_points.append(point.coords[0])
            extra_point_projections.append(line.project(point))

    # Now we need to insert the new points into their correct spots in the line.
    indices = np.searchsorted(projections, extra_point_projections)
    if len(indices) > 0:
        points = np.insert(points, indices, extra_points, axis=0)

    return shgeo.LineString(points)

def prepare_guide_line(line, shape):
    if line.geom_type != 'LineString' or not line.is_simple:
        line = repair_non_simple_line(line)

    if line.is_ring:
        # If they pass us a ring, break it to avoid dividing by zero when
        # calculating a unit vector from start to end.
        line = shgeo.LineString(line.coords[:-2])

    # extend the end points away from each other
    line = extend_line(line, shape)

    return line


def clean_offset_line(offset_line):
    offset_line = take_only_line_strings(offset_line)

    if isinstance(offset_line, shgeo.MultiLineString):
        offset_line = repair_multiple_parallel_offset_curves(offset_line)

    if not offset_line.is_simple:
        offset_line = repair_non_simple_line(offset_line)

    return offset_line


def _get_start_row(line, shape, row_spacing, line_direction):
    if line.intersects(shape):
        return 0

    point1, point2 = nearest_points(line, shape.centroid)
    distance = point1.distance(point2)
    row = int(distance / row_spacing)

    # This flips the sign of the starting row if the shape is on the other side
    # of the guide line
    shape_direction = InkstitchPoint.from_shapely_point(point2) - InkstitchPoint.from_shapely_point(point1)
    return copysign(row, shape_direction * line_direction)


def intersect_region_with_grating_guideline(shape, line, row_spacing, num_staggers, max_stitch_length, strategy,length_decrease, length_increase,angle_variation,row_spacing_randomness):
    line = prepare_guide_line(line, shape)

    debug.log_line_string(shape.exterior, "guided fill shape")

    translate_direction = InkstitchPoint(*line.coords[-1]) - InkstitchPoint(*line.coords[0])
    translate_direction = translate_direction.unit().rotate_left()

    shape_envelope = shapely.prepared.prep(shape.convex_hull)

    start_row = _get_start_row(line, shape, row_spacing, translate_direction)
    row = start_row
    direction = 1
    offset_line = None
    row_spacing_factor=1

    rows = []
    
    
    while True:
        if row_spacing_randomness:
            row_spacing_factor=uniform(-row_spacing_randomness/100, row_spacing_randomness/100)
        translate_amount = translate_direction * row_spacing*(row_spacing_factor + row)
        if strategy == 0:
            offset_line = translate(line, xoff=translate_amount.x, yoff=translate_amount.y)
        elif strategy == 1:
            offset_line = line.parallel_offset(translate_amount, 'left', join_style=shgeo.JOIN_STYLE.round)

        offset_line = clean_offset_line(offset_line)

        if strategy == 1 and direction == -1:
            # negative parallel offsets are reversed, so we need to compensate
            offset_line = reverse_line_string(offset_line)

        debug.log_line_string(offset_line, f"offset {row}")
        

        stitched_line = apply_stitches(offset_line, max_stitch_length, num_staggers, row_spacing, row * direction,length_decrease, length_increase,angle_variation,row_spacing_randomness)
        intersection = shape.intersection(stitched_line)
        
        if shape_envelope.intersects(stitched_line):
            for segment in take_only_line_strings(intersection).geoms:
                rows.append(segment.coords[:])
            row += direction
        else:
            if direction == 1:
                direction = -1
                row = start_row - 1
            else:
                break

    return rows
