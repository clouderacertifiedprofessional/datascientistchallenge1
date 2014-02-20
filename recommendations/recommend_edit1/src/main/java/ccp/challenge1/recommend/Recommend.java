package ccp.challenge1.recommender;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.eval.RecommenderBuilder;
import org.apache.mahout.cf.taste.eval.RecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.AverageAbsoluteDifferenceRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.eval.RMSRecommenderEvaluator;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.neighborhood.ThresholdUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.recommender.slopeone.SlopeOneRecommender;
import org.apache.mahout.cf.taste.impl.recommender.svd.ALSWRFactorizer;
import org.apache.mahout.cf.taste.impl.recommender.svd.ExpectationMaximizationSVDFactorizer;
import org.apache.mahout.cf.taste.impl.recommender.svd.ImplicitLinearRegressionFactorizer;
import org.apache.mahout.cf.taste.impl.recommender.svd.SVDRecommender;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.impl.similarity.TanimotoCoefficientSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.Recommender;

public class Recommend {
   private static final int ITERATIONS = 10;

   public static void main(String[] args) throws Exception {
      final DataModel ratingDataModel = new FileDataModel(new File("../explicit.csv"));
      final DataModel allDataModel = new FileDataModel(new File("../implicit.csv"));
      final LogLikelihoodSimilarity ll = new LogLikelihoodSimilarity(allDataModel);
      final TanimotoCoefficientSimilarity tanimoto = new TanimotoCoefficientSimilarity(allDataModel);
      RecommenderEvaluator rmse = new RMSRecommenderEvaluator();
      RecommenderEvaluator abs = new AverageAbsoluteDifferenceRecommenderEvaluator();
      Map<String, RecommenderBuilder> recs = new HashMap<String, RecommenderBuilder>();

      recs.put("User-user n-nearest neighbor with Tanimoto",
              new RecommenderBuilder() {
                 public Recommender buildRecommender(DataModel dm) throws TasteException {
                    UserNeighborhood nearest = new NearestNUserNeighborhood(10, tanimoto, allDataModel);

                    return new GenericUserBasedRecommender(dm, nearest, tanimoto);
                 }
              });
      recs.put("User-user n-nearest neighbor with log-likelihood",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            UserNeighborhood nearest = new NearestNUserNeighborhood(10, ll, allDataModel);

            return new GenericUserBasedRecommender(dm, nearest, ll);
         }
      });
      recs.put("User-user threshold with Tanimoto",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            UserNeighborhood nearest = new ThresholdUserNeighborhood(0.7, tanimoto, allDataModel);

            return new GenericUserBasedRecommender(dm, nearest, tanimoto);
         }
      });
      recs.put("User-user threshold with log-likelihood",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            UserNeighborhood nearest = new ThresholdUserNeighborhood(0.7, ll, allDataModel);

            return new GenericUserBasedRecommender(dm, nearest, ll);
         }
      });
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
      recs.put("Slope One",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SlopeOneRecommender(dm);
         }
      });
      recs.put("SVD with ALS",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ALSWRFactorizer(dm, 20, 1, 20));
         }
      });
      recs.put("SVD with EM",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ExpectationMaximizationSVDFactorizer(dm, 20, 20));
         }
      });
      recs.put("SVD with implicit linear regression",
              new RecommenderBuilder() {
         public Recommender buildRecommender(DataModel dm) throws TasteException {
            return new SVDRecommender(dm, new ImplicitLinearRegressionFactorizer(dm));
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

