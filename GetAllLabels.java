/*
Reference : https://cloud.google.com/vision/docs/reference/libraries
The Vision API, and all the code for sending images and receiving labels have been taken from the above reference.
I DON'T claim any ownership for most of the code in this file.
*/

/*
Program description:
Given the path to a folder that contains a list of images, this folder calls the Google's image recognition API 
and prints all labels for the images. (USing Eclipse to mirror the console output to a file)
*/
package com.google.cloud.google_cloud;

import com.google.cloud.vision.v1.AnnotateImageRequest;
import com.google.cloud.vision.v1.AnnotateImageResponse;
import com.google.cloud.vision.v1.BatchAnnotateImagesResponse;
import com.google.cloud.vision.v1.EntityAnnotation;
import com.google.cloud.vision.v1.Feature;
import com.google.cloud.vision.v1.Feature.Type;
import com.google.cloud.vision.v1.Image;
import com.google.cloud.vision.v1.ImageAnnotatorClient;
import com.google.protobuf.ByteString;

//import java.io.BufferedWriter;
import java.io.File;
//import java.io.FileWriter;
//import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
//import java.util.stream.Stream;
import java.util.Set; 
import java.util.TreeSet;

public class GetAllLabels {
  public static void main(String... args) throws Exception {
    // Instantiates a client
    try (ImageAnnotatorClient vision = ImageAnnotatorClient.create()) {
      
        //THIS IS THE PART THAT READS THE FOLDER.
      String folderName = "/Users/chitti/Desktop/CloudComputingS3uploads"; //Add folder that contains all the .jpeg and .jpg
      String fileName = null;
      
      
    File f = new File(folderName);
    File[] allfiles = f.listFiles();
    Path[] allpaths = new Path[allfiles.length];
      
      for(int i=0;i<allfiles.length;i++)
          allpaths[i] = allfiles[i].toPath();
      
      /*for(int i=0;i<allpaths.length;i++)
      {
          fileName = allpaths[i].toString();
          System.out.println(fileName.substring(fileName.length()-3, fileName.length()));
      }*/
      Set<String> l = new TreeSet<String>();
      //int counter = 1;
      
      for(Path p : allpaths)
      {
            //System.out.println(counter);
            //counter++;
            fileName = p.toString();
            
            String check1 = fileName.substring(fileName.length()-3, fileName.length());
            String check2 = fileName.substring(fileName.length()-4, fileName.length());
            
            if(!((check1.equals("jpg")) || check2.equals("jpeg")))
              continue;

        // Reads the image file into memory
        Path path = Paths.get(fileName);
        byte[] data = Files.readAllBytes(path);
        ByteString imgBytes = ByteString.copyFrom(data);
        
        //System.out.println("Hola!");
  
        // Builds the image annotation request
        List<AnnotateImageRequest> requests = new ArrayList<AnnotateImageRequest>();
        Image img = Image.newBuilder().setContent(imgBytes).build();
        Feature feat = Feature.newBuilder().setType(Type.LABEL_DETECTION).build();
        AnnotateImageRequest request = AnnotateImageRequest.newBuilder()
            .addFeatures(feat)
            .setImage(img)
            .build();
        requests.add(request);
  
        // Performs label detection on the image file
        BatchAnnotateImagesResponse response = vision.batchAnnotateImages(requests);
        List<AnnotateImageResponse> responses = response.getResponsesList();
  
        for (AnnotateImageResponse res : responses) {
          if (res.hasError()) {
            System.out.printf("Error: %s\n", res.getError().getMessage());
            return;
          }
          //FileWriter fwriter = new FileWriter("/Users/chitti/Desktop/labels.txt");
          //BufferedWriter bwriter = new BufferedWriter(fwriter);
          
          
          for (EntityAnnotation annotation : res.getLabelAnnotationsList()) 
          {
            annotation.getAllFields().forEach((k, v)->{
                /*try{bwriter.write(v.toString() +"\n");}catch(Exception e) {};
            });*/
              //annotation.getDescription()
              String toput = annotation.getDescription();
              if(!(l.contains(toput)))
                {
                  l.add(toput);
                  //System.out.printf(annotation.getDescription() +"\n");
                }
              });
              //bwriter.close();
          }
        }
      }
      
      //System.out.println(counter);
      for(String s: l)
      {
          System.out.println(s);
      }
    }
  }
}