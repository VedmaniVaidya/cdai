import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Scanner;


public class UtilityList {
    public static void main(String[] args) {
        ArrayList<Student> students = new ArrayList<>();
        createList(students);
        printlist(students);
        
    }

    public static void sortByRollno(ArrayList<Student> students){
           Collections.sort(students);
           for(Student std:students){
            System.out.println(std);
           }
    }

    public static void sortByPercentage(ArrayList<Student> students){
           Collections.sort(students,new StudentComparatorByPercentage());
           for(Student std:students){
            System.out.println(std);
           }
    }

    private static void printlist(ArrayList<Student> students) {
        for(Student st:students){
            System.out.println(st);
        }
    }

    public static void createList(ArrayList<Student> students){
        Scanner sc = new Scanner(System.in);
        
        for(int i = 0;i<5;i++){
            int rollno = sc.nextInt();
            sc.nextLine();
            String name = sc.nextLine();
            double percentage = sc.nextDouble();
            students.add(new Student(rollno, name, percentage, getHobbies()));
        }
      
    }

    private static HashSet<String> getHobbies() {
        HashSet<String> hobbies = new HashSet<>();
        Scanner sc = new Scanner(System.in);
        System.out.println("enter number of hobbies");
        int n = sc.nextInt(                               );
        for(int i = 0;i<n;i++){
           hobbies.add(sc.next());
        }
        return hobbies;
    }

}
