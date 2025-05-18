import java.util.Scanner;

class MultiplyByTwo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Prompt user for input
        int number = scanner.nextInt();

        // Multiply by 2
        int result = number * 2;

        // Print the result
        System.out.println(result);

        scanner.close();
    }
}
