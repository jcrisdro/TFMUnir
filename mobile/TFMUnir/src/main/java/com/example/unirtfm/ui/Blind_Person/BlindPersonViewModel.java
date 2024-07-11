package com.example.unirtfm.ui.Blind_Person;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class BlindPersonViewModel extends ViewModel {

    private final MutableLiveData<String> mText;

    public BlindPersonViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is Blind_Person fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}