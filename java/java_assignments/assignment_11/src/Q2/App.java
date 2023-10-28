package Q2;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class App {
    public static void main(String[] args) {
        try {
            // Create a Scanner object to read the file
            File inputFile = new File("/home/dai/java/assignment_11/src/Q2/src.txt");
            Scanner scanner = new Scanner(inputFile);

            // Create a FileWriter object to write to the new file
            File outputFile = new File("/home/dai/java/assignment_11/src/Q2/dest2.txt");
            FileWriter writer = new FileWriter(outputFile);

            // Create a separate thread for reading from the input file
            Thread readerThread = new Thread(new ReaderRunnable(scanner, writer));

            // Start the reader thread
            readerThread.start();

            // Wait for the reader thread to finish
            synchronized (readerThread) {
                readerThread.wait();
            }

            System.out.println("New file created successfully.");
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    // Runnable implementation for reading from the input file
    static class ReaderRunnable implements Runnable {
        private Scanner scanner;
        private FileWriter writer;

        public ReaderRunnable(Scanner scanner, FileWriter writer) {
            this.scanner = scanner;
            this.writer = writer;
        }

        @Override
        public void run() {
            try {
                while (scanner.hasNextLine()) {
                    String line = scanner.nextLine();
                    // You can process the line here if needed
                    synchronized (writer) {
                        writer.write(line);
                        writer.write(System.lineSeparator()); // Add line separator after each line
                    }
                }
                scanner.close();
                writer.close();
                synchronized (Thread.currentThread()) {
                    Thread.currentThread().notify(); // Notify the main thread
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
