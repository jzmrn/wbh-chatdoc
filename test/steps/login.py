from behave import *

use_step_matcher("re")

@given("the user is logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is logged in')

@given("the user attempts to access the application")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user attempts to access the application')


@then("the user is redirected to the Microsoft Entra ID login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is redirected to the Microsoft Entra ID login page')


@given("the user navigates to the Microsoft Entra ID login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user navigates to the Microsoft Entra ID login page')


@when("the user enters valid credentials")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user enters valid credentials')


@then("the user is redirected to the main page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is redirected to the main page')


@when("the user enters invalid credentials")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user enters invalid credentials')


@then("the user remains on the login page and receives an error message")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user remains on the login page and receives an error message')


@step("the user's authentication token is invalid")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user\'s authentication token is invalid')