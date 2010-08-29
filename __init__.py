"""Convenience functions to render html tables into python data structures.

Uses the lxml.html module for processing of raw html text.
"""

from lxml import html as _html

def first_or_none(it):
    return next(iter(it), None)

def parse_table(table,
                rows_xpath='tbody/tr',
                cells_xpath='td | th',
                cell_content_xpath='text()',
                content_select=first_or_none,
                cells_select=list,
                rows_select=list):
    """Parses `table` assuming that each cell is 1 row wide.

        `rows_xpath` finds rows relative to the table root.

        `cells_xpath` finds cells relative to each row.
        
        `cell_content_xpath` is the relative xpath
        from each table cell to the desired content.

        `content_select` will be applied to each cell found by `cell_content_xpath`.
        By default this is the first cell or None if no cells matched.

        `cells_select` will be applied to the iterator of each parsed row.

        `rows_select` is applied to the top-level iterator.
        To have this function return an iterator, pass `rows_select=iter`.

        The `_select` functions can be used to introduce filters,
          or to have `parse_table` return iterators rather than lists.

        Returns a list of lists or whatever the combination of
        `cells_select` and `rows_select` results in.
    """
    rows = table.xpath(rows_xpath)

    def cells(row):
        return row.xpath(cells_xpath)

    def content(cell):
        return content_select(cell.xpath(cell_content_xpath))

    def process_row(row):
        return cells_select(content(cell) for cell in cells(row))

    processed_rows = (process_row(row) for row in rows)

    return rows_select(processed_rows)

def parse_text(text, *args, **kwargs):
    """Parses the first table in the supplied html text.
    
        Returns None if no table is found.

        Additional parameters are passed on to `parse_table`.
    """
    tree = _html.fromstring(text)
    try:
        table = tree.xpath('//table')[0]
        return parse_table(table, *args, **kwargs)
    except IndexError:
        return None
