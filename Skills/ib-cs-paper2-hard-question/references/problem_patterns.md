# Codeforces 1300–1500 ideas that fit the IB syllabus

Each idea needs only arrays, loops, selection, methods, a class, Big O, binary/linear search,
simple sorts or non-branching recursion. Pick one core insight per question, give it a fresh
real-world context, and scaffold it with the naive → analysis → efficient structure from
`ib_style_guide.md`. Don't reuse the exemplar's context (solar farm) unless the user asks for it.

| # | Core insight | Naive (parts b–d) | Efficient final part (f) | Example contexts |
|---|---|---|---|---|
| 1 | **2D prefix sums + binary search on the answer** (the exemplar) | sum every K×K block, O(N⁴) | cumulative table, O(1) block sum, binary search on K using monotonicity | solar panels, crop yields, pixel brightness, seating sales |
| 2 | **1D prefix sums**: range totals in O(1); best window of length k | re-sum each window, O(n·k) | prefix array; or count pairs whose difference is a multiple of m using a remainder-count array of size m | daily step counts, rainfall, sales per hour |
| 3 | **Two pointers / sliding window**: longest window with total ≤ budget (non-negative values) | try every start and end, O(n²) | expand right, shrink left, O(n). The (f)(i) explanation: why left never moves back | streaming data caps, a hiker's water budget, bus ride fares |
| 4 | **Binary search on the answer** (min-max): smallest capacity so items can be split into ≤ d consecutive groups | try every capacity, O(n·S) | greedy feasibility check O(n), with binary search over [max, total]; monotonic feasibility | delivery truck loads, chapters per day, printer job batches |
| 5 | **Difference array** for many range increments | update every cell of each range, O(q·n) | +v at l, −v at r+1, then one running total, O(n+q); then find the most-booked slot | room bookings, road works, festival crowd shifts |
| 6 | **Greedy after sorting** (bubble/selection sort written by the student) | try all orders / all pairs | sort, then a greedy scan (e.g. max non-overlapping intervals by end time, pairing heaviest with lightest under a limit) | canoe pairing, meeting rooms, exam scheduling |
| 7 | **Frequency/count arrays** over a small range (0–25, 0–100) | compare every pair, O(n²) | counting array, O(n + range): anagram windows, first unique character, mode | DNA strings, survey scores, licence plates |
| 8 | **Stack-based matching / nearest greater element** | for each element scan forward, O(n²) | monotonic stack, O(n); explain why each element is pushed/popped once | stock prices "days until warmer", bracket validation with depths, skyline views |
| 9 | **Queue simulation** with timing | — | queue of arrivals with service times; output waiting times; detect overflow | bank counters, print spooler, car wash |
| 10 | **Non-branching recursion** | iterative version first | fast exponentiation by squaring (x^n mod m in O(log n)), digital root, recursive binary search, Euclid's GCD; trace the call stack | encryption keys, repeated interest, gear ratios |
| 11 | **Grid simulation with parity/period detection** | simulate all T steps, O(T) | spot the cycle length and reduce T mod period; show the state repeats | traffic lights, rotating robot, light patterns |
| 12 | **String processing** (B2.1.2) | rebuild strings repeatedly | single pass with substring extraction: run-length encode/decode, longest palindromic substring by centre expansion (O(n²) instead of O(n³)) | barcode compression, DNA, message validation |

## Making it "the hardest question" without breaking IB scope
- The difficulty should come from **an insight plus careful indices**, not from obscure APIs.
- Always ask for a **monotonicity or invariant explanation** (f)(i) before the efficient construct.
  This is the reasoning step a Codeforces solver does silently.
- Include one **exact-boundary trap**: inclusive bounds, −1 when there is no answer, tie rules.
- State a size constraint (e.g. 10⁶ cells, 10⁵ items) that clearly rules out the naive method, so
  the Big O parts have a reason to exist.
- Values non-negative / within a small range: say so explicitly when correctness depends on it.
- Integer overflow: state "you may assume all totals fit in an `int`", or choose sizes that fit.
- Give a small figure (4×5, 8–12 elements) where the brute-force answer can be checked by hand, and
  where the tie rule and the "no answer" case can actually happen.
