# Concepts

## Order Types
Participants in Frontrunner markets submit `buy` and `sell` orders of 
two different types:
* `long`: in favor of the `long_entity` outcome
* `short`: in favor of the `short_entity` if present. If no `short_entity`
is present, this outcome is simply the inverse or "not" of the `long_entity`. 
See the [Non-Binary Markets](#non-binary-markets) section below for additional context.

## Market Types

### Binary markets
In Frontrunner's binary markets, both the `long` and the `short`
side represent distinct entities. All `game` markets that **cannot** end in a draw 
are binary markets because there are only two possible outcomes.

For example, the `game` `winner` market `Miami Heat @ Orlando Magic` is a binary market where the Heat are 
the `long_entity` and the Magic are the `short_entity`.

For binary markets, long positions resolve at $1 (and short positions at $0) if the
outcome represented by the `long_entity` occurs; short positions resolve at $1 (and long positions at $0) 
if the outcome represented by the `short_entity` occurs.

### Non-Binary Markets
Non-binary markets are represented by a group of binary markets that do not have `short_entity` 
specified. When there is no `short_entity`, taking a `short` position is simply betting against the 
`long` outcome. All `game` markets that **can** end in a draw and futures markets are non-binary markets.

For example, the `game` `winner` market `Arsenal FC v Chelsea FC` is a non-binary market 
represented by 3 distinct Frontrunner markets:
* `Arsenal FC`: `long` in this market resolves at $1 if Arsenal wins and $0 if they lose or draw. 
`short` in this market resolves at $1 if Arsenal loses or draws. `short` can be thought of as "Not Arsenal"
* `Chelsea FC`: `long` in this market resolves at $1 if Chelsea wins and $0 if they lose or draw.
`short` in this market resolves at $1 if Chelsea loses or draws. `short` can be thought of as "Not Chelsea"
* `Draw`: `long` in this market resolves at $1 if the game ends in a draw.
  `short` in this market resolves at $1 if the game does not end in a draw. `short` can be thought of as "Not Draw"

## Home and Away