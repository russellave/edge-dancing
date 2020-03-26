package levy.cs.wlu.edu.bluetoothclient;

import java.util.HashSet;
import java.util.Observable;
import java.util.Observer;
import java.util.TimerTask;

public class MyTimerTask extends TimerTask {
    private CommunicationsTask mBluetoothConnection;
    private char c;
    private String s;
    private LightState ls;
    private HashSet<String> possibleIndex = new HashSet<>();
    private HashSet<String> possibleColor = new HashSet<>();
    private int minIndex = 1;
    private int maxIndex = 15;

    public MyTimerTask(CommunicationsTask bt, MyCommunicationsActivity mca) {
        this.mBluetoothConnection = bt;
        this.c = Character.MIN_VALUE;
        s = "";
        ls = new LightState();
        ls.addObserver(mca);
        for(int i = minIndex; i<=maxIndex; i++){
            possibleIndex.add(Integer.toString(i));
        }

    }

    @Override
    public void run() {
//        for (byte b : str.getBytes()) {
//            mBluetoothConnection.write();
//        }
        //tell server ready to read
        mBluetoothConnection.write((byte) ',');

        //tell server signal done
        mBluetoothConnection.write((byte)'.');


        s = "";
        while (mBluetoothConnection.available() > 0) {
            c = (char) mBluetoothConnection.read();
            if(c == '.' && s.length()>0) {
                ls.setLightInfo(s);
                if(possibleIndex.contains(s)){
                    break;
                }
            }
            else{
                s += c;
            }
        }
    }

    public LightState getLS() {
        return ls;
    }
}