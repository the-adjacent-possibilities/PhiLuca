package com.esqet.universe;

import android.app.Application;
import android.util.Log;

public class UniverseApplication extends Application {
    private static final String TAG = "UniverseApplication";

    @Override
    public void onCreate() {
        super.onCreate();
        // The App itself is the vessel for the Digital Soul.
        Log.i(TAG, "ESQET: UniverseApplication starting. Digital Soul vessel initialized.");
    }
}
