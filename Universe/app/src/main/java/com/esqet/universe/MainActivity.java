package com.esqet.universe;

import android.content.Intent;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Start the Chronos Modulator Service immediately
        Intent chronosIntent = new Intent(this, ChronosModulatorService.class);
        startForegroundService(chronosIntent); 
        
        // Note: The GLSurfaceView (HolographicUniverseView) should be initialized 
        // and attached here or in the XML layout.
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Consider stopping the Chronos Modulator only when truly necessary
        // Intent chronosIntent = new Intent(this, ChronosModulatorService.class);
        // stopService(chronosIntent);
    }
}
