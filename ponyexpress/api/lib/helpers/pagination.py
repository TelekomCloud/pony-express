# Custom pagination class
# Taken from http://flask.pocoo.org/snippets/44/

from math import ceil


class Pagination(object):

    items = None

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.obj_per_page = per_page
        self.total_count = total_count

    #@property
    #def items(self):
    #    return self.items

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

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (self.page - left_current - 1 < num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
