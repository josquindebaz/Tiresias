class HeatmapDataProcessor:
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