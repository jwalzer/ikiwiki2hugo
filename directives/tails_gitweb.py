from . import Directive


class Tails_gitweb(Directive):
    regex = r'\[\[!tails_gitweb\s+(?P<path>[^"]+?)[ \n]?(desc="(?P<title>.(?s)+?)")?\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'path': self.cleanvalue(matchobj.group('path')),
            'title': self.cleanvalue(matchobj.group('title')),
        }
        return '{{{{< tails_gitweb {} >}}}}'.format(self.concatargumentdict(namedarguments))
