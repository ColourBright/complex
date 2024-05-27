import cmath
import math
import numpy as np
from typing import Callable

from parser import Expression, Token, TokenType, ExpressionType, Parser


class Solver:
    constants = Parser.constants

    @staticmethod
    def get_solution_for_array(exp: Expression) -> Callable[[list[complex]], list[complex]]:
        return np.vectorize(Solver.get_solution(exp))

    @staticmethod
    def get_solution(exp: Expression) -> Callable[[complex], complex]:
        if exp.type == ExpressionType.VAL:
            return Solver.get_solution_for_val(exp.value)
        if exp.type == ExpressionType.FUNC:
            return Solver.get_solution_for_func(exp.value)
        if exp.type == ExpressionType.UNARY:
            return Solver.get_solution_for_unary(exp.value)
        if exp.type == ExpressionType.PAR:
            return Solver.get_solution_for_par(exp.value)
        if exp.type == ExpressionType.BINARY:
            return Solver.get_solution_for_binary(exp.value)
        raise ValueError(f'Not sopported expression type: {exp.type}')

    @staticmethod
    def get_solution_for_val(exp: list[Expression | Token]) -> Callable[[complex], complex]:
        value = exp[0].value
        e_type = exp[0].type
        if e_type == TokenType.CONST:
            if value == 'i':
                return lambda z: 1j
            elif value == 'pi':
                return lambda z: np.pi
            elif value == 'e':
                return lambda z: np.e
            else:
                raise ValueError(f'Not implemented: {value}')
        elif e_type == TokenType.NUM:
            return lambda x: float(value)
        else:
            return lambda z: z

    # 'real', 'im', 'sin', 'cos', 'tg', 'asin', 'acos', 'atg', 'ln', 'abs', 'phi'
    @staticmethod
    def get_func1(f_name) -> Callable[[complex], complex]:
        if f_name == 'real':
            return lambda z: z.real
        if f_name == 'im':
            return lambda z: z.imag
        if f_name == 'sin':
            return lambda z: np.sin(z)
        if f_name == 'cos':
            return lambda z: np.cos(z)
        if f_name == 'tg':
            return lambda z: np.tan(z)
        if f_name == 'asin':
            return lambda z: np.arcsin(z)
        if f_name == 'acos':
            return lambda z: np.arccos(z)
        if f_name == 'atg':
            return lambda z: np.arctan(z)
        if f_name == 'ln':
            return lambda z: np.log(z)
        if f_name == 'abs':
            return lambda z: np.abs(z)
        if f_name == 'phi':
            return lambda z: cmath.phase(z)
        raise ValueError(f'Unknown func: {f_name}')

    # log
    @staticmethod
    def get_func2(f_name):
        if f_name == 'log':
            return lambda x, y: np.log(x+0j) / np.log(y+0j)
        raise ValueError(f'Unknown func: {f_name}')

    @staticmethod
    def get_solution_for_func(exp: list[Expression | Token]) -> Callable[[complex], complex]:
        if exp[0].type == TokenType.FUNC1:
            solve = Solver.get_func1(exp[0].value)  # func ( exp )
            return lambda z: solve((Solver.get_solution(exp[2]))(z))
        elif exp[0].type == TokenType.FUNC2:
            solve1 = Solver.get_solution(exp[2])
            solve2 = Solver.get_solution(exp[4])  # func ( exp , exp )
            return lambda z: Solver.get_func2(exp[0].value)(solve1(z), solve2(z))

    @staticmethod
    def get_solution_for_unary(exp: list[Expression | Token]) -> Callable[[complex], complex]:
        value = exp[0].value
        e_type = exp[0].type
        if e_type == TokenType.UNARY:
            if value == '-':
                return lambda z: -(Solver.get_solution(exp[1])(z))
        raise ValueError(f'Not implemented: {value}')

    @staticmethod
    def get_solution_for_par(exp: list[Expression | Token]) -> Callable[[complex], complex]:
        value = exp[0].value
        if exp[0].type == TokenType.PARL and exp[2].type == TokenType.PARR:
            return lambda z: Solver.get_solution(exp[1])(z)
        raise ValueError(f'Not implemented: {value}')

    @staticmethod
    def get_solution_for_binary(exp: list[Expression | Token]) -> Callable[[complex], complex]:
        if exp[1].type == TokenType.BINARY:
            op = exp[1].value
            solve1 = Solver.get_solution(exp[0])
            solve2 = Solver.get_solution(exp[2])  # exp op exp
            if op == '+':
                return lambda z: solve1(z) + solve2(z)
            if op == '-':
                return lambda z: solve1(z) - solve2(z)
            if op == '*':
                return lambda z: solve1(z) * solve2(z)
            if op == '/':
                return lambda z: solve1(z) / solve2(z)
            if op == '^':
                return lambda z: solve1(z) ** solve2(z)
        raise ValueError(f'Not implemented: {exp[1].value}')