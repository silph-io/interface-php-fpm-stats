from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class ProvidesPHPFPMStats(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:php-fpm-stats}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:php-fpm-stats}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.connected')

    def configure(self, port, status_url, ping_url, ping_reply='pong'):
        address = hookenv.unit_get('private-address')
        url = 'http://{}:{}/{}'
        relation_info = {
            'status_url': url.format(address, port, status_url),
            'ping_url': url.format(address, port, ping_url),
            'ping_reply': ping_reply,
        }

        self.set_remote(**relation_info)
        self.set_state('{relation_name}.configured')
