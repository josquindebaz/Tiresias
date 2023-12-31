class HeatmapSvgWriter:
    def __init__(self, data, step=50):
        self.step = step
        self.data = data
        self.color = "blue"

    def produce_svg(self):
        svg = self.write_svg_header()
        svg += self.write_y_axis_legend()
        svg += self.write_svg_map()
        svg += self.write_svg_barplot()
        svg += self.write_svg_legend()
        svg += "\n</svg>"

        return svg

    def write_svg_header(self):
        svg_width = compute_svg_width(self.step, self.data)
        return (f"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
                f"<svg version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\" width=\"{svg_width}\">\n"
                f"<style>\n"
                f"    .norm {{ font:14px sans-serif; }}\n"
                f"    .small {{ font:12px sans-serif; }}\n"
                f"    .vert {{ font:14px sans-serif; writing-mode: tb; }}\n"
                f"    .rect {{ stroke:gray; stroke-width:1; fill:{self.color}; }}\n"
                f"</style>\n")

    def write_y_axis_legend(self):
        x_coordinate = self.step - 15
        reversed_month_index = "dnosajjmamfj"

        months = [f'<text x="{x_coordinate}" y="{645 - (12 - index) * 50}" class="norm">{month_initial}</text>\n'
                  for index, month_initial in enumerate(reversed_month_index)]

        return "".join(months)

    def write_svg_map(self):
        result = ""

        all_data = self.data.get_all_data
        y = 0
        for year in self.data.get_year_range:
            y += self.step

            for month in [month for month in range(12, 0, -1) if month in all_data[year]]:
                result += self.write_svg_month_map(y, month, all_data, year)

            result += f'<text x="{y + self.step / 2}" y="630" class="vert">{year}</text>\n'

        return result

    def write_svg_month_map(self, y, month, all_data, year):
        return (f' <rect width="{self.step}" height="50" '
                f'x="{y}" y="{620 - month * 50}" class="rect" '
                f'style="fill-opacity:{all_data[year][month] / float(self.data.get_max_monthly_values)}">'
                f'<title>{month}/{year}: {all_data[year][month]}</title></rect>\n')

    def write_svg_barplot(self):
        result = ""
        max_year_value = max(self.data.year_sums.values())

        x = 0
        for year in self.data.get_year_range:
            x += self.step

            year_sum = self.data.year_sums[year]
            y_value = 100 * year_sum / float(max_year_value)

            result += f'   <rect width="{self.step}" height="{y_value}" x="{x}" y="670" class="rect">' \
                      f'<title>{year}: {year_sum}</title></rect>\n' \
                      f'   <text x="{x}" y="{y_value + 685}" class="small">{year_sum}</text>\n'

        return result

    def write_svg_legend(self):
        legend_list = self.create_legend_list()
        y = len(self.data.get_year_range) * self.step
        rect_x_coordinate = y + self.step + 10
        text_x_coordinate = y + 2 * self.step + 15

        legends = [f'<rect width="{self.step}" height="50" '
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

    def create_legend_list(self):
        minimum_value = self.data.get_min_monthly_values
        q2 = self.data.get_quartile2
        q3 = self.data.get_quartile3
        maximum_value = self.data.get_max_monthly_values

        legend_list = [[minimum_value, minimum_value / maximum_value]]
        if q3 < int(maximum_value / 4) and q3 != 0:
            legend_list.extend([["Q3:%s" % q3, q3 / maximum_value],
                                [int(maximum_value / 2), 0.5],
                                [int(3 * maximum_value / 4), 0.75]])
        else:
            if q2 <= int(maximum_value / 4) and q2 != 0:
                legend_list.append(["Q2:%s" % q2, q2 / maximum_value])
            else:
                legend_list.append([int(maximum_value / 4), 0.25])
            legend_list.extend([[int(maximum_value / 2), 0.5], [int(3 * maximum_value / 4), 0.75]])
        legend_list.append([maximum_value, maximum_value])

        return legend_list


def compute_svg_width(step, data):
    svg_width = step * (data.get_max_year - data.get_min_year) + 250

    if svg_width < 1000:
        return svg_width

    step = (1000 - 200) / (data.get_max_year - data.get_min_year)
    if step < 20:
        step = 20

    return int(step * (data.get_max_year - data.get_min_year) + 200)
