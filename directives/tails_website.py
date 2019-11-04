from . import Directive


class Tails_website(Directive):
    regex = r'\[\[!tails_website\s+(?P<path>.(?s)+?)\s*(desc="(?P<description>.(?s)+?)")?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'path': self.cleanvalue(matchobj.group('path')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return '{{{{< tails_website {} >}}}}'.format(self.concatargumentdict(namedarguments))
