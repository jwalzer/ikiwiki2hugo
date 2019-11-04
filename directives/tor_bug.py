from . import Directive


class Tor_bug(Directive):
    regex = r'\[\[!tor_bug\s+(?P<id>\d{2,5}?)\s*(desc="?(?P<description>.(?s)+?)"?)?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'id': self.cleanvalue(matchobj.group('id')),
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< tor_bug {} >}}}}'.format(self.concatargumentdict(namedarguments))
