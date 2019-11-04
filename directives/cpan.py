from . import Directive


class Cpan(Directive):
    regex = r'\[\[!cpan\s+(?P<searchterm>[^]]+?)\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'searchterm': self.cleanvalue(matchobj.group('searchterm')),
        }
        return '{{{{< cpan {} >}}}}'.format(self.concatargumentdict(namedarguments))
