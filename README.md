## About

The tool for grabbing Russian translation of [What If?][1] articles from
[Notabenoid][2].

[1]: http://what-if.xkcd.com
[2]: http://notabenoid.org

## Usage

Get a cookies file in the Netscape compatible format. I’m using the [Cookies
Manager+][3] addon for Firefox (and replace `%2F` in the PATH field with `/`,
see [here][4]).

Run the script:

```
$ ./wbuild.py [options] cookies.txt
```

By default the script will print only last top rated translation of each
fragment. Add `--all` option to print a list of articles, original fragments
and all translations of each fragment.

A script `--all` output can be diff'ed with files produced by [What If?
grabbing tool](https://github.com/whatifrussian/what_if_parse).

[3]: https://addons.mozilla.org/en-US/firefox/addon/cookies-manager-plus/
[4]: https://github.com/vanowm/FirefoxCookiesManagerPlus/issues/124

## License

The code, documentation and other repository content are in public domain.
