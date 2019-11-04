from . import Directive


class Tails_roadmap(Directive):
    regex = r'\[\[!tails_roadmap\s*(desc="(?P<description>.(?s)+?)")?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< tails_roadmap {} >}}}}'.format(self.concatargumentdict(namedarguments))
