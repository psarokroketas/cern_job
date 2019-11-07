import utmpaccess
import utmp
from UTMPCONST import *
import time
from netaddr import *
import collectd

PLUGIN_NAME = 'session'

collectd.debug('session : Loading Python Plugin' +PLUGIN_NAME)

Domains= None

def config_func(config):
        global domains
        domains = []
        for node in config.children:
          key = node.key

          if key == 'Domains':
             domains.extend(node.values)

        collectd.debug('Domains is: %s' % ', '.join(domains) )

def read_func():
         total=0
         domain_counter = {}
         for d in domains:
           domain_counter[d] = 0
         records = utmp.UtmpRecord()
         for rec in records:
                 if rec.ut_type == USER_PROCESS:
                         (rec.ut_user, rec.ut_line, rec.ut_pid,
                         rec.ut_host, time.ctime(rec.ut_tv[0]))
                         host=rec.ut_host
                         for d in domains:
                            collectd.debug("HERE: %s %s" % (host,d))
                            if d in host and host.endswith(d)==True :
                              collectd.debug('Matches')
                              domain_counter[d] = domain_counter[d] + 1
                         total = total + 1
         records.endutent()
         datapoint = collectd.Values(plugin='sessions',)
         datapoint.type = 'count'
         datapoint.type_instance = 'total_sessions'
         datapoint.values = [total]
         collectd.debug('Dispatching a value of %s for total sessions' % total)
         datapoint.dispatch()

         for d in domains:
           datapoint = collectd.Values(plugin='sessions',)
           datapoint.type = 'count'
           datapoint.type_instance = d
           datapoint.values = [domain_counter[d]]
           collectd.debug('Dispatching a value of %s for domain sessions %s' % (domain_counter[d], d))
           datapoint.dispatch()

collectd.register_config(config_func)
collectd.register_read(read_func)

