import java.util.Scanner;

class AccountHolder {
    static int num_accounts = 0;
    
    private int account_number;
    private String name;
    private float balance;

    public AccountHolder(int account_number, String name, float balance) {
        this.account_number = account_number;
        this.name = name;
        this.balance = balance;
        num_accounts+=1;
    }

    public AccountHolder() {
        this.account_number = 123123123;
        this.name = "abc";
        this.balance = 100000;
    }
    
    //getters
    public int getAccount_number() {
        return account_number;
    }

    public String getName() {
        return name;
    }

    public float getBalance() {
        return balance;
    }
    //setters
    public void setAccount_number(int account_number) {
        this.account_number = account_number;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setBalance(float balance) {
        this.balance = balance;
    }
    
    public void deposit(float amount){
        this.balance+=amount;
        System.out.println(this.balance);
    }

    public void withdraw(float amount){
        this.balance-=amount;
        System.out.println(this.balance);
    }


    @Override
    public String toString() {
        return "[account_number=" + account_number + ", name=" + name + ", balance=" + balance + "]";
    }
    
    
}

public class Q5 {
    public static void main(String[] args) {
        AccountHolder account = new AccountHolder();
        account.deposit(10000);
        // System.out.println(account.getBalance());
        account.withdraw(10000);
        // System.out.println(account.getBalance());

        AccountHolder[] accounts = new AccountHolder[10];
        int def_acc_num = 1000;
        String def_acc_name = "John Doe";
        float def_acc_bal = 0;
        for(int i=0;i<accounts.length;i++){
            accounts[i] = new AccountHolder(def_acc_num+i,def_acc_name,def_acc_bal);
        }

        menu(accounts);

    }

    public static void menu(AccountHolder[] accounts){
        int choice;
        int flag=0;
        while(flag!=-1){
        Scanner sc = new Scanner(System.in);
        System.out.println("Select choice:\n"+//
                "1. Add record for account holder\n" + //
                "2. Display details of all account holders.\n" + //
                "3. Deposite an amount into perticular account\n" + //
                "4. Withdraw an amount from perticular account");
        choice = sc.nextInt();
        switch (choice) {
            case 1:
                // TODO: Adding a record to array of account holders
                // maybe write a static AccountHolder method which will be used to create the account which will update (add) the object of newly created object
                // to the static AccountHolder array in that class itself

                break;

            case 2:
                System.out.println("Details of all accounts");
                for (AccountHolder acc:accounts){
                    System.out.println(acc);
                }
                break;

            case 3:
                System.out.println("Enter your account number for deposit");
                int acc_num = sc.nextInt();
                for(int i=0;i<accounts.length;i++){
                    if(accounts[i].getAccount_number()==acc_num){
                        System.out.println("Enter how much amount you want to deposit");
                        float amount = sc.nextFloat();
                        accounts[i].deposit(amount);
                    }
                }    
                    break;
                case 4:
                    System.out.println("Enter your account number for withdrawl");
                    acc_num = sc.nextInt();
                    
                    for(int i=0;i<accounts.length;i++){
                        if(accounts[i].getAccount_number()==acc_num){
                            System.out.println("Enter how much amount you want to wihtdraw");
                            float amount = sc.nextFloat();
                            accounts[i].withdraw(amount);
                        }
                    }    
                    break;

                case 5:
                    flag = -1;
                    break;
            default:
            System.out.println("Invalid choice");
                break;
        }

    }
}

}
