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
    private int refreshRate = 500; //ms

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        mMessageTextView = (TextView) findViewById(R.id.serverReplyText);

        mButton = (Button) findViewById((R.id.start));


        mButton.setOnClickListener(new View.OnClickListener() {
            @Override

            public void onClick(View v) {
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
        try{
            int result = Integer.parseInt(mMessageFromServer);
            if(result>=minIndex && result<=maxIndex){
                changeColor(Integer.toString(result), Color.RED);
            }
        }
        catch (IllegalArgumentException e){

        }
    }

    public void changeColor(String buID, int color){
        findViewById(getResources().getIdentifier("b"+buID, "id", getPackageName())).setBackgroundColor((color));
    }

}








