import re


class HeatmapDataProcessor:
    def __init__(self, data):
        self.data = data
        self.only_values = self.init_only_values()
        self.quartile1, self.quartile2, self.quartile3 = quartiles(self.only_values)
        self.year_sums = sum_year_values(self.get_year_range, self.data)

    @property
    def get_all_data(self):
        return self.data

    def init_only_values(self):
        return [item for items in
                [month.values() for month in self.data.values()]
                for item in items]

    @property
    def get_only_values(self):
        return self.only_values

    @property
    def get_quartile1(self):
        return self.quartile1

    @property
    def get_quartile2(self):
        return self.quartile2

    @property
    def get_quartile3(self):
        return self.quartile3

    @property
    def get_year_sums(self):
        return self.year_sums

    @property
    def get_max_monthly_values(self):
        return max(self.only_values)

    @property
    def get_min_monthly_values(self):
        return min(self.only_values)

    @property
    def get_year_range(self):
        return range(self.get_min_year, self.get_max_year + 1)

    @property
    def get_min_year(self):
        return min(self.data)

    @property
    def get_max_year(self):
        return max(self.data)


def sum_year_values(year_range, values):
    year_sums = {}

    for year in year_range:
        year_sum = 0
        for month in range(12, 0, -1):
            if month in values[year]:
                year_sum += values[year][month]
        year_sums[year] = year_sum

    return year_sums


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
        if re.search("sans date", line) or re.match(r"^\s*$", line):
            continue

        row = line.split('\t')
        _date = row[0].split("/")
        year = int(_date[1])
        if year in values:
            values[year][months[_date[0]]] = int(row[1])
        else:
            values[year] = {months[_date[0]]: int(row[1])}
    return values
