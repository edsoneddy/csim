public class prob201 {
    public static void main(String[] args) {
        // Fibonacci sequence up to the 10th term
        int n = 10;
        int[] fib = new int[n];
        fib[0] = 0;
        fib[1] = 1;
        for (int i = 2; i < n; i++) {
            fib[i] = fib[i - 1] + fib[i - 2];
        }
        // Print the Fibonacci sequence
        for (int i = 0; i < n; i++) {
            System.out.print(fib[i] + " ");
        }
        System.out.println();
    }
}