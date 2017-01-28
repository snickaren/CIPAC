#!/bin/bash
# Example usage of knormalize.pl

if [ "$1" == "" ] || [ ! -f "$1" ]; then
	echo "Usage: $0 <filename>"
	exit;
fi

HISTFILE=`mktemp`
echo "working on $1.clean1.tif"
convert $1.clean1.tif -depth 8 -format "%c" histogram:info:- > $HISTFILE

KNORM=`cat $HISTFILE|./knormalize.pl`
BLACK=${KNORM%,*}
WHITE=${KNORM#*,}

convert -strip -level ${BLACK}%,${WHITE}% $1.clean1.tif $1.normalized.tif
