
from cStringIO import StringIO
from greplin import scales
from greplin.scales import formats, graphite, meter
import webob.dec
import re


class ApplicationStats(object):
    status_ok = scales.SumAggregationStat('status_ok')
    status_failed = scales.SumAggregationStat('status_failed')
    status_forbidden = scales.SumAggregationStat('status_forbidden')
    status_not_found = scales.SumAggregationStat('status_not_found')
    status_not_modified = scales.SumAggregationStat('status_not_modified')
    status_redirect = scales.SumAggregationStat('status_redirect')
    requests = scales.SumAggregationStat('requests')
    latency = scales.SumAggregationStat('latency')

    _statuses = {
         200: 'status_ok',
         201: 'status_ok',
         302: 'status_redirect',
         304: 'status_not_modified',
         401: 'status_forbidden',
         403: 'status_forbidden',
         404: 'status_not_found',
         500: 'status_failed',
         }

    def __init__(self, name='application'):
        scales._Stats.init(self, '/' + name)

    def statuses(self, code):
        return getattr(self, self._statuses.get(code, 'status_failed'))


class Stats(ApplicationStats):
    status_ok = meter.MeterStat('status_ok')
    status_failed = meter.MeterStat('status_failed')
    status_forbidden = meter.MeterStat('status_forbidden')
    status_not_found = meter.MeterStat('status_not_found')
    status_not_modified = meter.MeterStat('status_not_modified')
    status_redirect = meter.MeterStat('status_redirect')
    requests = meter.MeterStat('requests')
    latency = scales.PmfStat('latency')

    def __init__(self, parent, name, regexp=None):
        scales._Stats.initChild(self, name, '', parent=parent)
        if regexp is not None:
            self.pattern = re.compile(regexp)


class ScalesMiddleware(object):

    def __init__(self, app, name, signature='++stats++', stats=[]):
        self.app = app
        self.signature = '/' + signature
        parent = ApplicationStats(name)
        self.default = Stats(parent, 'default', )
        self.stats = []
        for key, value in stats:
            self.stats.append(Stats(parent, key, value))

    def find(self, path):
        for sub in self.stats:
            if sub.pattern.match(path):
                return sub
        return self.default

    @webob.dec.wsgify
    def __call__(self, request):
        if request.path_info.startswith(self.signature):
            query = request.GET.get('query')
            output = StringIO()
            formats.htmlHeader(output, self.signature, request.host_url, query)
            formats.htmlFormat(output, query=query)
            return output.getvalue()
        scale = self.find(request.path_info)
        scale.requests.mark()
        with scale.latency.time():
            response = request.get_response(self.app)
        result = scale.statuses(response.status_int)
        if result is not None:
            result.mark()
        return response


def make_middleware(app, global_config, **config):
    if 'graphite_server' in config:
        hostname, port = config['graphite_server'].split(':', 1)
        try:
            port = int(port)
        except:
            raise RuntimeError("Invalid graphite port")
        prefix = config.get('graphite_prefix')
        graphite.GraphitePeriodicPusher(hostname, port, prefix).start()
    stats = []
    for key, value in config.items():
        if key.startswith('scales_'):
            stats.append((key[7:], value))
    return ScalesMiddleware(
        app,
        name=config.get('name', 'application'),
        signature=config.get('publisher_signature', '++stats++'),
        stats=stats)
