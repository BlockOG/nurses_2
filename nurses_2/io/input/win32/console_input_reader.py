from ctypes.wintypes import DWORD, HANDLE
from ctypes import pointer, windll

from ....data_structures import Point
from ...win32_types import (
    INPUT_RECORD,
    KEY_EVENT_RECORD,
    MOUSE_EVENT_RECORD,
    STD_INPUT_HANDLE,
    EventTypes,
)
from ..keys import Key
from ..event_data_structures import MouseEvent, PasteEvent
from ..mouse_data_structures import *
from .key_maps import *

RIGHT_ALT_PRESSED = 0x0001
LEFT_ALT_PRESSED = 0x0002
RIGHT_CTRL_PRESSED = 0x0004
LEFT_CTRL_PRESSED = 0x0008
SHIFT_PRESSED = 0x0010

FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001
RIGHTMOST_BUTTON_PRESSED =  0x0002

MOUSE_MOVED = 0x0001
MOUSE_WHEELED = 0x0004

MAX_BYTES = 2048


class ConsoleInputReader:
    def __init__(self, recognize_paste=True):
        self.recognize_paste = recognize_paste
        self.handle = HANDLE(windll.kernel32.GetStdHandle(STD_INPUT_HANDLE))

    def read(self):
        """
        Yield input events.

        http://msdn.microsoft.com/en-us/library/windows/desktop/ms684961(v=vs.85).aspx
        """
        arrtype = INPUT_RECORD * MAX_BYTES
        input_records = arrtype()

        windll.kernel32.ReadConsoleInputW(
            self.handle, pointer(input_records), MAX_BYTES, pointer(DWORD(0))
        )

        keys, mouse_events = self._get_keys(input_records)

        # Correct non-bmp characters that are passed as separate surrogate codes
        keys = tuple(self._merge_paired_surrogates(keys))

        if self.recognize_paste and self._is_paste(keys):
            key_iter = iter(keys)

            for key in key_iter:
                paste_text = [ ]

                while key and (not isinstance(key, Key) or key is Key.ControlJ):
                    paste_text.append("\n" if key is Key.ControlJ else key)
                    key = next(gen, False)

                if paste_text:
                    yield PasteEvent("".join(paste_text))

                if key:
                    yield key
        else:
            yield from keys

        yield from mouse_events

    def _get_keys(self, input_records):
        """
        Fill keys and mouse_events with events from input_records.
        """
        keys = [ ]
        mouse_events = [ ]
        handle_key = self._handle_key
        handle_mouse = self._handle_mouse

        for ir in input_records:
            if attr := EventTypes.get(ir.EventType, False):
                ev = getattr(ir.Event, attr)

                if type(ev) is KEY_EVENT_RECORD and ev.KeyDown:
                    keys.extend(handle_key(ev))

                elif type(ev) is MOUSE_EVENT_RECORD:
                    mouse_events.append(handle_mouse(ev))

        return keys, mouse_events

    @staticmethod
    def _merge_paired_surrogates(keys):
        """
        Combines consecutive Key with high and low surrogates into
        single characters
        """
        buffered_high_surrogate = None

        for key in keys:
            is_text = not isinstance(key, Key)
            is_high_surrogate = is_text and "\uD800" <= key <= "\uDBFF"
            is_low_surrogate = is_text and "\uDC00" <= key <= "\uDFFF"

            if buffered_high_surrogate:
                if is_low_surrogate:
                    yield (
                        (buffered_high_surrogate + key)
                        .encode("utf-16-le", "surrogatepass")
                        .decode("utf-16-le")
                    )
                    buffered_high_surrogate = None
                else:
                    yield buffered_high_surrogate
                    buffered_high_surrogate = key

            elif is_high_surrogate:
                buffered_high_surrogate = key
            else:
                yield key

        if buffered_high_surrogate:
            yield buffered_high_surrogate

    @staticmethod
    def _is_paste(keys):
        """
        Return `True` when we should consider this list of keys as a paste
        event. Pasted text on windows will be turned into a
        `Key.BracketedPaste` event. (It's not 100% correct, but it is probably
        the best possible way to detect pasting of text and handle that
        correctly.)
        """
        # Consider paste when it contains at least one newline and at least one
        # other character.
        text_count = 0
        newline_count = 0

        for key in keys:
            if not isinstance(key, Key):
                text_count += 1
            elif key is Key.ControlM:
                newline_count += 1

        return newline_count >= 1 and text_count > 1

    @staticmethod
    def _handle_key(ev: KEY_EVENT_RECORD):
        """
        Yield a Key (or two: if left-alt is pressed, Key.Escape will be yielded before key) from a KEY_EVENT_RECORD.
        """
        control_key_state = ev.ControlKeyState
        u_char = ev.uChar.UnicodeChar

        key = (
            KEY_CODES.get(ev.VirtualKeyCode) if u_char == "\x00"
            else ANSI_SEQUENCES.get(u_char.encode("utf-8", "surrogatepass"), u_char)
        )

        if not key:
            return

        if (
            control_key_state & LEFT_CTRL_PRESSED
            or control_key_state & RIGHT_CTRL_PRESSED
        ):
            if key == " ":
                key = Key.ControlSpace

            elif key is Key.ControlJ:
                key = Key.Escape

            elif control_key_state & SHIFT_PRESSED:
                key = CONTROL_SHIFT_KEYS.get(key, key)

            else:
                key = CONTROL_KEYS.get(key, key)

        elif control_key_state & SHIFT_PRESSED:
            key = SHIFT_KEYS.get(key, key)

        if control_key_state & LEFT_ALT_PRESSED:
            yield Key.Escape

        yield key

    @staticmethod
    def _handle_mouse(ev):
        position = Point(ev.MousePosition.Y, ev.MousePosition.X)

        # Event type
        if ev.EventFlags & MOUSE_MOVED:
            event_type = MouseEventType.MOUSE_MOVE
        elif ev.EventFlags & MOUSE_WHEELED:
            if ev.ButtonState > 0:
                event_type = MouseEventType.SCROLL_UP
            else:
                event_type = MouseEventType.SCROLL_DOWN
        elif not ev.ButtonState:
            event_type = MouseEventType.MOUSE_UP
        else:
            event_type = MouseEventType.MOUSE_DOWN

        # Buttons
        if not ev.ButtonState:
            button = MouseButton.NO_BUTTON
        elif ev.ButtonState & FROM_LEFT_1ST_BUTTON_PRESSED:
            button = MouseButton.LEFT
        elif ev.ButtonState & RIGHTMOST_BUTTON_PRESSED:
            button = MouseButton.RIGHT
        # More buttons here:
        #     https://docs.microsoft.com/en-us/windows/console/mouse-event-record-str?redirectedfrom=MSDN
        # For now, just assume middle-mouse button.
        else:
            button = MouseButton.MIDDLE

        # Modifiers
        mods = 0
        if ev.ControlKeyState & LEFT_ALT_PRESSED or ev.ControlKeyState & RIGHT_ALT_PRESSED:
            mods |= MouseModifierKey.ALT
        if ev.ControlKeyState & LEFT_CTRL_PRESSED or ev.ControlKeyState & RIGHT_CTRL_PRESSED:
            mods |= MouseModifierKey.CONTROL
        if ev.ControlKeyState & SHIFT_PRESSED:
            mods |= MouseModifierKey.SHIFT

        modifier = MouseModifier(mods)

        return MouseEvent(position, event_type, button, modifier)