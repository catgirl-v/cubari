#!/bin/sh
set -xe

new_tweets=$(mktemp --suffix=".fawnduu.jsonl")
all_tweets="series/Fawnduu/tweets.jsonl"

# Fetch new tweets
since="$(jq -sr 'last.created_at' "${all_tweets}")"
#twint --utc --full-text -u "Fawnduu" --since "${since% UTC}" --json --hide-output -o "${new_tweets}" --count
# FIXME this ignores tweets with the same date as the latest indexed tweet,
# but ideally we'd like to deduplicate on tweet IDs instead
#jq -sc --arg since "${since}" 'reverse[] | select(.created_at != $since)' "${new_tweets}" >> "${all_tweets}"
#rm "${new_tweets}"

# Filter tweets from the My Dragon Girlfriend thread and generate cubari.json
my_dragon_gf="series/Fawnduu/My Dragon Girlfriend"
jq -c "select(.conversation_id == \"914484965215227904\" or .conversation_id == \"914854813694693378\" or .conversation_id == \"915276793766170626\") | del((.language | select(. == \"en\")), .date, .time, .timezone, (.[] | select(. == \"\" or . == [])))" "${all_tweets}" > "${my_dragon_gf}/tweets.jsonl"
jq -sf "${my_dragon_gf}/cubari.jq" "${my_dragon_gf}/tweets.jsonl" > "${my_dragon_gf}/cubari.json"

# Scrape ADHDinos
#./series/Ryan\ Keats/ADHDinos/adhdinos.py
