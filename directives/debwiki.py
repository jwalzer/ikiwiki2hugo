from . import Directive


class Debwiki(Directive):
    regex = r'\[\[!debwiki\s+(?P<page>[\w_/-]+?)\s*(desc="?(?P<description>.(?s)+?)"?)?\s*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'page': self.cleanvalue(matchobj.group('page')),
            'description': self.cleanvalue(matchobj.group('description'))
        }
        return '{{{{< debwiki {} >}}}}'.format(self.concatargumentdict(namedarguments))

