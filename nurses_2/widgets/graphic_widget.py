from enum import IntEnum

import cv2
import numpy as np

from ..colors import BLACK_ON_BLACK
from ..data_structures import Point, Size
from ..utils import clamp
from .widget import Widget, overlapping_region
from .widget_data_structures import Rect


class Interpolation(IntEnum):
    NEAREST = cv2.INTER_NEAREST
    LINEAR = cv2.INTER_LINEAR
    CUBIC = cv2.INTER_CUBIC
    AREA = cv2.INTER_AREA
    LANCZOS = cv2.INTER_LANCZOS4


class GraphicWidget(Widget):
    """
    Base for graphic widgets.

    Graphic widgets are widgets that are rendered entirely with the upper half block character, "▀".
    Graphic widgets' color information is stored in a (2 * height, width, 4)-shaped array, `texture`.
    `texture` can be treated as a uint8 RGBA image texture. Unlike its parent Widget, GraphicWidget
    does not have `canvas` or `colors` attributes.

    Parameters
    ----------
    is_transparent : bool, default: True
        If False the underlying texture's alpha channel is ignored.
    alpha : float, default: 1.0
        If widget is transparent, the alpha channel of the underlying texture will be multiplied by this
        value. (0 <= alpha <= 1.0)
    interpolation : Interpolation, default: Interpolation.LINEAR
        The interpolation used when resizing the GraphicWidget.
    """
    def __init__(
        self,
        size: Size=Size(10, 10),
        pos: Point=Point(0, 0),
        *,
        is_transparent=True,
        is_visible=True,
        is_enabled=True,
        default_char="▀",
        default_color_pair=BLACK_ON_BLACK,
        alpha=1.0,
        interpolation=Interpolation.LINEAR,
    ):
        self._size = h, w = size
        self.pos = pos
        self.is_transparent = is_transparent
        self.is_visible = is_visible
        self.is_enabled = is_enabled

        self.default_char = default_char
        self.default_color_pair = default_color_pair

        self.interpolation = interpolation
        self.alpha = clamp(alpha, 0, 1.0)

        self.parent = None
        self.children = [ ]

        self.texture = np.full(
            (2 * h, w, 4),
            (*self.default_bg_color, 255),
            dtype=np.uint8,
        )

    def resize(self, size: Size):
        """
        Resize widget.
        """
        self._size = h, w = size
        self.texture = cv2.resize(
            self.texture,
            (w, 2 * h),
            interpolation=self.interpolation,
        )

        for child in self.children:
            child.update_geometry()

    def normalize_canvas(self):
        raise NotImplementedError

    def get_view(self):
        raise NotImplementedError

    def render(self, canvas_view, colors_view, rect: Rect):
        """
        Paint region given by rect into canvas_view and colors_view.
        """
        t, l, b, r, _, _ = rect

        canvas_view[:] = self.default_char

        alpha = self.alpha

        texture = self.texture
        even_rows = texture[2 * t: 2 * b: 2, l: r]
        odd_rows = texture[2 * t + 1: 2 * b: 2, l: r]

        foreground = colors_view[..., :3]
        background = colors_view[..., 3:]

        if not self.is_transparent:
            foreground[:] = even_rows[..., :3]
            background[:] = odd_rows[..., :3]
        else:
            even_buffer = np.subtract(even_rows[..., :3], foreground, dtype=np.float16)
            odd_buffer = np.subtract(odd_rows[..., :3], background, dtype=np.float16)

            np.multiply(even_buffer, even_rows[..., 3, None], out=even_buffer)
            np.multiply(even_buffer, alpha, out=even_buffer)
            np.divide(even_buffer, 255, out=even_buffer)

            np.multiply(odd_buffer, odd_rows[..., 3, None], out=odd_buffer)
            np.multiply(odd_buffer, alpha, out=odd_buffer)
            np.divide(odd_buffer, 255, out=odd_buffer)

            np.add(even_buffer, foreground, out=foreground, casting="unsafe")
            np.add(odd_buffer, background, out=background, casting="unsafe")

        for child in self.children:
            if not child.is_visible or not child.is_enabled:
                continue

            if region := overlapping_region(rect, child):
                dest_slice, child_rect = region
                child.render(canvas_view[dest_slice], colors_view[dest_slice], child_rect)