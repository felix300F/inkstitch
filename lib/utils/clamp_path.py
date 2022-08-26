from shapely.geometry import LineString, MultiLineString, Point as ShapelyPoint
from shapely.prepared import prep
from collections import deque

from .geometry import Point


def path_to_segments(path):
    """Convert a path of Points into a list of segments as LineStrings"""
    for start, end in zip(path[:-1], path[1:]):
        yield LineString((start, end))


def segments_to_path(segments):
    """Convert a list of contiguous LineStrings into a list of Points."""
    coords = [segments[0].coords[0]]

    for segment in segments:
        coords.extend(segment.coords[1:])

    return [Point(x, y) for x, y in coords]


def extend_segment(line_string):
    """Move a line segment's start and end away from each other to ensure intersections."""
    p0 = line_string.coords[0]
    p1 = line_string.coords[1]

    length = line_string.length
    direction = ((p0[0] - p1[0]) / length, (p0[1] - p1[1]) / length)
    offset = (direction[0] * 1e-9, direction[1] * 1e-9)

    new_p0 = (p0[0] + offset[0], p0[1] + offset[1])
    new_p1 = (p1[0] - offset[0], p1[1] - offset[1])

    return LineString((new_p0, new_p1))


def fix_starting_point(border_pieces):
    """Reconnect the starting point of a polygon border's pieces.

    When splitting a polygon border with two lines, we want to get two
    pieces.  However, that's not quite how Shapely works.  The outline
    of the polygon is a LinearRing that starts and ends at the same place,
    but Shapely still knows where that starting point is and splits there
    too.

    We don't want that third piece, so we'll reconnect the segments that
    touch the starting point.
    """

    if len(border_pieces) == 3:
        # Fortunately, Shapely keeps the starting point of the LinearRing
        # as the starting point of the first segment.  That means it's also
        # the ending point of the last segment.  Reconnecting is super simple:
        return [border_pieces[1],
                LineString(border_pieces[2].coords[:] + border_pieces[0].coords[1:])]
    else:
        # We probably cut exactly at the starting point.
        return border_pieces


def adjust_line_end(line, end):
    """Reverse line if necessary to ensure that it ends near end."""

    line_start = ShapelyPoint(*line.coords[0])
    line_end = ShapelyPoint(*line.coords[-1])

    if line_end.distance(end) < line_start.distance(end):
        return line
    else:
        return LineString(line.coords[::-1])


def ensure_list_of_geometries(thing):
    try:
        return list(thing.geoms)
    except AttributeError:
        return [thing]


def find_border(polygon, line):
    for border in polygon.interiors:
        if border.intersects(line):
            return border
    else:
        return polygon.exterior


def clamp_path_to_polygon(path, polygon):
    """Constrain a path to a Polygon.

    Description: https://gis.stackexchange.com/questions/428848/clamp-linestring-to-polygon
    """
    segments = deque(path_to_segments(path))
    result = []
    exiting_segment = None
    was_inside = False

    # contains() checks can fail without this.
    buffered_polygon = prep(polygon.buffer(1e-9))
    boundary = polygon.boundary

    while segments:
        current_segment = segments.popleft()
        pieces = ensure_list_of_geometries(current_segment.difference(boundary))

        if pieces[0].coords[0] != current_segment.coords[0]:
            # The initial part of this line segment coincided with part of the
            # polygon border and was removed.

            if was_inside:
                # If we were already inside, we include this border segment.
                result.append(LineString((current_segment.coords[0], pieces[0].coords[0])))

            # Push the rest back on to be processed later.
            # Note that extendleft() reverses its arguments, so we have to compensate.
            segments.extendleft(reversed(pieces))
        elif len(pieces) > 1:
            # This segment crosses the border, or touches the border at a single point,
            # or maybe crosses multiple times, and might even coincide with the border
            # for a while.  Basically, it's complicated.
            #
            # Split the first portion off and push it and the rest to be reprocessed
            # in the following iterations.
            segments.appendleft(LineString((pieces[0].coords[1], current_segment.coords[-1])))
            segments.appendleft(pieces[0])
        else:
            # This segment is either all inside or all outside the polygon.
            is_inside = buffered_polygon.contains(current_segment)
            if is_inside:
                if not was_inside:
                    # We've crossed from outside to inside exactly at the starting
                    # point of this line segment.

                    if exiting_segment:
                        # Earlier we crossed out from the inside, now we're
                        # crossing back in.  Find the shortest path along
                        # the border that gets from the exit point to the
                        # entry point and add it to the result.

                        entering_segment = extend_segment(current_segment)
                        border = find_border(polygon, entering_segment)
                        difference = border.difference(MultiLineString((exiting_segment, entering_segment)))
                        border_pieces = ensure_list_of_geometries(difference)
                        border_pieces = fix_starting_point(border_pieces)

                        if len(border_pieces) == 1:
                            # We re-entered exactly where we left, so we
                            # don't include any of the border.
                            pass
                        else:
                            shorter = min(border_pieces, key=lambda piece: piece.length)

                            # We don't know which direction the polygon border
                            # piece should be.  adjust_line_end() will figure
                            # that out.
                            result.append(adjust_line_end(shorter, ShapelyPoint(*current_segment.coords[0])))

                        exiting_segment = None

                # This piece is inside, so always include it.
                result.append(current_segment)
                was_inside = True
            elif was_inside:
                # Like the previous case, but we've crossed to outside.  Store
                # an extended version of this segment as the exit point.
                exiting_segment = extend_segment(current_segment)
                was_inside = False

    return segments_to_path(result)
