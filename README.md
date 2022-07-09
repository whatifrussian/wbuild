## About

The tool for grabbing Russian translation of [What If?][1] articles from
[Notabenoid][2].

[1]: http://what-if.xkcd.com
[2]: http://notabenoid.org

## Usage

Get a cookies file in the Netscape compatible format. Use an addon for your Web
browser to extract the cookies file. You can use the `extract_cookies.sh`
script from this repository for Firefox.

Run the script:

```
$ ./wbuild.py [options] cookies.txt
```

By default the script will print only last top rated translation of each
fragment. Add `--all` option to print a list of articles, original fragments
and all translations of each fragment.

A script `--all` output can be diff'ed with files produced by [What If?
grabbing tool](https://github.com/whatifrussian/what_if_parse).

## License

The code, documentation and other repository content are in public domain.
