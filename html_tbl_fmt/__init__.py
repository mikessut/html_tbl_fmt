"""
htf = HTMLTableFormatter(html_snippet)
htf.odd_even_columns()
htf.add_column_conditional(condition, css_cls)

<style>

    .odd_col_cls {
        background-color: #ddd;
    }
    .even_col_cls {
        background-color: #ccc;
    }
</style>
"""
import lxml.html


class HTMLTableFormatter:

    def __init__(self, html_fragment: str):
        self._dom = lxml.html.fragment_fromstring(html_fragment)

    def odd_even_columns(self, odd_cls='odd_col_cls', even_cls='even_col_cls'):
        """
        Do this by adding (if necessary) <colgroup> to begining of table
        """
        colgrp = self._dom.find('.//colgroup')
        if colgrp is None:
            table = self._dom if self._dom.tag == 'table' else self._dom.find('.//table')
            colgrp = lxml.html.Element('colgroup')
            table.insert(0, colgrp)

        for n in range(len(self._dom.find('.//thead').findall('.//th'))):
            if n % 2 == 0:
                # even
                colgrp.append(lxml.html.Element('col', **{'class': even_cls}))
            else:
                colgrp.append(lxml.html.Element('col', **{'class': odd_cls}))

    def add_column_conditional(self, condition: 'ConditionColVal', css_cls: str):
        row_num = 0
        for tr in self._dom.find('.//tbody').iter('tr'):
            col_num = 0
            for td in tr.iter('td'):
                val = td.text
                if condition._col._col == col_num and condition.eval(float(val)):
                    td.classes.add(css_cls)
                col_num += 1
            row_num += 1
    
    def tostring(self):
        return lxml.html.tostring(self._dom)


class ConditionColVal:
    
    def __init__(self, col, val, op):
        self._col = col
        self._val = val
        self._op = op

    def eval(self, val: float):
        return getattr(val, self._op)(self._val)


class TableCol:

    def __init__(self, col):
        self._col = col

    def __gt__(self, other) -> ConditionColVal:
        return ConditionColVal(self, other, '__gt__')

