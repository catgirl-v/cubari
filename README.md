# catgirl-v's Cubari series

Enjoy!

## Series

+ [Fawnduu - My Dragon Girlfriend][Fawnduu/My Dragon Girlfriend/Cubari] ([Cubari source][Fawnduu/My Dragon Girlfriend/cubari.json])
  + Author & series information goes here!

[Fawnduu/My Dragon Girlfriend/Cubari]: https://cubari.moe/read/gist/cmF3L2NhdGdpcmwtdi9jdWJhcmkvZC9jYXRnaXJsLXYvbWFpbi9zZXJpZXMvRmF3bmR1dS9NeSUyMERyYWdvbiUyMEdpcmxmcmllbmQvY3ViYXJpLmpzb24/
[Fawnduu/My Dragon Girlfriend/cubari.json]: https://raw.githubusercontent.com/catgirl-v/cubari/d/catgirl-v/main/series/Fawnduu/My%20Dragon%20Girlfriend/cubari.json

## Initial import notes

```
twint --utc --full-text -u "Fawnduu" --since "2017-08-01 00:00:00" --json --hide-output -o "series/Fawnduu/tweets.jsonl" --count
jq -c "select(.conversation_id == \"914484965215227904\" or .conversation_id == \"914854813694693378\" or .conversation_id == \"915276793766170626\") | del((.language | select(. == \"en\")), .date, .time, .timezone, (.[] | select(. == \"\" or . == [])))" "series/Fawnduu/tweets.jsonl" > "series/Fawnduu/My Dragon Girlfriend/tweets.jsonl"
```
