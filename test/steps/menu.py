from behave import *

use_step_matcher("re")


@when("the user clicks on the document management menu item")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user clicks on the document management menu item')


@when("the user clicks on the chat menu item")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user clicks on the chat menu item')


@then("the user is navigated to the chat section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is navigated to the chat section')