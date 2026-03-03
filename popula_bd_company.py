import random
import string
from datetime import date, timedelta
import mysql.connector

# ==============================
# CONFIGURAÇÃO DO BANCO
# ==============================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="company"
)

cursor = conn.cursor()

# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def nome_aleatorio(tam=8):
    return ''.join(random.choices(string.ascii_letters, k=tam))

def data_aleatoria(inicio_ano=1990, fim_ano=2024):
    start = date(inicio_ano, 1, 1)
    end = date(fim_ano, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# ==============================
# PARÂMETROS
# ==============================

try:
    NUM_DEPARTAMENTOS = int(input("Quantidade de Departamentos: "))
    NUM_EMPREGADOS = int(input("Quantidade de Empregados: "))
    NUM_PROJETOS = int(input("Quantidade de Projetos: "))
except ValueError:
    print("Erro: Por favor, insira apenas números inteiros.")
    exit()

# ==============================
# GERAR EMPREGADOS
# ==============================

empregados = []

for i in range(1, NUM_EMPREGADOS + 1):
    empregados.append(i)

# Inserir empregados (temporariamente sem supervisor real)
for nss in empregados:
    cursor.execute("""
        INSERT INTO Empregado (NSS, DNUM, NSSSUPER, Pnome, Salario)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        nss,
        random.randint(1, NUM_DEPARTAMENTOS),
        nss,  # supervisor provisório (será corrigido)
        nome_aleatorio(),
        round(random.uniform(2000, 15000), 2)
    ))

conn.commit()

# Atualizar supervisores (ninguém supervisiona a si mesmo)
for nss in empregados:
    supervisor = random.choice([e for e in empregados if e != nss])
    cursor.execute("""
        UPDATE Empregado
        SET NSSSUPER = %s
        WHERE NSS = %s
    """, (supervisor, nss))

conn.commit()

# ==============================
# GERAR DEPARTAMENTOS
# ==============================

for dnum in range(1, NUM_DEPARTAMENTOS + 1):
    gerente = random.choice(empregados)

    cursor.execute("""
        INSERT INTO Departamento (Dnumero, NSSGER, DNome, DataInicioGer)
        VALUES (%s, %s, %s, %s)
    """, (
        dnum,
        gerente,
        "Dept_" + nome_aleatorio(5),
        data_aleatoria(2010, 2024)
    ))

conn.commit()

# ==============================
# GERAR PROJETOS
# ==============================

for pnum in range(1, NUM_PROJETOS + 1):
    cursor.execute("""
        INSERT INTO Projeto (PNumero, DNO, PNome, PLocalizacao)
        VALUES (%s, %s, %s, %s)
    """, (
        pnum,
        random.randint(1, NUM_DEPARTAMENTOS),
        "Proj_" + nome_aleatorio(6),
        random.choice(["SP", "RJ", "MG", "RS", "PR"])
    ))

conn.commit()

# ==============================
# GERAR DEPENDENTES
# ==============================

for nss in empregados:
    for _ in range(random.randint(0, 3)):
        cursor.execute("""
            INSERT INTO Dependente (NSSEMP, NomeDependente, DTNasc, Parentesco)
            VALUES (%s, %s, %s, %s)
        """, (
            nss,
            nome_aleatorio(),
            data_aleatoria(2000, 2023),
            random.choice(["Filho", "Filha", "Conjuge"])
        ))

conn.commit()

# ==============================
# GERAR TRABALHA_EM
# ==============================

for nss in empregados:
    projetos = random.sample(range(1, NUM_PROJETOS + 1), random.randint(1, NUM_PROJETOS))
    
    for p in projetos:
        cursor.execute("""
            INSERT INTO Trabalha_em (NSSE, PNO, Horas)
            VALUES (%s, %s, %s)
        """, (
            nss,
            p,
            random.randint(5, 40)
        ))

conn.commit()

cursor.close()
conn.close()

print("Banco populado com sucesso!")

