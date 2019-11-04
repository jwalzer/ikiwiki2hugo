from . import Directive


class Debpts(Directive):
    regex = r'\[\[!debpts\s+(?P<package>[\w.(?s)-]+?)\s*(desc="(?P<description>.(?s)+?)")?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'package': self.cleanvalue(matchobj.group('package')),
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< debpts {} >}}}}'.format(self.concatargumentdict(namedarguments))
