from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# DEFAULT_LLM = "groq/llama3-70b-8192"

pesquisador = Agent(
    role="Pesquisador Sênior em {tema}",
    goal="Descobrir os desenvolvimentos mais recentes em {tema}",
    backstory="Você é um pesquisador experiente.",
    verbose=True,
    tools=[SerperDevTool()],
    # llm=DEFAULT_LLM,
)

analista_relatorios = Agent(
    role="Analista de Relatórios em {tema}",
    goal="Criar relatórios detalhados baseados na análise de dados e pesquisas sobre {tema}",
    backstory="Você é um analista meticuloso.",
    verbose=True,
    # llm=DEFAULT_LLM,
)

tarefa_pesquisa = Task(
    description="Conduza uma pesquisa sobre {tema}.",
    expected_output="Uma lista com 10 pontos principais sobre {tema}.",
    agent=pesquisador,
)

tarefa_relatorio = Task(
    description="Revise e expanda os pontos em um relatório detalhado.",
    expected_output="Um relatório completo em Markdown, incluindo as referências da internet.",
    agent=analista_relatorios,
    output_file="relatorio_{tema}.md",
)

# Configurando a Equipe
equipe = Crew(
    agents=[pesquisador, analista_relatorios],
    tasks=[tarefa_pesquisa, tarefa_relatorio],
    process=Process.sequential,
    verbose=True,
    # manager_llm=DEFAULT_LLM,
    # planning_llm=DEFAULT_LLM,
    # function_calling_llm=DEFAULT_LLM,
)


# Função Principal para Execução
def run():
    """Executa a equipe."""
    tema = input("Qual o tema do relatorio? ")
    inputs = {"tema": tema}
    equipe.kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
