# TravellingSalesmanProblem
This project is a website using Flask to help solving Travelling Salesman Problem.

## TSP ALgorithm
Using <b>Branch and Bound Algorithm</b> with Reduced Cost Matrix<br>
This algorithm is suitable for solving TSP problem which given a set of places
and the distance between every pair of them, while the problem that should be solved is
finding the shortest possible route that visits every city exactly once and returns to
starting point.
<br>
With this algorithm, we dont have to explore every nodes before backtracking. Some 
nodes can be rejected when we know that they won't lead to a better solution than the promosing node that has the best-solution-so-far.

## Technologies
<b>Flask with Python3</b><br>
This framework is a good start for getting into website development because
it provides simplicity, flexibility and fine-grained control. For backend, this project
uses <b>MySQLdb</b> for managing database because this library is easy-to-use for using
database in our local DBMS.

## Librarires
* datetime, os, sys, copy
* MySQLdb
* matplotlib

## How To Run
1. 

## Status
Complete on: June 21, 2021

## Author
Rahmah Khoirussyifa' Nurdini

## References
Bootstrap, W3Schools