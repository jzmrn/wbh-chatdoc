from behave import *

use_step_matcher("re")

@given("the user is logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is logged in')

@given("the unauthorized user attempts to access the application")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user attempts to access the application')

@given("the user navigates to the Microsoft Entra ID login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user navigates to the Microsoft Entra ID login page')

@given("the admin user is logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the admin user is logged in')

@given("the user with role (?P<role>.+) is logged in")
def step_impl(context, role):
    """
    :type context: behave.runner.Context
    :type role: str
    """
    raise NotImplementedError(f'STEP: And the user with role {role} is logged in')

@when("the user enters valid credentials")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user enters valid credentials')

@when("the user enters invalid credentials")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user enters invalid credentials')

@then("the user is redirected to the Microsoft Entra ID login page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is redirected to the Microsoft Entra ID login page')

@then("the user is redirected to the main page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is redirected to the main page')

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


@step("a new user is logged in")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And a new user is logged in')