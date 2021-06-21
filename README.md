# TravellingSalesmanProblem
This project is a website using Flask to help solving Travelling Salesman Problem.

## TSP Algorithm
Using <b>Branch and Bound Algorithm</b> with Reduced Cost Matrix<br><br>
This algorithm is suitable for solving TSP problem which given a set of places.
and the distance between every pair of them, while the problem that should be solved is
finding the shortest possible route that visits every city exactly once and returns to
starting point.
<br><br>
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
1. Go to `src` folder
2. Run `python app.py`
3. Click `Get Started`
4. You can choose whether you want to <b>Upload Only, Manually Input Only,</b> or both <b>Upload and Manually Input</b>
5. If you want to <b>Upload</b>, click `Choose Files` and select files in `test` folder. Don't forget to click `Upload` to submit the files
6. If you want to <b>Manually Input</b>, click `Manually Input Route`. Complete the form and click `Add Identity`. Add the destinations by completing the next form. If you are ready to find the shortest route, click `Find Shortest Route`
7. The result will be displayed. You can click `<` or `>` button to see how the route is created
8. If you want to search delivery histories, you can click `History` in the navbar

## Status
Complete on: June 21, 2021

## Author
Rahmah Khoirussyifa' Nurdini

## References
* Specification: https://github.com/gilliantuerah/BantuKurir-TSP
* Layout: Bootstrap, W3Schools
