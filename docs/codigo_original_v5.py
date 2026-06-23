
"""
SISTEMA COMPLETO DE MÉTODOS NUMÉRICOS E ANÁLISE DE ERROS - VERSÃO 5.0

Inclui:
- Erro absoluto
- Erro relativo
- Máximo erro relativo de arredondamento
- Proporção de erro
- MMC, MDC e fatoração prima
- Operações com frações
- Underflow e Overflow
- Bisseção
- Falsa Posição
- Newton-Raphson
- Secantes
- Ponto Fixo com tolerância manual, casas decimais, análise de convergência/divergência e função flexível
- Eliminação de Gauss
- Decomposição LU
- Gauss-Jacobi
- Gauss-Seidel
- Interpolação de Lagrange
- Interpolação de Newton
- Integração por Trapézios
- Integração por Simpson 1/3
- Derivação Numérica
- Decomposição de Cholesky

Uso didático: o programa mostra fórmulas, substituições, tabelas e resultados.

Entrada flexível de funções:
- x**3 - x - 2
- x^3 - x - 2
- x³ - x - 2
- sen(x) - x/2
- raiz(x) - 2
- √x - 2
- 2x + 3
- e^x - 3x
"""

from fractions import Fraction
from math import gcd
from functools import reduce
import math
import re


# ============================================================
# UTILIDADES
# ============================================================

def linha(tamanho=90):
    print("=" * tamanho)


def separador(tamanho=90):
    print("-" * tamanho)


def titulo(texto):
    linha()
    print(texto.center(90))
    linha()


def subtitulo(texto):
    print("\n" + texto)
    separador()


def pausa():
    input("\nPressione ENTER para continuar...")


def ler_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_float(msg):
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def ler_fracao(msg):
    while True:
        try:
            return Fraction(input(msg).strip().replace(",", "."))
        except Exception:
            print("Entrada inválida. Use 1/2, 0.5 ou 3.")


def imprimir_matriz(M, nome="Matriz"):
    print(f"\n{nome}:")
    for linha_m in M:
        print("[", end=" ")
        for v in linha_m:
            print(f"{v:>14.8f}", end=" ")
        print("]")


def imprimir_vetor(v, nome="Vetor"):
    print(f"\n{nome}:")
    for i, val in enumerate(v, start=1):
        print(f"x{i} = {val:.10f}")


