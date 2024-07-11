package com.example.unirtfm.ui.sign_language;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class SignLanguageViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public SignLanguageViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is sign_language fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}