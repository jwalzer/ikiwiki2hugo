ikiwiki2hugo
============

This script converts the content of an [ikiwiki](https://ikiwiki.info/)
installation to a content directory for a [hugo](https://gohugo.io/) content
directory.

It is heavily based on [anarcats ikiwiki2hugo
script](https://gitlab.com/anarcat/scripts/blob/master/ikiwiki2hugo.py) which
itself was inspired by
[https://blog.jak-linux.org/2018/10/25/migrated-website-from-ikiwiki-to-hugo/](https://blog.jak-linux.org/2018/10/25/migrated-website-from-ikiwiki-to-hugo/)
and [anarcats notes on the matter](https://anarc.at/services/wiki/ikiwiki-hugo-conversion/).

What does it do?
================

For every ikiwiki `*.mdwn` or `*.html` file, it creates a Markdown file with
[hugo frontmatter](https://gohugo.io/content-management/front-matter/). If
there is a \*.po file with the same name, the script creates a `*.XX.md` file
with the strings translated.

Then the content is converted:

The ikiwiki `[!meta` directives are being converted to [hugo
frontmatter](https://gohugo.io/content-management/front-matter/).  The content
of the Markdown files is a copy of the content of the ikiwiki files with the
ikiwiki directives replaced by [hugo
shortcodes](https://gohugo.io/content-management/shortcodes/).  There are a lot
of [directives](https://ikiwiki.info/ikiwiki/directive/) out there and I only
implemented replacements for some of them.  My test ikiwiki instance was the
the [Tails](https://tails.boum.org) ikiwiki source, so I only mostly
implemented directives used there.  Merge requests or patches for additional
directives are welcome- to add a replacement for a directive, look in the
`directives` folder, all the replacement python modules inherit from the
`Directive` class. The shortcode files are `assets/shortcodes` folder.

Usage:
`./ikiwiki2hugo <ikiwikidirectory> <hugocontentdirectory>`

The script wont overwrite an existing hugo content directory.

What it does *not* do?
======================

Probably the more important question ;)

There are a lot of directives whose replacements are not implemented. Most
important probably the `[[!inline` directive with multiple (and negative)
arguments and the `[[!map` directive.

Also, `hugo` is more strict regarding Markdown syntax. It does not convert
markdown syntax that is embedded in `<div>...</div>`.
