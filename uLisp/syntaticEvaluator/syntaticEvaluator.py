from uLisp.interpreter import global_env,Symbol,Environment
from uLisp.utils.utils import change_function


class SyntacticExpression(object):
    """
    This a common interface to define syntaticEvaluator expressions
    """

    def __init__(self, evaluator):
        self.evaluator = evaluator

    def check_condition(self, expression, env=global_env):
        raise NotImplementedError

    def do_action(self, expression, env):
        raise NotImplementedError


class DynamicSyntacticExpression(SyntacticExpression):
    """
    This a common interface to define syntaticEvaluator expressions, that can be set on runtime
    """

    def __init__(self, evaluator, condition, action):
        super().__init__(evaluator)
        change_function(self, 'check_condition', condition)
        change_function(self, 'do_action', action)

    def check_condition(self, expression, env=global_env):
        pass

    def do_action(self, expression, env):
        pass


class VariableReferenceExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return isinstance(expression, Symbol)

    def do_action(self, expression, env):
        return env.find(expression)[expression]


class ConstantLiteralExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return not isinstance(expression, list)

    def do_action(self, expression, env):
        return expression


class ConstantListExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return expression[0] == 'cons'

    def do_action(self, expression, env):
        print(expression)
        return expression[1:]


class QuoteExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return expression[0] == 'quote'

    def do_action(self, expression, env):
        (_, expression) = expression


class IfConditionExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return expression[0] == 'if'

    def do_action(self, expression, env):
        (_, test, conseq, alt) = expression
        return self.evaluator.evaluate((conseq if self.evaluator.evaluate(test, env) else alt), env)


class SetVariableExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return expression[0] == 'setq'

    def do_action(self, expression, env):
        (_, var, exp) = expression
        env.find(var)[var] = self.evaluator.evaluate(exp, env)


class DefunExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return expression[0] == 'defun'

    def do_action(self, expression, env):
        (_, var, exp) = expression
        env[var] = self.evaluator.evaluate(exp, env)


class LambdaExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return expression[0] == 'lambda'

    def do_action(self, expression, env):
        (_, variables, exp) = expression
        return lambda *args: self.evaluator.evaluate(exp, Environment(variables, args, env))


class BeginExpression(SyntacticExpression):
    def check_condition(self, expression, env=global_env):
        return expression[0] == 'begin'

    def do_action(self, expression, env):
        for exp in expression[1:]:
            value = self.evaluator.evaluate(exp, env)
        return value


global_eval_expressions = [VariableReferenceExpression, ConstantLiteralExpression, QuoteExpression,
                           IfConditionExpression, SetVariableExpression, DefunExpression, LambdaExpression,
                           BeginExpression, ConstantListExpression]


class SyntacticEvaluator(object):
    def __init__(self, initial_evaluator=global_eval_expressions):
        self.expressions = []
        for expression in initial_evaluator:
            self.add_syntatic_expression(expression)

    def add_syntatic_expression(self, expression_class):
        self.expressions.append(expression_class(self))

    def add_dynamic_syntatic_expression(self, expression_tuple):
        self.expressions.append(SyntacticExpression(*expression_tuple))

    def evaluate(self, expression, env=global_env):
        for expr in self.expressions:
            if expr.check_condition(expression, env):
                return expr.do_action(expression, env)
                # (proc exp*)
        #TODO: reify this default action as an another Syntatic Expression class
        exps = [self.evaluate(exp, env) for exp in expression]
        proc = exps.pop(0)
        return proc(*exps)

