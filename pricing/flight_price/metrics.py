import re


class Metrics:
    def __init__(self, metric):
        self.metric = metric

    def construct_metrics(self):
        metrics = {}
        metrics['price'] = self.metric['price']['total']
        metrics['id'] = self.metric['id']
        metrics['min'] = self.metric['priceMetrics'][0]['amount']
        metrics['first'] = self.metric['priceMetrics'][1]['amount']
        metrics['median'] = self.metric['priceMetrics'][2]['amount']
        metrics['third'] = self.metric['priceMetrics'][3]['amount']
        metrics['max'] = self.metric['priceMetrics'][4]['amount']