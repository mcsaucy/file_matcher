#!/bin/bash

WANT='{
    "./testdata/a/1": {
        "individual_size": 7,
        "matches": [
            "./testdata/b/1"
        ]
    }
}'


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"
HAVE=$(
	INCLUDE_SMOL=yes_because_testdata \
	"./glom.py" "./testdata/a" "./testdata/b")

if [[ "$HAVE" != "$WANT" ]]; then
	{
		echo "Test failed!"
		echo
		echo HAVE:
		echo "$HAVE"
		echo
		echo
		echo WANT:
		echo "$WANT"
		diff <(echo "$HAVE") <(echo "$WANT")
	} >&2
	exit 1
else
	echo "Test passed. :)"
fi
