from behave import *

use_step_matcher("re")

@given("the user has a previous chat history")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user has a previous chat history')

@given("the user has a previous chat history greater than (?P<char_count>\d+) characters")
def step_impl(context, char_count):
    """
    :type context: behave.runner.Context
    :type char_count: int
    """
    raise NotImplementedError(f'STEP: Given the user has a previous chat history greater than {char_count} characters')

@given("the user has a previous chat history with 100 entries")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user has a previous chat history with 100 entries')

@when("the user selects a previous chat")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user selects a previous chat')

@when("the user selects the large chat")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user selects the large chat')

@when("the user deletes a previous chat")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user deletes a previous chat')

@then("the chat conversation is displayed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the chat conversation is displayed')

@then("the user can continue the conversation if needed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user can continue the conversation if needed')

@then("the user can't continue the conversation")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user can\'t continue the conversation')

@then("the chat conversation is deleted")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the chat conversation is deleted')

@then("the oldest chat entry is deleted")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the oldest chat entry is deleted')


@then("the chat chat history is empty")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the chat chat history is empty')