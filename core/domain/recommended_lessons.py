import random
from core.domain import exp_services
from core.domain import user_services
from core.domain import topic_services

#codigo refatorado final 
def get_recommendations(user_id, exploration_id):
    """Retorna recomendações de explorações para o usuário com base em tópicos similares e explorações
    não concluídas."""
    exploration = exp_services.get_exploration_by_id(exploration_id)
    if not exploration:
        return []

    topic_id = exploration.topic_id
    similar_topics = topic_services.get_similar_topics(topic_id)

    all_explorations = exp_services.get_all_explorations()
    completed_explorations = set(user_services.get_completed_explorations(user_id))

    recommended_explorations = [
        exp.exp_id for exp in all_explorations
        if exp.exp_id != exploration_id
        and exp.exp_id not in completed_explorations
        and (exp.topic_id == topic_id or exp.topic_id in similar_topics)
    ]

    random.shuffle(recommended_explorations)
    return recommended_explorations[:5]  # retorna no máximo 5 recomendações
