package com.example.unirtfm.data;

import com.google.gson.annotations.SerializedName;

public class VideoData3 {

    @SerializedName("VIDEO_ID")
    private String videoId;

    @SerializedName("VIDEO_PATH")
    private String videoPath;

    @SerializedName("SENTENCE_INPUT")
    private String sentenceInput;

    @SerializedName("SENTENCE_OUTPUT")
    private String sentenceOutput;

    @SerializedName("EMBEDDINGS_DISTANCES")
    private double embeddingsDistances;

    // Getters y Setters
    public String getVideoId() {
        return videoId;
    }

    public void setVideoId(String videoId) {
        this.videoId = videoId;
    }

    public String getVideoPath() {
        return videoPath;
    }

    public void setVideoPath(String videoPath) {
        this.videoPath = videoPath;
    }

    public String getSentenceInput() {
        return sentenceInput;
    }

    public void setSentenceInput(String sentenceInput) {
        this.sentenceInput = sentenceInput;
    }

    public String getSentenceOutput() {
        return sentenceOutput;
    }

    public void setSentenceOutput(String sentenceOutput) {
        this.sentenceOutput = sentenceOutput;
    }

    public double getEmbeddingsDistances() {
        return embeddingsDistances;
    }

    public void setEmbeddingsDistances(double embeddingsDistances) {
        this.embeddingsDistances = embeddingsDistances;
    }
}
