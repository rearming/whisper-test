#!/bin/zsh

#URL="https://www.youtube.com/watch?v=EzEuylNSn-Q&list=LL&index=21&t=153s&ab_channel=AIExplained"
#NAME=close-to-agi

URL="https://www.youtube.com/watch?v=LhVFnnJvwQk&list=LL&index=28&ab_channel=BusinessDisruptors"
NAME="AGI-is-already-exist"
PROMPT="--prompt "

#URL="https://www.youtube.com/watch?v=xLi83prR5fg&list=LL&index=18&ab_channel=LexClips"
#NAME="early-agi"

python3 yt2audio.py "$URL" --out yt_audio --name "$NAME"
python3 speech2text.py yt_audio/$NAME.mp3 --prompt "a podcast talk between two IT guys about closeness of AGI"