def normalizar_expressao(expr):
    """
    Permite que o usuário digite funções de forma mais natural.

    Exemplos aceitos:
    x^3 - x - 2
    x³ - x - 2
    sen(x) - x/2
    raiz(x) - 2
    ln(x) - 1
    """

    expr_original = expr
    expr = expr.strip()

    # Troca vírgula decimal por ponto.
    expr = expr.replace(",", ".")

    # Troca expoentes unicode comuns por notação Python.
    expoentes = {
        "²": "**2",
        "³": "**3",
        "⁴": "**4",
        "⁵": "**5",
        "⁶": "**6",
        "⁷": "**7",
        "⁸": "**8",
        "⁹": "**9",
        "¹": "**1",
        "⁰": "**0"
    }

    for simbolo, substituto in expoentes.items():
        expr = expr.replace(simbolo, substituto)

    # Troca símbolo de raiz por sqrt.
    # Exemplos:
    # √x vira sqrt(x)
    # √(x+1) vira sqrt(x+1)
    expr = re.sub(r"√\(([^\)]+)\)", r"sqrt(\1)", expr)
    expr = re.sub(r"√([a-zA-Z0-9\.]+)", r"sqrt(\1)", expr)

    # Troca potência com ^ para **.
    expr = expr.replace("^", "**")

    # Permite e**x e e**(x+1) como exp(x) e exp(x+1).
    expr = re.sub(r"\be\*\*\(([^\)]+)\)", r"exp(\1)", expr)
    expr = re.sub(r"\be\*\*([a-zA-Z0-9\.]+)", r"exp(\1)", expr)

    # Nomes em português ou formatos comuns.
    substituicoes = {
        "sen": "sin",
        "tg": "tan",
        "raiz": "sqrt",
        "ln": "log"
    }

    for antigo, novo in substituicoes.items():
        expr = re.sub(rf"\b{antigo}\b", novo, expr, flags=re.IGNORECASE)

    # Permite escrever 2x, 3(x+1), x(x+1), 2sin(x), etc.
    expr = re.sub(r"(\d)(x)", r"\1*\2", expr)
    expr = re.sub(r"(x)(\d)", r"\1*\2", expr)
    expr = re.sub(r"(\d)\(", r"\1*(", expr)
    expr = re.sub(r"\)(\d)", r")*\1", expr)
    expr = re.sub(r"(x)\(", r"\1*(", expr)
    expr = re.sub(r"\)(x)", r")*\1", expr)

    # Evita quebrar nomes de funções conhecidos antes de parênteses.
    for nome_funcao in ["sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "log", "log10", "exp", "abs"]:
        expr = expr.replace(f"{nome_funcao}*(", f"{nome_funcao}(")

    return expr_original, expr


def criar_funcao(expr):
    expr_original, expr_normalizada = normalizar_expressao(expr)

    ambiente = {
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "exp": math.exp,
        "log": math.log,
        "log10": math.log10,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "pow": pow
    }

    def f(x):
        return eval(expr_normalizada, {"__builtins__": {}}, {**ambiente, "x": x})

    f.expr_original = expr_original
    f.expr_normalizada = expr_normalizada

    return f


def validar_e_mostrar_funcao(f, nome="f"):
    """
    Mostra como a função foi interpretada e faz testes simples.
    """

    print("\nFunção informada:")
    print(f"{nome}(x) =", getattr(f, "expr_original", "não disponível"))

    print("\nFunção interpretada pelo Python:")
    print(f"{nome}(x) =", getattr(f, "expr_normalizada", "não disponível"))

    print("\nTeste de validação:")

    pontos_teste = [0, 1, 2]

    for p in pontos_teste:
        try:
            valor = f(p)
            print(f"{nome}({p}) = {valor}")
        except Exception as erro:
            print(f"{nome}({p}) não pôde ser calculada: {erro}")

    print("\nFunção validada. Se os testes fizerem sentido para o exercício, continue normalmente.")


def derivada_numerica_func(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


def segunda_derivada_numerica_func(f, x, h=1e-4):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)


# ============================================================
# ARITMÉTICA / ERROS
# ============================================================

def fatoracao_prima(n):
    fatores = {}
    n = abs(int(n))
    if n in (0, 1):
        return fatores
    d = 2
    while d * d <= n:
        while n % d == 0:
            fatores[d] = fatores.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        fatores[n] = fatores.get(n, 0) + 1
    return fatores


def formatar_fatoracao(n):
    if n == 0:
        return "0 não possui fatoração prima"
    if abs(n) == 1:
        return str(n)
    fatores = fatoracao_prima(n)
    partes = []
    for p, e in fatores.items():
        partes.append(str(p) if e == 1 else f"{p}^{e}")
    return " × ".join(partes)


def calcular_mdc(lista):
    return reduce(gcd, [abs(x) for x in lista])


def calcular_mmc(lista):
    def mmc2(a, b):
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // gcd(a, b)
    return reduce(mmc2, lista)


def erro_absoluto():
    titulo("ERRO ABSOLUTO")
    ex = ler_fracao("Valor exato: ")
    ap = ler_fracao("Valor aproximado: ")
    r = abs(ex - ap)
    print("\nErro absoluto = |valor exato - valor aproximado|")
    print(f"Erro absoluto = |{ex} - {ap}|")
    print(f"Erro absoluto = |{ex - ap}|")
    print("Resultado =", r)
    print("Decimal =", float(r))


def erro_relativo():
    titulo("ERRO RELATIVO")
    ex = ler_fracao("Valor exato: ")
    ap = ler_fracao("Valor aproximado: ")
    print("\nErro relativo = |valor exato - valor aproximado| / |valor exato|")
    if ex == ap:
        print("Erro relativo = 0 (valor exatamente representado).")
        return
    if ex == 0:
        print("Não foi possível calcular o erro relativo com os dados atuais.")
        return
    ea = abs(ex - ap)
    er = ea / abs(ex)
    print(f"Erro relativo = {ea} / |{ex}|")
    print("Resultado =", er)
    print("Decimal =", float(er))
    print("Percentual =", float(er) * 100, "%")


def max_erro_arred():
    titulo("MÁXIMO ERRO RELATIVO DE ARREDONDAMENTO")
    base = ler_int("Base do sistema: ")
    mantissa = ler_int("Quantidade de dígitos/bits da mantissa: ")
    if base <= 0 or mantissa <= 0:
        print("Base e mantissa devem ser maiores que zero.")
        return
    eps = Fraction(base, 2) * Fraction(1, base ** mantissa)
    print("\nε = (base / 2) × base^(-mantissa)")
    print(f"ε = ({base}/2) × {base}^(-{mantissa})")
    print("Resultado =", eps)
    print("Decimal =", float(eps))


def proporcao_erro():
    titulo("PROPORÇÃO DE ERRO")
    ex = ler_fracao("Valor exato: ")
    ap = ler_fracao("Valor aproximado: ")
    if ex == 0:
        print("Não foi possível calcular, pois o valor exato é zero.")
        return
    ea = abs(ex - ap)
    p = ea / abs(ex)
    print("\nProporção de erro = erro absoluto / |valor exato|")
    print(f"Proporção = {ea} / |{ex}|")
    print("Resultado =", p)
    print("Decimal =", float(p))
    print("Percentual =", float(p) * 100, "%")


def mmc_mdc():
    titulo("MMC, MDC E FATORAÇÃO")
    nums = [int(x) for x in input("Digite os números separados por espaço: ").split()]
    print("\nFatoração:")
    for n in nums:
        print(f"{n} = {formatar_fatoracao(n)}")
    mdc = calcular_mdc(nums)
    mmc = calcular_mmc(nums)
    print("\nMDC =", mdc, "=", formatar_fatoracao(mdc))
    print("MMC =", mmc, "=", formatar_fatoracao(mmc))


def operacoes_fracoes():
    titulo("OPERAÇÕES COM FRAÇÕES")
    print("1 - Soma")
    print("2 - Subtração")
    print("3 - Multiplicação")
    print("4 - Divisão")
    op = input("Escolha: ").strip()

    n1 = ler_int("Numerador 1: ")
    d1 = ler_int("Denominador 1: ")
    n2 = ler_int("Numerador 2: ")
    d2 = ler_int("Denominador 2: ")

    if d1 == 0 or d2 == 0:
        print("Denominador não pode ser zero.")
        return

    mmc = calcular_mmc([d1, d2])
    mdc_den = calcular_mdc([d1, d2])

    print("\nFatoração dos denominadores:")
    print(f"{d1} = {formatar_fatoracao(d1)}")
    print(f"{d2} = {formatar_fatoracao(d2)}")
    print("MMC =", mmc, "=", formatar_fatoracao(mmc))
    print("MDC =", mdc_den, "=", formatar_fatoracao(mdc_den))

    if op == "1":
        a = n1 * (mmc // d1)
        b = n2 * (mmc // d2)
        num, den = a + b, mmc
        print(f"\n{n1}/{d1} + {n2}/{d2}")
        print(f"= ({a} + {b})/{mmc}")
    elif op == "2":
        a = n1 * (mmc // d1)
        b = n2 * (mmc // d2)
        num, den = a - b, mmc
        print(f"\n{n1}/{d1} - {n2}/{d2}")
        print(f"= ({a} - {b})/{mmc}")
    elif op == "3":
        num, den = n1 * n2, d1 * d2
        print(f"\n{n1}/{d1} × {n2}/{d2} = {num}/{den}")
    elif op == "4":
        if n2 == 0:
            print("Divisão inválida.")
            return
        num, den = n1 * d2, d1 * n2
        print(f"\n{n1}/{d1} ÷ {n2}/{d2} = {n1}/{d1} × {d2}/{n2} = {num}/{den}")
    else:
        print("Opção inválida.")
        return

    m = gcd(abs(num), abs(den))
    print("\nSimplificação:")
    print(f"MDC({abs(num)}, {abs(den)}) = {m}")
    print(f"{num}/{den} ÷ {m} = {num//m}/{den//m}")
    print("Resultado final =", Fraction(num, den))
    print("Decimal =", float(Fraction(num, den)))


def underflow_overflow():
    titulo("UNDERFLOW / OVERFLOW")
    pedir = input("O exercício pede essa análise? (S/N): ").strip().upper()
    if pedir != "S":
        print("Análise de Underflow/Overflow não solicitada.")
        return
    valor = ler_float("Valor calculado: ")
    menor = ler_float("Menor positivo representável: ")
    maior = ler_float("Maior representável: ")
    if abs(valor) > maior:
        print("Overflow detectado.")
    elif valor != 0 and abs(valor) < menor:
        print("Underflow detectado.")
    else:
        print("Valor representável no sistema.")


# ============================================================
# EQUAÇÕES NÃO LINEARES
# ============================================================

def ler_funcao_padrao():
    print("Digite a função com variável x.")
    print("Exemplos aceitos:")
    print("x**3 - x - 2")
    print("x^3 - x - 2")
    print("x³ - x - 2")
    print("sen(x) - x/2")
    print("sin(x) - x/2")
    print("raiz(x) - 2")
    print("sqrt(x) - 2")
    print("√x - 2")
    print("2x + 3")
    print("e^x - 3x")
    expr = input("f(x) = ").strip()
    f = criar_funcao(expr)

    # Teste mínimo para detectar erro de sintaxe.
    f(1)

    validar_e_mostrar_funcao(f, "f")

    return getattr(f, "expr_normalizada", expr), f


def bissecao():
    titulo("MÉTODO DA BISSEÇÃO")
    try:
        expr, f = ler_funcao_padrao()
    except Exception as e:
        print("Erro na função:", e)
        return

    a = ler_float("Intervalo a: ")
    b = ler_float("Intervalo b: ")
    tol_fx = ler_float("Tolerância para |f(x)|: ")
    tol_intervalo = ler_float("Tolerância para |b-a| (digite 0 para ignorar): ")
    max_it = ler_int("Máximo de iterações: ")

    fa, fb = f(a), f(b)
    print(f"\nf(a) × f(b) = {fa} × {fb} = {fa*fb}")
    if fa * fb > 0:
        print("Não há garantia de raiz pelo Teorema de Bolzano.")
        return

    print("\nFórmula: xm = (a+b)/2")
    print(f"{'i':>3} | {'a':>12} | {'b':>12} | {'xm':>12} | {'f(xm)':>14} | {'|f(xm)|':>14} | {'|b-a|':>12}")
    separador()

    raiz = None
    for i in range(1, max_it + 1):
        xm = (a + b) / 2
        fxm = f(xm)
        print(f"{i:>3} | {a:>12.8f} | {b:>12.8f} | {xm:>12.8f} | {fxm:>14.8f} | {abs(fxm):>14.8f} | {abs(b-a):>12.8f}")

        if abs(fxm) <= tol_fx or (tol_intervalo > 0 and abs(b-a) <= tol_intervalo):
            raiz = xm
            break

        if f(a) * fxm < 0:
            b = xm
        else:
            a = xm

    if raiz is None:
        raiz = (a + b) / 2

    print("\nResultado final:")
    print("Raiz aproximada =", raiz)
    print("f(raiz) =", f(raiz))


def falsa_posicao():
    titulo("MÉTODO DA FALSA POSIÇÃO")
    try:
        expr, f = ler_funcao_padrao()
    except Exception as e:
        print("Erro na função:", e)
        return

    a = ler_float("Intervalo a: ")
    b = ler_float("Intervalo b: ")
    tol_fx = ler_float("Tolerância para |f(x)|: ")
    tol_erro = ler_float("Tolerância para |x_novo - x_antigo| (digite 0 para ignorar): ")
    max_it = ler_int("Máximo de iterações: ")

    fa, fb = f(a), f(b)
    print(f"\nf(a) × f(b) = {fa} × {fb} = {fa*fb}")
    if fa * fb > 0:
        print("Não há garantia de raiz pelo Teorema de Bolzano.")
        return

    print("\nFórmula:")
    print("x = (a*f(b) - b*f(a)) / (f(b) - f(a))")

    print(f"{'i':>3} | {'a':>12} | {'b':>12} | {'x':>12} | {'f(x)':>14} | {'erro':>12}")
    separador()

    x_ant = None
    raiz = None

    for i in range(1, max_it + 1):
        fa, fb = f(a), f(b)
        if fb - fa == 0:
            print("Divisão por zero.")
            return

        x = (a * fb - b * fa) / (fb - fa)
        fx = f(x)
        erro = abs(x - x_ant) if x_ant is not None else float("inf")

        print(f"{i:>3} | {a:>12.8f} | {b:>12.8f} | {x:>12.8f} | {fx:>14.8f} | {erro:>12.8f}")

        if abs(fx) <= tol_fx or (tol_erro > 0 and x_ant is not None and erro <= tol_erro):
            raiz = x
            break

        if fa * fx < 0:
            b = x
        else:
            a = x

        x_ant = x

    if raiz is None:
        raiz = x

    print("\nResultado final:")
    print("Raiz aproximada =", raiz)
    print("f(raiz) =", f(raiz))


def newton_raphson():
    titulo("MÉTODO DE NEWTON-RAPHSON")
    try:
        expr, f = ler_funcao_padrao()
    except Exception as e:
        print("Erro na função:", e)
        return

    usar = input("Deseja inserir f'(x)? (S/N): ").strip().upper()
    if usar == "S":
        try:
            df_expr = input("f'(x) = ")
            df = criar_funcao(df_expr)
            df(1)
            validar_e_mostrar_funcao(df, "f'")
        except Exception as e:
            print("Erro na derivada:", e)
            return
    else:
        df = lambda x: derivada_numerica_func(f, x)

    x = ler_float("Chute inicial x0: ")
    tol_fx = ler_float("Tolerância para |f(x)|: ")
    tol_erro = ler_float("Tolerância para |x_novo - x_antigo|: ")
    max_it = ler_int("Máximo de iterações: ")

    print("\nFórmula: x(n+1) = x(n) - f(x(n))/f'(x(n))")
    print(f"{'i':>3} | {'x':>14} | {'f(x)':>14} | {'f’(x)':>14} | {'x novo':>14} | {'erro':>14}")
    separador()

    for i in range(1, max_it + 1):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            print("Derivada zero. Método interrompido.")
            return
        xn = x - fx / dfx
        erro = abs(xn - x)
        print(f"{i:>3} | {x:>14.8f} | {fx:>14.8f} | {dfx:>14.8f} | {xn:>14.8f} | {erro:>14.8f}")
        if abs(f(xn)) <= tol_fx or erro <= tol_erro:
            print("\nRaiz aproximada =", xn)
            print("f(raiz) =", f(xn))
            return
        x = xn

    print("\nÚltima aproximação =", x)
    print("f(x) =", f(x))


def secantes():
    titulo("MÉTODO DAS SECANTES")
    try:
        expr, f = ler_funcao_padrao()
    except Exception as e:
        print("Erro na função:", e)
        return

    x0 = ler_float("x0: ")
    x1 = ler_float("x1: ")
    tol_fx = ler_float("Tolerância para |f(x)|: ")
    tol_erro = ler_float("Tolerância para |x2 - x1|: ")
    max_it = ler_int("Máximo de iterações: ")

    print("\nFórmula: x2 = (x0*f(x1) - x1*f(x0)) / (f(x1) - f(x0))")
    print(f"{'i':>3} | {'x0':>14} | {'x1':>14} | {'x2':>14} | {'f(x2)':>14} | {'erro':>14}")
    separador()

    for i in range(1, max_it + 1):
        fx0, fx1 = f(x0), f(x1)
        den = fx1 - fx0
        if den == 0:
            print("Divisão por zero.")
            return
        x2 = (x0 * fx1 - x1 * fx0) / den
        fx2 = f(x2)
        erro = abs(x2 - x1)
        print(f"{i:>3} | {x0:>14.8f} | {x1:>14.8f} | {x2:>14.8f} | {fx2:>14.8f} | {erro:>14.8f}")
        if abs(fx2) <= tol_fx or erro <= tol_erro:
            print("\nRaiz aproximada =", x2)
            print("f(raiz) =", fx2)
            return
        x0, x1 = x1, x2

    print("\nÚltima aproximação =", x1)
    print("f(x) =", f(x1))


def ponto_fixo():
    titulo("MÉTODO DO PONTO FIXO")
    print("Neste método você informa g(x), onde x = g(x).")
    print("Exemplo: para x^3 - x - 2 = 0, uma forma possível é g(x) = (x+2)**(1/3)")

    try:
        g_expr = input("g(x) = ").strip()
        g = criar_funcao(g_expr)
        g(1)
        validar_e_mostrar_funcao(g, "g")
    except Exception as e:
        print("Erro em g(x):", e)
        return

    x = ler_float("Chute inicial x0: ")

    print("\nEscolha o critério de parada:")
    print("1 - Tolerância manual para |x_novo - x_antigo|")
    print("2 - Número de casas decimais desejadas")
    criterio = input("Opção: ").strip()

    casas_decimais = None

    if criterio == "1":
        tol_erro = ler_float("Tolerância para |x_novo - x_antigo|: ")

    elif criterio == "2":
        casas_decimais = ler_int("Quantidade de casas decimais desejadas: ")

        if casas_decimais <= 0:
            print("A quantidade de casas decimais deve ser maior que zero.")
            return

        tol_erro = 0.5 * (10 ** (-casas_decimais))

        print("\nConversão automática:")
        print("Para garantir n casas decimais corretas, usa-se:")
        print("tolerância = 0.5 × 10^(-n)")
        print(f"tolerância = 0.5 × 10^(-{casas_decimais})")
        print("tolerância =", tol_erro)

    else:
        print("Opção inválida.")
        return

    max_it = ler_int("Máximo de iterações: ")

    print("\nAnálise inicial de convergência:")
    print("Para o Método do Ponto Fixo, uma condição suficiente de convergência local é:")
    print("|g'(x)| < 1")

    try:
        g_linha_x0 = derivada_numerica_func(g, x)
        print(f"g'({x}) ≈ {g_linha_x0}")
        print(f"|g'({x})| ≈ {abs(g_linha_x0)}")

        if abs(g_linha_x0) < 1:
            print("Conclusão inicial: há indício de CONVERGÊNCIA local, pois |g'(x0)| < 1.")
        elif abs(g_linha_x0) > 1:
            print("Conclusão inicial: há indício de DIVERGÊNCIA local, pois |g'(x0)| > 1.")
        else:
            print("Conclusão inicial: caso inconclusivo, pois |g'(x0)| ≈ 1.")
    except Exception as e:
        print("Não foi possível estimar g'(x0).")
        print("Motivo:", e)

    print("\nFórmula:")
    print("x(n+1) = g(x(n))")

    print("\nCritério de parada usado:")
    if casas_decimais is None:
        print(f"|x_novo - x_antigo| <= {tol_erro}")
    else:
        print(f"{casas_decimais} casas decimais corretas")
        print(f"|x_novo - x_antigo| <= 0.5 × 10^(-{casas_decimais}) = {tol_erro}")

    print(f"\n{'i':>3} | {'x atual':>18} | {'x novo':>18} | {'erro':>18} | {'|g’(x novo)|':>18} | {'tendência':>14} | {'parada':>12}")
    separador()

    erros = []
    tendencia_final = "Inconclusiva"

    for i in range(1, max_it + 1):
        try:
            xn = g(x)
        except Exception as e:
            print("\nErro ao calcular g(x).")
            print("Motivo:", e)
            print("Conclusão: o método divergiu ou a função ficou fora do domínio permitido.")
            return

        erro = abs(xn - x)
        erros.append(erro)

        try:
            g_linha_xn = derivada_numerica_func(g, xn)
            modulo_derivada = abs(g_linha_xn)
        except Exception:
            modulo_derivada = float("nan")

        if len(erros) >= 2:
            if erros[-1] < erros[-2]:
                tendencia = "convergindo"
            elif erros[-1] > erros[-2]:
                tendencia = "divergindo"
            else:
                tendencia = "estável"
        else:
            tendencia = "inicial"

        tendencia_final = tendencia
        status = "SIM" if erro <= tol_erro else "NÃO"

        print(
            f"{i:>3} | "
            f"{x:>18.{casas_decimais + 4 if casas_decimais else 10}f} | "
            f"{xn:>18.{casas_decimais + 4 if casas_decimais else 10}f} | "
            f"{erro:>18.10f} | "
            f"{modulo_derivada:>18.10f} | "
            f"{tendencia:>14} | "
            f"{status:>12}"
        )

        print(f"\nIteração {i}:")
        print(f"x{i} = g(x{i-1}) = g({x}) = {xn}")
        print(f"erro = |x{i} - x{i-1}| = |{xn} - {x}| = {erro}")

        if not math.isfinite(xn) or not math.isfinite(erro):
            print("\nConclusão: o método DIVERGIU, pois gerou valor infinito ou indefinido.")
            return

        if erro <= tol_erro:
            print("\nCritério de parada atingido.")
            print(f"erro = {erro} <= {tol_erro}")

            print("\nAnálise final de convergência:")
            print("O método CONVERGIU para o critério informado.")

            try:
                g_linha_final = derivada_numerica_func(g, xn)
                print(f"g'({xn}) ≈ {g_linha_final}")
                print(f"|g'({xn})| ≈ {abs(g_linha_final)}")

                if abs(g_linha_final) < 1:
                    print("Confirmação: |g'(raiz aproximada)| < 1, indicando convergência local.")
                elif abs(g_linha_final) > 1:
                    print("Atenção: |g'(raiz aproximada)| > 1, o que pode indicar instabilidade.")
                else:
                    print("Atenção: |g'(raiz aproximada)| ≈ 1, caso limite.")
            except Exception:
                print("Não foi possível avaliar g'(raiz aproximada).")

            print("\nResultado final:")
            if casas_decimais is None:
                print("Ponto fixo aproximado =", xn)
            else:
                print(f"Ponto fixo aproximado com {casas_decimais} casas decimais =", round(xn, casas_decimais))
                print("Valor sem arredondar =", xn)

            return

        # Critério simples para alertar divergência durante as iterações:
        # se os últimos 3 erros aumentaram continuamente, há forte indício de divergência.
        if len(erros) >= 4 and erros[-1] > erros[-2] > erros[-3] > erros[-4]:
            print("\nAlerta de divergência:")
            print("Os erros aumentaram em várias iterações consecutivas.")
            print("Conclusão parcial: o método apresenta tendência de DIVERGÊNCIA para esse g(x) e x0.")
            continuar = input("Deseja continuar mesmo assim? (S/N): ").strip().upper()
            if continuar != "S":
                print("Método interrompido por tendência de divergência.")
                return

        x = xn

    print("\nO método parou pelo número máximo de iterações.")
    print("Última aproximação =", x)

    print("\nAnálise final de convergência:")
    if erros and erros[-1] <= tol_erro:
        print("O método CONVERGIU para o critério informado.")
    elif len(erros) >= 2 and erros[-1] < erros[0]:
        print("O método apresenta tendência de CONVERGÊNCIA, mas não atingiu a tolerância dentro do número máximo de iterações.")
    elif len(erros) >= 2 and erros[-1] > erros[0]:
        print("O método apresenta tendência de DIVERGÊNCIA ou instabilidade.")
    else:
        print("Não foi possível concluir claramente se houve convergência ou divergência.")

    if casas_decimais is not None:
        print(f"Última aproximação arredondada com {casas_decimais} casas decimais =", round(x, casas_decimais))


# ============================================================
# SISTEMAS LINEARES
# ============================================================

def ler_sistema():
    n = ler_int("Ordem do sistema: ")
    A = []
    b = []
    print("\nDigite a matriz A:")
    for i in range(n):
        linha_atual = []
        for j in range(n):
            linha_atual.append(ler_float(f"A[{i+1}][{j+1}]: "))
        A.append(linha_atual)
    print("\nDigite o vetor b:")
    for i in range(n):
        b.append(ler_float(f"b[{i+1}]: "))
    return A, b


def gauss():
    titulo("ELIMINAÇÃO DE GAUSS")
    A, b = ler_sistema()
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]

    imprimir_matriz(M, "Matriz aumentada inicial")

    for k in range(n - 1):
        subtitulo(f"Etapa {k+1}")
        if abs(M[k][k]) < 1e-15:
            troca = None
            for i in range(k + 1, n):
                if abs(M[i][k]) > 1e-15:
                    troca = i
                    break
            if troca is None:
                print("Não há pivô adequado.")
                return
            M[k], M[troca] = M[troca], M[k]
            print(f"Troca L{k+1} <-> L{troca+1}")

        for i in range(k + 1, n):
            m = M[i][k] / M[k][k]
            print(f"m{i+1}{k+1} = {M[i][k]} / {M[k][k]} = {m}")
            for j in range(k, n + 1):
                M[i][j] -= m * M[k][j]
        imprimir_matriz(M, "Matriz atual")

    x = [0.0] * n
    subtitulo("Retrosubstituição")
    for i in range(n - 1, -1, -1):
        soma = sum(M[i][j] * x[j] for j in range(i + 1, n))
        if abs(M[i][i]) < 1e-15:
            print("Divisão por zero.")
            return
        x[i] = (M[i][n] - soma) / M[i][i]
        print(f"x{i+1} = ({M[i][n]} - {soma}) / {M[i][i]} = {x[i]}")

    imprimir_vetor(x, "Solução")


def lu():
    titulo("DECOMPOSIÇÃO LU")
    A, b = ler_sistema()
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        L[i][i] = 1.0

    for k in range(n):
        subtitulo(f"Etapa {k+1}")
        for j in range(k, n):
            soma = sum(L[k][s] * U[s][j] for s in range(k))
            U[k][j] = A[k][j] - soma
            print(f"U[{k+1}][{j+1}] = {A[k][j]} - {soma} = {U[k][j]}")

        if abs(U[k][k]) < 1e-15:
            print("Pivô zero. LU sem pivotamento interrompida.")
            return

        for i in range(k + 1, n):
            soma = sum(L[i][s] * U[s][k] for s in range(k))
            L[i][k] = (A[i][k] - soma) / U[k][k]
            print(f"L[{i+1}][{k+1}] = ({A[i][k]} - {soma}) / {U[k][k]} = {L[i][k]}")

    imprimir_matriz(L, "L")
    imprimir_matriz(U, "U")

    y = [0.0] * n
    subtitulo("Resolver Ly = b")
    for i in range(n):
        soma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - soma) / L[i][i]
        print(f"y{i+1} = ({b[i]} - {soma}) / {L[i][i]} = {y[i]}")

    x = [0.0] * n
    subtitulo("Resolver Ux = y")
    for i in range(n - 1, -1, -1):
        soma = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - soma) / U[i][i]
        print(f"x{i+1} = ({y[i]} - {soma}) / {U[i][i]} = {x[i]}")

    imprimir_vetor(x, "Solução")


def jacobi():
    titulo("MÉTODO DE GAUSS-JACOBI")
    A, b = ler_sistema()
    n = len(A)
    x = [ler_float(f"Chute inicial x{i+1}: ") for i in range(n)]
    tol = ler_float("Tolerância para erro máximo: ")
    max_it = ler_int("Máximo de iterações: ")

    print("\nFórmula geral:")
    print("x_i^(k+1) = (b_i - soma(a_ij*x_j^(k), j≠i)) / a_ii")

    for i in range(n):
        if abs(A[i][i]) < 1e-15:
            print("Elemento diagonal zero. Método não pode continuar.")
            return

    print(f"{'i':>3} | " + " | ".join([f"x{j+1}".rjust(14) for j in range(n)]) + " | erro")
    separador()

    for it in range(1, max_it + 1):
        xn = [0.0] * n
        for i in range(n):
            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            xn[i] = (b[i] - soma) / A[i][i]
        erro = max(abs(xn[i] - x[i]) for i in range(n))
        print(f"{it:>3} | " + " | ".join([f"{v:>14.8f}" for v in xn]) + f" | {erro:.8f}")
        if erro <= tol:
            imprimir_vetor(xn, "Solução aproximada")
            return
        x = xn

    imprimir_vetor(x, "Última aproximação")


def gauss_seidel():
    titulo("MÉTODO DE GAUSS-SEIDEL")
    A, b = ler_sistema()
    n = len(A)
    x = [ler_float(f"Chute inicial x{i+1}: ") for i in range(n)]
    tol = ler_float("Tolerância para erro máximo: ")
    max_it = ler_int("Máximo de iterações: ")

    print("\nFórmula geral:")
    print("Usa os valores novos assim que são calculados.")

    for i in range(n):
        if abs(A[i][i]) < 1e-15:
            print("Elemento diagonal zero. Método não pode continuar.")
            return

    print(f"{'i':>3} | " + " | ".join([f"x{j+1}".rjust(14) for j in range(n)]) + " | erro")
    separador()

    for it in range(1, max_it + 1):
        x_old = x[:]
        for i in range(n):
            soma1 = sum(A[i][j] * x[j] for j in range(i))
            soma2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
            x[i] = (b[i] - soma1 - soma2) / A[i][i]
        erro = max(abs(x[i] - x_old[i]) for i in range(n))
        print(f"{it:>3} | " + " | ".join([f"{v:>14.8f}" for v in x]) + f" | {erro:.8f}")
        if erro <= tol:
            imprimir_vetor(x, "Solução aproximada")
            return

    imprimir_vetor(x, "Última aproximação")


def cholesky():
    titulo("DECOMPOSIÇÃO DE CHOLESKY")
    A, b = ler_sistema()
    n = len(A)

    for i in range(n):
        for j in range(n):
            if abs(A[i][j] - A[j][i]) > 1e-9:
                print("A matriz não é simétrica. Cholesky não recomendado.")
                return

    L = [[0.0] * n for _ in range(n)]

    print("\nObjetivo: A = L × Lᵀ")

    for i in range(n):
        for j in range(i + 1):
            soma = sum(L[i][k] * L[j][k] for k in range(j))

            if i == j:
                valor = A[i][i] - soma
                if valor <= 0:
                    print("Matriz não é definida positiva.")
                    return
                L[i][j] = math.sqrt(valor)
                print(f"L[{i+1}][{j+1}] = sqrt({A[i][i]} - {soma}) = {L[i][j]}")
            else:
                L[i][j] = (A[i][j] - soma) / L[j][j]
                print(f"L[{i+1}][{j+1}] = ({A[i][j]} - {soma}) / {L[j][j]} = {L[i][j]}")

    imprimir_matriz(L, "L")

    y = [0.0] * n
    subtitulo("Resolver Ly = b")
    for i in range(n):
        soma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - soma) / L[i][i]
        print(f"y{i+1} = ({b[i]} - {soma}) / {L[i][i]} = {y[i]}")

    x = [0.0] * n
    subtitulo("Resolver Lᵀx = y")
    for i in range(n - 1, -1, -1):
        soma = sum(L[j][i] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - soma) / L[i][i]
        print(f"x{i+1} = ({y[i]} - {soma}) / {L[i][i]} = {x[i]}")

    imprimir_vetor(x, "Solução")


# ============================================================
# INTERPOLAÇÃO
# ============================================================

def ler_pontos():
    n = ler_int("Quantidade de pontos: ")
    xs = []
    ys = []
    for i in range(n):
        xs.append(ler_float(f"x{i}: "))
        ys.append(ler_float(f"y{i}: "))
    return xs, ys


def interpolacao_lagrange():
    titulo("INTERPOLAÇÃO DE LAGRANGE")
    xs, ys = ler_pontos()
    x = ler_float("Valor de x para interpolar: ")
    n = len(xs)

    print("\nFórmula:")
    print("P(x) = soma y_i * L_i(x)")
    print("L_i(x) = produto (x - x_j)/(x_i - x_j), j ≠ i")

    resultado = 0.0
    for i in range(n):
        Li = 1.0
        print(f"\nL{i}(x):")
        for j in range(n):
            if i != j:
                fator = (x - xs[j]) / (xs[i] - xs[j])
                Li *= fator
                print(f"({x} - {xs[j]}) / ({xs[i]} - {xs[j]}) = {fator}")
        termo = ys[i] * Li
        resultado += termo
        print(f"y{i}*L{i} = {ys[i]} * {Li} = {termo}")

    print("\nResultado final:")
    print(f"P({x}) = {resultado}")


def interpolacao_newton():
    titulo("INTERPOLAÇÃO DE NEWTON - DIFERENÇAS DIVIDIDAS")
    xs, ys = ler_pontos()
    x = ler_float("Valor de x para interpolar: ")
    n = len(xs)

    tabela = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        tabela[i][0] = ys[i]

    for j in range(1, n):
        for i in range(n - j):
            tabela[i][j] = (tabela[i+1][j-1] - tabela[i][j-1]) / (xs[i+j] - xs[i])

    print("\nTabela de diferenças divididas:")
    for i in range(n):
        print([tabela[i][j] for j in range(n - i)])

    resultado = tabela[0][0]
    produto = 1.0

    print("\nPolinômio:")
    print(f"P(x) = {tabela[0][0]}", end="")

    for j in range(1, n):
        produto *= (x - xs[j-1])
        termo = tabela[0][j] * produto
        resultado += termo
        print(f" + ({tabela[0][j]})", end="")
        for k in range(j):
            print(f"(x - {xs[k]})", end="")

        print(f"\nTermo {j}: {tabela[0][j]} * {produto} = {termo}")

    print("\nResultado final:")
    print(f"P({x}) = {resultado}")


# ============================================================
# INTEGRAÇÃO E DERIVAÇÃO NUMÉRICA
# ============================================================

def trapezios():
    titulo("INTEGRAÇÃO NUMÉRICA - REGRA DOS TRAPÉZIOS")
    try:
        expr, f = ler_funcao_padrao()
    except Exception as e:
        print("Erro:", e)
        return

    a = ler_float("Limite inferior a: ")
    b = ler_float("Limite superior b: ")
    n = ler_int("Número de subintervalos n: ")
    if n <= 0:
        print("n deve ser maior que zero.")
        return

    h = (b - a) / n
    soma = f(a) + f(b)

    print("\nFórmula composta:")
    print("Integral ≈ h/2 * [f(x0) + 2*sum(f(xi)) + f(xn)]")
    print("h =", h)

    for i in range(1, n):
        xi = a + i * h
        fxi = f(xi)
        soma += 2 * fxi
        print(f"x{i} = {xi}, f(x{i}) = {fxi}, contribuição = 2*{fxi}")

    resultado = (h / 2) * soma
    print("\nResultado final:")
    print("Integral aproximada =", resultado)


def simpson_13():
    titulo("INTEGRAÇÃO NUMÉRICA - SIMPSON 1/3")
    try:
        expr, f = ler_funcao_padrao()
    except Exception as e:
        print("Erro:", e)
        return

    a = ler_float("Limite inferior a: ")
    b = ler_float("Limite superior b: ")
    n = ler_int("Número de subintervalos n par: ")

    if n <= 0 or n % 2 != 0:
        print("Para Simpson 1/3, n deve ser positivo e par.")
        return

    h = (b - a) / n
    soma = f(a) + f(b)

    print("\nFórmula composta:")
    print("Integral ≈ h/3 * [f(x0) + 4*sum(f(x ímpares)) + 2*sum(f(x pares)) + f(xn)]")
    print("h =", h)

    for i in range(1, n):
        xi = a + i * h
        fxi = f(xi)
        peso = 4 if i % 2 != 0 else 2
        soma += peso * fxi
        print(f"x{i} = {xi}, f(x{i}) = {fxi}, peso = {peso}, contribuição = {peso*fxi}")

    resultado = (h / 3) * soma
    print("\nResultado final:")
    print("Integral aproximada =", resultado)


def derivacao_numerica():
    titulo("DERIVAÇÃO NUMÉRICA")
    try:
        expr, f = ler_funcao_padrao()
    except Exception as e:
        print("Erro:", e)
        return

    x = ler_float("Ponto x: ")
    h = ler_float("Passo h: ")

    if h == 0:
        print("h não pode ser zero.")
        return

    print("\nEscolha:")
    print("1 - Diferença progressiva")
    print("2 - Diferença regressiva")
    print("3 - Diferença central")
    print("4 - Segunda derivada central")
    op = input("Opção: ").strip()

    if op == "1":
        r = (f(x + h) - f(x)) / h
        print("f'(x) ≈ [f(x+h)-f(x)]/h")
        print(f"= [{f(x+h)} - {f(x)}] / {h}")
    elif op == "2":
        r = (f(x) - f(x - h)) / h
        print("f'(x) ≈ [f(x)-f(x-h)]/h")
        print(f"= [{f(x)} - {f(x-h)}] / {h}")
    elif op == "3":
        r = (f(x + h) - f(x - h)) / (2 * h)
        print("f'(x) ≈ [f(x+h)-f(x-h)]/(2h)")
        print(f"= [{f(x+h)} - {f(x-h)}] / {2*h}")
    elif op == "4":
        r = (f(x + h) - 2*f(x) + f(x - h)) / (h ** 2)
        print("f''(x) ≈ [f(x+h)-2f(x)+f(x-h)]/h²")
        print(f"= [{f(x+h)} - 2*{f(x)} + {f(x-h)}] / {h**2}")
    else:
        print("Opção inválida.")
        return

    print("\nResultado =", r)


# ============================================================
# MENUS
# ============================================================

def menu_erros():
    while True:
        titulo("MENU - ANÁLISE DE ERROS")
        print("1 - Erro absoluto")
        print("2 - Erro relativo")
        print("3 - Máximo erro relativo de arredondamento")
        print("4 - Proporção de erro")
        print("5 - MMC/MDC e fatoração")
        print("6 - Operações com frações")
        print("7 - Underflow/Overflow")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1": erro_absoluto(); pausa()
        elif op == "2": erro_relativo(); pausa()
        elif op == "3": max_erro_arred(); pausa()
        elif op == "4": proporcao_erro(); pausa()
        elif op == "5": mmc_mdc(); pausa()
        elif op == "6": operacoes_fracoes(); pausa()
        elif op == "7": underflow_overflow(); pausa()
        elif op == "0": break
        else: print("Opção inválida.")


def menu_nao_lineares():
    while True:
        titulo("MENU - EQUAÇÕES NÃO LINEARES")
        print("1 - Bisseção")
        print("2 - Falsa Posição")
        print("3 - Newton-Raphson")
        print("4 - Secantes")
        print("5 - Ponto Fixo com tolerância manual, casas decimais, análise de convergência/divergência e função flexível")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1": bissecao(); pausa()
        elif op == "2": falsa_posicao(); pausa()
        elif op == "3": newton_raphson(); pausa()
        elif op == "4": secantes(); pausa()
        elif op == "5": ponto_fixo(); pausa()
        elif op == "0": break
        else: print("Opção inválida.")


def menu_lineares():
    while True:
        titulo("MENU - SISTEMAS LINEARES")
        print("1 - Eliminação de Gauss")
        print("2 - Decomposição LU")
        print("3 - Gauss-Jacobi")
        print("4 - Gauss-Seidel")
        print("5 - Cholesky")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1": gauss(); pausa()
        elif op == "2": lu(); pausa()
        elif op == "3": jacobi(); pausa()
        elif op == "4": gauss_seidel(); pausa()
        elif op == "5": cholesky(); pausa()
        elif op == "0": break
        else: print("Opção inválida.")


def menu_interpolacao_integracao():
    while True:
        titulo("MENU - INTERPOLAÇÃO, INTEGRAÇÃO E DERIVAÇÃO")
        print("1 - Interpolação de Lagrange")
        print("2 - Interpolação de Newton")
        print("3 - Regra dos Trapézios")
        print("4 - Regra de Simpson 1/3")
        print("5 - Derivação Numérica")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1": interpolacao_lagrange(); pausa()
        elif op == "2": interpolacao_newton(); pausa()
        elif op == "3": trapezios(); pausa()
        elif op == "4": simpson_13(); pausa()
        elif op == "5": derivacao_numerica(); pausa()
        elif op == "0": break
        else: print("Opção inválida.")


def menu_principal():
    while True:
        titulo("SISTEMA COMPLETO DE MÉTODOS NUMÉRICOS - VERSÃO 2.0")
        print("1 - Análise de erros, frações, MMC/MDC e overflow")
        print("2 - Equações não lineares")
        print("3 - Sistemas lineares")
        print("4 - Interpolação, integração e derivação")
        print("0 - Sair")
        op = input("Escolha: ").strip()
        try:
            if op == "1": menu_erros()
            elif op == "2": menu_nao_lineares()
            elif op == "3": menu_lineares()
            elif op == "4": menu_interpolacao_integracao()
            elif op == "0":
                print("Programa encerrado.")
                break
            else:
                print("Opção inválida.")
        except KeyboardInterrupt:
            print("\nPrograma interrompido pelo usuário.")
            break
        except Exception as e:
            print("\nOcorreu um erro:")
            print(e)
            pausa()


if __name__ == "__main__":
    menu_principal()
