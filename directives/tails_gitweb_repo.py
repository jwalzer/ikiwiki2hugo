from . import Directive


class Tails_gitweb_repo(Directive):
    regex = r'\[\[!tails_gitweb_repo\s+(?P<repository>.(?s)+?)\s*(desc="(?P<description>.(?s)+?)")?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'repository': self.cleanvalue(matchobj.group('repository')),
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< tails_gitweb_repo {} >}}}}'.format(self.concatargumentdict(namedarguments))
