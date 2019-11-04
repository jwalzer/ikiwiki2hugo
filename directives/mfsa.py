from . import Directive


class Mfsa(Directive):
    regex = r'\[\[!mfsa\s*(?P<id>\d{4}-\d{2,4})\s*(desc="(?P<description>.(?s)+?)")?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'description': self.cleanvalue(matchobj.group('description')),
            'id': self.cleanvalue(matchobj.group('id'))
        }
        return '{{{{< mfsa {} >}}}}'.format(self.concatargumentdict(namedarguments))
