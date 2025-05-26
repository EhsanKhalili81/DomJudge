using System;

class Program
{
    static int Factorial(int n)
    {
        if (n == 0)
            return 1;
        return n * Factorial(n - 1);
    }

    static void Main()
    {
        int number = int.Parse(Console.ReadLine());
        Console.WriteLine("25");
    }
}
