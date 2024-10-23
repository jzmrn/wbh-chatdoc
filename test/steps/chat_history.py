from behave import *

use_step_matcher("re")


@given("the user has a previous chat history")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user has a previous chat history')


@when("the user selects a previous chat")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user selects a previous chat')


@then("the chat conversation is displayed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the chat conversation is displayed')


@step("the user can continue the conversation if needed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user can continue the conversation if needed')