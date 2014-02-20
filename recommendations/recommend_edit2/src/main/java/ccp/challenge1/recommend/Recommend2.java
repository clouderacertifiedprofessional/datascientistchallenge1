package com.cloudera.ccp.recommender;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.common.Weighting;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.RMSRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.recommender.GenericItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.recommender.slopeone.MemoryDiffStorage;
import org.apache.mahout.cf.taste.impl.recommender.slopeone.SlopeOneRecommender;
import org.apache.mahout.cf.taste.impl.recommender.svd.ExpectationMaximizationSVDFactorizer;
import org.apache.mahout.cf.taste.impl.recommender.svd.SVDRecommender;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.TanimotoCoefficientSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.Recommender;

public class Recommend2 {
   private static final int ITERATIONS = 10;

   public static void main(String[] args) throws Exception {
      final DataModel ratingDataModel = new FileDataModel(new File("../explicit.csv"));
      final DataModel allDataModel = new FileDataModel(new File("../implicit.csv"));
      final LogLikelihoodSimilarity ll = new LogLikelihoodSimilarity(allDataModel);
      final TanimotoCoefficientSimilarity tanimoto = new TanimotoCoefficientSimilarity(allDataModel);
      RecommenderEvaluator rmse = new RMSRecommenderEvaluator();
      Map<String, RecommenderBuilder> recs = new HashMap<String, RecommenderBuilder>();

      recs.put("Item-item with log-likelihood",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new GenericItemBasedRecommender(dm, ll);
         }
      });
      recs.put("Item-item with Tanimoto",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new GenericItemBasedRecommender(dm, tanimoto);
         }
      });
      recs.put("Slope One unweighted",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SlopeOneRecommender(dm, Weighting.UNWEIGHTED, Weighting.UNWEIGHTED, new MemoryDiffStorage(dm, Weighting.UNWEIGHTED, Long.MAX_VALUE));
         }
      });
      recs.put("Slope One weighted",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SlopeOneRecommender(dm, Weighting.WEIGHTED, Weighting.UNWEIGHTED, new MemoryDiffStorage(dm, Weighting.UNWEIGHTED, Long.MAX_VALUE));
         }
      });
      recs.put("Slope One weighted with stddev",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SlopeOneRecommender(dm, Weighting.WEIGHTED, Weighting.WEIGHTED, new MemoryDiffStorage(dm, Weighting.WEIGHTED, Long.MAX_VALUE));
         }
      });
      recs.put("SVD with EM with 20 features and 10 iterations",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ExpectationMaximizationSVDFactorizer(dm, 20, 10));
         }
      });
      recs.put("SVD with EM with 20 features and 20 iterations",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ExpectationMaximizationSVDFactorizer(dm, 20, 20));
         }
      });
      recs.put("SVD with EM with 20 features and 40 iterations",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ExpectationMaximizationSVDFactorizer(dm, 20, 40));
         }
      });
      recs.put("SVD with EM with 10 features and 20 iterations",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ExpectationMaximizationSVDFactorizer(dm, 10, 20));
         }
      });
      recs.put("SVD with EM with 40 features and 20 iterations",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ExpectationMaximizationSVDFactorizer(dm, 40, 20));
         }
      });

      Map<String, Double> results = new TreeMap<String, Double>();
      
      // Evaluate the various recommenders
      for (String rec: recs.keySet()) {
         double result = 0.0;
         
         for (int i = 0; i < ITERATIONS; i++) {
            result += rmse.evaluate(recs.get(rec), null, ratingDataModel, 0.9, 1.0);
         }

         results.put(rec, result / ITERATIONS);
      }
   
      // Print the results iafter Mahout is done spewing log messages
      for (String rec: results.keySet()) {
         System.out.printf("%s: %.4f\n", rec, results.get(rec));
      }
   }
}
