from model_content import ContentBasedRecommender
from colab import ColaborativeRecommender
import pandas as pd

class HybridRecommender:
    def __init__(self, collaborative_recommender, content_based_recommender, alpha=0.5):
        self.collaborative_recommender = collaborative_recommender
        self.content_based_recommender = content_based_recommender
        self.alpha = alpha

    def recommend(self, data_new_user, title, K_to_recommend=10):
        cl_model, cl_interactions, cl_weights = self.collaborative_recommender.new_user_model(data_new_user)
        cl_model = self.collaborative_recommender.train_new_user(cl_model, cl_interactions)
        map_watched = self.collaborative_recommender.generate_map_watched(data_new_user)
        projected_user_embedding = self.collaborative_recommender.generate_embeds(cl_model, map_watched)
        collaborative_recommendations, collaborative_animes_ratings = self.collaborative_recommender.predict_N_best_recommendations(map_watched, projected_user_embedding, K_to_recommend)

        content_based_recommendations = self.content_based_recommender.recommend(title, K_to_recommend)

        hybrid_recommendations = {}
        
        for anime_id, rating in collaborative_animes_ratings:
            hybrid_recommendations[anime_id] = self.alpha * rating

        for anime_name in content_based_recommendations:
            anime_id = self.collaborative_recommender.get_anime_mapped(anime_name)
            if anime_id in hybrid_recommendations:
                hybrid_recommendations[anime_id] += (1 - self.alpha)

        sorted_hybrid = sorted(hybrid_recommendations.items(), key=lambda x: x[1], reverse=True)
        recs = [self.collaborative_recommender.get_anime_originalID(anime_id) for anime_id, _ in sorted_hybrid if anime_id is not None]
        
        return recs

#cb = ContentBasedRecommender()
#cl = ColaborativeRecommender()
#data_new_user = pd.read_csv("./new_user.csv")

#hr = HybridRecommender(cl, cb)

#titles = hr.recommend(data_new_user, "Serial Experiments Lain", 0.1)
#print(titles)

#titles = hr.recommend(data_new_user, "Serial Experiments Lain", 0.5)
#print(titles)

#titles = hr.recommend(data_new_user, "Serial Experiments Lain", 1)
#print(titles)