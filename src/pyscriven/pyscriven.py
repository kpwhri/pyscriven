import imghdr
import math
import os
from io import BytesIO
import matplotlib.pyplot as plt
import pytablewriter
from pyscriven.utils import make_safe_title, generate_random_string


class Table:

    def __init__(self, header=None, data=None, footnotes=None, title=None):
        self.header = header
        self.data = data or []
        # self.types = types or ['mix'] * len(self.data)
        self.title = title
        self.footnotes = footnotes or []

    def add_row(self, row):
        self.data.append(row)

    def add_header(self, header):
        self.header = header

    def add_footnote(self, text):
        self.footnotes.append(text)


class Image:

    def __init__(self, image: BytesIO, fmt, title='', caption='', name=None):
        self._image = image
        self.title = title
        self.caption = caption
        self.fmt = fmt
        if name:
            self.name = name
        else:
            if self.title:
                self.name = make_safe_title(title) + '_' + generate_random_string(size=4)
            else:
                self.name = generate_random_string(size=10)

    @property
    def filename(self):
        return self.name + '.' + self.fmt

    @property
    def image(self):
        self._image.seek(0)
        return self._image.read()

    @classmethod
    def from_matplotlib(cls, figure=None, fmt='png', **kwargs):
        imgdata = BytesIO()
        if not figure:
            figure = plt  # assume figure is in progress
        figure.savefig(imgdata, format=fmt)
        return cls(imgdata, fmt=fmt, **kwargs)

    @classmethod
    def from_path(cls, fp, **kwargs):
        with open(fp, 'rb') as fh:
            return cls(BytesIO(fh.read()), fmt=imghdr.what(fp), **kwargs)


class RestWriter:
    HEADINGS = {
        1: '=',
        2: '-',
        3: '\'',
        4: '.',
        5: '*',
        6: '+',
        7: '^',
    }

    def __init__(self, fp, mode='w'):
        self.fp = fp
        self.parent = os.path.dirname(os.path.abspath(self.fp))
        os.makedirs(self.parent, exist_ok=True)
        self._current_heading = 0
        self.mode = mode
        self.lines = []

    @staticmethod
    def _get_tablewriter():
        return pytablewriter.RstGridTableWriter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.fp, self.mode) as out:
            out.write('\n'.join(self.lines + ['']))

    def _next_heading(self, level):
        if level <= self._current_heading + 1:  # can choose any more important level
            self._current_heading = level
        else:  # invalid request (headings need to be in correct order)
            self._current_heading += 1
        return self.HEADINGS[min(self._current_heading, len(self.HEADINGS))]

    def add_lines(self, lines, sep=True):
        if sep:
            self.lines.append('')
        self.lines += lines

    def write_all(self, data):
        buffer = []
        prev = None
        has_subtitle = False
        for i, (label, item, *kwargs) in enumerate(data):
            if kwargs:
                kwargs = kwargs[0]  # get dict
            else:
                kwargs = {}

            if i == 0:
                if label == 'title':
                    self.write_title(item, **kwargs)
                    continue
                else:
                    self.write_title('Document Title', **kwargs)
                    if label == 'subtitle':
                        self.write_title(item, level=2)
                        continue
                    else:
                        self.write_title('Subtitle', level=2)
                    has_subtitle = True
            elif i == 1 and not has_subtitle:
                if label == 'subtitle':
                    self.write_title(item, level=2)
                    continue
                else:
                    self.write_title('Subtitle', level=2)

            if prev and prev != label:
                if prev == 'sentence':
                    self.write_sentences_to_paragraph(buffer)
                    prev = None
                    buffer = []
            if label == 'heading':
                self.write_header(item, **kwargs)
            elif label == 'transition':
                self.write_transition(**kwargs)
            elif label == 'paragraph':
                self.write_paragraph(item, **kwargs)
            elif label == 'sentence':
                buffer.append(item)
                prev = 'sentence'
            elif label == 'table':
                self.write_table(item)
            elif label == 'image':
                self.write_image(item)
        if prev:
            if prev == 'sentence':
                self.write_sentences_to_paragraph(buffer)

    def write_title(self, title, level=1):
        separator = self.HEADINGS[level] * len(title)
        self.add_lines([separator, title, separator])

    def write_header(self, header, level=1):
        separator = self._next_heading(level) * len(header)
        self.add_lines([header, separator])

    def write_transition(self, length=8, symbol='-'):
        self.add_lines([symbol * length])

    def write_paragraph(self, text, **kwargs):
        self.add_lines([text])

    def write_sentences_to_paragraph(self, sentences):
        self.add_lines(sentences)

    def write_image(self, image: Image):
        path = os.path.join(self.parent, image.filename)
        with open(path, 'wb') as out:
            out.write(image.image)
        lines = []
        if image.title or image.caption:
            lines.append('.. figure:: {}'.format(path))
            lines.append('    :align: center')
            if image.title:
                lines.append('')
                lines.append(image.title)
            else:
                lines.append('')
                lines.append(image.caption)
        else:
            lines.append('.. image::')
            lines.append('    :align: center')
        self.add_lines(lines)

    def write_table(self, table: Table):
        tw = self._get_tablewriter()
        tw.table_name = table.title
        tw.header_list = table.header
        tw.value_matrix = table.data
        lines = tw.dumps().strip().split('\n')
        line_sep = lines[-1]
        max_line = len(line_sep) - 5
        prev = 0
        pre = tw.char_left_side_row + ' - '
        pre_cont = tw.char_left_side_row + '    '
        post = tw.char_right_side_row
        for footnote in table.footnotes:
            for i in range(math.ceil(len(footnote) / max_line)):
                if i == 0:
                    line = pre + footnote[prev: i * max_line]
                else:
                    line = pre_cont + footnote[prev: i * max_line]
                prev = i * max_line
                line = line.ljust(len(line_sep) - 1) + post
                lines.append(line)
        self.add_lines(lines)
