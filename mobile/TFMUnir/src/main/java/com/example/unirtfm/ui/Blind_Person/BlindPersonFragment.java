package com.example.unirtfm.ui.Blind_Person;

import android.app.ProgressDialog;
import android.content.SharedPreferences;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.speech.tts.TextToSpeech;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.unirtfm.service.ApiService;
import com.example.unirtfm.service.ApiService2;
import com.example.unirtfm.data.JsonProcessor;
import com.example.unirtfm.data.ObjectosDetectados;
import com.example.unirtfm.service.RetrofitClient;
import com.example.unirtfm.service.RetrofitClient2;
import com.example.consumirwebservice.databinding.FragmentSlideshowBinding;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;

import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import android.widget.Toast;

import org.jetbrains.annotations.Nullable;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;


public class BlindPersonFragment extends Fragment implements TextToSpeech.OnInitListener {

    private FragmentSlideshowBinding binding;
    private static final int REQUEST_IMAGE_CAPTURE = 1;
    private static final int REQUEST_PERMISSIONS = 2;
    private String currentPhotoPath;
    private ImageView imageViewResult;

    private TextView textViewName;
    private TextView textViewColor;
    private TextView textViewDistance;
    static final int REQUEST_TAKE_PHOTO = 1;
    String ObjectosEncotrados = "";
    private TextToSpeech textToSpeech;
    private Handler handler = new Handler(Looper.getMainLooper());
    ProgressDialog progressDialog;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        BlindPersonViewModel slideshowViewModel = new ViewModelProvider(this).get(BlindPersonViewModel.class);

        binding = FragmentSlideshowBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        // final TextView textView = binding.textHome;

        ImageButton captureButton = binding.captureButton;
        imageViewResult      = binding.imageViewResult;
        textViewName         = binding.textViewName;
        textViewColor        = binding.textViewColor;
        textViewDistance     = binding.textViewDistance;

        textToSpeech = new TextToSpeech(getActivity(), this);


        captureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (checkPermissions()) {
                    dispatchTakePictureIntent();
                } else {
                    requestPermissions();
                }

