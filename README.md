# catgirl-v's Cubari series

Enjoy!

## Series

+ [Fawnduu - My Dragon Girlfriend][Fawnduu/My Dragon Girlfriend]
  + [Cubari][Fawnduu/My Dragon Girlfriend/Cubari]
  + [gist source][Fawnduu/My Dragon Girlfriend/cubari.json]
+ [Ryan Keats - ADHDinos][ADHDinos]
  + [Cubari][ADHDinos/Cubari]
  + [gist source][ADHDinos/cubari.json]
+ [Xanthippe Hutcheon - Pandora's Tale][Pandora]
  + [Cubari][Pandora/Cubari]
  + [gist source][Pandora/cubari.json]

[Fawnduu/My Dragon Girlfriend]: https://www.webtoons.com/en/canvas/my-dragon-girlfriend/list?title_no=162918
[Fawnduu/My Dragon Girlfriend/Cubari]: https://cubari.moe/read/gist/cmF3L2NhdGdpcmwtdi9jdWJhcmkvZC9jYXRnaXJsLXYvbWFpbi9zZXJpZXMvRmF3bmR1dS9NeSUyMERyYWdvbiUyMEdpcmxmcmllbmQvY3ViYXJpLmpzb24/
[Fawnduu/My Dragon Girlfriend/cubari.json]: https://raw.githubusercontent.com/catgirl-v/cubari/d/catgirl-v/main/series/Fawnduu/My%20Dragon%20Girlfriend/cubari.json

[ADHDinos]: https://www.adhdinos.com/
[ADHDinos/Cubari]: https://cubari.moe/read/gist/cmF3L2NhdGdpcmwtdi9jdWJhcmkvZC9jYXRnaXJsLXYvbWFpbi9zZXJpZXMvUnlhbiUyMEtlYXRzL0FESERpbm9zL2N1YmFyaS5qc29u/
[ADHDinos/cubari.json]: https://raw.githubusercontent.com/catgirl-v/cubari/d/catgirl-v/main/series/Ryan%20Keats/ADHDinos/cubari.json

[Pandora]: https://pandorastale.com/
[Pandora/Cubari]: https://cubari.moe/read/gist/cmF3L2NhdGdpcmwtdi9jdWJhcmkvZC9jYXRnaXJsLXYvbWFpbi9zZXJpZXMvWGFudGhpcHBlJTIwSHV0Y2hlb24vUGFuZG9yYSdzJTIwVGFsZS9jdWJhcmkuanNvbg/
[Pandora/cubari.json]: https://raw.githubusercontent.com/catgirl-v/cubari/d/catgirl-v/main/series/Xanthippe%20Hutcheon/Pandora's%20Tale/cubari.json

## Initial import notes

```
twint --utc --full-text -u "Fawnduu" --since "2017-08-01 00:00:00" --json --hide-output -o "series/Fawnduu/tweets.jsonl" --count
jq -c "select(.conversation_id == \"914484965215227904\" or .conversation_id == \"914854813694693378\" or .conversation_id == \"915276793766170626\") | del((.language | select(. == \"en\")), .date, .time, .timezone, (.[] | select(. == \"\" or . == [])))" "series/Fawnduu/tweets.jsonl" > "series/Fawnduu/My Dragon Girlfriend/tweets.jsonl"
```
