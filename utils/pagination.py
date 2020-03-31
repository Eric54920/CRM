from django.utils.safestring import mark_safe


class Pagination:

    def __init__(self, page, data_count, per_num=10, max_show=11):
        try:
            page = int(page)
            if page <= 0:
                page = 1
        except Exception:
            page = 1

        #  1  0   10
        #  2  10  20
        self.start = (page - 1) * per_num
        self.end = page * per_num
        # 总数据量
        # data_count = len(users)
        # 总页码数
        sum_page_num, more = divmod(data_count, per_num)
        if more:
            sum_page_num += 1
        # 最多显示的页码数
        # max_show = 11
        half_show = max_show // 2

        if sum_page_num <= max_show:
            page_start = 1
            page_end = sum_page_num
        else:
            if page - half_show <= 0:
                page_start = 1
                page_end = max_show
            elif page + half_show > sum_page_num:
                page_end = sum_page_num
                page_start = page_end - max_show + 1

            else:
                # 页码的起始值
                page_start = page - half_show
                # 页码的终止值
                page_end = page + half_show

        page_html_list = []

        if page == 1:

            page_html_list.append(
                '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            page_html_list.append(
                '<li><a href="?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    page - 1))

        for i in range(page_start, page_end + 1):
            if i == page:
                page_html_list.append('<li class="active"><a href="?page={}">{}</a></li>'.format(i, i))
            else:
                page_html_list.append('<li><a href="?page={}">{}</a></li>'.format(i, i))
        if page == sum_page_num:

            page_html_list.append(
                '<li class="disabled"><a aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            page_html_list.append(
                '<li><a href="?page={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    page + 1))

        self.page_html = ''.join(page_html_list)


class Pagination:

    def __init__(self, page, data_count, params, per_num=10, max_show=11):
        try:
            page = int(page)
            if page <= 0:
                page = 1
        except Exception:
            page = 1
        self.page = page
        self.per_num = per_num
        self.data_count = data_count
        self.max_show = max_show
        self.params = params

        #  1  0   10
        #  2  10  20

    @property
    def start(self):
        return (self.page - 1) * self.per_num

    @property
    def end(self):
        return self.page * self.per_num

    @property
    def page_html(self):

        # 总页码数
        sum_page_num, more = divmod(self.data_count, self.per_num)
        if more:
            sum_page_num += 1
        # 最多显示的页码数
        # max_show = 11
        half_show = self.max_show // 2

        if sum_page_num <= self.max_show:
            page_start = 1
            page_end = sum_page_num
        else:
            if self.page - half_show <= 0:
                page_start = 1
                page_end = self.max_show
            elif self.page + half_show > sum_page_num:
                page_end = sum_page_num
                page_start = page_end - self.max_show + 1

            else:
                # 页码的起始值
                page_start = self.page - half_show
                # 页码的终止值
                page_end = self.page + half_show

        page_html_list = []

        if self.page == 1:

            page_html_list.append(
                '<li class="disabled"><a aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            self.params['page']=self.page - 1
            page_html_list.append(
                '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.params.urlencode()))

        for i in range(page_start, page_end + 1):
            self.params['page'] = i
            if i == self.page:
                page_html_list.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                page_html_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
        if self.page == sum_page_num:

            page_html_list.append(
                '<li class="disabled"><a aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            self.params['page'] = self.page + 1
            page_html_list.append(
                '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.params.urlencode()))

        return mark_safe(''.join(page_html_list))
