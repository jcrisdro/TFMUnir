package com.example.unirtfm.data;


public class ObjectosDetectados {
    private String name;
    private String color;
    private double distance;

    public ObjectosDetectados(String name, String color, double distance) {
        this.name = name;
        this.color = color;
        this.distance = distance;
    }

    public String getName() {
        return name;
    }

    public String getColor() {
        return color;
    }

    public double getDistance() {
        return distance;
    }

    @Override
    public String toString() {
        String result = String.format("%.2f",distance);

        return  "The object is a '" + name + '\'' +
                //", Color='" + color + '\'' +
                ", is at a distance of " +result+" meters. \n \n";
    }
}
