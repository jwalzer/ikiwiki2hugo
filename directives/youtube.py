from . import Directive


class Youtube(Directive):
    regex = r'\[\[!template\s+id=youtube\s+v="(?P<id>.+?)"\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'id': self.cleanvalue(matchobj.group('id')),
        }
        return '{{{{< youtube {} >}}}}'.format(self.concatargumentdict(namedarguments))
