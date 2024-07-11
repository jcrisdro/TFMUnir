package com.example.unirtfm.service;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitClient {
    private static  String BASE_URL;
    private static Retrofit retrofit = null;

    public static Retrofit getClient(String BASE_URL2) {
        if (retrofit == null) {
            BASE_URL = BASE_URL2;
            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
}
