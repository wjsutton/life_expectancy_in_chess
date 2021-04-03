<h1 style="font-weight:normal"> 
  Life Expectancy in Chess ♟
</h1>

[![Status](https://img.shields.io/badge/status-active-success.svg)]() [![GitHub Issues](https://img.shields.io/github/issues/wjsutton/life_expectancy_in_chess.svg)](https://github.com/wjsutton/life_expectancy_in_chess/issues) [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/wjsutton/life_expectancy_in_chess.svg)](https://github.com/wjsutton/life_expectancy_in_chess/pulls) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

Understanding which pieces in chess are more likely to survive a game of chess than others.

:construction: Repo Under Construction :construction: 

[Twitter][Twitter] :speech_balloon:&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[LinkedIn][LinkedIn] :necktie:&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[GitHub :octocat:][GitHub]&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Website][Website] :link:

<!--/div-->

<!--
Quick Link 
-->

[Twitter]:https://twitter.com/WJSutton12
[LinkedIn]:https://www.linkedin.com/in/will-sutton-14711627/
[GitHub]:https://github.com/wjsutton
[Website]:https://wjsutton.github.io/

### :a: About

This repo is to calculate a chess piece's likelihood to survive a game of chess.

To calculate survival rates we take a 10K game sample from [https://database.lichess.org/#standard_games](https://database.lichess.org/#standard_games). We use the script [chess_survival_statistics.py](https://github.com/wjsutton/life_expectancy_in_chess/blob/main/chess_survival_statistics.py) to iterate through 10,000 games and write the data locally, [calculate_survival.py](https://github.com/wjsutton/life_expectancy_in_chess/blob/main/calculate_survival.py) will then read the file and calculate the survival rates for each chess piece, and produce the dataset [chess_piece_survival_rates.csv](https://github.com/wjsutton/life_expectancy_in_chess/blob/main/data/chess_piece_survival_rates.csv)

To add interest and a storytelling aspect to the dashboard the user can choose to a famous chess match to play, details of the famous matches are as follows:

- Garry Kasparov vs Magnus Carlsen: [https://lichess.org/study/dkBrvFEK](https://lichess.org/study/dkBrvFEK)
- Garry Kasparov VS Deep Blue: [https://lichess.org/study/mMd71FFj](https://lichess.org/study/mMd71FFj)
- Judit Polgar vs Garry Kasparov, Moscow 2002: [https://lichess.org/study/IKi04lMM/bkjHPMaE](https://lichess.org/study/IKi04lMM/bkjHPMaE)
- Carlsen, Magnus vs 	Nepomniachtchi, Ian: [https://lichess.org/broadcast/chess24-legends-of-chess-finals-day-2/kRHLCPAl](https://lichess.org/broadcast/chess24-legends-of-chess-finals-day-2/kRHLCPAl)
- All beth harmon: [https://lichess.org/study/dffUtue4/cOBFJKQI](https://lichess.org/study/dffUtue4/cOBFJKQI)

The script [queens_gambit_final.py](https://github.com/wjsutton/life_expectancy_in_chess/blob/main/queens_gambit_final.py) will process the famous matches to create the datasets [match_survival.csv](https://github.com/wjsutton/life_expectancy_in_chess/blob/main/data/match_survival.csv) & [match_timeline.csv](https://github.com/wjsutton/life_expectancy_in_chess/blob/main/data/match_timeline.csv)

Useful links:
- Understanding SAN notation [https://blog.chesshouse.com/how-to-read-and-write-algebraic-chess-notation/](https://blog.chesshouse.com/how-to-read-and-write-algebraic-chess-notation/)
- C# repo on surviving chess pieces [ojb500/survivingpieces](https://github.com/ojb500/survivingpieces)
- Converting SAN notation to Long Algebraic notations [https://chess.stackexchange.com/questions/2895/how-to-convert-pgn-moves-to-long-algebraic-notation-in-python](https://chess.stackexchange.com/questions/2895/how-to-convert-pgn-moves-to-long-algebraic-notation-in-python)

### 📈 See the Dashboard 

URL: [https://public.tableau.com/profile/wjsutton#!/vizhome/ChessLifeExpectancy/Title](https://public.tableau.com/profile/wjsutton#!/vizhome/ChessLifeExpectancy/Title)

<div style="width: 300px; height:300px; overflow: hidden;margin: 0 10px 0 0">
<a href="https://public.tableau.com/profile/wjsutton#!/vizhome/ChessLifeExpectancy/Title">
<img src='https://raw.githubusercontent.com/wjsutton/life_expectancy_in_chess/main/dashboard_images/Title.png' width="80%">
  <img src='https://raw.githubusercontent.com/wjsutton/life_expectancy_in_chess/main/dashboard_images/Enrolment.png' width="49%">
  <img src='https://raw.githubusercontent.com/wjsutton/life_expectancy_in_chess/main/dashboard_images/Selection.png' width="49%">
  <img src='https://raw.githubusercontent.com/wjsutton/life_expectancy_in_chess/main/dashboard_images/Result.png' width="49%">
  <img src='https://raw.githubusercontent.com/wjsutton/life_expectancy_in_chess/main/dashboard_images/Barracks.png' width="49%">
</a>
</div>


