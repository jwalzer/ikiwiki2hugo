from . import Directive


class Mozbug(Directive):
    regex = r'\[\[!mozbug\s+(?P<id>\d{1,8}?)\s*(desc="(?P<description>.(?s)+?)")?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'id': self.cleanvalue(matchobj.group('id')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return '{{{{< mozbug {} >}}}}'.format(self.concatargumentdict(namedarguments))
