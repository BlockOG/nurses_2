from ..events import Mods, MouseEventType, MouseButton

MOUSE_UP = MouseEventType.MOUSE_UP
MOUSE_DOWN = MouseEventType.MOUSE_DOWN
MOUSE_MOVE = MouseEventType.MOUSE_MOVE
SCROLL_UP = MouseEventType.SCROLL_UP
SCROLL_DOWN = MouseEventType.SCROLL_DOWN

LEFT = MouseButton.LEFT
MIDDLE = MouseButton.MIDDLE
RIGHT = MouseButton.RIGHT
NO_BUTTON = MouseButton.NO_BUTTON
UNKNOWN_BUTTON = MouseButton.UNKNOWN_BUTTON

NO_MODS           = Mods.NO_MODS
ALT               = Mods(True , False, False)
CONTROL           = Mods(False, True , False)
SHIFT             = Mods(False, False, True )
ALT_CONTROL       = Mods(True , True , False)
ALT_SHIFT         = Mods(True , False, True )
CONTROL_SHIFT     = Mods(False, True , True )
ALT_CONTROL_SHIFT = Mods(True , True , True )

TERM_SGR = {
    ( 0, "m"): (MOUSE_UP, LEFT, NO_MODS),
    ( 4, "m"): (MOUSE_UP, LEFT, SHIFT),
    ( 8, "m"): (MOUSE_UP, LEFT, ALT),
    (12, "m"): (MOUSE_UP, LEFT, ALT_SHIFT),
    (16, "m"): (MOUSE_UP, LEFT, CONTROL),
    (20, "m"): (MOUSE_UP, LEFT, CONTROL_SHIFT),
    (24, "m"): (MOUSE_UP, LEFT, ALT_CONTROL),
    (28, "m"): (MOUSE_UP, LEFT, ALT_CONTROL_SHIFT),

    ( 1, "m"): (MOUSE_UP, MIDDLE, NO_MODS),
    ( 5, "m"): (MOUSE_UP, MIDDLE, SHIFT),
    ( 9, "m"): (MOUSE_UP, MIDDLE, ALT),
    (13, "m"): (MOUSE_UP, MIDDLE, ALT_SHIFT),
    (17, "m"): (MOUSE_UP, MIDDLE, CONTROL),
    (21, "m"): (MOUSE_UP, MIDDLE, CONTROL_SHIFT),
    (25, "m"): (MOUSE_UP, MIDDLE, ALT_CONTROL),
    (29, "m"): (MOUSE_UP, MIDDLE, ALT_CONTROL_SHIFT),

    ( 2, "m"): (MOUSE_UP, RIGHT, NO_MODS),
    ( 6, "m"): (MOUSE_UP, RIGHT, SHIFT),
    (10, "m"): (MOUSE_UP, RIGHT, ALT),
    (14, "m"): (MOUSE_UP, RIGHT, ALT_SHIFT),
    (18, "m"): (MOUSE_UP, RIGHT, CONTROL),
    (22, "m"): (MOUSE_UP, RIGHT, CONTROL_SHIFT),
    (26, "m"): (MOUSE_UP, RIGHT, ALT_CONTROL),
    (30, "m"): (MOUSE_UP, RIGHT, ALT_CONTROL_SHIFT),

    ( 0, "M"): (MOUSE_DOWN, LEFT, NO_MODS),
    ( 4, "M"): (MOUSE_DOWN, LEFT, SHIFT),
    ( 8, "M"): (MOUSE_DOWN, LEFT, ALT),
    (12, "M"): (MOUSE_DOWN, LEFT, ALT_SHIFT),
    (16, "M"): (MOUSE_DOWN, LEFT, CONTROL),
    (20, "M"): (MOUSE_DOWN, LEFT, CONTROL_SHIFT),
    (24, "M"): (MOUSE_DOWN, LEFT, ALT_CONTROL),
    (28, "M"): (MOUSE_DOWN, LEFT, ALT_CONTROL_SHIFT),

    ( 1, "M"): (MOUSE_DOWN, MIDDLE, NO_MODS),
    ( 5, "M"): (MOUSE_DOWN, MIDDLE, SHIFT),
    ( 9, "M"): (MOUSE_DOWN, MIDDLE, ALT),
    (13, "M"): (MOUSE_DOWN, MIDDLE, ALT_SHIFT),
    (17, "M"): (MOUSE_DOWN, MIDDLE, CONTROL),
    (21, "M"): (MOUSE_DOWN, MIDDLE, CONTROL_SHIFT),
    (25, "M"): (MOUSE_DOWN, MIDDLE, ALT_CONTROL),
    (29, "M"): (MOUSE_DOWN, MIDDLE, ALT_CONTROL_SHIFT),

    ( 2, "M"): (MOUSE_DOWN, RIGHT, NO_MODS),
    ( 6, "M"): (MOUSE_DOWN, RIGHT, SHIFT),
    (10, "M"): (MOUSE_DOWN, RIGHT, ALT),
    (14, "M"): (MOUSE_DOWN, RIGHT, ALT_SHIFT),
    (18, "M"): (MOUSE_DOWN, RIGHT, CONTROL),
    (22, "M"): (MOUSE_DOWN, RIGHT, CONTROL_SHIFT),
    (26, "M"): (MOUSE_DOWN, RIGHT, ALT_CONTROL),
    (30, "M"): (MOUSE_DOWN, RIGHT, ALT_CONTROL_SHIFT),

    (32, "M"): (MOUSE_MOVE, LEFT, NO_MODS),
    (36, "M"): (MOUSE_MOVE, LEFT, SHIFT),
    (40, "M"): (MOUSE_MOVE, LEFT, ALT),
    (44, "M"): (MOUSE_MOVE, LEFT, ALT_SHIFT),
    (48, "M"): (MOUSE_MOVE, LEFT, CONTROL),
    (52, "M"): (MOUSE_MOVE, LEFT, CONTROL_SHIFT),
    (56, "M"): (MOUSE_MOVE, LEFT, ALT_CONTROL),
    (60, "M"): (MOUSE_MOVE, LEFT, ALT_CONTROL_SHIFT),

    (33, "M"): (MOUSE_MOVE, MIDDLE, NO_MODS),
    (37, "M"): (MOUSE_MOVE, MIDDLE, SHIFT),
    (41, "M"): (MOUSE_MOVE, MIDDLE, ALT),
    (45, "M"): (MOUSE_MOVE, MIDDLE, ALT_SHIFT),
    (49, "M"): (MOUSE_MOVE, MIDDLE, CONTROL),
    (53, "M"): (MOUSE_MOVE, MIDDLE, CONTROL_SHIFT),
    (57, "M"): (MOUSE_MOVE, MIDDLE, ALT_CONTROL),
    (61, "M"): (MOUSE_MOVE, MIDDLE, ALT_CONTROL_SHIFT),

    (34, "M"): (MOUSE_MOVE, RIGHT, NO_MODS),
    (38, "M"): (MOUSE_MOVE, RIGHT, SHIFT),
    (42, "M"): (MOUSE_MOVE, RIGHT, ALT),
    (46, "M"): (MOUSE_MOVE, RIGHT, ALT_SHIFT),
    (50, "M"): (MOUSE_MOVE, RIGHT, CONTROL),
    (54, "M"): (MOUSE_MOVE, RIGHT, CONTROL_SHIFT),
    (58, "M"): (MOUSE_MOVE, RIGHT, ALT_CONTROL),
    (62, "M"): (MOUSE_MOVE, RIGHT, ALT_CONTROL_SHIFT),

    (35, "M"): (MOUSE_MOVE, NO_BUTTON, NO_MODS),
    (39, "M"): (MOUSE_MOVE, NO_BUTTON, SHIFT),
    (43, "M"): (MOUSE_MOVE, NO_BUTTON, ALT),
    (47, "M"): (MOUSE_MOVE, NO_BUTTON, ALT_SHIFT),
    (51, "M"): (MOUSE_MOVE, NO_BUTTON, CONTROL),
    (55, "M"): (MOUSE_MOVE, NO_BUTTON, CONTROL_SHIFT),
    (59, "M"): (MOUSE_MOVE, NO_BUTTON, ALT_CONTROL),
    (63, "M"): (MOUSE_MOVE, NO_BUTTON, ALT_CONTROL_SHIFT),

    # This is duplicated from the block above with lowercase "m" for WSL.
    (35, "m"): (MOUSE_MOVE, NO_BUTTON, NO_MODS),
    (39, "m"): (MOUSE_MOVE, NO_BUTTON, SHIFT),
    (43, "m"): (MOUSE_MOVE, NO_BUTTON, ALT),
    (47, "m"): (MOUSE_MOVE, NO_BUTTON, ALT_SHIFT),
    (51, "m"): (MOUSE_MOVE, NO_BUTTON, CONTROL),
    (55, "m"): (MOUSE_MOVE, NO_BUTTON, CONTROL_SHIFT),
    (59, "m"): (MOUSE_MOVE, NO_BUTTON, ALT_CONTROL),
    (63, "m"): (MOUSE_MOVE, NO_BUTTON, ALT_CONTROL_SHIFT),

    (64, "M"): (SCROLL_UP, NO_BUTTON, NO_MODS),
    (68, "M"): (SCROLL_UP, NO_BUTTON, SHIFT),
    (72, "M"): (SCROLL_UP, NO_BUTTON, ALT),
    (76, "M"): (SCROLL_UP, NO_BUTTON, ALT_SHIFT),
    (80, "M"): (SCROLL_UP, NO_BUTTON, CONTROL),
    (84, "M"): (SCROLL_UP, NO_BUTTON, CONTROL_SHIFT),
    (88, "M"): (SCROLL_UP, NO_BUTTON, ALT_CONTROL),
    (92, "M"): (SCROLL_UP, NO_BUTTON, ALT_CONTROL_SHIFT),

    (65, "M"): (SCROLL_DOWN, NO_BUTTON, NO_MODS),
    (69, "M"): (SCROLL_DOWN, NO_BUTTON, SHIFT),
    (73, "M"): (SCROLL_DOWN, NO_BUTTON, ALT),
    (77, "M"): (SCROLL_DOWN, NO_BUTTON, ALT_SHIFT),
    (81, "M"): (SCROLL_DOWN, NO_BUTTON, CONTROL),
    (85, "M"): (SCROLL_DOWN, NO_BUTTON, CONTROL_SHIFT),
    (89, "M"): (SCROLL_DOWN, NO_BUTTON, ALT_CONTROL),
    (93, "M"): (SCROLL_DOWN, NO_BUTTON, ALT_CONTROL_SHIFT),
}

TYPICAL = {
    32: (MOUSE_DOWN, LEFT, NO_MODS),
    33: (MOUSE_DOWN, MIDDLE, NO_MODS),
    34: (MOUSE_DOWN, RIGHT, NO_MODS),
    35: (MOUSE_UP, UNKNOWN_BUTTON, NO_MODS),

    64: (MOUSE_MOVE, LEFT, NO_MODS),
    65: (MOUSE_MOVE, MIDDLE, NO_MODS),
    66: (MOUSE_MOVE, RIGHT, NO_MODS),
    67: (MOUSE_MOVE, NO_BUTTON, NO_MODS),

    96: (SCROLL_UP, NO_BUTTON, NO_MODS),
    97: (SCROLL_DOWN, NO_BUTTON, NO_MODS),
}
