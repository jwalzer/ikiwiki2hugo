from . import Directive


class Debsa(Directive):
    regex = r'\[\[!debsa(?P<year>\d{4}) (?P<advisoryid>\d{2,5})\]\]'

    def newvalue(self, matchobj):
        year = matchobj.group('year')
        advisoryid = matchobj.group('advisoryid')
        return '{{{{< debsa {} {} >}}}}'.format(year, advisoryid)

