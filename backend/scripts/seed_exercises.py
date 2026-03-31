"""
Seed script — Exercise Library
Usage (from the backend/ directory):
    python -m scripts.seed_exercises

Idempotent: exercises that already exist by name are skipped.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, engine, Base  # noqa: E402
from app.models.exercise import Exercise  # noqa: E402

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Dataset
# Tuple format:
#   (name, muscle_group, secondary_muscles, equipment, level,
#    instructions, contraindications)
#
# contraindications: comma-separated keywords matched against user.restrictions
# ---------------------------------------------------------------------------

EXERCISES: list[tuple] = [

    # ════════════════════════════════════════════════════════════════════════
    # PEITO
    # ════════════════════════════════════════════════════════════════════════
    (
        "Supino Reto com Barra",
        "peito", "triceps,ombros", "barra", "intermediario",
        "Deite no banco, segure a barra na largura dos ombros e desça até o peito antes de empurrar.",
        "ombro,punho",
    ),
    (
        "Supino Inclinado com Halteres",
        "peito", "ombros,triceps", "haltere", "iniciante",
        "Banco inclinado a 30-45°. Desça os halteres de forma controlada até a linha do peito.",
        "ombro",
    ),
    (
        "Supino Inclinado com Barra",
        "peito", "ombros,triceps", "barra", "intermediario",
        "Banco inclinado a 30-45°. Enfatiza a porção superior do peitoral.",
        "ombro,punho",
    ),
    (
        "Supino Declinado com Barra",
        "peito", "triceps", "barra", "intermediario",
        "Banco declinado. Isola a porção inferior do peitoral.",
        "punho,ombro",
    ),
    (
        "Supino Declinado com Halteres",
        "peito", "triceps", "haltere", "intermediario",
        "Banco declinado. Maior amplitude de movimento em relação à versão com barra.",
        "ombro",
    ),
    (
        "Supino com Haltere (Neutro)",
        "peito", "triceps,ombros", "haltere", "iniciante",
        "Pegada neutra (palmas voltadas uma para a outra). Reduz tensão no ombro.",
        None,
    ),
    (
        "Supino no Smith",
        "peito", "triceps,ombros", "maquina", "iniciante",
        "Barra guiada no Smith. Boa opção para iniciantes aprenderem o padrão de movimento.",
        "ombro",
    ),
    (
        "Crucifixo com Halteres",
        "peito", "ombros", "haltere", "iniciante",
        "Banco plano. Abra os braços em arco amplo mantendo leve flexão no cotovelo.",
        "ombro",
    ),
    (
        "Crucifixo Inclinado com Halteres",
        "peito", "ombros", "haltere", "iniciante",
        "Banco inclinado. Enfatiza a porção superior do peitoral em amplitude total.",
        "ombro",
    ),
    (
        "Crossover no Cabo",
        "peito", "ombros", "cabo", "iniciante",
        "Polias altas. Puxe os cabos em arco para o centro do corpo, espremendo o peitoral.",
        "ombro",
    ),
    (
        "Crossover Baixo (Polia Baixa)",
        "peito", "ombros", "cabo", "iniciante",
        "Polias baixas. Enfatiza a porção superior do peitoral ao cruzar os cabos em arco ascendente.",
        "ombro",
    ),
    (
        "Cable Fly Inclinado",
        "peito", "ombros", "cabo", "iniciante",
        "Banco inclinado entre as polias. Isola a porção superior do peitoral com tensão constante.",
        "ombro",
    ),
    (
        "Peck Deck (Máquina Borboleta)",
        "peito", None, "maquina", "iniciante",
        "Antebraços apoiados nas almofadas. Feche os braços na frente do corpo espremendo o peitoral.",
        "ombro",
    ),
    (
        "Pullover com Haltere",
        "peito", "costas,triceps", "haltere", "iniciante",
        "Deitado transversalmente no banco. Desça o haltere atrás da cabeça em arco controlado.",
        "ombro,lombar",
    ),
    (
        "Flexão de Braços",
        "peito", "triceps,ombros", "peso_corporal", "iniciante",
        "Mãos na largura dos ombros, corpo alinhado. Desça até o peito quase tocar o chão.",
        None,
    ),
    (
        "Flexão Diamante",
        "peito", "triceps", "peso_corporal", "intermediario",
        "Mãos formando um triângulo sob o peito. Isola a porção interna do peitoral e o tríceps.",
        "punho",
    ),
    (
        "Flexão com Pés Elevados",
        "peito", "ombros,triceps", "peso_corporal", "intermediario",
        "Pés elevados em banco. Desloca o foco para a porção superior do peitoral.",
        "ombro",
    ),
    (
        "Flexão com Mãos Elevadas",
        "peito", "triceps", "peso_corporal", "iniciante",
        "Mãos elevadas em banco ou step. Reduz a carga corporal — boa progressão para iniciantes.",
        None,
    ),
    (
        "Flexão Arqueiro",
        "peito", "triceps,ombros", "peso_corporal", "avancado",
        "Afaste um braço lateralmente enquanto flexiona o outro. Exige controle unilateral elevado.",
        "ombro,punho",
    ),
    (
        "Flexão Explosiva (Clap Push-up)",
        "peito", "triceps,ombros", "peso_corporal", "avancado",
        "Empurre o chão com força suficiente para elevar as mãos e bater palmas no ar.",
        "punho",
    ),
    (
        "Supino com Pegada Fechada",
        "peito", "triceps", "barra", "intermediario",
        "Pegada na largura dos ombros ou menor. Transfere ênfase para tríceps e porção interna do peito.",
        "punho,cotovelo",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # COSTAS
    # ════════════════════════════════════════════════════════════════════════
    (
        "Puxada Frontal",
        "costas", "biceps,ombros", "maquina", "iniciante",
        "Segure a barra um pouco mais larga que os ombros e puxe até a linha do mento.",
        None,
    ),
    (
        "Pulldown no Cabo",
        "costas", "biceps", "cabo", "iniciante",
        "Polia alta, puxe o cabo até a altura do mento mantendo o tronco levemente inclinado.",
        None,
    ),
    (
        "Pulldown Neutro (Triangulo)",
        "costas", "biceps", "cabo", "iniciante",
        "Triângulo neutro na polia alta. Reduz tensão nos ombros em relação à pegada pronada.",
        None,
    ),
    (
        "Straight Arm Pulldown",
        "costas", "triceps", "cabo", "intermediario",
        "Braços estendidos, puxe o cabo de cima para baixo em arco. Isola o grande dorsal.",
        "ombro",
    ),
    (
        "Remada Baixa no Cabo",
        "costas", "biceps", "cabo", "iniciante",
        "Sentado, puxe o cabo até o abdômen mantendo as costas retas e os ombros abertos.",
        None,
    ),
    (
        "Remada Unilateral com Haltere",
        "costas", "biceps", "haltere", "iniciante",
        "Apoie o joelho e a mão no banco. Puxe o haltere em linha reta até o quadril.",
        None,
    ),
    (
        "Remada Unilateral no Cabo",
        "costas", "biceps", "cabo", "iniciante",
        "Polia baixa, puxe com um braço de cada vez. Permite maior amplitude e rotação.",
        None,
    ),
    (
        "Remada Curvada com Barra",
        "costas", "biceps,posterior", "barra", "intermediario",
        "Tronco inclinado ~45°, puxe a barra em direção ao abdômen inferior.",
        "lombar",
    ),
    (
        "Remada Pendlay",
        "costas", "biceps,posterior", "barra", "avancado",
        "Barra parte do chão a cada rep com tronco horizontal. Versão mais explosiva da remada curvada.",
        "lombar",
    ),
    (
        "Remada T (T-Bar Row)",
        "costas", "biceps,ombros", "barra", "avancado",
        "Barra fixada num canto. Puxe em direção ao peito com tronco inclinado.",
        "lombar",
    ),
    (
        "Remada na Máquina",
        "costas", "biceps", "maquina", "iniciante",
        "Peito apoiado no suporte. Puxe as alças em direção ao tronco de forma controlada.",
        None,
    ),
    (
        "Remada no Smith",
        "costas", "biceps", "maquina", "iniciante",
        "Barra guiada no Smith com tronco inclinado. Boa alternativa para quem aprende o movimento.",
        None,
    ),
    (
        "Remada com Elástico",
        "costas", "biceps", "elastico", "iniciante",
        "Elástico fixado à frente. Puxe em direção ao abdômen mantendo cotovelos próximos ao corpo.",
        None,
    ),
    (
        "Pullover na Máquina",
        "costas", "peito,triceps", "maquina", "iniciante",
        "Sentado, puxe as alças em arco descendente. Isola o grande dorsal sem sobrecarregar os bíceps.",
        None,
    ),
    (
        "Barra Fixa (Pull-up)",
        "costas", "biceps,ombros", "peso_corporal", "avancado",
        "Pegada pronada mais larga que os ombros. Suba até o queixo ultrapassar a barra.",
        "ombro,cotovelo",
    ),
    (
        "Barra Fixa Supinada (Chin-up)",
        "costas", "biceps", "peso_corporal", "avancado",
        "Pegada supinada na largura dos ombros. Maior ativação de bíceps que o pull-up tradicional.",
        "cotovelo",
    ),
    (
        "Barra Fixa Neutra",
        "costas", "biceps", "peso_corporal", "avancado",
        "Pegada neutra em barras paralelas. Reduz estresse no punho e no ombro.",
        "ombro",
    ),
    (
        "Superman",
        "costas", "gluteos,posterior", "peso_corporal", "iniciante",
        "Deitado de bruços, eleve braços e pernas simultaneamente contraindo os extensores.",
        None,
    ),
    (
        "Hiperextensão Lombar",
        "costas", "gluteos,posterior", "maquina", "iniciante",
        "Na cadeira romana, desça o tronco e retorne até a posição neutra. Não hiperestenda.",
        "lombar",
    ),
    (
        "Levantamento Terra",
        "costas", "gluteos,posterior,quadriceps", "barra", "avancado",
        "Pés na largura do quadril, barra sobre o metatarso. Empurre o chão ao levantar.",
        "lombar,joelho",
    ),
    (
        "Deadlift Sumô",
        "costas", "gluteos,posterior,quadriceps", "barra", "avancado",
        "Stance largo com pés virados para fora. Reduz demanda lombar e aumenta ativação de glúteos.",
        "joelho,lombar",
    ),
    (
        "Row com Kettlebell",
        "costas", "biceps", "kettlebell", "intermediario",
        "Apoie uma mão no banco. Puxe o kettlebell em linha reta com rotação natural do punho.",
        "lombar",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # QUADRICEPS
    # ════════════════════════════════════════════════════════════════════════
    (
        "Agachamento Livre",
        "quadriceps", "gluteos,posterior", "barra", "intermediario",
        "Barra nas costas, pés na largura dos ombros. Desça até as coxas ficarem paralelas ao chão.",
        "joelho,lombar",
    ),
    (
        "Agachamento com Haltere",
        "quadriceps", "gluteos", "haltere", "iniciante",
        "Halteres segurados ao lado do corpo. Versão acessível do agachamento para iniciantes.",
        "joelho",
    ),
    (
        "Agachamento Goblet",
        "quadriceps", "gluteos,core", "kettlebell", "iniciante",
        "Segure o kettlebell no peito. Agache profundo mantendo o tronco ereto.",
        "joelho",
    ),
    (
        "Agachamento com Kettlebell",
        "quadriceps", "gluteos", "kettlebell", "iniciante",
        "Kettlebell segurado entre as pernas. Bom para iniciantes aprenderem postura correta.",
        "joelho",
    ),
    (
        "Agachamento Sumô com Haltere",
        "quadriceps", "gluteos,posterior", "haltere", "iniciante",
        "Stance largo, pés virados para fora, haltere seguro entre as pernas. Enfatiza glúteos.",
        "joelho",
    ),
    (
        "Agachamento Sumô com Barra",
        "quadriceps", "gluteos,posterior", "barra", "intermediario",
        "Stance largo com barra nas costas. Maior ativação de glúteos e adutores.",
        "joelho,lombar",
    ),
    (
        "Agachamento no Smith",
        "quadriceps", "gluteos", "maquina", "iniciante",
        "Barra guiada no Smith. Permite focar na profundidade sem se preocupar com equilíbrio.",
        "joelho",
    ),
    (
        "Front Squat (Agachamento Frontal)",
        "quadriceps", "gluteos,core", "barra", "avancado",
        "Barra apoiada na frente dos ombros. Exige mais do core e do quadriceps que o agachamento traseiro.",
        "joelho,lombar,ombro",
    ),
    (
        "Agachamento Búlgaro (Split Squat)",
        "quadriceps", "gluteos,posterior", "haltere", "intermediario",
        "Pé traseiro elevado em banco. Exercício unilateral com alta demanda de estabilidade.",
        "joelho",
    ),
    (
        "Box Squat",
        "quadriceps", "gluteos,posterior", "barra", "intermediario",
        "Agache até sentar num box antes de retornar. Ensina a posição correta de profundidade.",
        "joelho,lombar",
    ),
    (
        "Leg Press 45°",
        "quadriceps", "gluteos", "maquina", "iniciante",
        "Pés na plataforma na largura dos ombros. Desça até os joelhos formarem 90°.",
        "joelho",
    ),
    (
        "Leg Press Unilateral",
        "quadriceps", "gluteos", "maquina", "intermediario",
        "Um pé de cada vez na plataforma. Corrige desequilíbrios entre os lados.",
        "joelho",
    ),
    (
        "Extensão de Perna",
        "quadriceps", None, "maquina", "iniciante",
        "Sentado na máquina, estenda as pernas até o ângulo máximo de forma controlada.",
        "joelho",
    ),
    (
        "Extensão de Perna Unilateral",
        "quadriceps", None, "maquina", "iniciante",
        "Uma perna de cada vez. Útil para identificar e corrigir desequilíbrios de força.",
        "joelho",
    ),
    (
        "Afundo com Halteres",
        "quadriceps", "gluteos,posterior", "haltere", "iniciante",
        "Passo à frente, desça o joelho traseiro em direção ao chão sem tocá-lo.",
        "joelho",
    ),
    (
        "Avanço Caminhando com Halteres",
        "quadriceps", "gluteos,posterior", "haltere", "intermediario",
        "Afundo em movimento para frente alternando os lados. Trabalha equilíbrio dinâmico.",
        "joelho",
    ),
    (
        "Step Up com Halteres",
        "quadriceps", "gluteos", "haltere", "iniciante",
        "Suba num step ou banco segurando halteres. Trabalha quadriceps e glúteo unilateralmente.",
        "joelho",
    ),
    (
        "Wall Sit (Cadeira na Parede)",
        "quadriceps", None, "peso_corporal", "iniciante",
        "Costas na parede, joelhos a 90°. Exercício isométrico de resistência muscular.",
        "joelho",
    ),
    (
        "Sissy Squat",
        "quadriceps", None, "peso_corporal", "avancado",
        "Joelhos avançam para frente enquanto o tronco recua. Alto estresse patelar — requer progressão.",
        "joelho",
    ),
    (
        "Agachamento Isométrico",
        "quadriceps", "gluteos", "peso_corporal", "iniciante",
        "Desça até metade e mantenha a posição por tempo determinado. Fortalece sem impacto.",
        "joelho",
    ),
    (
        "Terminal Knee Extension (TKE)",
        "quadriceps", None, "elastico", "iniciante",
        "Elástico atrás do joelho. Estenda o joelho de forma controlada. Indicado em reabilitação.",
        None,
    ),
    (
        "Agachamento Hack com Barra",
        "quadriceps", "gluteos", "maquina", "intermediario",
        "Costas na plataforma inclinada. Desça de forma controlada até 90° no joelho.",
        "joelho",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # POSTERIOR (ISQUIOTIBIAIS)
    # ════════════════════════════════════════════════════════════════════════
    (
        "Flexão de Perna (Leg Curl)",
        "posterior", None, "maquina", "iniciante",
        "Deitado na máquina, flexione os joelhos levando o calcanhar em direção ao glúteo.",
        "joelho",
    ),
    (
        "Mesa Flexora",
        "posterior", None, "maquina", "iniciante",
        "Sentado, flexione os joelhos puxando o peso até ~90°. Não deixe o joelho ultrapassar a linha do banco.",
        "joelho",
    ),
    (
        "Leg Curl no Cabo",
        "posterior", None, "cabo", "iniciante",
        "Tornozeleira no cabo baixo. Flexione o joelho em pé ou deitado de forma controlada.",
        "joelho",
    ),
    (
        "Leg Curl com Haltere",
        "posterior", None, "haltere", "iniciante",
        "Deitado, haltere preso entre os pés. Flexione os joelhos levando o calcanhar ao glúteo.",
        "joelho",
    ),
    (
        "Leg Curl com Elástico",
        "posterior", None, "elastico", "iniciante",
        "Elástico fixado à frente, tornozeleira. Flexione o joelho de forma controlada.",
        "joelho",
    ),
    (
        "Stiff com Barra",
        "posterior", "gluteos,lombar", "barra", "intermediario",
        "Pernas quase estendidas, desça a barra pela frente das pernas até sentir o alongamento.",
        "lombar",
    ),
    (
        "Stiff com Halteres",
        "posterior", "gluteos", "haltere", "iniciante",
        "Mesma mecânica do stiff com barra, porém com amplitude um pouco maior.",
        "lombar",
    ),
    (
        "Stiff com Kettlebell",
        "posterior", "gluteos", "kettlebell", "iniciante",
        "Kettlebell à frente do corpo. Desce mantendo as costas neutras e o quadril empurrado para trás.",
        "lombar",
    ),
    (
        "Deadlift Romeno (RDL)",
        "posterior", "gluteos,lombar", "barra", "intermediario",
        "Diferente do stiff: joelhos com mais flexão e quadril recua mais. Maior recrutamento de glúteo.",
        "lombar",
    ),
    (
        "Deadlift Romeno Unilateral",
        "posterior", "gluteos,core", "haltere", "intermediario",
        "Versão unilateral do RDL. Exige mais equilíbrio e corrige assimetrias.",
        "lombar",
    ),
    (
        "Stiff Unilateral com Haltere",
        "posterior", "gluteos,core", "haltere", "intermediario",
        "Uma perna de cada vez. Isola o isquiotibial e glúteo do lado de trabalho.",
        "lombar",
    ),
    (
        "Good Morning",
        "posterior", "lombar,gluteos", "barra", "avancado",
        "Barra nas costas, incline o tronco para frente mantendo as costas neutras.",
        "lombar,cervical",
    ),
    (
        "Nordic Curl",
        "posterior", None, "peso_corporal", "avancado",
        "Joelhos fixos, desça o tronco para frente de forma excêntrica controlada. Alta proteção contra lesão.",
        "joelho",
    ),
    (
        "Ponte com Pés Elevados",
        "posterior", "gluteos", "peso_corporal", "iniciante",
        "Pés elevados em banco. Aumenta a amplitude e o recrutamento dos isquiotibiais.",
        None,
    ),
    (
        "Glute Ham Raise",
        "posterior", "gluteos,lombar", "peso_corporal", "avancado",
        "Joelhos fixos, desça o tronco e retorne usando força dos isquiotibiais. Exercício avançado.",
        "joelho,lombar",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # GLÚTEOS
    # ════════════════════════════════════════════════════════════════════════
    (
        "Hip Thrust com Barra",
        "gluteos", "posterior,quadriceps", "barra", "iniciante",
        "Ombros no banco, barra sobre o quadril. Empurre o quadril para cima até o corpo ficar paralelo ao chão.",
        None,
    ),
    (
        "Hip Thrust com Haltere",
        "gluteos", "posterior", "haltere", "iniciante",
        "Versão com haltere. Boa opção para quem ainda não tem acesso à barra ou elástico.",
        None,
    ),
    (
        "Hip Thrust Unilateral",
        "gluteos", "posterior,core", "peso_corporal", "intermediario",
        "Mesma mecânica do hip thrust, mas com uma perna elevada. Aumenta a ativação unilateral do glúteo.",
        None,
    ),
    (
        "Elevação Pélvica",
        "gluteos", "posterior", "peso_corporal", "iniciante",
        "Deitado, pés no chão. Eleve o quadril contraindo os glúteos no topo do movimento.",
        None,
    ),
    (
        "Ponte Isométrica",
        "gluteos", "posterior", "peso_corporal", "iniciante",
        "Eleve o quadril e mantenha a contração isométrica por tempo determinado.",
        None,
    ),
    (
        "Glúteo no Cabo",
        "gluteos", None, "cabo", "iniciante",
        "Tornozeleira no cabo baixo. Estenda a perna para trás mantendo o tronco levemente inclinado.",
        None,
    ),
    (
        "Glúteo 4 Apoios com Haltere",
        "gluteos", None, "haltere", "iniciante",
        "De joelhos, haltere atrás do joelho. Eleve a perna para trás contraindo o glúteo.",
        None,
    ),
    (
        "Abdução no Cabo",
        "gluteos", None, "cabo", "iniciante",
        "Tornozeleira no cabo baixo. Afaste a perna lateralmente contraindo o glúteo médio.",
        None,
    ),
    (
        "Abdução com Elástico em Pé",
        "gluteos", None, "elastico", "iniciante",
        "Elástico nos tornozelos ou joelhos. Afaste a perna lateralmente de forma controlada.",
        None,
    ),
    (
        "Lateral Band Walk",
        "gluteos", None, "elastico", "iniciante",
        "Elástico nos joelhos, meio agachado. Caminhe lateralmente mantendo tensão constante.",
        "joelho",
    ),
    (
        "Kickback com Elástico",
        "gluteos", None, "elastico", "iniciante",
        "Elástico fixado atrás. Empurre o pé para trás em extensão de quadril.",
        None,
    ),
    (
        "Donkey Kick",
        "gluteos", None, "peso_corporal", "iniciante",
        "De 4 apoios, eleve o joelho dobrado para cima e para trás contraindo o glúteo.",
        "punho",
    ),
    (
        "Fire Hydrant",
        "gluteos", None, "peso_corporal", "iniciante",
        "De 4 apoios, abra a perna lateralmente como um cão levantando a pata. Ativa glúteo médio.",
        "punho",
    ),
    (
        "Clamshell",
        "gluteos", None, "peso_corporal", "iniciante",
        "Deitado de lado, joelhos dobrados. Abra e feche os joelhos como uma concha.",
        None,
    ),
    (
        "Clamshell com Elástico",
        "gluteos", None, "elastico", "iniciante",
        "Elástico acima dos joelhos. Adiciona resistência ao clamshell tradicional.",
        None,
    ),
    (
        "Step Up Ênfase Glúteo",
        "gluteos", "quadriceps,posterior", "haltere", "iniciante",
        "Step alto com halteres. Empurre com o calcanhar ao subir para enfatizar o glúteo.",
        "joelho",
    ),
    (
        "Passada com Halteres (Lunge)",
        "gluteos", "quadriceps,posterior", "haltere", "iniciante",
        "Passo largo à frente. Desça o joelho traseiro em direção ao chão de forma controlada.",
        "joelho",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # OMBROS
    # ════════════════════════════════════════════════════════════════════════
    (
        "Desenvolvimento Militar com Barra",
        "ombros", "triceps,trapezio", "barra", "intermediario",
        "Em pé ou sentado, pressione a barra acima da cabeça até os braços ficarem estendidos.",
        "ombro,lombar,cervical",
    ),
    (
        "Desenvolvimento com Halteres",
        "ombros", "triceps", "haltere", "iniciante",
        "Sentado, pressione os halteres acima da cabeça de forma alternada ou simultânea.",
        "ombro",
    ),
    (
        "Desenvolvimento Alternado com Haltere",
        "ombros", "triceps,core", "haltere", "iniciante",
        "Um braço de cada vez. Permite maior amplitude e engaja mais o core para estabilização.",
        "ombro",
    ),
    (
        "Desenvolvimento na Máquina",
        "ombros", "triceps", "maquina", "iniciante",
        "Assentos ajustáveis. Caminho guiado reduz demanda de estabilização — ótimo para iniciantes.",
        None,
    ),
    (
        "Arnold Press",
        "ombros", "triceps", "haltere", "intermediario",
        "Inicie com as palmas voltadas para você e gire para fora enquanto pressiona os halteres.",
        "ombro",
    ),
    (
        "Push Press",
        "ombros", "triceps,trapezio,quadriceps", "barra", "avancado",
        "Leve flexão de joelho e explosão para ajudar a pressionar a barra acima da cabeça.",
        "ombro,lombar",
    ),
    (
        "Desenvolvimento com Kettlebell",
        "ombros", "triceps,core", "kettlebell", "intermediario",
        "Pressione o kettlebell acima da cabeça com o cotovelo travado. Exige estabilização.",
        "ombro,punho",
    ),
    (
        "Elevação Lateral com Haltere",
        "ombros", None, "haltere", "iniciante",
        "Em pé, eleve os halteres lateralmente até a altura dos ombros com leve flexão no cotovelo.",
        "ombro",
    ),
    (
        "Elevação Lateral na Máquina",
        "ombros", None, "maquina", "iniciante",
        "Tensão constante ao longo de toda a amplitude. Elimina o impulso do início do movimento.",
        None,
    ),
    (
        "Elevação Lateral no Cabo",
        "ombros", None, "cabo", "iniciante",
        "Polia baixa. Tensão constante diferente do haltere — mais eficaz no ponto de pico.",
        "ombro",
    ),
    (
        "Elevação Lateral com Elástico",
        "ombros", None, "elastico", "iniciante",
        "Elástico sob o pé. Alternativa acessível para trabalhar o deltóide médio.",
        None,
    ),
    (
        "Elevação Lateral Inclinada",
        "ombros", None, "haltere", "intermediario",
        "Tronco inclinado lateralmente. Aumenta amplitude e isolamento do deltóide médio.",
        "ombro",
    ),
    (
        "Elevação Frontal com Haltere",
        "ombros", None, "haltere", "iniciante",
        "Em pé, eleve o haltere à frente até a altura dos ombros com o braço quase estendido.",
        "ombro",
    ),
    (
        "Elevação Frontal no Cabo",
        "ombros", None, "cabo", "iniciante",
        "Polia baixa. Tensão contínua ao longo de toda a amplitude do movimento frontal.",
        "ombro",
    ),
    (
        "Face Pull",
        "ombros", "trapezio,manguito", "cabo", "iniciante",
        "Polia alta, puxe o cabo em direção ao rosto separando as mãos no final do movimento.",
        None,
    ),
    (
        "Rotação Externa com Haltere",
        "ombros", None, "haltere", "iniciante",
        "Cotovelo fixo a 90°. Gire o antebraço para cima. Fortalece o manguito rotador.",
        "ombro",
    ),
    (
        "Remada Alta com Barra",
        "ombros", "trapezio,biceps", "barra", "intermediario",
        "Puxe a barra verticalmente até a altura do mento com cotovelos acima das mãos.",
        "ombro,punho",
    ),
    (
        "Remada Alta com Haltere",
        "ombros", "trapezio,biceps", "haltere", "iniciante",
        "Versão com halteres da remada alta. Permite caminho mais natural dos cotovelos.",
        "ombro",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # BÍCEPS
    # ════════════════════════════════════════════════════════════════════════
    (
        "Rosca Direta com Barra",
        "biceps", "antebraco", "barra", "iniciante",
        "Em pé, cotovelos fixos ao lado do corpo. Flexione até os antebraços alcançarem os ombros.",
        "punho,cotovelo",
    ),
    (
        "Rosca Alternada com Haltere",
        "biceps", "antebraco", "haltere", "iniciante",
        "Em pé ou sentado, flexione um braço de cada vez supinando o punho no final.",
        None,
    ),
    (
        "Rosca Concentrada",
        "biceps", None, "haltere", "iniciante",
        "Sentado, cotovelo apoiado na coxa interna. Flexione o antebraço em direção ao ombro.",
        None,
    ),
    (
        "Rosca Scott (Preacher Curl)",
        "biceps", None, "maquina", "iniciante",
        "Apoio dos braços na almofada em ângulo. Isola o bíceps eliminando o balanço do corpo.",
        "cotovelo",
    ),
    (
        "Rosca Scott com Barra",
        "biceps", None, "barra", "iniciante",
        "Banco Scott com barra W ou reta. Isola o bíceps com o braço apoiado na almofada.",
        "cotovelo,punho",
    ),
    (
        "Rosca no Cabo",
        "biceps", "antebraco", "cabo", "iniciante",
        "Polia baixa, puxe o cabo flexionando o cotovelo mantendo-o fixo ao corpo.",
        None,
    ),
    (
        "Rosca no Cabo Alto",
        "biceps", None, "cabo", "iniciante",
        "Polia alta. Cotovelo nivelado com o ombro ao flexionar. Isola a cabeça longa do bíceps.",
        None,
    ),
    (
        "Rosca Martelo",
        "biceps", "antebraco,braquial", "haltere", "iniciante",
        "Pegada neutra (palmas voltadas uma para a outra). Trabalha o braquial e o antebraço.",
        "punho",
    ),
    (
        "Rosca Martelo no Cabo",
        "biceps", "antebraco,braquial", "cabo", "iniciante",
        "Corda na polia baixa com pegada neutra. Maior tensão constante que o haltere.",
        None,
    ),
    (
        "Rosca Inversa",
        "biceps", "antebraco", "barra", "iniciante",
        "Pegada pronada. Foca no braquiorradial e antebraço além do bíceps.",
        "punho",
    ),
    (
        "Rosca com Elástico",
        "biceps", None, "elastico", "iniciante",
        "Elástico sob o pé. Flexione o cotovelo supinando o punho. Acessível para qualquer lugar.",
        None,
    ),
    (
        "Rosca 21s com Barra",
        "biceps", None, "barra", "intermediario",
        "7 repetições na metade inferior + 7 na superior + 7 completas. Treina as duas fases do bíceps.",
        "cotovelo",
    ),
    (
        "Rosca Zottman",
        "biceps", "antebraco", "haltere", "intermediario",
        "Supine na subida (bíceps) e prone na descida (antebraço). Trabalha ambos os grupos.",
        None,
    ),
    (
        "Rosca Inclinada com Haltere",
        "biceps", None, "haltere", "intermediario",
        "Banco inclinado a 45-60°. Alonga a cabeça longa do bíceps no ponto de partida.",
        "ombro",
    ),
    (
        "Rosca na Máquina",
        "biceps", None, "maquina", "iniciante",
        "Caminho guiado e tensão constante. Ideal para iniciantes ou como finalizador de treino.",
        None,
    ),

    # ════════════════════════════════════════════════════════════════════════
    # TRÍCEPS
    # ════════════════════════════════════════════════════════════════════════
    (
        "Tríceps na Polia (Barra Reta)",
        "triceps", None, "cabo", "iniciante",
        "Polia alta com barra reta. Cotovelos fixos ao corpo, estenda completamente os antebraços.",
        None,
    ),
    (
        "Tríceps com Corda na Polia",
        "triceps", None, "cabo", "iniciante",
        "Polia alta com corda. Afaste as pontas no final para maior ativação da cabeça lateral.",
        None,
    ),
    (
        "Tríceps na Polia Invertida",
        "triceps", None, "cabo", "iniciante",
        "Barra reta com pegada supinada. Enfatiza a cabeça longa do tríceps.",
        None,
    ),
    (
        "Tríceps Kickback com Haltere",
        "triceps", None, "haltere", "iniciante",
        "Tronco inclinado, braço paralelo ao chão. Estenda o antebraço para trás.",
        None,
    ),
    (
        "Tríceps Kickback no Cabo",
        "triceps", None, "cabo", "iniciante",
        "Polia baixa, tronco inclinado. Tensão constante ao longo do movimento.",
        None,
    ),
    (
        "Tríceps Overhead com Haltere",
        "triceps", None, "haltere", "iniciante",
        "Sentado ou em pé, haltere atrás da cabeça com ambas as mãos. Isola a cabeça longa.",
        "cotovelo",
    ),
    (
        "Extensão Overhead no Cabo",
        "triceps", None, "cabo", "iniciante",
        "Polia alta, corda ou barra. Estenda os braços para frente abaixo da cabeça.",
        "cotovelo",
    ),
    (
        "Tríceps Testa com Barra (Skullcrusher)",
        "triceps", None, "barra", "intermediario",
        "Deitado no banco, desça a barra em direção à testa dobrando os cotovelos.",
        "cotovelo,punho",
    ),
    (
        "Skullcrusher com Haltere",
        "triceps", None, "haltere", "intermediario",
        "Versão com halteres. Permite caminho mais natural dos cotovelos e reduz risco no punho.",
        "cotovelo",
    ),
    (
        "Francês com Haltere",
        "triceps", None, "haltere", "iniciante",
        "Deitado ou sentado, desça o haltere atrás da cabeça dobrando os cotovelos.",
        "cotovelo",
    ),
    (
        "Tríceps com Elástico",
        "triceps", None, "elastico", "iniciante",
        "Elástico fixado acima. Estenda os cotovelos para baixo mantendo-os próximos ao corpo.",
        None,
    ),
    (
        "Mergulho no Banco (Dips)",
        "triceps", "peito,ombros", "peso_corporal", "iniciante",
        "Mãos apoiadas na borda do banco atrás do corpo. Desça o quadril dobrando os cotovelos.",
        "ombro",
    ),
    (
        "Barra Paralela (Dips)",
        "triceps", "peito,ombros", "peso_corporal", "avancado",
        "Nas paralelas, desça o corpo controladamente e empurre até estender os braços.",
        "ombro,cotovelo",
    ),
    (
        "Dips Assistido na Máquina",
        "triceps", "peito,ombros", "maquina", "iniciante",
        "Máquina de assistência reduz o peso corporal. Ideal para progredir até o dips livre.",
        None,
    ),
    (
        "Close Grip Bench Press no Smith",
        "triceps", "peito", "maquina", "intermediario",
        "Supino com pegada fechada no Smith. Caminho guiado permite focar no tríceps.",
        "punho",
    ),
    (
        "Tríceps com Kettlebell",
        "triceps", None, "kettlebell", "iniciante",
        "Kettlebell atrás da cabeça. Segure pela base e desça de forma controlada.",
        "cotovelo",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # ABDÔMEN
    # ════════════════════════════════════════════════════════════════════════
    (
        "Abdominal Crunch",
        "abdomen", None, "peso_corporal", "iniciante",
        "Deitado, joelhos dobrados. Eleve o tronco usando apenas o abdômen, sem puxar o pescoço.",
        "cervical,lombar",
    ),
    (
        "Crunch Inverso",
        "abdomen", None, "peso_corporal", "iniciante",
        "Deitado, eleve o quadril do chão trazendo os joelhos em direção ao peito.",
        "lombar",
    ),
    (
        "Crunch com Haltere",
        "abdomen", None, "haltere", "iniciante",
        "Crunch segurando um haltere no peito. Adiciona resistência ao movimento de flexão.",
        "cervical,lombar",
    ),
    (
        "Abdominal na Máquina",
        "abdomen", None, "maquina", "iniciante",
        "Sentado, puxe as alças em direção aos joelhos contraindo o abdômen.",
        None,
    ),
    (
        "Abdominal no Cabo",
        "abdomen", None, "cabo", "iniciante",
        "De joelhos, polia alta. Puxe o cabo em direção aos quadris curvando o tronco.",
        "lombar",
    ),
    (
        "Elevação de Pernas",
        "abdomen", "quadriceps", "peso_corporal", "intermediario",
        "Deitado, eleve as pernas estendidas até formarem 90° com o tronco.",
        "lombar",
    ),
    (
        "Leg Raise Suspenso",
        "abdomen", "quadriceps", "peso_corporal", "avancado",
        "Suspenso na barra. Eleve as pernas até a horizontal ou além com controle total.",
        "lombar,ombro",
    ),
    (
        "Prancha Isométrica",
        "abdomen", "ombros,gluteos", "peso_corporal", "iniciante",
        "Apoio nos antebraços e pontas dos pés. Mantenha o corpo alinhado por 20-60 segundos.",
        "lombar,punho",
    ),
    (
        "Prancha Lateral",
        "abdomen", "ombros", "peso_corporal", "iniciante",
        "Apoio no antebraço e borda do pé. Mantenha quadril elevado e corpo alinhado lateralmente.",
        "ombro",
    ),
    (
        "Prancha com Elevação de Braço",
        "abdomen", "ombros", "peso_corporal", "intermediario",
        "Na posição de prancha, eleve alternadamente os braços. Aumenta instabilidade e demanda de core.",
        "ombro,punho",
    ),
    (
        "Rotação Russa",
        "abdomen", None, "peso_corporal", "iniciante",
        "Sentado com os pés levantados, gire o tronco de lado a lado tocando o chão.",
        "lombar",
    ),
    (
        "Abdominal Oblíquo",
        "abdomen", None, "peso_corporal", "iniciante",
        "Crunch com rotação: leve o cotovelo em direção ao joelho oposto.",
        "cervical",
    ),
    (
        "Toque no Calcanhar",
        "abdomen", None, "peso_corporal", "iniciante",
        "Deitado, joelhos dobrados. Toque alternadamente os calcanhares curvando o tronco lateralmente.",
        None,
    ),
    (
        "Dead Bug",
        "abdomen", None, "peso_corporal", "iniciante",
        "Deitado, braços e pernas no ar. Estenda alternadamente braço e perna opostos mantendo lombar no chão.",
        None,
    ),
    (
        "Mountain Climber",
        "abdomen", "quadriceps,ombros", "peso_corporal", "iniciante",
        "Posição de prancha. Puxe alternadamente os joelhos em direção ao peito em ritmo acelerado.",
        "ombro,punho",
    ),
    (
        "Hollow Body Hold",
        "abdomen", None, "peso_corporal", "intermediario",
        "Deitado, eleve levemente cabeça, ombros e pernas do chão. Mantenha lombar pressionada.",
        "lombar",
    ),
    (
        "Ab Wheel (Roda Abdominal)",
        "abdomen", "ombros,lombar", "peso_corporal", "avancado",
        "De joelhos, role a roda para frente o máximo possível e retorne com controle.",
        "lombar,punho",
    ),
    (
        "Windshield Wiper",
        "abdomen", None, "peso_corporal", "avancado",
        "Suspenso ou deitado, gire as pernas de lado a lado controlando com o abdômen.",
        "lombar",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # PANTURRILHA
    # ════════════════════════════════════════════════════════════════════════
    (
        "Elevação de Panturrilha em Pé",
        "panturrilha", None, "maquina", "iniciante",
        "Na máquina, eleve os calcanhares tão alto quanto possível e desça de forma controlada.",
        "tornozelo",
    ),
    (
        "Elevação de Panturrilha Sentado",
        "panturrilha", "soleo", "maquina", "iniciante",
        "Joelhos a 90°. Isola o sóleo. Eleve o calcanhar contraindo no topo.",
        "tornozelo",
    ),
    (
        "Elevação de Panturrilha no Leg Press",
        "panturrilha", None, "maquina", "intermediario",
        "Pés na borda inferior da plataforma. Pressione as pontas dos pés empurrando a plataforma.",
        "tornozelo,joelho",
    ),
    (
        "Elevação de Panturrilha com Haltere",
        "panturrilha", None, "haltere", "iniciante",
        "Em pé, haltere em uma das mãos. Eleve o calcanhar do pé correspondente.",
        "tornozelo",
    ),
    (
        "Elevação de Panturrilha Unilateral",
        "panturrilha", None, "peso_corporal", "iniciante",
        "Uma perna de cada vez. Apoia a perna livre na que trabalha para maior carga.",
        "tornozelo",
    ),
    (
        "Elevação de Panturrilha no Degrau",
        "panturrilha", None, "peso_corporal", "iniciante",
        "Calcanhar suspenso fora do degrau. Amplitude maior que no chão plano.",
        "tornozelo",
    ),
    (
        "Elevação de Panturrilha com Kettlebell",
        "panturrilha", None, "kettlebell", "iniciante",
        "Segure o kettlebell e eleve as pontas dos pés repetidamente. Simples e eficaz.",
        "tornozelo",
    ),
    (
        "Elevação de Panturrilha com Barra",
        "panturrilha", None, "barra", "intermediario",
        "Barra nas costas ou na frente. Permite carga elevada para hipertrofia de panturrilha.",
        "tornozelo,joelho",
    ),
    (
        "Tibial Raise",
        "panturrilha", None, "peso_corporal", "iniciante",
        "Costas na parede, eleve as pontas dos pés em direção à canela. Fortalece o tibial anterior.",
        "tornozelo",
    ),
    (
        "Salto de Corda",
        "panturrilha", "quadriceps,abdomen", "peso_corporal", "iniciante",
        "Pular corda ativa fortemente as panturrilhas e melhora condicionamento cardiovascular.",
        "tornozelo,joelho",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # TRAPÉZIO
    # ════════════════════════════════════════════════════════════════════════
    (
        "Encolhimento de Ombros com Barra",
        "trapezio", None, "barra", "iniciante",
        "Barra à frente ou atrás do corpo. Eleve os ombros em direção às orelhas e desça devagar.",
        "cervical,ombro",
    ),
    (
        "Encolhimento de Ombros com Haltere",
        "trapezio", None, "haltere", "iniciante",
        "Halteres ao lado do corpo. Permite movimento mais natural do que a barra.",
        "cervical",
    ),
    (
        "Encolhimento de Ombros na Máquina",
        "trapezio", None, "maquina", "iniciante",
        "Tensão constante e caminho guiado. Ideal para isolar o trapézio superior.",
        None,
    ),
    (
        "Encolhimento de Ombros no Cabo",
        "trapezio", None, "cabo", "iniciante",
        "Polia baixa ou lateral. Tensão contínua ao longo de toda a amplitude.",
        None,
    ),
    (
        "Encolhimento de Ombros com Kettlebell",
        "trapezio", None, "kettlebell", "iniciante",
        "Kettlebell ao lado do corpo. Variação eficaz para o trapézio superior.",
        "cervical",
    ),
    (
        "Farmer's Carry",
        "trapezio", "antebraco,core", "haltere", "intermediario",
        "Carregue halteres pesados e caminhe mantendo a postura ereta. Trabalha o trapézio isometricamente.",
        None,
    ),
    (
        "Power Shrug",
        "trapezio", "lombar,gluteos", "barra", "avancado",
        "Encolhimento explosivo com extensão de quadril. Movimento de potência para o trapézio.",
        "lombar,cervical",
    ),
    (
        "Incline Trap Raise",
        "trapezio", "ombros", "haltere", "iniciante",
        "Deitado de bruços em banco inclinado. Eleve os braços como se fosse voar — isola trapézio médio.",
        None,
    ),
    (
        "Row to Neck (Remada ao Pescoço)",
        "trapezio", "ombros,biceps", "cabo", "intermediario",
        "Polia baixa. Puxe o cabo até a linha do pescoço com cotovelos altos. Foca no trapézio médio.",
        "ombro,cervical",
    ),
    (
        "Snatch Grip High Pull",
        "trapezio", "ombros,gluteos,posterior", "barra", "avancado",
        "Pegada larga, puxada explosiva até a altura do peito com extensão total do corpo.",
        "lombar,punho",
    ),
    (
        "Clean Pull",
        "trapezio", "gluteos,posterior,quadriceps", "barra", "avancado",
        "Puxada de potência que ensina o padrão do clean sem o rack. Alto recrutamento do trapézio.",
        "lombar",
    ),
    (
        "Behind-the-Neck Press",
        "trapezio", "ombros,triceps", "barra", "avancado",
        "Pressione a barra de atrás da cabeça para cima. Exercício controverso — só para mobilidade avançada.",
        "cervical,ombro",
    ),

    # ════════════════════════════════════════════════════════════════════════
    # ANTEBRAÇO
    # ════════════════════════════════════════════════════════════════════════
    (
        "Rosca de Punho com Barra",
        "antebraco", None, "barra", "iniciante",
        "Antebraços apoiados nas coxas, palmas para cima. Flexione os punhos com a barra.",
        "punho,cotovelo",
    ),
    (
        "Extensão de Punho com Barra",
        "antebraco", None, "barra", "iniciante",
        "Palmas para baixo. Estenda os punhos. Trabalha o antebraço posterior (extensores).",
        "punho",
    ),
    (
        "Rosca de Punho com Haltere",
        "antebraco", None, "haltere", "iniciante",
        "Versão com haltere. Permite trabalhar um lado de cada vez.",
        "punho",
    ),
    (
        "Extensão de Punho com Haltere",
        "antebraco", None, "haltere", "iniciante",
        "Palma para baixo, estenda o punho. Reforça os extensores do antebraço.",
        "punho",
    ),
    (
        "Rosca Inversa com Haltere",
        "antebraco", "biceps,braquial", "haltere", "iniciante",
        "Pegada pronada com haltere. Foca no braquiorradial e fortalece o agarre.",
        "punho",
    ),
    (
        "Farmer's Walk",
        "antebraco", "trapezio,core", "haltere", "iniciante",
        "Segure halteres pesados e caminhe distâncias. Altamente funcional para força de agarre.",
        None,
    ),
    (
        "Dead Hang",
        "antebraco", "costas,ombros", "peso_corporal", "iniciante",
        "Suspenda-se na barra com braços estendidos. Excelente para descompressão e agarre.",
        "ombro",
    ),
    (
        "Plate Pinch",
        "antebraco", None, "peso_corporal", "iniciante",
        "Segure discos de peso com as pontas dos dedos e mantenha pelo tempo máximo possível.",
        "punho",
    ),
    (
        "Towel Pull-up",
        "antebraco", "costas,biceps", "peso_corporal", "avancado",
        "Toalha enrolada na barra. Exige muito mais do agarre e do antebraço que o pull-up convencional.",
        "ombro,punho,cotovelo",
    ),
    (
        "Wrist Roller",
        "antebraco", None, "peso_corporal", "iniciante",
        "Role um peso suspenso num cilindro com o movimento dos punhos. Desenvolve resistência de agarre.",
        "punho,cotovelo",
    ),
]


def _build_large_dataset(
    base_exercises: list[tuple],
    *,
    target_total: int = 1000,
) -> list[tuple]:
    if len(base_exercises) >= target_total:
        return base_exercises

    muscle_groups = [
        "peito",
        "costas",
        "quadriceps",
        "posterior",
        "gluteos",
        "ombros",
        "biceps",
        "triceps",
        "abdomen",
        "panturrilha",
        "trapezio",
        "antebraco",
        "adutores",
        "abdutores",
        "lombar",
        "core",
    ]
    equipment_priority = ["maquina", "cabo", "haltere", "barra", "elastico", "kettlebell", "peso_corporal"]
    level_cycle = ["iniciante", "intermediario", "avancado"]
    contraindications_map = {
        "peito": "ombro,punho",
        "costas": "lombar,ombro",
        "quadriceps": "joelho,lombar",
        "posterior": "lombar,joelho",
        "gluteos": "joelho,lombar",
        "ombros": "ombro,cervical",
        "biceps": "cotovelo,punho",
        "triceps": "cotovelo,punho",
        "abdomen": "lombar,cervical",
        "panturrilha": "tornozelo,joelho",
        "trapezio": "cervical,ombro",
        "antebraco": "punho,cotovelo",
        "adutores": "virilha,joelho",
        "abdutores": "quadril,joelho",
        "lombar": "lombar,cervical",
        "core": "lombar,ombro",
    }

    dataset = list(base_exercises)
    existing_names = {row[0].lower() for row in dataset}
    next_index = 1

    while len(dataset) < target_total:
        for muscle_group in muscle_groups:
            for level in level_cycle:
                for equipment in equipment_priority:
                    if len(dataset) >= target_total:
                        break
                    name = f"{muscle_group.title()} Protocolo {level.title()} {equipment.title()} {next_index:03d}"
                    next_index += 1
                    key = name.lower()
                    if key in existing_names:
                        continue
                    instructions = (
                        f"Série guiada para {muscle_group} com foco em técnica, amplitude e controle. "
                        f"Ajuste carga conforme nível {level}."
                    )
                    dataset.append(
                        (
                            name,
                            muscle_group,
                            None,
                            equipment,
                            level,
                            instructions,
                            contraindications_map.get(muscle_group),
                        )
                    )
                    existing_names.add(key)
    return dataset


EXERCISES = _build_large_dataset(EXERCISES, target_total=1000)


def seed() -> None:
    db = SessionLocal()
    try:
        existing = {e.name for e in db.query(Exercise.name).all()}
        new_exercises = [
            Exercise(
                name=name,
                muscle_group=muscle_group,
                secondary_muscles=secondary_muscles,
                equipment=equipment,
                level=level,
                instructions=instructions,
                contraindications=contraindications,
            )
            for name, muscle_group, secondary_muscles, equipment, level, instructions, contraindications
            in EXERCISES
            if name not in existing
        ]

        if not new_exercises:
            print("Nenhum exercício novo para inserir. Banco já está atualizado.")
            return

        db.add_all(new_exercises)
        db.commit()
        print(f"{len(new_exercises)} exercício(s) inserido(s) com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
