from wcwidth import wcswidth

__all__ = "CanvasView",


class CanvasView:
    """
    A wrapper around a `numpy` `ndarray` with a convenient `add_text` method.

    Notes
    -----
    One-dimensional views will have an extra axis pre-pended to make them two-dimensional.
    E.g., rows and columns with shape (m,) will be re-shaped to (1, m) so that
    the `add_text` `row` and `column` parameters make sense.
    """
    __slots__ = "canvas",

    def __init__(self, canvas):
        if canvas.ndim == 1:
            canvas = canvas[None]

        self.canvas = canvas

    def __getattr__(self, attr):
        return getattr(self.canvas, attr)

    def __getitem__(self, key):
        return type(self)(self.canvas[key])

    def __setitem__(self, key, value):
        self.canvas[key] = value

    def add_text(self, text, row=0, column=0):
        """
        Add text to the canvas.

        Parameters
        ----------
        text: str
            Text to add to canvas.
        row: int | tuple[int, ...] | slice
            Row or rows to which text is added. This will be passed as-is as the first argument
            to `numpy`'s `ndarray.__getitem__`.
        column: int
            The first column to which text is added.

        Notes
        -----
        Text is meant to be a single line of text. Text is not wrapped if it is too long, instead
        index error is raised.
        """
        canvas = self.canvas
        columns = canvas.shape[1]

        if column < 0:
            column += columns

        i = 0
        for letter in text:
            if column + i >= columns:
                break

            match wcswidth(letter):
                case 0:
                    continue
                case 1:
                    canvas[row, column + i] = letter
                    i += 1
                case 2:
                    canvas[row, column + i] = letter
                    if column + i + 1 < columns:
                        canvas[row, column + i + 1] = chr(0x200B)  # Zero-width space
                    i += 2