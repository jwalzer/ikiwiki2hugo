from . import Directive


class Tails_ticket_1(Directive):
    regex = r'\[\[!tails_ticket\s+desc="(?P<description>[^"\]]+)"\s*(?P<id>[#\d\w-]+)\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'id': self.cleanvalue(matchobj.group('id')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return "{{< tails_ticket {} >}}".format(self.concatargumentdict(namedarguments))

