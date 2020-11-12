import re


class Metrics:
    def __init__(self, metric):
        self.metric = metric

    def construct_metrics(self):
        try:
            metrics = {'min': self.metric[0]['priceMetrics'][0]['amount'],
                       'first': self.metric[0]['priceMetrics'][1]['amount'],
                       'median': self.metric[0]['priceMetrics'][2]['amount'],
                       'third': self.metric[0]['priceMetrics'][3]['amount'],
                       'max': self.metric[0]['priceMetrics'][4]['amount']}
        except (IndexError, TypeError, AttributeError, KeyError):
            return None
        return metrics
