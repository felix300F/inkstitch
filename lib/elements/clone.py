# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import atan2, degrees

from inkex import NSS

from ..commands import is_command_symbol
from ..i18n import _
from ..svg.path import get_node_transform
from ..svg.svg import find_elements
from ..svg.tags import (EMBROIDERABLE_TAGS, INKSTITCH_ATTRIBS, SVG_USE_TAG,
                        XLINK_HREF)
from ..utils import cache
from .element import EmbroideryElement, param
from .fill_stitch import FillStitch
from .validation import ObjectTypeWarning, ValidationWarning


class CloneWarning(ValidationWarning):
    name = _("Clone Object")
    description = _("There are one or more clone objects in this document.  "
                    "Ink/Stitch can work with single clones, but you are limited to set a very few parameters. ")
    steps_to_solve = [
        _("If you want to convert the clone into a real element, follow these steps:"),
        _("* Select the clone"),
        _("* Run: Edit > Clone > Unlink Clone (Alt+Shift+D)")
    ]


class CloneSourceWarning(ObjectTypeWarning):
    name = _("Clone is not embroiderable")
    description = _("There are one ore more clone objects in this document. A clone must be a direct child of an embroiderable element. "
                    "Ink/Stitch cannot embroider clones of groups or other not embroiderable elements (text or image).")
    steps_to_solve = [
        _("Convert the clone into a real element:"),
        _("* Select the clone."),
        _("* Run: Edit > Clone > Unlink Clone (Alt+Shift+D)")
    ]


class Clone(EmbroideryElement):
    # A clone embroidery element is linked to an embroiderable element.
    # It will be ignored if the source element is not a direct child of the xlink attribute.

    element_name = "Clone"

    def __init__(self, *args, **kwargs):
        super(Clone, self).__init__(*args, **kwargs)

    @property
    @param('clone', _("Clone"), type='toggle', inverse=False, default=True)
    def clone(self):
        return self.get_boolean_param("clone")

    @property
    @param('angle',
           _('Custom fill angle'),
           tooltip=_("This setting will apply a custom fill angle for the clone."),
           unit='deg',
           type='float')
    @cache
    def clone_fill_angle(self):
        return self.get_float_param('angle') or None

    def clone_to_element(self, node):
        from .utils import node_to_elements
        return node_to_elements(node, True)

    def to_stitch_groups(self, last_patch=None):
        patches = []

        source_node = get_clone_source(self.node)
        if source_node.tag not in EMBROIDERABLE_TAGS:
            return []

        self.node.style = source_node.specified_style()

        inkstitch_attribs = {k: v for k, v in source_node.attrib.iteritems() if NSS['inkstitch'] in k}
        for key, value in inkstitch_attribs.items():
            if not key == INKSTITCH_ATTRIBS['angle']:
                self.node.set(key, value)

        # if no explicit fill angle is set use calculated rotation
        calculated_fill_angle = False
        if self.clone_fill_angle is None and self.node.style['fill'] is not None:
            # source node fill angle
            source_fill_angle = float(source_node.get(INKSTITCH_ATTRIBS['angle'], 0))

            # inkex has transform.rotation_degrees(), but in some cases it fails (skewing). So let's calculate the
            # angle between the minimum rotated rectangle of the source element and clone element
            source_direction = self.get_element_direction(source_node)
            clone_direction = self.get_element_direction(self.node)
            angle = source_fill_angle + source_direction - clone_direction

            # set angle value
            self.node.set(INKSTITCH_ATTRIBS['angle'], str(angle))
            calculated_fill_angle = True

        elements = self.clone_to_element(self.node)

        for element in elements:
            patches.extend(element.to_stitch_groups(last_patch))

        # cleanup attributes
        for key, value in inkstitch_attribs.items():
            if not key == INKSTITCH_ATTRIBS['angle'] or calculated_fill_angle is True:
                self.node.pop(key)

        return patches

    def get_element_direction(self, node):
        element = FillStitch(node)
        rect = element.shape.minimum_rotated_rectangle.exterior.coords
        return round(degrees(atan2(rect[2][1] - rect[0][1], rect[2][0] - rect[0][0])) % 360)

    def get_clone_style(self, style_name, node, default=None):
        style = node.style[style_name] or default
        return style

    def center(self, source_node):
        transform = get_node_transform(self.node.getparent())
        center = self.node.bounding_box(transform).center
        return center

    def validation_warnings(self):
        source_node = get_clone_source(self.node)
        if source_node.tag not in EMBROIDERABLE_TAGS:
            point = self.center(source_node)
            yield CloneSourceWarning(point)
        else:
            point = self.center(source_node)
            yield CloneWarning(point)


def is_clone(node):
    if node.tag == SVG_USE_TAG and node.get(XLINK_HREF) and not is_command_symbol(node):
        return True
    return False


def is_embroiderable_clone(node):
    if is_clone(node) and get_clone_source(node).tag in EMBROIDERABLE_TAGS:
        return True
    return False


def get_clone_source(node):
    source_id = node.get(XLINK_HREF)[1:]
    xpath = ".//*[@id='%s']" % (source_id)
    source_node = find_elements(node, xpath)[0]
    return source_node
