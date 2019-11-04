from . import Directive


class Wikipedia1(Directive):
    regex = r'\[\[!wikipedia(_(?P<lang>\w{2}))?\s+desc="(?P<description>.(?s)+?)"\s*(?P<title>.(?s)+?)\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'title': self.cleanvalue(matchobj.group('title')),
            'lang': self.cleanvalue(matchobj.group('lang')),
            'description': self.cleanvalue(matchobj.group('description')),
        }
        return '{{{{< wikipedia {} >}}}}'.format(self.concatargumentdict(namedarguments))
