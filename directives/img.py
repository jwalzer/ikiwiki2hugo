from . import Directive


class Img(Directive):
    regex = r'\[\[!img\s*"?(?P<src>\S+?)"?\s*(align="?(?P<alignment>.(?s)*?)"?\s*|size="?(?P<size>.(?s)*?)"?\s*|link="?(?P<link>.(?s)*?)"?\s*|class="?(?P<class>.(?s)*?)"?\s*|alt="(?P<alt>.(?s)*?)"\s*|caption="?(?P<caption>.(?s)*?)"?\s*)*\]\]'

    def newvalue(self, matchobj):
        namedarguments = {
            'src': self.cleanvalue(matchobj.group('src')),
            'alt': self.cleanvalue(matchobj.group('alt')),
            'caption': self.cleanvalue(matchobj.group('caption')),
            'class': self.cleanvalue(matchobj.group('class')),
            'link': self.cleanvalue(matchobj.group('link'))
        }
        if namedarguments['link'] == 'no':
            namedarguments['link'] = None
        # The upstream shipped 'img' shortcode does not have size and aligment
        # options. Its probably better to set these options using css anyway.
        # see also: https://github.com/spf13/spf13.com/blob/master/layouts/shortcodes/img.html
        return '{{{{< img {} >}}}}'.format(self.concatargumentdict(namedarguments))

