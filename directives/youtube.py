from . import Directive


class Youtube(Directive):
    regex = r'\[\[!template\s+id=youtube\s+v="(?P<vid>.+?)"\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'vid': self.cleanvalue(matchobj.group('vid')),
        }
        return '{{{{< youtube {} >}}}}'.format(self.concatargumentdict(namedarguments))
