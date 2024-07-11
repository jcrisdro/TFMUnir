// SignLanguageFragment.java

package com.example.unirtfm.ui.sign_language;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.VideoView;
import android.widget.MediaController;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.unirtfm.service.ApiClient;
import com.example.unirtfm.data.VideoData;
import com.example.unirtfm.data.VideoData2;
import com.example.unirtfm.data.VideoData3;
import com.example.consumirwebservice.databinding.FragmentGalleryBinding;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonSyntaxException;

import org.jetbrains.annotations.Nullable;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Locale;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Response;


public class SignLanguageFragment extends Fragment {

    private FragmentGalleryBinding binding;
    private TextView videoIdTextView;
    private VideoView videoView;
    private TextView sentenceInputTextView;
    private TextView sentenceOutputTextView;
    private TextView embeddingsDistancesTextView;

    private static final int REQUEST_CODE_SPEECH_INPUT = 1000;
    private TextView TextOut;
    private ImageButton button;
    private ApiClient apiClient;

    ProgressDialog progressDialog;

    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        SignLanguageViewModel galleryViewModel = new ViewModelProvider(this).get(SignLanguageViewModel.class);

        binding = FragmentGalleryBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        videoIdTextView = binding.videoIdTextView;
        videoView = binding.videoView;
        sentenceInputTextView = binding.sentenceInputTextView;
        sentenceOutputTextView = binding.sentenceOutputTextView;
        embeddingsDistancesTextView = binding.embeddingsDistancesTextView;
        TextOut = binding.TextOut;
        button = binding.button;


