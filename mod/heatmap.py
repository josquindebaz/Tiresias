""" Prospéro month distribution to heatmap svg
Author Josquin Debaz
GPL 3
"""
import re


def quartiles(values):
    """return quartiles of a series"""
    values = sorted(values)
    size = len(values)
    if size % 2:
        first = values[(size // 4)]
        median = values[(size // 2)]
        third = values[(size * 3 // 4)]
    else:
        first = (values[size // 4] + values[(size // 4) + 1]) / 2
        median = (values[size // 2] + values[(size // 2) + 1]) / 2
        third = (values[size * 3 // 4] + values[(size * 3 // 4) + 1]) / 2
    return first, median, third


def parse_data(data):
    values = {}
    months = {"janvier": 1,
              "février": 2,
              "mars": 3,
              "avril": 4,
              "mai": 5,
              "juin": 6,
              "juillet": 7,
              "août": 8,
              "septembre": 9,
              "octobre": 10,
              "novembre": 11,
              "décembre": 12}

    for line in data.split("\n"):
        if not re.search("sans date", line) and not re.match(r"^\s*$", line):
            row = line.split('\t')
            _date = row[0].split("/")
            year = int(_date[1])
            if year in values:
                values[year][months[_date[0]]] = int(row[1])
            else:
                values[year] = {months[_date[0]]: int(row[1])}
    return values


def create_svg(values):
    month_index = {1: "j",
                   2: "f",
                   3: "m",
                   4: "a",
                   5: "m",
                   6: "j",
                   7: "j",
                   8: "a",
                   9: "s",
                   10: "o",
                   11: "n",
                   12: "d"}

    text_num = []
    for year, months in values.items():
        for month, texts in months.items():
            text_num.append(texts)
    max_value = max(text_num)
    min_value = min(text_num)
    first_q, median, third_q = quartiles(text_num)

    step = 50
    svg_width = step * (max(values) - min(values)) + 250
    if svg_width > 1000:
        step = (1000 - 200) / (max(values) - min(values))
        if step < 20:
            step = 20
        svg_width = step * (max(values) - min(values)) + 200

    svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="%s">
<style>
    .norm { font:14px sans-serif; }
    .small { font:12px sans-serif; }
    .vert { font:14px sans-serif; writing-mode: tb; }
    .rect { stroke:gray; stroke-width:1; fill:blue; }
</style>
""" % svg_width

    for month in range(12, 0, -1):
        svg += '<text x="%s" y="%s" ' % (step - 15, 645 - month * 50)
        svg += 'class="norm">%s</text>\n' % (month_index[month])

    y = 0
    year_sums = {}
    for year in range(min(values), max(values) + 1):
        y += step
        year_sum = 0
        for month in range(12, 0, -1):
            if month in values[year]:
                year_sum += values[year][month]
                svg += ' <rect width="%s" height="50" ' % step
                svg += 'x="%d" y="%d" class="rect" ' % (y, 620 - month * 50)
                svg += 'style="fill-opacity:%s">' % (values[year][month] / float(max_value))
                svg += '<title>%s/%s: %s</title>' % (month,
                                                     year,
                                                     values[year][month])
                svg += '</rect>\n'
                year_sum += values[year][month]
        svg += '<text x="%s" y="%s" ' % (y + step / 2, 630)
        svg += 'class="vert">%s</text>\n' % year
        year_sums[year] = year_sum

    x = 0
    max_year_value = max(year_sums.values())
    for year in range(min(values), max(values) + 1):
        x += step
        y_value = 100 * year_sums[year] / float(max_year_value)
        svg += '   <rect width="%d" height="%s" ' % (step, y_value)
        svg += 'x="%d" y="%d" class="rect">' % (x, 670)
        svg += '<title>%s: %d</title>' % (year, year_sums[year])
        svg += '</rect>\n   <text x="%s" y="%s" ' % (x, y_value + 685)
        svg += 'class="small">%s</text>\n' % year_sums[year]

    legend_list = [[min_value, min_value / max_value]]
    if third_q < int(max_value / 4) and third_q != 0:
        legend_list.extend([["Q3:%s" % third_q, third_q / max_value],
                            [int(max_value / 2), 0.5],
                            [int(3 * max_value / 4), 0.75]])
    else:
        if median <= int(max_value / 4) and median != 0:
            legend_list.append(["Q2:%s" % median, median / max_value])
        else:
            legend_list.append([int(max_value / 4), 0.25])
        legend_list.extend([[int(max_value / 2), 0.5],
                            [int(3 * max_value / 4), 0.75]])
    legend_list.append([max_value, max_value])

    svg += write_svg_legend(legend_list, y, step)

    ##    svg += '\n <text x="%s" y="380" font-family="sans-serif" \
    ##font-size="14">Q1:%s</text>\n' %(y+60, first_q)
    ##    svg += '\n <text x="%s" y="400" font-family="sans-serif" \
    ##font-size="14">Q2:%s</text>\n' %(y+60, median)
    ##    svg += '\n <text x="%s" y="420" font-family="sans-serif" \
    ##font-size="14">Q3:%s</text>\n' %(y+60, third_q)

    svg += "\n</svg>"

    return svg


def write_svg_legend(legend_list, y, step):
    result = ""
    for index, legend in enumerate(legend_list):
        result += '<rect width="%s" height="50" ' % step
        result += 'x="%s" y="%s" ' % (y + step + 10, 300 - 50 * index)
        result += 'class="rect" style="'
        result += 'fill-opacity:%s"></rect>' % (legend[1])
        result += '\n <text x="%s" y="%s" ' % (y + 2 * step + 15, 330 - 50 * index)
        result += 'class="norm">%s</text>\n' % (legend[0])

    return result
