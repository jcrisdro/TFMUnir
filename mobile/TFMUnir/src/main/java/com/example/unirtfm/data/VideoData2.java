package com.example.unirtfm.data;

public class VideoData2 {
    private String VIDEO_ID;
    private String VIDEO_PATH;
    private String SENTENCE_INPUT;
    private String SENTENCE_OUTPUT;
   // private double[] EMBEDDINGS_DISTANCES;

    // Getters and Setters
    public String getVIDEO_ID() {
        return VIDEO_ID;
    }

    public void setVIDEO_ID(String VIDEO_ID) {
        this.VIDEO_ID = VIDEO_ID;
    }

    public String getVIDEO_PATH() {
        return VIDEO_PATH;
    }

    public void setVIDEO_PATH(String VIDEO_PATH) {
        this.VIDEO_PATH = VIDEO_PATH;
    }

    public String getSENTENCE_INPUT() {
        return SENTENCE_INPUT;
    }

    public void setSENTENCE_INPUT(String SENTENCE_INPUT) {
        this.SENTENCE_INPUT = SENTENCE_INPUT;
    }

    public String getSENTENCE_OUTPUT() {
        return SENTENCE_OUTPUT;
    }

    public void setSENTENCE_OUTPUT(String SENTENCE_OUTPUT) {
        this.SENTENCE_OUTPUT = SENTENCE_OUTPUT;
    }

   /* public double[] getEMBEDDINGS_DISTANCES() {
        return EMBEDDINGS_DISTANCES;
    }*/

   /* public void setEMBEDDINGS_DISTANCES(double[] EMBEDDINGS_DISTANCES) {
        this.EMBEDDINGS_DISTANCES = EMBEDDINGS_DISTANCES;
    }*/
}
