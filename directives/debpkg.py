from . import Directive


class Debpkg(Directive):
    regex = r'\[\[!debpkg\s+(?P<package>[\w.-]+?)\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'package': self.cleanvalue(matchobj.group('package')),
        }
        return '{{{{< debpkg {} >}}}}'.format(self.concatargumentdict(namedarguments))
