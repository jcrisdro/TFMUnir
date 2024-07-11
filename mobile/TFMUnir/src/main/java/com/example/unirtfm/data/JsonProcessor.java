package com.example.unirtfm.data;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.util.ArrayList;
import java.util.List;

public class JsonProcessor {

    public static List<ObjectosDetectados> processJson(String jsonString) {
        List<ObjectosDetectados> carList = new ArrayList<>();

        JsonObject jsonObject = JsonParser.parseString(jsonString).getAsJsonObject();
        JsonArray objectsArray = jsonObject.getAsJsonArray("objects");

        for (int i = 0; i < objectsArray.size(); i++) {
            JsonObject carObject = objectsArray.get(i).getAsJsonObject();
            String name = carObject.get("name").getAsString();
            String color = carObject.get("color").getAsString();
            double distance = carObject.get("distance").getAsDouble();

            ObjectosDetectados car = new ObjectosDetectados(name, color, distance);
            carList.add(car);
        }

        return carList;
    }
}
