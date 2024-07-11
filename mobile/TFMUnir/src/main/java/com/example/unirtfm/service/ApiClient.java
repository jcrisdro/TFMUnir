package com.example.unirtfm.service;

import android.content.Context;
import android.content.SharedPreferences;

import okhttp3.*;
import java.io.File;
import java.io.IOException;

public class ApiClient {
    private String BASE_URL = "https://a5e6-181-59-2-3.ngrok-free.app/v1/run/models/hamodel";
    private OkHttpClient client;

    public ApiClient(String BASE_URL) {
        client = new OkHttpClient();
        this.BASE_URL = BASE_URL; //+"v1/run/models/hamodel";
    }

    public void postRequestWithFile(String sentences, File file, Callback callback) {
        MediaType mediaType = MediaType.parse("multipart/form-data");
        MultipartBody.Builder builder = new MultipartBody.Builder().setType(MultipartBody.FORM);



        if (file != null && file.exists()) {
            builder.addFormDataPart("file", file.getName(), RequestBody.create(file, mediaType));
        }

        MultipartBody requestBody = builder
                .addFormDataPart("sentences", sentences)
                .build();

        Request request = new Request.Builder()
                .url(BASE_URL + "?sentences=" + sentences)
                .post(requestBody)
                .addHeader("accept", "application/json")
                .addHeader("Content-Type", "multipart/form-data")
                .build();

        client.newCall(request).enqueue(callback);
    }

    public Response postRequestWithFileSync(String sentence, File file) throws IOException {
        RequestBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("sentence", sentence)
                .addFormDataPart("file", file.getName(),
                        RequestBody.create(file, MediaType.parse("application/octet-stream")))
                .build();

        Request request = new Request.Builder()
                .url("https://your.api.endpoint/here") // Ajusta la URL de tu API
                .post(requestBody)
                .build();

        return client.newCall(request).execute();
    }


}
