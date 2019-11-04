from . import Directive


class Tails_ticket_2(Directive):
    regex = r'\[\[!tails_ticket\s+(?P<id>[#\d\w-]+)\s*(desc="?(?P<description>[^"]+)"?)?\s?\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'id': self.cleanvalue(matchobj.group('id')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return "{{< tails_ticket {} >}}".format(self.concatargumentdict(namedarguments))

