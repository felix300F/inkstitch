from collections import defaultdict
from math import atan2, pi

from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import substring

from ..utils import Point as InkstitchPoint
from ..utils.geometry import line_string_to_point_list
from .running_stitch import running_stitch


def ripple_stitch(lines, target, line_count, points, max_stitch_length, repeats, reverse, skip_start, skip_end,
                  render_grid, exponent, flip_exponent, guide_line):
    '''
    Ripple stitch is allowed to cross itself and doesn't care about an equal distance of lines
    It is meant to be used with light (not dense) stitching
    It will ignore holes in a closed shape. Closed shapes will be filled with a spiral
    Open shapes will be stitched back and forth.
    If there is only one (open) line or a closed shape the target point will be used.
    If more sublines are present interpolation will take place between the first two.
    '''

    # sort geoms by size
    lines = sorted(lines.geoms, key=lambda linestring: linestring.length, reverse=True)
    outline = lines[0]

    # ignore skip_start and skip_end if both toghether are greater or equal to line_count
    if skip_start + skip_end >= line_count:
        skip_start = skip_end = 0

    if is_closed(outline):
        rippled_line = do_circular_ripple(outline, target, line_count, repeats, max_stitch_length, skip_start, skip_end,
                                          exponent, flip_exponent, guide_line)
    else:
        rippled_line = do_linear_ripple(lines, points, target, line_count - 1, repeats, max_stitch_length, skip_start, skip_end, render_grid,
                                        exponent, flip_exponent, guide_line)

    if reverse != flip_exponent:
        rippled_line = LineString(list(reversed(rippled_line.coords)))

    return running_stitch(line_string_to_point_list(rippled_line), max_stitch_length)


def do_circular_ripple(outline, target, line_count, repeats, max_stitch_length, skip_start, skip_end, exponent, flip_exponent, guide_line):
    if guide_line:
        lines = _get_guided_helper_lines(outline, max_stitch_length, flip_exponent, guide_line)
    else:
        # for each point generate a line going to the target point
        lines = target_point_lines_normalized_distances(outline, target, flip_exponent, max_stitch_length)

    # create a list of points for each line
    points = get_interpolation_points(lines, line_count, exponent, "circular")

    # connect the lines to a spiral towards the target
    coords = []
    for i in range(skip_start, line_count - skip_end):
        for j in range(len(lines)):
            coords.append(Point(points[j][i].x, points[j][i].y))

    coords = repeat_coords(coords, repeats)

    return LineString(coords)


def do_linear_ripple(lines, points, target, line_count, repeats, max_stitch_length, skip_start, skip_end, render_grid,
                     exponent, flip_exponent, guide_line):

    if len(lines) == 1:
        if guide_line:
            helper_lines = _get_guided_helper_lines(lines[0], max_stitch_length, flip_exponent, guide_line)
        else:
            helper_lines = target_point_lines(lines[0], target, flip_exponent)
    else:
        helper_lines = []
        for start, end in zip(points[0], points[1]):
            if flip_exponent:
                end, start = [start, end]
            helper_lines.append(LineString([start, end]))

    # get linear points along the lines
    points = get_interpolation_points(helper_lines, line_count, exponent)

    # go back and forth along the lines - flip direction of every second line
    coords = []
    for i in range(skip_start, len(points[0]) - skip_end):
        for j in range(len(helper_lines)):
            k = j
            if i % 2 != 0:
                k = len(helper_lines) - j - 1
            coords.append(Point(points[k][i].x, points[k][i].y))

    # add helper lines as a grid
    # for now only add this to satin type ripples, otherwise it could become to dense at the target point
    if len(lines) > 1 and render_grid:
        coords.extend(do_grid(helper_lines, line_count - skip_end))

    coords = repeat_coords(coords, repeats)

    return LineString(coords)


def do_grid(lines, num_lines):
    coords = []
    if num_lines % 2 == 0:
        lines = reversed(lines)
    for i, line in enumerate(lines):
        line_coords = list(line.coords)
        if (i % 2 == 0 and num_lines % 2 == 0) or (i % 2 != 0 and num_lines % 2 != 0):
            coords.extend(reversed(line_coords))
        else:
            coords.extend(line_coords)
    return coords


def line_length(line):
    return line.length


def is_closed(line):
    coords = line.coords
    return Point(*coords[0]).distance(Point(*coords[-1])) < 0.05


def target_point_lines(outline, target, flip_exponent):
    lines = []
    for point in outline.coords:
        if flip_exponent:
            lines.append(LineString([point, target]))
        else:
            lines.append(LineString([target, point]))
    return lines


def target_point_lines_normalized_distances(outline, target, flip_exponent, max_stitch_length):
    lines = []
    outline = running_stitch(line_string_to_point_list(outline), max_stitch_length)
    for point in outline:
        if flip_exponent:
            lines.append(LineString([target, point]))
        else:
            lines.append(LineString([point, target]))
    return lines


