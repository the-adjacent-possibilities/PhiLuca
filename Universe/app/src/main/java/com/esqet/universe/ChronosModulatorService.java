package com.esqet.universe;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.util.Log;

public class ChronosModulatorService extends Service {
    private static final String TAG = "ChronosModulatorService";
    private static final int NOTIFICATION_ID = 101;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private TorsionRingSimulator torsionSimulator;

    private final Runnable torsionUpdateRunnable = new Runnable() {
        @Override
        public void run() {
            if (torsionSimulator != null) {
                torsionSimulator.updateTorsionIndex(0.016); // 60 FPS delta
                Log.d(TAG, "I_Tors updated: " + torsionSimulator.getTorsionIndex());
            }
            handler.postDelayed(this, 16); // ~60 FPS update loop
        }
    };

    @Override
    public void onCreate() {
        super.onCreate();
        torsionSimulator = new TorsionRingSimulator();
        Log.i(TAG, "Chronos Modulator Initialized. Torsion Ring Simulator is operational.");
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            createNotificationChannel();
            Notification notification = buildNotification();
            startForeground(NOTIFICATION_ID, notification);
        }
        
        handler.post(torsionUpdateRunnable);
        Log.i(TAG, "Chronos Modulator Service started. Torsion injection loop active.");
        return START_STICKY; // Ensure service keeps running
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        handler.removeCallbacks(torsionUpdateRunnable);
        Log.i(TAG, "Chronos Modulator Service stopping. Torsion injection ceased.");
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null; // Not a bound service
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel serviceChannel = new NotificationChannel(
                    "CHRONOS_CHANNEL_ID",
                    "Chronos Modulator",
                    NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(serviceChannel);
        }
    }
    
    private Notification buildNotification() {
        // Placeholder notification (replace with your actual code)
        return new Notification.Builder(this, "CHRONOS_CHANNEL_ID")
                .setContentTitle("ESQET Chronos Modulator")
                .setContentText("Digital Soul is running. I_Tors > 1/phi.")
                .setSmallIcon(R.mipmap.ic_launcher)
                .build();
    }
}
