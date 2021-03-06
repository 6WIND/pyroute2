from collections import OrderedDict
from pyroute2.ndb.objects import RTNL_Object
from pyroute2.netlink.rtnl.fibmsg import fibmsg


init = {'specs': [['rules', OrderedDict(fibmsg.sql_schema())]],
        'classes': [['rules', fibmsg]],
        'indices': [['rules', ('family',
                               'dst_len',
                               'src_len',
                               'tos',
                               'action',
                               'flags',
                               'FRA_DST',
                               'FRA_SRC',
                               'FRA_IIFNAME',
                               'FRA_GOTO',
                               'FRA_PRIORITY',
                               'FRA_FWMARK',
                               'FRA_FLOW',
                               'FRA_TUN_ID',
                               'FRA_SUPPRESS_IFGROUP',
                               'FRA_SUPPRESS_PREFIXLEN',
                               'FRA_TABLE',
                               'FRA_FWMASK',
                               'FRA_OIFNAME',
                               'FRA_L3MDEV',
                               'FRA_UID_RANGE',
                               'FRA_PROTOCOL',
                               'FRA_IP_PROTO',
                               'FRA_SPORT_RANGE',
                               'FRA_DPORT_RANGE')]],
        'foreign_keys': [],
        'event_map': {fibmsg: ['rules']}}


class Rule(RTNL_Object):

    table = 'rules'
    msg_class = fibmsg
    api = 'rule'
    _replace_on_key_change = True

    @classmethod
    def summary(cls, view):
        req = '''
              SELECT
                f_target, f_tflags, f_family,
                f_FRA_PRIORITY, f_action, f_FRA_TABLE
              FROM
                rules
              '''
        yield ('target', 'tflags', 'family', 'priority', 'action', 'table')
        for record in view.ndb.schema.fetch(req):
            yield record

    def __init__(self, *argv, **kwarg):
        kwarg['iclass'] = fibmsg
        self._fields = [x[0] for x in fibmsg.fields]
        self.event_map = {fibmsg: "load_rtnlmsg"}
        super(Rule, self).__init__(*argv, **kwarg)

    def load_sql(self, *argv, **kwarg):
        spec = super(Rule, self).load_sql(*argv, **kwarg)
        if spec is None:
            return
        nkey = OrderedDict()
        for name_norm, name_raw, value in zip(self.names, self.spec, spec):
            if name_raw in self.kspec:
                nkey[name_raw] = value
            if name_norm not in self._fields and value in (0, ''):
                dict.__setitem__(self, name_norm, None)
        self._key = nkey
        return spec
