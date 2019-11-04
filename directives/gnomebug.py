from . import Directive


class Gnomebug(Directive):
    regex = r'\[\[!gnomebug\s+(?P<id>\d{1,6})\s*(desc="?(?P<description>.(?s)+?)"?)?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'id': self.cleanvalue(matchobj.group('id')),
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< gnomebug {} >}}}}'.format(self.concatargumentdict(namedarguments))
