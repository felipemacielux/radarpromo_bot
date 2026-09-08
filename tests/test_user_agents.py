from antidetect.user_agents import UserAgentManager


def test_user_agent_estavel_durante_a_mesma_instancia():
    manager = UserAgentManager()
    primeiro = manager.get_user_agent_aleatorio()
    segundo = manager.get_user_agent_aleatorio()
    assert primeiro == segundo


def test_user_agent_nao_vazio():
    manager = UserAgentManager()
    assert manager.get_user_agent_aleatorio()


def test_instancias_diferentes_sao_independentes():
    manager_a = UserAgentManager()
    manager_b = UserAgentManager()
    manager_a.get_user_agent_aleatorio()
    manager_b.get_user_agent_aleatorio()
    assert manager_a._atual is not None
    assert manager_b._atual is not None
