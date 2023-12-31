""" Prospéro month distribution to heatmap svg
Author Josquin Debaz
GPL 3
"""

from mod.HeatmapDataProcessor import HeatmapDataProcessor
from mod.HeatmapSvgWriter import HeatmapSvgWriter


def create_svg(monthly_values):
    data_processor = HeatmapDataProcessor(monthly_values)
    svg_writer = HeatmapSvgWriter(step=50, data=data_processor)

    return svg_writer.produce_svg()


