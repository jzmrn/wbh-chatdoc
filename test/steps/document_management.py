from behave import *

use_step_matcher("re")


@given("the user is in the document upload section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is in the document upload section')


@given("the user is in the document management section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Given the user is in the document management section')


@given("document (?P<document_name>.+) with role (?P<role>.+) is uploaded")
def step_impl(context, document_name, role):
    """
    :type context: behave.runner.Context
    :type document_name: str
    :type role: str
    """
    raise NotImplementedError(f'STEP: And document {document_name} with role {role} is uploaded')


@given("no other documents are uploaded")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And no other documents are uploaded')


@when("the user uploads a document in (?P<format>.+) format")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user uploads a document in {format} format')


@when("the user attempts to upload a document in an unsupported format")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user attempts to upload a document in an unsupported format')


@when("the user accesses the document management section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user accesses the document management section')


@when("the user uploads a new document")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user uploads a new document')


@when("the user deletes a document")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user deletes a document')


@when("the user uploads a document in pdf format greater than 10MB")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: When the user uploads a document in pdf format greater than 10MB')


@then("the document is successfully added to the system")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is successfully added to the system')


@then("the document is not uploaded and an error message is displayed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is not uploaded and an error message is displayed')


@then("the user is navigated to the document management section")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user is navigated to the document management section')


@then("the user sees only private and role related documents")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user sees only private and role related documents')


@then("the document is added in the document list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is added in the document list')


@then("the document is not uploaded")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is not uploaded')


@then("the document is removed from the document list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the document is removed from the document list')


@then("the user sees the documents (?P<document_name>.+)")
def step_impl(context, document_name):
    """
    :param document_name:
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Then the user sees the documents {document_name}')


@step("the user does not see the documents (?P<document_name>.+)")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the user does not see the documents {document_name}')
