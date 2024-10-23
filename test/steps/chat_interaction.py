from behave import *

use_step_matcher("re")


@given("the user is in the chat section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is in the chat section')


@when("the user asks the question (?P<question>.+)")
def step_impl(context, question):
    """
    :type context: behave.runner.Context
    :type question: str
    """
    raise NotImplementedError(u'STEP: When the user asks the question <question>')


@then("the answer contains (?P<answer>.+) and a link to (?P<link>.+)")
def step_impl(context, answer, link):
    """
    :type context: behave.runner.Context
    :type answer: str
    :type link: str
    """
    raise NotImplementedError(u'STEP: Then the answer contains <answer> and a link to <link>')


@then("the user is navigated to the chat section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is navigated to the chat section')