# Custom pagination class
# Taken from http://flask.pocoo.org/snippets/44/

from math import ceil


class Pagination(object):

    obj_items = None

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.obj_per_page = per_page
        self.total_count = total_count

    @property
    def items(self):
        start = 0 if self.page <= 1 else (self.prev_num * self.per_page)
        stop = self.total_count if not self.has_next else self.page * self.per_page

        if start > self.total_count:
            return []

        r = self.obj_items[start:stop]

        return r

    @property
    def per_page(self):
        return self.obj_per_page

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def next_num(self):
        p = self.page + 1
        return p if p <= self.pages else self.page

    @property
    def prev_num(self):
        p = self.page - 1
        return p if p >= 1 else self.page

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages
