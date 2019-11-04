from . import Directive


class Rfc(Directive):
    regex = r'\[\[!rfc\s+(?P<number>\d{1,6}?)\s*(desc="(?P<description>.(?s)+?)")?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'number': self.cleanvalue(matchobj.group('number')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return '{{{{< rfc {} >}}}}'.format(self.concatargumentdict(namedarguments))
