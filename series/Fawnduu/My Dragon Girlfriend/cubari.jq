. as $tweets |
{
  "1": "1",
  "65": "2",
  "177": "3",
  "485": "4",
} as $chapterVolume |
[foreach $tweets[] as $tweet ({cubariVolume: "0", cubariChapter: "0"};
  ($tweet | if has("photos") then .tweet = (.tweet | sub(" https?:\\/\\/t.co\\/[A-Za-z0-9]+$"; ""; "ms")) else . end) as $tweet |
  ($tweet | .tweet = (.tweet | sub(
    "(?:\\s*behind\\?)?(?:\\s*(?:catch up(?: (?:with|on) the comic)?|check it out)(?::|(?: here| o[nr] (?:webtoons?|tapas))+[:.!]?)|(?:(?:\\s*(?:webtoons?|tapas):)?\\s*(?:\\(links? in pinned tweet\\)|https:\\/\\/t\\.co\\/(?:YbOBcsMB3H|YbOBcsuZF7|PDmmL4ixY6|jxEW0zB01t|XZVhG99JjP|7lDupa8nrh|BvO9MnecX3|Q8cVgszhsG|NF6bjBl9Ox|NF6bjBCKG5))))"
  ; ""; "gmsi"))) as $tweet |
  ($tweet.tweet | first(capture(
    "^.*?(?:p(?:age|g)\\.?\\s*0*(?<chapterP>\\d+(?:\\.\\d+)?)\\.?|(?:^|\\s+)0*(?<chapter>\\d+(?:\\.\\d+)?)[.\\n])\\s*(?<title>.*?)$"
  ; "msi"), {})) as $tweetCaptures |
  {cubariVolume: .cubariVolume, cubariChapter: .cubariChapter} + $tweet | . + {
    "tweet": ($tweetCaptures.tweet? // .tweet),
    "cubariChapter": ($tweetCaptures.chapterP? // $tweetCaptures.chapter? // (.cubariChapter | sub("(?:\\.(?<subchapter>\\d+))?$"; ".\((.subchapter // 0 | tonumber) + 1)"))),
    "cubariTitle": $tweetCaptures.title?,
  } | $chapterVolume[.cubariChapter]? as $volume | if $volume != null then . + {
    "cubariVolume": $volume,
  } else . end;
  .
)] as $tweets |
{
  "$schema": "../../../schema/cubari/gistSource.schema.json",
  "title": "My Dragon Girlfriend",
  "description": "A heartwarming story about two girls falling in love, but one of them is a dragon!?",
  "artist": "Fawnduu",
  "author": "Fawnduu",
  "cover": "https://d30womf5coomej.cloudfront.net/sa/bb/5fca3154-c673-4c79-a5c4-d48c768a21c6_z.jpg",
  "chapters": [$tweets[] | if has("photos") then
    {key: .cubariChapter, value: {
      "title": (.cubariTitle // .tweet),
      "volume": .cubariVolume,
      "groups": {
        "Twitter: @Fawnduu": (.photos | map(
          sub(
            "(?<base>https:\\/\\/pbs.twimg.com\\/media\\/[A-Za-z0-9_-]+)(?:\\.(?<format>[a-z]+))?";
            "\(.base)?format=\(.format? // "jpg")&name=orig"
          ; "ms")
        ))
      },
      "last_updated": (.created_at | sub("(?<date>\\S+) (?<time>\\S+) UTC"; "\(.date)T\(.time)Z"; "") | "\(fromdateiso8601)"),
    }}
  else empty end] | from_entries
}
