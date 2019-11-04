from . import Directive


class Ubupkg(Directive):
    regex = r'\[\[!ubupkg\s+(?P<name>[^]]*)\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'name': self.cleanvalue(matchobj.group('name')),
        }
        return '{{{{< ubupkg {} >}}}}'.format(self.concatargumentdict(namedarguments))
