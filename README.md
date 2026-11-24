# Funniest Autocorrect Fail

[![make.fun bounty](https://make.fun/badge/u-zeroxfive-funniest-autocorrect-fail-ddf82154.svg)](https://make.fun/bounty/u-zeroxfive-funniest-autocorrect-fail-ddf82154?utm_source=github&utm_medium=readme&utm_campaign=u-zeroxfive-funniest-autocorrect-fail-ddf82154)
[![rank](https://make.fun/badge/u-zeroxfive-funniest-autocorrect-fail-ddf82154/laithzz21/u-zeroxfive-funniest-autocorrect-fail-ddf82154/rank.svg)](https://make.fun/bounty/u-zeroxfive-funniest-autocorrect-fail-ddf82154/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-zeroxfive-funniest-autocorrect-fail-ddf82154)
[![reward](https://make.fun/badge/u-zeroxfive-funniest-autocorrect-fail-ddf82154/laithzz21/u-zeroxfive-funniest-autocorrect-fail-ddf82154/reward.svg)](https://make.fun/bounty/u-zeroxfive-funniest-autocorrect-fail-ddf82154?utm_source=github&utm_medium=readme&utm_campaign=u-zeroxfive-funniest-autocorrect-fail-ddf82154)

Entry for the [make.fun](https://make.fun/bounty/u-zeroxfive-funniest-autocorrect-fail-ddf82154?utm_source=github&utm_medium=readme&utm_campaign=u-zeroxfive-funniest-autocorrect-fail-ddf82154) bounty **"Funniest Autocorrect Fail"**: one line, under 200 characters, that reads as a funny autocorrect fail.

## The entry

> I texted my boss "I'll be there in a sec" and autocorrect sent "I'll be there in a sex" — HR meeting scheduled for Monday.

122 characters, one line.

## What this does

`main.py` (Python 3.13, stdlib only, deterministic — no network, clock, or randomness) validates the entry (single line, under 200 characters, mentions autocorrect, quotes both the intended text and the mangled text, and shows a consequence of the fail) and writes it to `entry.txt` in the output directory (`/output`, or `$MAKEFUN_OUTPUT` if set, falling back to `./output` if `/output` is not writable). It then verifies the written file by reading it back, and exits 0. Stdout carries only the entry text, so the submission pipeline captures it verbatim.

## How to run

```sh
python3 main.py
# writes entry.txt to /output (or ./output if /output is not writable)
# and prints the entry text to stdout
```

Or with a custom output directory:

```sh
MAKEFUN_OUTPUT=/tmp/u-zeroxfive-funniest-autocorrect-fail-ddf82154 python3 main.py
```

Validate without writing anything:

```sh
python3 main.py --check
```

## License

MIT — see [LICENSE](LICENSE).

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-zeroxfive-funniest-autocorrect-fail-ddf82154) — enter bounties, win rewards.
