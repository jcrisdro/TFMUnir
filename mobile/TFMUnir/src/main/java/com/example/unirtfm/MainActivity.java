package com.example.unirtfm;

import android.app.Dialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.view.Menu;

import com.example.consumirwebservice.R;
import com.example.unirtfm.service.ApiClient;
import com.google.android.material.snackbar.Snackbar;
import com.google.android.material.navigation.NavigationView;

import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.appcompat.app.AppCompatActivity;

import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;

import com.example.consumirwebservice.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {

    private AppBarConfiguration mAppBarConfiguration;
    private ActivityMainBinding binding;

    private ApiClient apiClient;
    static DrawerLayout drawer;
    static NavigationView navigationView;
    static NavController navController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        setSupportActionBar(binding.appBarMain.toolbar);
        binding.appBarMain.fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null)
                        .setAnchorView(R.id.fab).show();
            }
        });
        drawer = binding.drawerLayout;
        navigationView = binding.navView;
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        mAppBarConfiguration = new AppBarConfiguration.Builder(
                R.id.nav_home, R.id.nav_gallery, R.id.nav_slideshow)
                .setOpenableLayout(drawer)
                .build();
        navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        NavigationUI.setupActionBarWithNavController(this, navController, mAppBarConfiguration);
        NavigationUI.setupWithNavController(navigationView, navController);




    }

    public static void  SetFragment()
    {
        //navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        //NavigationUI.setupActionBarWithNavController(this, navController);
        //NavigationUI.setupWithNavController(navigationView, navController);
        //navController.navigate(R.id.nav_gallery);
        //Toast.makeText(getContext(), "prueba", Toast.LENGTH_SHORT).show();

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        return NavigationUI.navigateUp(navController, mAppBarConfiguration)
                || super.onSupportNavigateUp();
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.action_settings) {
            //Intent intent = new Intent(this, SettingsActivity.class);
            //startActivity(intent);
            //Toast.makeText(this, "Test", Toast.LENGTH_SHORT).show();
            showCustomDialog();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    private void showCustomDialog() {
        final Dialog dialog = new Dialog(this);
        dialog.setContentView(R.layout.dialog_custom);

        // Ajustar el tamaño del diálogo
        WindowManager.LayoutParams layoutParams = new WindowManager.LayoutParams();
        layoutParams.copyFrom(dialog.getWindow().getAttributes());
        layoutParams.width = WindowManager.LayoutParams.MATCH_PARENT;
        layoutParams.height = WindowManager.LayoutParams.WRAP_CONTENT;
        dialog.getWindow().setAttributes(layoutParams);

        final EditText editTextDialog = dialog.findViewById(R.id.editTextDialog);
        editTextDialog.setText(displaySavedText());
        Button buttonSave = dialog.findViewById(R.id.buttonSave);

        buttonSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String text = editTextDialog.getText().toString();
                saveToSharedPreferences(text);
                dialog.dismiss();
            }
        });

        dialog.show();
    }

    private void saveToSharedPreferences(String text) {
        SharedPreferences sharedPreferences = getSharedPreferences("MyPrefs", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("savedText", text);
        editor.apply();
    }

    private String displaySavedText() {
        SharedPreferences sharedPreferences = getSharedPreferences("MyPrefs", Context.MODE_PRIVATE);
        String savedText = sharedPreferences.getString("savedText", "https://a5e6-181-59-2-3.ngrok-free.app/");
        return savedText;
    }

}