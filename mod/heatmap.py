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


def create_svg(monthly_values):
    data_processor = MonthlyData(monthly_values)

    step = 50
    svg_width = compute_svg_width(step, data_processor)

    svg = write_svg_header(svg_width)
    svg += write_y_axis_legend(step)
    svg += write_svg_map(step, data_processor)
    svg += write_svg_barplot(step, data_processor)
    legend_list = create_legend_list(data_processor)
    svg += write_svg_legend(legend_list, step, data_processor)
    svg += "\n</svg>"

    return svg


class MonthlyData:
    def __init__(self, data):
        self.data = data
        self.only_values = self.init_only_values()
        self.quartile1, self.quartile2, self.quartile3 = quartiles(self.only_values)
        self.year_sums = sum_year_values(self.get_year_range(), self.data)

    def get_all_data(self):
        return self.data

    def init_only_values(self):
        return [item for items in
                [month.values() for month in self.data.values()]
                for item in items]

    def get_only_values(self):
        return self.only_values

    def get_quartile1(self):
        return self.quartile1

    def get_quartile2(self):
        return self.quartile2

    def get_quartile3(self):
        return self.quartile3

    def get_year_sums(self):
        return self.year_sums

    def get_max_monthly_values(self):
        return max(self.only_values)

    def get_min_monthly_values(self):
        return min(self.only_values)

    def get_year_range(self):
        return range(self.get_min_year(), self.get_max_year() + 1)

    def get_min_year(self):
        return min(self.data)

    def get_max_year(self):
        return max(self.data)


def write_y_axis_legend(step):
    x_coordinate = step - 15
    reversed_month_index = "dnosajjmamfj"

    months = [f'<text x="{x_coordinate}" y="{645 - (12 - index) * 50}" class="norm">{month_initial}</text>\n'
              for index, month_initial in enumerate(reversed_month_index)]

    return "".join(months)


def write_svg_header(svg_width):
    return """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="%s">
<style>
    .norm { font:14px sans-serif; }
    .small { font:12px sans-serif; }
    .vert { font:14px sans-serif; writing-mode: tb; }
    .rect { stroke:gray; stroke-width:1; fill:blue; }
</style>
""" % svg_width


def write_svg_legend(legend_list, step, data):
    y = len(data.get_year_range()) * step
    rect_x_coordinate = y + step + 10
    text_x_coordinate = y + 2 * step + 15

    legends = [f'<rect width="{step}" height="50" '
               f'x="{rect_x_coordinate}" y="{300 - 50 * index}" '
               f'class="rect" style="fill-opacity:{legend_item[1]}"></rect>\n'
               f' <text x="{text_x_coordinate}" y="{330 - 50 * index}" class="norm">{legend_item[0]}</text>\n'
               for index, legend_item in enumerate(legend_list)]

    #    svg += '\n <text x="%s" y="380" font-family="sans-serif" \
    # font-size="14">Q1:%s</text>\n' %(y+60, first_q)
    #    svg += '\n <text x="%s" y="400" font-family="sans-serif" \
    # font-size="14">Q2:%s</text>\n' %(y+60, median)
    #    svg += '\n <text x="%s" y="420" font-family="sans-serif" \
    # font-size="14">Q3:%s</text>\n' %(y+60, third_q)

    return "".join(legends)


def create_legend_list(data):
    legend_list = [[data.get_min_monthly_values(), data.get_min_monthly_values() / data.get_max_monthly_values()]]
    if data.get_quartile3() < int(data.get_max_monthly_values() / 4) and data.get_quartile3() != 0:
        legend_list.extend([["Q3:%s" % data.get_quartile3(), data.get_quartile3() / data.get_max_monthly_values()],
                            [int(data.get_max_monthly_values() / 2), 0.5],
                            [int(3 * data.get_max_monthly_values() / 4), 0.75]])
    else:
        if data.get_quartile2() <= int(data.get_max_monthly_values() / 4) and data.get_quartile2() != 0:
            legend_list.append(["Q2:%s" % data.get_quartile2(), data.get_quartile2() / data.get_max_monthly_values()])
        else:
            legend_list.append([int(data.get_max_monthly_values() / 4), 0.25])
        legend_list.extend([[int(data.get_max_monthly_values() / 2), 0.5],
                            [int(3 * data.get_max_monthly_values() / 4), 0.75]])
    legend_list.append([data.get_max_monthly_values(), data.get_max_monthly_values()])

    return legend_list


def compute_svg_width(step, data):
    svg_width = step * (data.get_max_year() - data.get_min_year()) + 250

    if svg_width < 1000:
        return svg_width

    step = (1000 - 200) / (data.get_max_year() - data.get_min_year())
    if step < 20:
        step = 20

    return int(step * (data.get_max_year() - data.get_min_year()) + 200)


def write_svg_barplot(step, data):
    result = ""
    max_year_value = max(data.year_sums.values())

    x = 0
    for year in data.get_year_range():
        x += step

        year_sum = data.year_sums[year]
        y_value = 100 * year_sum / float(max_year_value)

        result += f'   <rect width="{step}" height="{y_value}" x="{x}" y="670" class="rect">' \
                  f'<title>{year}: {year_sum}</title></rect>\n' \
                  f'   <text x="{x}" y="{y_value + 685}" class="small">{year_sum}</text>\n'

    return result


def sum_year_values(year_range, values):
    year_sums = {}

    for year in year_range:
        year_sum = 0
        for month in range(12, 0, -1):
            if month in values[year]:
                year_sum += values[year][month]
        year_sums[year] = year_sum

    return year_sums


def write_svg_map(step, data):
    result = ""
    y = 0
    for year in data.get_year_range():
        y += step
        for month in range(12, 0, -1):
            if month in data.get_all_data()[year]:
                result += (f' <rect width="{step}" height="50" '
                           f'x="{y}" y="{620 - month * 50}" class="rect" '
                           f'style="fill-opacity:{data.get_all_data()[year][month] / float(data.get_max_monthly_values())}">'
                           f'<title>{month}/{year}: {data.get_all_data()[year][month]}</title></rect>\n')
        result += f'<text x="{y + step / 2}" y="630" class="vert">{year}</text>\n'

    return result
