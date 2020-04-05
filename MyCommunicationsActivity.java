/*
Simple example of a Bluetooth communications activity
Provides a seek-bar (slider) to send values to the server, and a text widget to display the server's reply
Copyright 2018  Gunnar Bowman, Emily Boyes, Trip Calihan, Simon D. Levy, Shepherd Sims
MIT License
*/


package levy.cs.wlu.edu.bluetoothclient;

import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.IOException;
import java.util.HashMap;
import java.util.Observable;
import java.util.Observer;
import java.util.Timer;
import java.util.TimerTask;

public class MyCommunicationsActivity extends CommunicationsActivity implements Observer {

    private String mMessageFromServer = "";

    private TextView mMessageTextView;
    private Button mButton;
    private MyCommunicationsActivity mca = this;
    private int minIndex = 1;
    private int maxIndex = 15;
    private int refreshRate = 25; //ms
    private HashMap<Character, Integer> colormap = new HashMap<>();


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        mMessageTextView = (TextView) findViewById(R.id.serverReplyText);

        mButton = (Button) findViewById((R.id.start));


        mButton.setOnClickListener(new View.OnClickListener() {
            @Override

            public void onClick(View v) {
                //request color map information
                for(byte b: "color.".getBytes())
                    mBluetoothConnection.write(b);

                Timer t = new Timer();
                MyTimerTask mt = new MyTimerTask(mBluetoothConnection, mca);
                t.schedule(mt, 0, refreshRate);
            }

        });
    }
    @Override
    public void onDestroy() {
        super.onDestroy();
    }


    @Override
    public void update(Observable o, Object arg){
        mMessageFromServer = ((LightState) o).getLightInfo();
        runOnUiThread(new Runnable(){
            @Override
            public void run(){
                mMessageTextView.setText(mMessageFromServer);
            }

        });
        System.out.println("UPDATINGGGGGGGGGGGGGGGGGG");
        System.out.println(mMessageFromServer);

        //do stuff from message
        try{
            //initialize color map at start
            if(mMessageFromServer.split(":")[0].equals("col")){
                String colorString = mMessageFromServer.split(":")[1];
                for(String rgb: colorString.split("_")){
                    char k = rgb.charAt(0);
                    int r = makeValidColor(Integer.parseInt(rgb.substring(1, 4)));
                    int g = makeValidColor(Integer.parseInt(rgb.substring(4, 7)));
                    int b = makeValidColor(Integer.parseInt(rgb.substring(7, 10)));
                    int myColor = Color.rgb(r, b, g);
                    colormap.put(k, myColor);
                }
                for(byte b: "start.".getBytes()) {
                    mBluetoothConnection.write(b);
                }

            }

            else {
                //change color live
                int index = 1;
                for (char c : mMessageFromServer.toCharArray()) {
                    if (colormap.containsKey(c)) {

                        changeColor(Integer.toString(index), colormap.get(c));
                        index++;
                    }
                }
            }

        }
        catch(ArrayIndexOutOfBoundsException e){

        }

    }

    public int makeValidColor(int col){
        if(col>255) return 255;
        if(col<0) return 0;
        return col;
    }

    public void changeColor(String buID, int color){
        findViewById(getResources().getIdentifier("b"+buID, "id", getPackageName())).setBackgroundColor((color));
    }

    public void BuClick(View view) {
        //send information back
        String id_str= view.getResources().getResourceName(view.getId()).split("/")[1];
        byte[] id = id_str.getBytes();
        //starts at one because id's first char is b (ex. b1 is button 1)
        for(int i = 1; i<id.length; i++){
            mBluetoothConnection.write(id[i]);
        }
        mBluetoothConnection.write((byte)'.');

    }
}








