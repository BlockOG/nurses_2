from ..widget_utilities import clamp
from .grabbable_behavior import GrabbableBehavior


class DraggableBehavior(GrabbableBehavior):
    """
    Draggable behavior for a widget. Translate a widget by clicking and dragging it.

    Parameters
    ----------
    disable_oob : bool, default: False
        If true, widget won't be traslated outside of its parent's bounding box.
    disable_ptf : bool, default: False
        If true, widget won't be pulled-to-front when clicked.
    allow_vertical : bool, default: True
        Allow vertical translation.
    allow_horizontal : bool, default: True
        Allow horizontal translation.
    """
    def __init__(
        self,
        *args,
        disable_oob=False,
        disable_ptf=False,
        allow_vertical=True,
        allow_horizontal=True,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.disable_oob = disable_oob
        self.disable_ptf = disable_ptf
        self.allow_vertical = allow_vertical
        self.allow_horizontal = allow_horizontal

    def grab(self, mouse_event):
        super().grab(mouse_event)
        self._last_mouse_pos = mouse_event.position

        if not self.disable_ptf:
            self.parent.pull_to_front(self)

    def grab_update(self, mouse_event):
        last_y, last_x = self._last_mouse_pos
        y, x = self._last_mouse_pos = mouse_event.position

        if self.allow_vertical:
            self.top += y - last_y
        if self.allow_horizontal:
            self.left += x - last_x

        if self.disable_oob:
            self.top = clamp(self.top, 0, self.parent.height - self.height)
            self.left = clamp(self.left, 0, self.parent.width - self.width)