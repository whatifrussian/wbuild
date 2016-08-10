## About

The tool for grabbing Russian translation of [What If?](http://what-if.xkcd.com) articles from [Notabenoid](http://notabenoid.org).

## Usage

```
$ ./wbuild.py [options] cookies.txt
```

A cookies file should be in Netscape compatible format. By default the script will print only last top rated translation of each fragment. Add `--all` option to print a list of articles, original fragments and all translations of each fragment.

A script `--all` output can be diff'ed with files produced by [What If? grabbing tool](https://github.com/whatifrussian/what_if_parse).

## License

The code, documentation and other repository content are in public domain.
