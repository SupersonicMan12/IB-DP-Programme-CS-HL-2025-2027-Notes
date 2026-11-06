import java.util.*;
public class TestSolarFarm {
    static int brute(int[][] g, int t) {
        int R=g.length,C=g[0].length;
        for (int k=1;k<=Math.min(R,C);k++)
            for (int a=0;a+k<=R;a++) for (int b=0;b+k<=C;b++) {
                int s=0; for(int r=a;r<a+k;r++) for(int c=b;c<b+k;c++) s+=g[r][c];
                if (s>=t) return k;
            }
        return -1;
    }
    public static void main(String[] x) {
        int[][] g={{3,1,4,1,5},{9,2,6,5,3},{5,8,9,7,9},{3,2,3,8,4}};
        SolarFarm f=new SolarFarm(g);
        System.out.println(f.blockTotal(1,2,2));
        for (int k=1;k<=4;k++) System.out.println("k="+k+" -> "+f.bestBlock(k));
        System.out.println(Arrays.deepToString(f.buildCumulative()));
        int[] ts={0,1,9,10,28,29,50,54,55,77,78,100};
        for(int t:ts) System.out.println("target "+t+" -> "+f.smallestBlock(t));
        Random rnd=new Random(1);
        java.io.PrintStream o=System.out;
        System.setOut(new java.io.PrintStream(new java.io.OutputStream(){public void write(int b){}}));
        for (int it=0;it<20000;it++){
            int R=1+rnd.nextInt(7),C=1+rnd.nextInt(7);
            int[][] h=new int[R][C];
            for(int i=0;i<R;i++)for(int j=0;j<C;j++)h[i][j]=rnd.nextInt(4)==0?0:rnd.nextInt(20);
            SolarFarm s=new SolarFarm(h);
            int t=rnd.nextInt(300);
            if (s.smallestBlock(t)!=brute(h,t)) { o.println("MISMATCH"); return; }
        }
        // big timing
        int N=1000; int[][] big=new int[N][N];
        for(int i=0;i<N;i++)for(int j=0;j<N;j++)big[i][j]=rnd.nextInt(1001);
        long st=System.nanoTime(); int ans=new SolarFarm(big).smallestBlock(400_000_000);
        o.println("all random tests OK; big ans="+ans+" time ms="+(System.nanoTime()-st)/1e6);
    }
}
