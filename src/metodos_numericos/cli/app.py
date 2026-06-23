from __future__ import annotations
from metodos_numericos.representacao_numerica.troca_de_base.conversor import convert_base
from metodos_numericos.representacao_numerica.erros_numericos.erros import absolute_error, relative_error, percentage_error
from metodos_numericos.representacao_numerica.aritmetica_basica.fracao_mmc_mdc import prime_factorization, lcm, fraction_operation
from metodos_numericos.representacao_numerica.ponto_flutuante.maquina import classify_float_event
from metodos_numericos.equacoes_nao_lineares.bissecao.metodo_bissecao import bisection
from metodos_numericos.equacoes_nao_lineares.falsa_posicao.metodo_falsa_posicao import false_position
from metodos_numericos.equacoes_nao_lineares.newton.metodo_newton import newton
from metodos_numericos.equacoes_nao_lineares.secantes.metodo_secantes import secant
from metodos_numericos.equacoes_nao_lineares.ponto_fixo.metodo_ponto_fixo import fixed_point
from metodos_numericos.sistemas_lineares.gauss.eliminacao_gauss import gaussian_elimination
from metodos_numericos.sistemas_lineares.lu.decomposicao_lu import lu_decomposition
from metodos_numericos.sistemas_lineares.cholesky.decomposicao_cholesky import cholesky
from metodos_numericos.sistemas_lineares.metodos_iterativos.gauss_jacobi import jacobi
from metodos_numericos.sistemas_lineares.metodos_iterativos.gauss_seidel import gauss_seidel
from metodos_numericos.interpolacao_polinomial.lagrange.metodo_lagrange import lagrange
from metodos_numericos.interpolacao_polinomial.newton_diferencas_divididas.formula_newton import newton_interpolation
from metodos_numericos.interpolacao_polinomial.minimos_quadrados.ajuste_linear import least_squares_line
from metodos_numericos.calculo_numerico.integracao.trapezios import trapezoidal
from metodos_numericos.calculo_numerico.integracao.simpson_um_terco import simpson_one_third
from metodos_numericos.calculo_numerico.derivacao.diferencas_finitas import finite_difference
from metodos_numericos.compartilhado.funcoes import build_function


def read_float(message: str) -> float:
    return float(input(message).replace(",", "."))


def read_int(message: str) -> int:
    return int(input(message))


def read_vector(message: str) -> list[float]:
    return [float(x.replace(",", ".")) for x in input(message).replace(";", ",").split(",") if x.strip()]


def read_matrix() -> list[list[float]]:
    n = read_int("Ordem da matriz: ")
    matrix = []
    for i in range(n):
        matrix.append(read_vector(f"Linha {i + 1} separada por vírgula: "))
    return matrix


def print_result(result) -> None:
    print("\n" + result.as_text())


def menu() -> None:
    options = {
        "1": "Troca de base",
        "2": "Erros numéricos",
        "3": "Bisseção",
        "4": "Falsa posição",
        "5": "Newton-Raphson",
        "6": "Secantes",
        "7": "Ponto fixo",
        "8": "Eliminação de Gauss",
        "9": "Decomposição LU",
        "10": "Gauss-Jacobi",
        "11": "Gauss-Seidel",
        "12": "Cholesky",
        "13": "Lagrange",
        "14": "Newton interpolação",
        "15": "Mínimos quadrados linear",
        "16": "Trapézios",
        "17": "Simpson 1/3",
        "18": "Derivação numérica",
        "0": "Sair",
    }
    while True:
        print("\n=== Sistema de Métodos Numéricos ===")
        for key, label in options.items():
            print(f"{key} - {label}")
        choice = input("Escolha: ").strip()
        try:
            if choice == "0":
                break
            if choice == "1":
                number = input("Número: ")
                result = convert_base(number, read_int("Base origem: "), read_int("Base destino: "))
                print(f"Resultado: {result.converted} | decimal: {result.decimal_value}")
                for step in result.steps: print(f"- {step.description}: {step.value}")
            elif choice == "2":
                print("1 Erro absoluto/relativo | 2 Fatoração/MMC | 3 Fração | 4 Underflow/Overflow")
                sub = input("Tipo: ")
                if sub == "1":
                    ex, ap = read_float("Exato: "), read_float("Aproximado: ")
                    print("Erro absoluto:", absolute_error(ex, ap))
                    print("Erro relativo:", relative_error(ex, ap))
                    print("Erro percentual:", percentage_error(ex, ap))
                elif sub == "2":
                    nums = [int(v) for v in input("Números separados por vírgula: ").split(",")]
                    print("MMC:", lcm(*nums))
                    for n in nums: print(n, prime_factorization(n))
                elif sub == "3":
                    print(fraction_operation(input("a: "), input("operador: "), input("b: ")))
                else:
                    print(classify_float_event(read_float("Valor: "), read_int("Base: "), read_int("Precisão: "), read_int("Expoente mín: "), read_int("Expoente máx: ")))
            elif choice in {"3", "4", "5", "6", "7", "16", "17", "18"}:
                f = build_function(input("Função f(x) ou g(x): "))
                if choice == "3": print_result(bisection(f, read_float("a: "), read_float("b: "), read_float("tolerância: ")))
                if choice == "4": print_result(false_position(f, read_float("a: "), read_float("b: "), read_float("tolerância: ")))
                if choice == "5": print_result(newton(f, read_float("x0: "), read_float("tolerância: ")))
                if choice == "6": print_result(secant(f, read_float("x0: "), read_float("x1: "), read_float("tolerância: ")))
                if choice == "7": print_result(fixed_point(f, read_float("x0: "), read_float("tolerância: ")))
                if choice == "16": print_result(trapezoidal(f, read_float("a: "), read_float("b: "), read_int("n: ")))
                if choice == "17": print_result(simpson_one_third(f, read_float("a: "), read_float("b: "), read_int("n par: ")))
                if choice == "18": print_result(finite_difference(f, read_float("x: "), read_float("h: "), input("modo central/progressiva/regressiva: ")))
            elif choice in {"8", "9", "10", "11", "12"}:
                A = read_matrix()
                if choice == "8": print_result(gaussian_elimination(A, read_vector("Vetor b: ")))
                if choice == "9": print_result(lu_decomposition(A))
                if choice == "10": print_result(jacobi(A, read_vector("Vetor b: ")))
                if choice == "11": print_result(gauss_seidel(A, read_vector("Vetor b: ")))
                if choice == "12": print_result(cholesky(A))
            elif choice in {"13", "14", "15"}:
                xs = read_vector("Valores de x: ")
                ys = read_vector("Valores de y: ")
                if choice == "13": print_result(lagrange(xs, ys, read_float("x para calcular: ")))
                if choice == "14": print_result(newton_interpolation(xs, ys, read_float("x para calcular: ")))
                if choice == "15": print_result(least_squares_line(xs, ys))
        except Exception as exc:
            print(f"Erro: {exc}")

if __name__ == "__main__":
    menu()
