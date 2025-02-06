from core.domain import exp_services, recommended_lessons, topic_fetchers
from core.tests import test_utils


class RecommendationServicesTests(test_utils.GenericTestBase):
    """Testes para o sistema de recomendação."""

    def test_get_recommendations_returns_list_of_explorations(self):
        """Verifica se a função retorna uma lista de explorações recomendadas."""
        user_id = "test_user"
        exploration_id = "exp123"
        recommendations = recommended_lessons.get_recommendations(user_id, exploration_id)

        # lista de ids com o resultado
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(all(isinstance(exp_id, str) for exp_id in recommendations))
        
    def test_get_recommendations_considers_user_history(self):
        user_id = "test_user"
        exploration_id = "exp123"
        completed_explorations = ["exp456", "exp789"]

        recommendations = recommended_lessons.get_recommendations(user_id, exploration_id)

        for exp_id in completed_explorations:
            self.assertNotIn(exp_id, recommendations)  # ve se não recomenda algo que ja foi feito

    def test_get_recommendations_suggests_explorations_from_same_topic(self):   
        # topicos e explorações associadas a ele 
        topic_id = "topic_123"
        topic = topic_fetchers.get_topic_by_id(topic_id)

        exp1 = exp_services.save_new_exploration("exp1", self.user_id, {"title": "Exp 1", "topic_id": topic_id})
        exp2 = exp_services.save_new_exploration("exp2", self.user_id, {"title": "Exp 2", "topic_id": topic_id})
        exp3 = exp_services.save_new_exploration("exp3", self.user_id, {"title": "Exp 3", "topic_id": topic_id})
        user_id = "test_user"
        recommendations = recommended_lessons.get_recommendations(user_id, "exp1")

        # verificacao de recomendações do mesmo topico
        self.assertIn(exp1, recommendations)
        self.assertIn(exp2, recommendations)
        self.assertNotIn(exp3, recommendations)  # nao recomendar ele mesmo