mport java.util.Random;

public class Main {

    public static void main(String[] args) {
        
        int[] bitSequence = generateRandomBitSequence(128);

       
        for (int bit : bitSequence) {
            System.out.print(bit);
        }
    }

    public static int[] generateRandomBitSequence(int length) {
        
        Random random = new Random();

        
        int[] bitSequence = new int[length];

        
        for (int i = 0; i < bitSequence.length; i++) {
            bitSequence[i] = random.nextInt(2);
        }
        return bitSequence;
    }

}