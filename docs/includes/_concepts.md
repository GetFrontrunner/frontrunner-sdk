# Concepts

## Order Types
Participants in Frontrunner markets submit `buy` (a.k.a. bid) and `sell` (a.k.a. ask) 
orders of two different types:

* `long`: in favor of the `long_entity` outcome
* `short`: in favor of the `short_entity` if present. If no `short_entity` is present (i.e. in non-binary markets), this outcome is simply the inverse or "not" of the `long_entity`. See the [Non-Binary Markets](#non-binary-markets) section below for additional context.

## Market Types

### Binary markets
In Frontrunner's binary markets, both the `long` and the `short`
side represent distinct entities. All `game` markets that **cannot** end in a draw 
are binary markets because there are only two possible standard outcomes.

For example, the `game` `winner` market `Miami Heat @ Orlando Magic` is a binary market where the Heat are 
the `long_entity` and the Magic are the `short_entity`.

For binary markets, long positions resolve at $1 (and short positions at $0) if the
outcome represented by the `long_entity` occurs; short positions resolve at $1 (and long positions at $0) 
if the outcome represented by the `short_entity` occurs.

<aside class="notice">
Sports with non-standard draw scenarios (i.e. extremely low probabilities of draws occurring) 
are also binary markets despite the fact that they can end in a draw.  
If such a game ends in a draw, both <code>long</code> and <code>short</code> positions resolve at $0.50.
Markets that can resolve at $0.50 are listed here:
<ul type="disc">
    <li>NFL regular season games</li>
    <li>MLB regular season games</li>
</ul>
</aside>

### Non-Binary Markets
Non-binary markets are represented by a group of binary markets that do not have `short_entity` 
specified. When there is no `short_entity`, taking a `short` position is simply betting against the 
`long` outcome. All `game` markets that **can** end in a draw (besides NFL) and futures markets are non-binary markets.

For example, the `game` `winner` market `Arsenal FC v Chelsea FC` is a non-binary market 
represented by 3 distinct Frontrunner markets:

* `Arsenal FC`: `long` in this market resolves at $1 if Arsenal wins and $0 if they lose or draw.
`short` in this market resolves at $1 if Arsenal loses or draws. `short` can be thought of as "Not Arsenal"
* `Chelsea FC`: `long` in this market resolves at $1 if Chelsea wins and $0 if they lose or draw.
`short` in this market resolves at $1 if Chelsea loses or draws. `short` can be thought of as "Not Chelsea"
* `Draw`: `long` in this market resolves at $1 if the game ends in a draw.
`short` in this market resolves at $1 if the game does not end in a draw. `short` can be thought of as "Not Draw"

Futures markets may exist for season winners like the NFL Championship, Premier League Season, and NBA Finals.
For futures markets, one market exists for each entity with sufficient chances of winning (at the discretion of Frontrunner).

## Home and Away
Frontrunner defines the `long` entity as the first entity in the matchup description.
This definition changes depending on the sport - the different options are listed below.

| League    | Sport Event Name | Long Entity | Short Entity |
|-----------|------------------|-------------|--------------|
| EPL       | Home v Away      | n/a*        | n/a          |
| Formula 1 | n/a**            | n/a*        | n/a          |
| MLB       | Away @ Home      | Away        | Home         |
| NBA       | Away @ Home      | Away        | Home         |
| NFL       | Away @ Home      | Away        | Home         |
*The home/away designation does correlate directly to long/short entities for non-binary markets like EPL markets 
(as well as futures) due to their structure. However, the home team can still be detected based on the Sport Event Name.
See the [Non-Binary Markets](#non-binary-markets) section above for additional context.  
**Formula 1 information from Frontrunner does not include information about player/team nationalities.
