from behave import *

use_step_matcher("re")


@given("the user is in the (?P<section>.+) section")
def step_impl(context, section):
    """
    :type context: behave.runner.Context
    :type section: str
    """
    raise NotImplementedError(f'STEP: Given the user is in the {section} section')


@when("the user asks the question (?P<question>.+)")
def step_impl(context, question):
    """
    :type context: behave.runner.Context
    :type question: str
    """
    raise NotImplementedError(f'STEP: When the user asks the question {question}')


@then("the answer contains (?P<answer>.+) and a link to (?P<link>.+)")
def step_impl(context, answer, link):
    """
    :type context: behave.runner.Context
    :type answer: str
    :type link: str
    """
    raise NotImplementedError(f'STEP: Then the answer contains {answer} and a link to {link}')


@when("the user starts a new chat")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user starts a new chat')