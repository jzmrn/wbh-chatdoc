from behave import *

use_step_matcher("re")


@given("the user is in the document upload section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is in the document upload section')


@when("the user uploads a document in pdf format")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user uploads a document in pdf format')


@then("the document is successfully added to the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is successfully added to the system')


@when("the user attempts to upload a document in an unsupported format")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user attempts to upload a document in an unsupported format')


@then("the document is not uploaded an error message is displayed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is not uploaded an error message is displayed')


@then("the user is navigated to the document management section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is navigated to the document management section')


@given("the user has the role test")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user has the role test')


@when("the user accesses the document management section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user accesses the document management section')


@then("the user sees only private and role related documents")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user sees only private and role related documents')


@given("the user is in the document management section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is in the document management section')


@when("the user uploads a new document")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user uploads a new document')


@then("the document is added in the document list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is added in the document list')