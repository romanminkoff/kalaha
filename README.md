# Game Kalaha for 2+ players

kalaha.Board is useful to analyse stratagies.

kalaha.ConsoleGame is a simple implementation of interactive mode.<br>
Example:

In [1]: import kalaha<br>
In [2]: kalaha.ConsoleGame().new_game()<br>
Number of players: 3<br>
Number of player holes: 2<br>
Number of stones per hole: 2<br>
----- Board layout -----<br>
   0   1   2   3   4   5   6   7   8<br>
   <b>0</b>   2   2   <b>0</b>   2   2   <b>0</b>   2   2<br>
Player with hole #0 is moving.<br>
Which hole id to start with? 8<br>
   0   1   2   3   4   5   6   7   8<br>
   <b>2</b>   0   3   <b>0</b>   3   0   <b>0</b>   3   1<br>
...
