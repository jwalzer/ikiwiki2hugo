from . import Directive


class Toc(Directive):
    regex = r'\[\[!toc(\s*startlevel=(?P<startlevel>\d)|\s*levels="?(?P<level>\d)"?)*\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'level': self.cleanvalue(matchobj.group('level')),
            'startlevel': self.cleanvalue(matchobj.group('startlevel'))
        }
        return '{{{{< toc {} >}}}}'.format(self.concatargumentdict(namedarguments))
