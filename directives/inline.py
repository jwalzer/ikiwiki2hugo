from . import Directive


class Inline(Directive):
    regex = r'\[\[!inline\spages="(?P<path>[\w/_.-]+?)"(\s*raw="?yes"?|\s*sort="?age"?)+\]\]'

    def newvalue(self, matchobj):
        return '{{{{< inline path="{}.md" >}}}}'.format(matchobj.group('path'))