                //dispatchTakePictureIntent();

            } //public
        });

        // Nombre del archivo en la carpeta assets
        String fileName = "imagen4.jpg";




        try {
            File file = copyAssetToFile(getContext(), fileName);
           // uploadImage_new(file);
            // Usa el objeto File como necesites
        } catch (IOException e) {
            e.printStackTrace();
        }




        return root;
    }

    private void uploadImage_new(File file) {

        progressDialog = new ProgressDialog(getActivity());
        progressDialog.setMessage("Please Wait .......");
        progressDialog.show();

        RequestBody requestFile = RequestBody.create(MediaType.parse("image/jpeg"), file);
        MultipartBody.Part body = MultipartBody.Part.createFormData("file", file.getName(), requestFile);

        ApiService2 service = RetrofitClient2.getClient(displaySavedText(getActivity())).create(ApiService2.class);
        Call<ResponseBody> call = service.uploadImage(body);

        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                if (response.isSuccessful() && response.body() != null) {
                    try {
                        String responseBody = response.body().string();
                        List<ObjectosDetectados> OjectList = JsonProcessor.processJson(responseBody);


                        ObjectosEncotrados = "";
                        progressDialog.dismiss();

                        for (ObjectosDetectados car : OjectList) {
                           // System.out.println(car.toString());
                             ObjectosEncotrados = ObjectosEncotrados+car.toString();
                            //System.out.println(car.getName());
                        }

                        int cantidad = OjectList.size();

                        speakOut(cantidad+" objects were detected in the image");

                        System.out.println(ObjectosEncotrados);

                        // Delay de 5 segundos (5000 milisegundos)
                        handler.postDelayed(new Runnable() {
                            @Override
                            public void run() {
                                // Llamada al segundo speakOut después del delay
                                speakOut(ObjectosEncotrados);
                            }
                        }, 3000);
                        //speakOut(ObjectosEncotrados);

                        JsonObject jsonObject = JsonParser.parseString(responseBody).getAsJsonObject();

                        JsonObject carObject = jsonObject.getAsJsonArray("objects").get(0).getAsJsonObject();
                        String name = carObject.get("name").getAsString();
                        String color = carObject.get("color").getAsString();
                        double distance = carObject.get("distance").getAsDouble();

                        String pictureBase64 = jsonObject.get("picture").getAsString();
                        byte[] imageBytes = Base64.decode(pictureBase64, Base64.DEFAULT);

                        // Actualizar la interfaz de usuario
                        textViewName.setText(cantidad+" objects were detected in the image");
                        textViewColor.setText(ObjectosEncotrados);
                        //textViewName.setText("Name: " + name);
                        //textViewColor.setText("Color: " + color);
                        //textViewDistance.setText("Distance: " + distance + " meters");

                        Bitmap bitmap = BitmapFactory.decodeByteArray(imageBytes, 0, imageBytes.length);
                        imageViewResult.setImageBitmap(bitmap);
                    } catch (Exception e) {

                        progressDialog.dismiss();
                        Log.e("BlindPersonFragment", "call.enqueue(new Callback<ResponseBody>()  Error ==> "+e.getMessage());
                        textViewName.setText("No object detected");
                        textViewColor.setText("");
                        textViewName.setTextColor(Color.RED);
                        try {
                            InputStream inputStream = getActivity().getAssets().open("nodetectado.jpeg");
                            Bitmap bitmap = BitmapFactory.decodeStream(inputStream);
                            imageViewResult.setImageBitmap(bitmap);
                        } catch (IOException e2) {
                            e2.printStackTrace();
                        }


                    }
                } else {
                    System.out.println("Upload failed: " + response.errorBody().toString());
                    Log.e("BlindPersonFragment", "Upload failed: " + response.errorBody().toString());
                    progressDialog.dismiss();
                }
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                t.printStackTrace();
                Log.e("BlindPersonFragment", "Call<ResponseBody> call, Throwable t" + t.getMessage());
                progressDialog.dismiss();
            }
        });
    }

    private void compressImageFile(File originalFile) throws IOException {
        // Decode the image file into a Bitmap
        Bitmap bitmap = BitmapFactory.decodeFile(originalFile.getAbsolutePath());

        // Compress the bitmap into a byte array
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        int quality = 100;
        bitmap.compress(Bitmap.CompressFormat.JPEG, quality, baos);

        // Reduce the quality to keep the file size around 1.5 MB
        while (baos.toByteArray().length / 1024 > 1500 && quality > 10) {
            baos.reset();
            quality -= 10;
            bitmap.compress(Bitmap.CompressFormat.JPEG, quality, baos);
        }

        // Create a new file for the compressed image
        File compressedImage = new File(originalFile.getParent(), "COMPRESSED_" + originalFile.getName());
        FileOutputStream fos = new FileOutputStream(compressedImage);
        fos.write(baos.toByteArray());
        fos.flush();
        fos.close();

        // Update the currentPhotoPath to the compressed image path
        currentPhotoPath = compressedImage.getAbsolutePath();
    }

    private File copyAssetToFile(Context context, String fileName) throws IOException {
        AssetManager assetManager = context.getAssets();
        InputStream inputStream = assetManager.open(fileName);

        // Crear un archivo temporal en el almacenamiento interno
        File outFile = new File(context.getCacheDir(), fileName);
        FileOutputStream outputStream = new FileOutputStream(outFile);

        byte[] buffer = new byte[1024];
        int bytesRead;
        while ((bytesRead = inputStream.read(buffer)) != -1) {
            outputStream.write(buffer, 0, bytesRead);
        }

        inputStream.close();
        outputStream.close();

        return outFile;
    }

    private String convertImageToBase64FromAssets(String fileName) throws IOException {
        AssetManager assetManager = getContext().getAssets();
        InputStream inputStream = assetManager.open(fileName);
        byte[] bytes = convertInputStreamToByteArray(inputStream);
        inputStream.close();
        return Base64.encodeToString(bytes, Base64.DEFAULT);
    }

    private byte[] convertInputStreamToByteArray(InputStream inputStream) throws IOException {
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int bytesRead;
        while ((bytesRead = inputStream.read(buffer)) != -1) {
            byteArrayOutputStream.write(buffer, 0, bytesRead);
        }
        return byteArrayOutputStream.toByteArray();
    }

    private boolean checkPermissions() {
        return ContextCompat.checkSelfPermission(getContext(), Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED &&
                ContextCompat.checkSelfPermission(getContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED;
    }

    private void requestPermissions() {
        ActivityCompat.requestPermissions(getActivity(),
                new String[]{Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE},
                REQUEST_PERMISSIONS);
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getActivity().getPackageManager()) != null) {
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                Toast.makeText(getContext(), "Error occurred while creating the file", Toast.LENGTH_SHORT).show();
            }
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(getContext(),
                        "com.example.consumirwebservice.fileprovider",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
            }
        }
    }



    @Override
    public void onDestroyView() {

        if (textToSpeech != null) {
            textToSpeech.stop();
            textToSpeech.shutdown();
        }
        super.onDestroyView();
        binding = null;
    }



    @Override
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_TAKE_PHOTO && resultCode == getActivity().RESULT_OK) {
            File file = new File(currentPhotoPath);
            //uploadImage_new(file);

            try {
                compressImageFile(file); // Comprimir la imagen
                uploadImage_new(new File(currentPhotoPath)); // Subir la imagen comprimida
            } catch (IOException e) {
                e.printStackTrace();
            }

          //  Bitmap bitmap = BitmapFactory.decodeFile(currentPhotoPath);
           // imageViewResult.setImageBitmap(bitmap);
        }
    }

    private void uploadImage(File file) {
        ApiService apiService = RetrofitClient.getClient(displaySavedText(getActivity())).create(ApiService.class);

        RequestBody requestFile = RequestBody.create(MediaType.parse("image/jpeg"), file);
        MultipartBody.Part body = MultipartBody.Part.createFormData("file", file.getName(), requestFile);

        Call<ResponseBody> call = apiService.uploadImage(body);
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(getContext(), "Upload successful", Toast.LENGTH_SHORT).show();
                    // Assuming the response contains a base64 encoded image string.
                    try {
                        String base64Image = response.body().string();
                        byte[] decodedString = android.util.Base64.decode(base64Image, android.util.Base64.DEFAULT);
                        android.graphics.Bitmap decodedByte = android.graphics.BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                        imageViewResult.setImageBitmap(decodedByte);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } else {
                    Toast.makeText(getContext(), "Upload failed: " + response.message(), Toast.LENGTH_SHORT).show();
                    Log.e("BlindPersonFragment", "Upload failed: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Toast.makeText(getContext(), "Upload failed: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                Log.e("BlindPersonFragment", "Upload failed: " + t.getMessage());
            }
        });
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == REQUEST_PERMISSIONS) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                dispatchTakePictureIntent();
            } else {
                Toast.makeText(getContext(), "Permissions required to use camera", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void dispatchTakePictureIntent2() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getActivity().getPackageManager()) != null) {
            File photoFile = null;
            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
            if (photoFile != null) {
                Uri photoURI = FileProvider.getUriForFile(getActivity(),
                        "com.example.consumirwebservice.fileprovider",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, REQUEST_TAKE_PHOTO);
            }
        }
    }

    private File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = getActivity().getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,
                ".jpg",
                storageDir
        );

        currentPhotoPath = image.getAbsolutePath();
        //currentPhotoPath = compressImageFile()
        return image;
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            int result = textToSpeech.setLanguage(Locale.US);

            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                System.err.println("Language is not supported");
            } else {
               // buttonSpeak.setEnabled(true);
                //Toast.makeText(getContext(), "Puede leer ", Toast.LENGTH_SHORT).show();
                Log.e("void onInit(int status) ", " Puede leer " );
            }
        } else {
            System.err.println("Initialization failed");
        }
    }

    private void speakOut(String text) {
        textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
    }

    private String displaySavedText(Context context) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE);
        String savedText = sharedPreferences.getString("savedText", "https://a5e6-181-59-2-3.ngrok-free.app/");
        return savedText;
    }


}