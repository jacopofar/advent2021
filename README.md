# Advent of code 2021

These are the solution to the [Advent of code 2021](https://adventofcode.com/) in Python.

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
* day 10: done
* day 11: done
* day 12: done
* day 13: done
* day 14: done
* day 15: done
* day 16: skipped, I didn't have time and didn't look very interesting
* day 17: done (no video, had no time)
* day 18: skipped, very long description and no time
* day 19: done (video description, no live coding)
* day 20: done with an ugly workaround
* day 21: done (no live coding)
* day 22: done (no video yet)
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

The problem doesn't state it explicitly, but every basin is delimited by 9s or the grid edges. This is a result of the fact 9s are in no basin and each cell can be in only one basin at the time, which is possible only when 9s form borders.
This eliminates the need to search for taller neighbors and the code can be a bit shorter.

## Day 20

Here the problem seems simple: we iterate over the coordinates and from the small 3x3 area calculate the new set of values. The problem is that the first value in the "algorithm" can be a #, which means we end up with an infinite grid.

I tried to handle this by passing an infinite_on flag meaning that the values outside the search area have to be handled as # or not.
The function calculating the step also handles this flag, so the infinite grid can be represented.

The approach seems sound and works on the sample input I crafted to test it, but fails on the real problem input. There must be some edge case to handle, but I have no time so used an ugly (but working!) approach: by adding some abundant padding and removing it at the end, the infinite can be ignored as long as the steps to calculate are lower than the padding.
