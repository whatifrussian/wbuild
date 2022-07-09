#!/bin/bash

set -eu -o pipefail

# Based on https://gist.github.com/hackerb9/d382e09683a52dcac492ebcdaf1b79af

# Firefox locks its sqlite file, let's copy it.
cp ~/.mozilla/firefox/*/cookies.sqlite ./cookies.sqlite

echo "# Netscape HTTP Cookie File" > cookies.txt
sqlite3 -separator $'\t' cookies.sqlite >> cookies.txt <<- EOF
	.mode tabs
	.header off
	select host,
	case substr(host,1,1)='.' when 0 then 'FALSE' else 'TRUE' end,
	path,
	case isSecure when 0 then 'FALSE' else 'TRUE' end,
	expiry,
	name,
	value
	from moz_cookies
	where host like "%notabenoid.org%";
EOF

rm cookies.sqlite