        MediaController mediaController = new MediaController(getContext());

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startVoiceInput();
            }
        });

      //GetData(" Many families begin to home school not because of concerns of academics or because of concerns of the local public or private school because they are concerned about things relative to the family.");
       //new FetchJsonDataTask().execute("http://192.168.100.244:8080/api/service1.php?param=All right I'm back, I'm just doing a little fast clean up.");

        return root;
    }

    public void GetData(String Sentece ){
        ////
        progressDialog = new ProgressDialog(getContext());
        progressDialog.setMessage("Please Wait .......");

        apiClient = new ApiClient(displaySavedText(getContext())+"v1/run/models/hamodel");
        //apiClient = new ApiClient("https://a5e6-181-59-2-3.ngrok-free.app/v1/run/models/hamodel");
        // Ruta del archivo a enviar (ajusta la ruta según tu archivo)
        File file = new File("/path/to/your/file");

        // Realizar la solicitud POST con el archivo adjunto
        apiClient.postRequestWithFile(Sentece, file, new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("MainActivity", "Error: " + e.getMessage());

            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    String responseBody = response.body().string();

                    ////
                   VideoData2 videoData =GetParams(responseBody);
                    Log.i("MainActivity", "Response ==> getVIDEO_ID : " + videoData.getVIDEO_ID().toString());

                    try {
                       // videoIdTextView.setText(videoData.getVIDEO_ID());
                        sentenceInputTextView.setText(videoData.getSENTENCE_INPUT());
                        sentenceOutputTextView.setText(videoData.getSENTENCE_OUTPUT());
                        //embeddingsDistancesTextView.setText(arrayToString(videoData.getEMBEDDINGS_DISTANCES()));
                    }catch (Exception e)
                    {
                        Log.e("SignLanguageFragment", "Failed Erro1 "+e.getMessage() );
                        progressDialog.dismiss();

                    }



                    String videoPath = videoData.getVIDEO_PATH();
                    //File videoFile = convertHexToFile(videoPath);
                    File videoFile = convertBase64ToFile(videoPath, "video.mp4");

                    if (videoFile != null) {
                        // Ensure the following code runs on the main thread
                        getActivity().runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                try {
                                    videoView.setVideoPath(videoFile.getAbsolutePath());
                                    MediaController mediaController = new MediaController(getContext());
                                    mediaController.setAnchorView(videoView);
                                    videoView.setMediaController(mediaController);
                                    videoView.start();

                                    progressDialog.dismiss();
                                }catch (Exception e)
                                {
                                    progressDialog.dismiss();
                                }

                               // Log.e("SignLanguageFragment", "videoFile.getAbsolutePath()==>"+videoFile.getAbsolutePath());
                            }
                        });
                    } else {
                        Log.e("SignLanguageFragment", "Failed to convert hex to file");
                        progressDialog.dismiss();
                    }

                    Log.i("MainActivity", "Response: " + responseBody);
                    videoView.start();
                }
            }
        });
    }

    public void GetData_old(String sentence) {
        new GetDataTask().execute(sentence);
    }

    private class GetDataTask extends AsyncTask<String, Void, VideoData2> {
        private ProgressDialog progressDialog;
        private Exception exception;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            progressDialog = new ProgressDialog(getContext());
            progressDialog.setMessage("Please Wait .......");
            progressDialog.show();
        }

        @Override
        protected VideoData2 doInBackground(String... params) {
            String sentence = params[0];
            apiClient = new ApiClient(displaySavedText(getContext()));
            File file = new File("/path/to/your/file");

            try {
                Response response = apiClient.postRequestWithFileSync(sentence, file);
                if (response.isSuccessful()) {
                    String responseBody = response.body().string();
                    return GetParams(responseBody);
                } else {
                    throw new IOException("Unexpected code " + response);
                }
            } catch (IOException e) {
                this.exception = e;
                return null;
            }
        }

        @Override
        protected void onPostExecute(VideoData2 videoData) {
            super.onPostExecute(videoData);
            //progressDialog.dismiss();

            if (exception != null) {
                Log.e("MainActivity", "Error: " + exception.getMessage());
                return;
            }

            if (videoData != null) {
                Log.i("MainActivity", "Response ==> getVIDEO_ID : " + videoData.getVIDEO_ID().toString());

                try {
                    videoIdTextView.setText(videoData.getVIDEO_ID());
                    sentenceInputTextView.setText(videoData.getSENTENCE_INPUT());
                    sentenceOutputTextView.setText(videoData.getSENTENCE_OUTPUT());
                    // embeddingsDistancesTextView.setText(arrayToString(videoData.getEMBEDDINGS_DISTANCES()));
                } catch (Exception e) {
                    Log.e("SignLanguageFragment", "Failed Erro1 " + e.getMessage());
                    return;
                }

                String videoPath = videoData.getVIDEO_PATH();
                // File videoFile = convertHexToFile(videoPath);
                File videoFile = convertBase64ToFile(videoPath, "video.mp4");

                            videoView.setVideoPath(videoFile.getAbsolutePath());
                            MediaController mediaController = new MediaController(getContext());
                            mediaController.setAnchorView(videoView);
                            videoView.setMediaController(mediaController);
                            videoView.start();
                            progressDialog.dismiss();

            }
        }
    }

    private File convertBase64ToFile(String base64, String fileName) {
        File videoFile = null;
        try {
            // Crear archivo temporal
            videoFile = new File(getContext().getCacheDir(), fileName);
            byte[] decodedBytes = Base64.decode(base64, Base64.DEFAULT);

            // Escribir bytes decodificados en el archivo
            try (FileOutputStream fos = new FileOutputStream(videoFile)) {
                fos.write(decodedBytes);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return videoFile;
    }
    private String arrayToString(double[] array) {
        StringBuilder stringBuilder = new StringBuilder();
        for (double value : array) {
            stringBuilder.append(value).append(", ");
        }
        return stringBuilder.length() > 0 ? stringBuilder.substring(0, stringBuilder.length() - 2) : "";
    }

    private File convertHexToFile(String hexData) {
        try {
            byte[] bytes = hexStringToByteArray(hexData);
            File outputDir = getContext().getFilesDir(); // Use the internal storage cache directory getCacheDir();
            File outputFile = File.createTempFile("video", ".mp4", outputDir);
            BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(outputFile));
            bos.write(bytes);
            bos.close();
            return outputFile;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    private byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i + 1), 16));
        }
        return data;
    }

    protected VideoData2 GetParams(String response){
        Gson gson = new GsonBuilder().create();
        return gson.fromJson(response, VideoData2.class);
    }

    private void startVoiceInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Hi, speak something");

        try {
            startActivityForResult(intent, REQUEST_CODE_SPEECH_INPUT);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQUEST_CODE_SPEECH_INPUT) {
            if (resultCode == getActivity().RESULT_OK && data != null) {
                ArrayList<String> result = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                if (result != null && !result.isEmpty()) {
                    TextOut.setText(result.get(0));
                    GetData(result.get(0));
                    //new FetchJsonDataTask().execute("https://brainsofttechdom.com/api/service1.php");
                }
            }
        }
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    private class FetchJsonDataTask_old extends AsyncTask<String, Void, VideoData> {
        @Override
        protected VideoData doInBackground(String... urls) {
            try {
                URL url = new URL(urls[0]);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");
                int responseCode = urlConnection.getResponseCode();

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String inputLine;

                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();
                    Gson gson = new GsonBuilder().create();
                    return gson.fromJson(response.toString(), VideoData.class);
                } else {
                    Log.e("FetchJsonDataTask", "GET request failed: " + responseCode);
                }
            } catch (Exception e) {
                e.printStackTrace();
                Log.e("FetchJsonDataTask", "Exception: " + e.getMessage());
            }
            return null;
        }

        @Override
        protected void onPostExecute(VideoData videoData) {
            if (videoData != null) {
                videoIdTextView.setText(videoData.getVIDEO_ID());
                sentenceInputTextView.setText(videoData.getSENTENCE_INPUT());
                sentenceOutputTextView.setText(videoData.getSENTENCE_OUTPUT());
                embeddingsDistancesTextView.setText(arrayToString(videoData.getEMBEDDINGS_DISTANCES()));

                String videoPath = videoData.getVIDEO_PATH();
                File videoFile = convertHexToFile(videoPath);
                if (videoFile != null) {
                    videoView.setVideoPath(videoFile.getAbsolutePath());
                    MediaController mediaController = new MediaController(getContext());
                    mediaController.setAnchorView(videoView);
                    videoView.setMediaController(mediaController);
                    videoView.start();
                } else {
                    Log.e("SignLanguageFragment", "Failed to convert hex to file");
                }
            } else {
                Log.e("SignLanguageFragment", "Failed to fetch JSON");
            }
        }

        private String arrayToString(double[] array) {
            StringBuilder stringBuilder = new StringBuilder();
            for (double value : array) {
                stringBuilder.append(value).append(", ");
            }
            return stringBuilder.length() > 0 ? stringBuilder.substring(0, stringBuilder.length() - 2) : "";
        }

        private File convertHexToFile(String hexData) {
            try {
                byte[] bytes = hexStringToByteArray(hexData);
                File outputDir = getContext().getCacheDir(); // Use the internal storage cache directory
                File outputFile = File.createTempFile("video", ".mp4", outputDir);
                BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(outputFile));
                bos.write(bytes);
                bos.close();
                return outputFile;
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }

        private byte[] hexStringToByteArray(String s) {
            int len = s.length();
            byte[] data = new byte[len / 2];
            for (int i = 0; i < len; i += 2) {
                data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                        + Character.digit(s.charAt(i + 1), 16));
            }
            return data;
        }


    }

    private class FetchJsonDataTask_conv_Video extends AsyncTask<String, Void, VideoData> {
        @Override
        protected VideoData doInBackground(String... urls) {
            try {
                URL url = new URL(urls[0]);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");
                int responseCode = urlConnection.getResponseCode();

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String inputLine;

                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();
                    Gson gson = new GsonBuilder().create();
                    return gson.fromJson(response.toString(), VideoData.class);
                } else {
                    Log.e("FetchJsonDataTask", "GET request failed: " + responseCode + " " + urlConnection.getResponseMessage());
                }
            } catch (Exception e) {
                e.printStackTrace();
                Log.e("FetchJsonDataTask", "Exception: " + e.getMessage());
            }
            return null;
        }

        @Override
        protected void onPostExecute(VideoData videoData) {
            if (videoData != null) {
                videoIdTextView.setText(videoData.getVIDEO_ID());
                sentenceInputTextView.setText(videoData.getSENTENCE_INPUT());
                sentenceOutputTextView.setText(videoData.getSENTENCE_OUTPUT());
                embeddingsDistancesTextView.setText(arrayToString(videoData.getEMBEDDINGS_DISTANCES()));

                String videoPath = videoData.getVIDEO_PATH();
                //File videoFile = convertHexToFile(videoPath);
                File videoFile = convertBase64ToFile(videoPath, "video.mp4");
                if (videoFile != null) {
                    videoView.setVideoPath(videoFile.getAbsolutePath());
                    MediaController mediaController = new MediaController(getContext());
                    mediaController.setAnchorView(videoView);
                    videoView.setMediaController(mediaController);
                    videoView.start();
                } else {
                    Log.e("SignLanguageFragment", "Failed to convert hex to file");
                }
            } else {
                Log.e("SignLanguageFragment", "Failed to fetch JSON");
            }
        }

        private File convertBase64ToFile(String base64, String fileName) {
            File videoFile = null;
            try {
                // Crear archivo temporal
                videoFile = new File(getContext().getCacheDir(), fileName);
                byte[] decodedBytes = Base64.decode(base64, Base64.DEFAULT);

                // Escribir bytes decodificados en el archivo
                try (FileOutputStream fos = new FileOutputStream(videoFile)) {
                    fos.write(decodedBytes);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            return videoFile;
        }

        private String arrayToString(double[] array) {
            StringBuilder stringBuilder = new StringBuilder();
            for (double value : array) {
                stringBuilder.append(value).append(", ");
            }
            return stringBuilder.length() > 0 ? stringBuilder.substring(0, stringBuilder.length() - 2) : "";
        }

        private File convertHexToFile(String hexData) {
            try {
                byte[] bytes = hexStringToByteArray(hexData);
                File outputDir = getContext().getCacheDir(); // Use the internal storage cache directory
                File outputFile = File.createTempFile("video", ".mp4", outputDir);
                BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(outputFile));
                bos.write(bytes);
                bos.close();
                return outputFile;
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }

        private byte[] hexStringToByteArray(String s) {
            int len = s.length();
            byte[] data = new byte[len / 2];
            for (int i = 0; i < len; i += 2) {
                data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                        + Character.digit(s.charAt(i + 1), 16));
            }
            return data;
        }
    }

    private class FetchJsonDataTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... urls) {
            try {
                URL url = new URL(urls[0]);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");
                int responseCode = urlConnection.getResponseCode();

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String inputLine;

                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();
                    return response.toString();
                } else {
                    Log.e("FetchJsonDataTask", "GET request failed: " + responseCode);
                }
            } catch (Exception e) {
                e.printStackTrace();
                Log.e("FetchJsonDataTask", "Exception: " + e.getMessage());
            }
            return null;
        }

        @Override
        protected void onPostExecute(String jsonString) {
            if (jsonString != null) {
                Gson gson = new GsonBuilder().create();

                try {
                    VideoData3 videoData = gson.fromJson(jsonString, VideoData3.class);
                    System.out.println("VIDEO_ID: " + videoData.getVideoId());
                    System.out.println("VIDEO_PATH: " + videoData.getVideoPath());
                    System.out.println("SENTENCE_INPUT: " + videoData.getSentenceInput());
                    System.out.println("SENTENCE_OUTPUT: " + videoData.getSentenceOutput());
                    System.out.println("EMBEDDINGS_DISTANCES: " + videoData.getEmbeddingsDistances());
                } catch (JsonSyntaxException e) {
                    e.printStackTrace();
                }


                VideoData3 videoData = gson.fromJson(jsonString, VideoData3.class);

                videoIdTextView.setText(videoData.getVideoId());
                //videoView.setVideoPath(videoData.getVIDEO_PATH());
                sentenceInputTextView.setText(videoData.getSentenceInput());
                sentenceOutputTextView.setText(videoData.getSentenceOutput());


                String videoPath = videoData.getVideoPath();
                //File videoFile = convertHexToFile(videoPath);
                File videoFile = convertBase64ToFile(videoPath, "video.mp4");


                if (videoFile != null) {
                    videoView.setVideoPath(videoFile.getAbsolutePath());
                    MediaController mediaController = new MediaController(getContext());
                    mediaController.setAnchorView(videoView);
                    videoView.setMediaController(mediaController);
                    videoView.start();
                } else {
                    Log.e("SignLanguageFragment", "Failed to convert hex to file");
                }
            } else {
                Log.e("MainActivity", "Failed to fetch JSON");
            }
        }

        private File convertBase64ToFile(String base64, String fileName) {
            File videoFile = null;
            try {
                // Crear archivo temporal
                videoFile = new File(getContext().getCacheDir(), fileName);
                byte[] decodedBytes = Base64.decode(base64, Base64.DEFAULT);

                // Escribir bytes decodificados en el archivo
                try (FileOutputStream fos = new FileOutputStream(videoFile)) {
                    fos.write(decodedBytes);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            return videoFile;
        }

        private String arrayToString(double[] array) {
            StringBuilder stringBuilder = new StringBuilder();
            for (double value : array) {
                stringBuilder.append(value).append(", ");
            }
            return stringBuilder.length() > 0 ? stringBuilder.substring(0, stringBuilder.length() - 2) : "";
        }

        private File convertHexToFile(String hexData) {
            try {
                byte[] bytes = hexStringToByteArray(hexData);
                File outputDir = getContext().getCacheDir(); // Use the internal storage cache directory
                File outputFile = File.createTempFile("video", ".mp4", outputDir);
                BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(outputFile));
                bos.write(bytes);
                bos.close();
                return outputFile;
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }

        private byte[] hexStringToByteArray(String s) {
            int len = s.length();
            byte[] data = new byte[len / 2];
            for (int i = 0; i < len; i += 2) {
                data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                        + Character.digit(s.charAt(i + 1), 16));
            }
            return data;
        }

    }

    private String displaySavedText(Context context) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE);
        String savedText = sharedPreferences.getString("savedText", "https://a5e6-181-59-2-3.ngrok-free.app/");
        return savedText;
    }
}




