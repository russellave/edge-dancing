package levy.cs.wlu.edu.bluetoothclient;

import java.util.ArrayList;
import java.util.List;
import java.util.Observable;

public class LightState extends Observable {
    private String lightInfo = "";
    private List<MyCommunicationsActivity> mcas = new ArrayList<>();

    public void setLightInfo(String info) {
        synchronized (this) {
            this.lightInfo = info;
        }
        setChanged();
        notifyObservers();
    }

    public synchronized String getLightInfo() {
        return lightInfo;
    }
}