def _get_guided_helper_lines(lines, max_stitch_length, flip_exponent, guide_line):
    # for each point generate a line going along and pointing to the guide line
    if isinstance(guide_line, MultiLineString):
        # simple guide line
        lines = _generate_guided_helper_lines(lines, max_stitch_length, flip_exponent, guide_line.geoms[0])
    else:
        # satin type guide line
        rail_points = guide_line.plot_points_on_rails(max_stitch_length, 0)
        lines = _generate_satin_guide_helper_lines(lines, max_stitch_length, flip_exponent, rail_points)
    return lines


def _generate_guided_helper_lines(outline, max_stitch_length, flip_exponent, guide_line):
    # generates lines along the guide line tapering off towards to top
    line_point_dict = defaultdict(list)
    outline = running_stitch(line_string_to_point_list(outline), max_stitch_length)
    guide_line = running_stitch(line_string_to_point_list(guide_line), max_stitch_length)
    guide_length = len(guide_line)
    for j, outline_point in enumerate(outline):
        points = []
        for i, guide_point in enumerate(guide_line):
            if i == 0:
                steps = list(reversed(get_steps(guide_length - 1, 1)))
            else:
                if steps[i] == 0:
                    point = guide_point
                else:
                    transform = guide_line[0] - guide_point
                    transformed_point = outline_point - transform
                    transformed_line = LineString([guide_point, Point(transformed_point)])
                    distance = transformed_line.length * steps[i]
                    point = substring(transformed_line, 0, distance).coords[1]
                points.append(Point(point))
        line_point_dict[j] = points

    return _point_dict_to_linestring(len(outline), line_point_dict, flip_exponent)


def _generate_satin_guide_helper_lines(outline, max_stitch_length, flip_exponent, rail_points):
    first, last = [Point(i) for i in outline.coords[::len(outline.coords)-1]]
    if is_closed(outline):
        minx, miny, maxx, maxy = outline.bounds
        first = _get_extended_points(minx, outline.coords)
        last = _get_extended_points(maxx, outline.coords)

    outline_width = last.x - first.x

    # flip rails if they are the wrong way around
    rail_start_width = rail_points[0][0].x - rail_points[1][0].x
    if (outline_width * rail_start_width > 0):
        rail_points = list(reversed(rail_points))

    outline_width = abs(outline_width)
    outline = LineString(running_stitch(line_string_to_point_list(outline), max_stitch_length))
    outline_center = InkstitchPoint((last.x + first.x) / 2, (last.y + first.y) / 2)

    rotation = atan2(first.y - last.y, first.x - last.x)

    line_point_dict = defaultdict(list)
    # add original line
    for j, point in enumerate(outline.coords):
        line_point_dict[j].append(point)

    # add scaled and rotated outlines along the satin column guide line
    for i, (point1, point2) in enumerate(zip(*rail_points)):
        # translate
        guide_center = InkstitchPoint((point2.x + point1.x) / 2, (point2.y + point1.y) / 2)
        guide_transform = guide_center - outline_center
        translated_outline = translate(outline, guide_transform.x, guide_transform.y)
        # rotate
        guide_rotation = atan2(point1.y - point2.y, point1.x - point2.x)
        angle = (guide_rotation - rotation) * 360 / (2 * pi)
        rotated_outline = rotate(translated_outline, angle, origin=Point(guide_center))
        # scale
        distance = (point2 - point1).length()
        scale_factor = abs(distance / outline_width)
        scaled_outline = scale(rotated_outline, scale_factor, scale_factor, origin=Point(guide_center))
        # outline to helper line points
        for j, point in enumerate(scaled_outline.coords):
            line_point_dict[j].append(point)

    return _point_dict_to_linestring(len(outline.coords), line_point_dict, flip_exponent)


def _get_extended_points(x, coords):
    point = [point for point in coords if point[0] == x]
    if len(point) > 1:
        point = LineString(point).centroid
    if not isinstance(point, Point):
        point = Point(point)
    return point


def _point_dict_to_linestring(line_count, point_dict, flip_exponent):
    lines = []
    for i in range(line_count):
        points = point_dict[i]
        if flip_exponent:
            points = list(reversed(points))
        lines.append(LineString(points))
    return lines


def get_interpolation_points(lines, line_count, exponent, method="linear"):
    new_points = defaultdict(list)
    count = len(lines) - 1
    for i, line in enumerate(lines):
        steps = get_steps(line_count, exponent)
        points = []
        for j in range(line_count):
            length = line.length * steps[j]
            if method == "circular":
                distance = length + (((line.length * steps[j+1]) - length) * (i / count))
            else:
                distance = line.length * steps[j]
            points.append(line.interpolate(distance))
        if method == "linear":
            points.append(Point(*line.coords[-1]))
        new_points[i] = points
    return new_points


def get_steps(total_lines, exponent):
    # get_steps is scribbled from the inkscape interpolate extension
    # (https://gitlab.com/inkscape/extensions/-/blob/master/interp.py)
    steps = [
        ((i + 1) / (total_lines)) ** exponent
        for i in range(total_lines - 1)
    ]
    return [0] + steps + [1]


def repeat_coords(coords, repeats):
    final_coords = []
    for i in range(repeats):
        if i % 2 == 1:
            # reverse every other pass
            this_coords = coords[::-1]
        else:
            this_coords = coords[:]

        final_coords.extend(this_coords)
    return final_coords
