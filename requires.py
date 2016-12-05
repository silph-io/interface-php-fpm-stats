
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class RequiresPHPRPMStats(RelationBase):
    scope = scopes.UNIT

    auto_accessors = ['ping_url', 'status_url', 'ping_reply']

    @hook('{requires:php-fpm-stats}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        if conv.get_remote('status_url'):
            conv.set_state('{relation_name}.available')

    @hook('{requires:php-fpm-stats}-relation-{departed,broken}')
    def broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

    def configuration(self):
        conv = self.conversation()
        return {k: conv.get_remote(k) for k in self.auto_accessors}
