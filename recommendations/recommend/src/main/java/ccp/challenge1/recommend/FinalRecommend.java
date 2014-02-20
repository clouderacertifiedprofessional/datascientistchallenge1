package com.cloudera.ccp.recommender;

import java.io.File;
import java.io.PrintWriter;
import org.apache.mahout.cf.taste.common.NoSuchItemException;
import org.apache.mahout.cf.taste.common.NoSuchUserException;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.recommender.slopeone.SlopeOneRecommender;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.common.iterator.FileLineIterable;

public class FinalRecommend {
   private static final Float GLOBAL_AVERAGE = 3.6836f;

   public static void main(String[] args) throws Exception {
      DataModel explicitDataModel = new FileDataModel(new File("../explicit.csv"));
      Recommender recommender = new SlopeOneRecommender(explicitDataModel);
      PrintWriter out = new PrintWriter("../Task3Solution.csv");
      File in = new File("../rateme.csv");
      
      for (String testDatum : new FileLineIterable(in)) {
         String[] tokens = testDatum.split(",");
         String itemIdString = tokens[1];
         long userId = Long.parseLong(tokens[0]);
         long itemId = Long.parseLong(itemIdString);
         float estimate;
         
         try {
            estimate = recommender.estimatePreference(userId, itemId);
         } catch(NoSuchUserException e) {
            estimate = GLOBAL_AVERAGE;
         } catch(NoSuchItemException e) {
            estimate = GLOBAL_AVERAGE;
         }
         
         if (Float.isNaN(estimate)) {
            estimate = GLOBAL_AVERAGE;
         }
         
         if (itemId > 50000) {
            int i = itemIdString.lastIndexOf("00");
            
            itemIdString = itemIdString.substring(0, i) + 'e' + itemIdString.substring(i+2);
         }
         
         out.printf("%d,%s,%.4f\n", userId, itemIdString, estimate);
      }
      
      out.close();
   }
}

