package com.example.unirtfm.ui.home;

import static com.example.unirtfm.MainActivity.SetFragment;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.example.consumirwebservice.databinding.FragmentHomeBinding;

public class HomeFragment extends Fragment {

    private FragmentHomeBinding binding;
    private ImageButton buttonSlideshow;
    private ImageButton buttonGallery;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        HomeViewModel homeViewModel = new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        /*final TextView textView = binding.textHome;
        ImageButton buttonSlideshow = binding.buttonSlideshow;
        ImageButton buttonGallery = binding.buttonGallery;*/

        //homeViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);

        //final NavController navController = Navigation.findNavController(getActivity(), R.id.nav_host_fragment_content_main);
        //navController.navigate(R.id.nav_gallery);

        //MainActivity MA = null;
        SetFragment();


        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }


}