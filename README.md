# Advent of code 2021

These are the solution to the Advent of code 2021 in Python.

The goal of this repo is to show some practical live coding and how a problem is solved quickly, and how issues are troubleshoot.

There's no nice test or formatting, except for some typos or docstrings I keep the resulting code as it looks like at the end of the video.


## State

* day 01: done
* day 02: done
* day 03: done
* day 04: done
* day 05: done (+ nicer solution)
* day 06: done
* day 07: done
* day 08: done
* day 09: done

## Nicer solutions

In the folder `advent2021_nicer` you can find a few improved solutions, not covered in the videos.

The videos usually show the first approach that cam eto my mind, usually simple and easy to follow but not necessarily elegant or efficient. Sometimes, after taking the video I think about it or discuss with my friends and find a better solution.

If the solution is particularly nice and I have time to implement it, you can find it in the `advent2021_nicer` folder.

### Day 05

In this day we have to calculate the points that are in a segment and have discrete (integer) coordinates (all segments have a slope multiple of 45° and the extremes have always discrete coordinates). My first solution is a bit verbose, because I explicitly calculate the values of X and Y in order, and since `range` in Python doesn't accept a backward interval (without providign a step of -1, but it's not very intuitive) a few if blocks are needed to handle negative slopes.
A smarter solution is to calculate the offsets in the two axes, a value that is -1, 0 or +1 and tells us how much we move on each axis as we cross the segment.
Then, we start from the first coordinate and increase X and Y by their offsets until we reach the end point. This makes the code shorter and most importantly easier to read. It's also a bit faster.

A second optimization is applied to be able to handle large inputs (note: this was not part of the original advent of code problem!). If segments have coordinates as large as 10 millions, enumerating all the points becomes hard if not impossible. A solution is to calculate only points and intersections in a small tile, and iterate over the tiles. Once a tile is calculated only the amount of intersection is kept, so the memory usage remains low.

## Day 07

We don't need to iterate over all possible crab-position combinations.
Instead, we can go from left to right and keep the count of how many crabs we found so far and how fast the total distance is growing.
We need to do it twice (left-to-right and back) and go from `O(p * c)` to `O(p)` where `p` is the amount of positions and `c` the amount of crabs.

## Day 09

The problem doesn't state it explicitly, but every basid is delimited by 9s or the grid edges. This is a result of the fact 9s are in no basin and each cell can be in only one basin at the time, which is possible only when 9s form borders.
This eliminates the need to search for taller neighbors and the code can be a bit shorter.