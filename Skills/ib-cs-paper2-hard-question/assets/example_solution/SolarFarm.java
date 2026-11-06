public class SolarFarm {
    private int[][] output;
    private int rows;
    private int cols;

    public SolarFarm(int[][] output) {
        this.output = output;
        this.rows = output.length;
        this.cols = output[0].length;
    }

    public int blockTotal(int top, int left, int k) {
        int total = 0;
        for (int r = top; r < top + k; r++) {
            for (int c = left; c < left + k; c++) {
                total = total + output[r][c];
            }
        }
        return total;
    }

    public int bestBlock(int k) {
        int bestTotal = -1;
        int bestRow = 0;
        int bestCol = 0;
        for (int top = 0; top <= rows - k; top++) {
            for (int left = 0; left <= cols - k; left++) {
                int total = blockTotal(top, left, k);
                if (total > bestTotal) {
                    bestTotal = total;
                    bestRow = top;
                    bestCol = left;
                }
            }
        }
        System.out.println("Row: " + bestRow + " Column: " + bestCol);
        return bestTotal;
    }

    public int[][] buildCumulative() {
        int[][] cum = new int[rows + 1][cols + 1];
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= cols; j++) {
                cum[i][j] = output[i - 1][j - 1] + cum[i - 1][j]
                          + cum[i][j - 1] - cum[i - 1][j - 1];
            }
        }
        return cum;
    }

    public int smallestBlock(int target) {
        int[][] cum = buildCumulative();
        int low = 1;
        int high = rows;
        if (cols < high) {
            high = cols;
        }
        int answer = -1;
        while (low <= high) {
            int mid = (low + high) / 2;
            boolean found = false;
            for (int top = 0; top <= rows - mid && !found; top++) {
                for (int left = 0; left <= cols - mid && !found; left++) {
                    int total = cum[top + mid][left + mid]
                              - cum[top][left + mid]
                              - cum[top + mid][left]
                              + cum[top][left];
                    if (total >= target) {
                        found = true;
                    }
                }
            }
            if (found) {
                answer = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return answer;
    }
}
