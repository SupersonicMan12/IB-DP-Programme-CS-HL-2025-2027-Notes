"""Python mirror of SolarFarm.java plus a brute-force cross-check.

Use this pattern when Java is not available in the sandbox: translate the Java model answer
line-for-line into Python, test the mirror, then re-read the Java against the mirror.
"""
class SolarFarm:
    def __init__(self, output):
        self.output = output
        self.rows = len(output)
        self.cols = len(output[0])

    def block_total(self, top, left, k):
        total = 0
        for r in range(top, top + k):
            for c in range(left, left + k):
                total = total + self.output[r][c]
        return total

    def best_block(self, k):
        best_total = -1
        best_row = 0
        best_col = 0
        for top in range(self.rows - k + 1):
            for left in range(self.cols - k + 1):
                total = self.block_total(top, left, k)
                if total > best_total:
                    best_total = total
                    best_row = top
                    best_col = left
        print("Row:", best_row, "Column:", best_col)
        return best_total

    def build_cumulative(self):
        cum = []
        for i in range(self.rows + 1):
            cum.append([0] * (self.cols + 1))
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                cum[i][j] = (self.output[i - 1][j - 1] + cum[i - 1][j]
                             + cum[i][j - 1] - cum[i - 1][j - 1])
        return cum

    def smallest_block(self, target):
        cum = self.build_cumulative()
        low = 1
        high = self.rows
        if self.cols < high:
            high = self.cols
        answer = -1
        while low <= high:
            mid = (low + high) // 2
            found = False
            for top in range(self.rows - mid + 1):
                for left in range(self.cols - mid + 1):
                    total = (cum[top + mid][left + mid]
                             - cum[top][left + mid]
                             - cum[top + mid][left]
                             + cum[top][left])
                    if total >= target:
                        found = True
            if found:
                answer = mid
                high = mid - 1
            else:
                low = mid + 1
        return answer

import random, io, contextlib
def brute(g,t):
    R,C=len(g),len(g[0])
    for k in range(1,min(R,C)+1):
        for a in range(R-k+1):
            for b in range(C-k+1):
                if sum(g[r][c] for r in range(a,a+k) for c in range(b,b+k))>=t: return k
    return -1
def brute_best(g,k):
    R,C=len(g),len(g[0]); best=None
    for a in range(R-k+1):
        for b in range(C-k+1):
            s=sum(g[r][c] for r in range(a,a+k) for c in range(b,b+k))
            if best is None or s>best[0]: best=(s,a,b)
    return best
g=[[3,1,4,1,5],[9,2,6,5,3],[5,8,9,7,9],[3,2,3,8,4]]
f=SolarFarm(g)
print(f.block_total(1,2,2)); print(f.best_block(2)); print(f.build_cumulative())
print([f.smallest_block(t) for t in (0,9,10,28,29,50,54,55,77,78,100)])
random.seed(3)
for it in range(5000):
    R,C=random.randint(1,6),random.randint(1,6)
    h=[[random.choice([0,random.randint(0,20)]) for _ in range(C)] for _ in range(R)]
    s=SolarFarm(h); t=random.randint(0,250)
    assert s.smallest_block(t)==brute(h,t)
    k=random.randint(1,min(R,C))
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): tot=s.best_block(k)
    b=brute_best(h,k)
    assert tot==b[0] and buf.getvalue().split()==["Row:",str(b[1]),"Column:",str(b[2])]
print("python OK")
