import math


class Pagination:
    def __init__(self, page, total_rows, per_size=10, max_per=9):
        try:
            page = int(page)
        except Exception:
            page = 1

        total_pages = math.ceil(total_rows / per_size)

        if page <= 0:
            page = 1
        elif page > total_pages:
            page = total_pages

        self.total_pages = total_pages
        self.page = page
        self.total_rows = total_rows
        self.per_size = per_size
        self.max_per = max_per

    @property
    def start(self):
        return (self.page - 1) * self.per_size

    @property
    def end(self):
        if self.total_rows >= self.per_size:
            return self.page * self.per_size
        else:
            return self.total_rows

    def pagination(self):

        left_start = self.page - int(self.max_per / 2)
        right_end = self.page + int(self.max_per / 2) + 1
        if self.total_pages < self.max_per:
            left_start = 1
            right_end = self.total_pages + 1
        else:
            if left_start <= 0:
                left_start = 1
                right_end = left_start + self.max_per
            elif right_end >= self.total_pages:
                right_end = self.total_pages + 1
                left_start = right_end - self.max_per

        pagination = []
        if self.page == 1:
            pagination.append(
                '<li class="page-item disabled"><a class="page-link" href="?page={}">Previous</a></li>'
                .format(self.page - 1))
        else:
            pagination.append(
                '<li class="page-item"><a class="page-link" href="?page={}">Previous</a></li>'
                .format(self.page - 1))

        for i in range(left_start, right_end):
            if self.page == i:
                pagination.append(
                    '<li class="page-item active"><a class="page-link" href="?page={}">{}</a></li>'
                    .format(i, i))
            else:
                pagination.append(
                    '<li class="page-item"><a class="page-link" href="?page={}">{}</a></li>'
                    .format(i, i))
        if self.page == self.total_pages:
            pagination.append(
                '<li class="page-item disabled"><a class="page-link" href="?page={}">Next</a></li>'
                .format(self.page + 1))
        else:
            pagination.append(
                '<li class="page-item"><a class="page-link" href="?page={}">Next</a></li>'
                .format(self.page + 1))

        return ''.join(pagination)
