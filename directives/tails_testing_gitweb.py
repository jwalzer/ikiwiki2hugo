from . import Directive


class Tails_testing_gitweb(Directive):
    regex = r'\[\[!tails_testing_gitweb\s+(?P<path>[^"]+?)[ \n]?(desc="(?P<description>.(?s)+?)")?\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'path': self.cleanvalue(matchobj.group('path')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return '{{{{< tails_testing_gitweb {} >}}}}'.format(self.concatargumentdict(namedarguments))
