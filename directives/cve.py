from . import Directive


class Cve(Directive):
    regex = r'\[\[!cve\s+(?P<cve>(CVE-)?\d{4}-\d+)\]\]'

    def newvalue(self, matchobj):
        cve = matchobj.group('cve')
        return '{{{{< cve {} >}}}}'.format(cve)
