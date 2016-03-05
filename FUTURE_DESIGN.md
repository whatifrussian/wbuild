wbuild.py subcommand [options]

## TODO's

There are original articles, translated articles in progress (on Notabenoid),
translated articles on our website. So terms like 'build' and 'upload' don't
self-explanatory.

## Subcommands

`wbuild.py upgrade`

Update the script itself (git pull).
Send admin notification if some error occured a first time.
Exit code is success if new version is available, fail otherwise (1).

`wbuild.py regen`

Regenerate all found articles.
Send an admin notification about the differences.
Exit code is success if all right, fail otherwise (1).

`wbuild.py acheck`

Check for new article.
Don't send any notification about new article.
Send an admin notification if some error occured a first time.
Exit code is success if new article found, fail otherwise (1)
or when error occured (2, 3, etc).

`wbuild.py dcheck`

Check for differences in all found articles.
Send admin notification about the differences.
Send admin notification if some error occured a first time.
Exit code is success if the differences found, fail otherwise (1)
or when error occured (2, 3, etc).

`wbuild.py build`

Build a last article.
Send an admin notification with built article.
Send admin notification if some error occured a first time.
Exit code is success if all right, fail otherwise (2, 3, etc).

`wbuild.py upload`

TODO: upload to Notabenoid.

`wbuild.py draft`

TODO: Grab a last article from Notabenoid and build draft on separate website
for convenient reading. To be invoked from cron.

## Options

-d dir
Working tree with *.html, *.md, last_article, last_error, lock files.
Default is 'wbuild_stuff' directory in a current directory.

-s
Don't send any notifications, just dump it to a current directory.
For debugging purposes.

## Notes

The script blocks when another wbuild.py instance run on the same working tree.

## Process sketch

The process split to the two cron task.

```
# Build new article if any
DIR="..."
wbuild.py upgrade -d "${DIR}"
wbuild.py regen -d "${DIR}"
if wbuild.py acheck -d "${DIR}"; then
    wbuild.py build -d "${DIR}"
    # wbuild.py upload -d "${DIR}"
fi
```

```
# Notify about article changes if any
DIR="..."
wbuild.py dcheck -d "${DIR}"
```
