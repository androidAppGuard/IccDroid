package plugins.dataflow;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.lang.reflect.Field;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;

//import android.support.v4.app.Fragment;
//import android.support.v4.app.FragmentActivity;
//gradle.preperties android.useAndroidX=true

public class DataFlowAnalysis extends BroadcastReceiver {

    private static final String TAG = "DataFlowAnalysis";
    private static final String HOST = "127.0.0.1";
    private static final int PORT = 9999;
    private static final String LOCAL_SOCKET_NAME = HOST + "://" + String.valueOf(PORT) + "/816workspace";
    private static ServerSocket serverSocket = null;


    @Override
    public void onReceive(Context context, Intent intent) {
        try {
            startServer();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void startServer() throws IOException {
        if (serverSocket != null) return;
        Log.d(TAG, "Starting server on " + LOCAL_SOCKET_NAME);
        serverSocket = new ServerSocket(PORT);
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        final Socket socket = serverSocket.accept();
                        new Thread(new Runnable() {
                            @Override
                            public void run() {
                                try {
                                    Log.d(TAG, socket.toString() + "one client connected");
                                    // handle client message
                                    handleConnection(socket.getInputStream(), socket.getOutputStream());
                                    socket.close();
                                    Log.d(TAG, socket.toString() + "one client closed");
                                } catch (Exception e) {
                                    e.printStackTrace();
                                }
                            }
                        }).start();
                    } catch (IOException e) {
                        e.printStackTrace();
                        break;
                    }
                }
            }
        }).start();
    }

    private static void handleConnection(InputStream socketIn, OutputStream socketOut) {
        final BufferedReader netInput = new BufferedReader(new InputStreamReader(socketIn));
        final PrintWriter netOutput = new PrintWriter(socketOut, false);
        while (true) {
            String cmd = null;
            try {
                cmd = netInput.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }
            if (cmd == null) continue;
            cmd = cmd.trim();
            StringBuilder response = new StringBuilder();
            if (cmd.equals("getActivityDataflow")) {
                Activity activity = getActivity();
                if (activity == null) {
                    response.append("NoActivity");
                } else {
                    Intent intent = activity.getIntent();
                    Bundle bundle = intent.getExtras();
                    // no data passing
                    if (bundle == null) {
                        response.append("NoDataPassing");
                    } else {
                        response.append("DataPassing_");
                        StringBuilder dataflows = new StringBuilder();
                        for (String key : bundle.keySet()) {
                            Object object = bundle.get(key);
                            String dataflow = dispose(object);
                            dataflows.append(dataflow);
                        }
                        String dataflow_hash = getMd5(dataflows.toString());
                        response.append(dataflow_hash);
                        Log.e("Activity Data Passing", dataflows.toString());
                    }
                }
            } else if (cmd.equals("getFragementDataflow")) {
                response.append("NoFragment");
            } else if (cmd.equals("state")) {
                response.append("true");
            } else if (cmd.equals("exit")) {
                response.append("true");
                netOutput.println(response.toString());
                netOutput.flush();
                break;
            }
            netOutput.println(response.toString());
            netOutput.flush();

        }
        // stream close
        try {
            netInput.close();
            socketIn.close();
            netOutput.close();
            socketOut.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static Activity getActivity() {
        Class activityThreadClass = null;
        try {
            activityThreadClass = Class.forName("android.app.ActivityThread");
            Object activityThread = activityThreadClass.getMethod("currentActivityThread").invoke(null);
            Field activitiesField = activityThreadClass.getDeclaredField("mActivities");
            activitiesField.setAccessible(true);
            Map activities = (Map) activitiesField.get(activityThread);
            for (Object activityRecord : activities.values()) {
                Class activityRecordClass = activityRecord.getClass();
                Field pausedField = activityRecordClass.getDeclaredField("paused");
                pausedField.setAccessible(true);
                if (!pausedField.getBoolean(activityRecord)) {
                    Field activityField = activityRecordClass.getDeclaredField("activity");
                    activityField.setAccessible(true);
                    Activity activity = (Activity) activityField.get(activityRecord);
                    return activity;
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static String getMd5(String text) {
        MessageDigest md5 = null;
        try {
            md5 = MessageDigest.getInstance("MD5");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        byte[] bytes = md5.digest(text.getBytes());
        StringBuilder builder = new StringBuilder();
        for (byte aByte : bytes) {
            builder.append(Integer.toHexString((0x000000FF & aByte) | 0xFFFFFF00).substring(6));
        }
        return builder.toString();
    }

    public static String dispose(Object object) {
        HashSet<String> types = new HashSet<>(Arrays.asList("boolean", "java.lang.Boolean", "char", "java.lang.Character", "byte", "java.lang.Byte", "short", "java.lang.Short", "int", "java.lang.Integer", "long", "java.lang.Long", "float", "java.lang.Float", "double", "java.lang.Double", "java.lang.String"));
        if (types.contains(object.getClass().getName())) return String.valueOf(object);
        StringBuilder dataflow = new StringBuilder();
        Class cls = object.getClass();
        Field[] fields = cls.getDeclaredFields();
        for (int i = 0; i < fields.length; i++) {
            Field field = fields[i];
            field.setAccessible(true);
            String field_class = field.getGenericType().toString();
            if (field_class.startsWith("class")) {
                field_class = field_class.split(" ")[1];
            }
            if (types.contains(field_class)) {
                try {
                    dataflow.append(String.valueOf(field.get(object)) + "_");
                } catch (IllegalAccessException e) {
                    e.printStackTrace();
                }
            }
        }
        return dataflow.toString();
    }
}
