# 代码生成时间: 2025-10-09 02:09:31
from pyramid.view import view_config
def validate_field(field_name, data, error_message):
    """
    Validate a form field and return an error message if the data is invalid.
    
    :param field_name: The name of the field to validate.
    :param data: The data to validate.
    :param error_message: The error message to display if the data is invalid.
    :return: A tuple with a boolean indicating validity and an error message.
    """
    if not data:
        return False, error_message
    return True, ""


def validate_form(form_data):
    """
    Validate a form's data and return a dictionary of errors or an empty dictionary if valid.
    
    :param form_data: A dictionary containing form fields and their data.
    :return: A dictionary with field names as keys and error messages as values.
    """
    errors = {}
    for field_name, validator in form_data.items():
        # Assume validator is a function that takes data and returns (is_valid, error_message)
        is_valid, error_message = validator(field_name, validator["data"], validator["error_message"])
        if not is_valid:
            errors[field_name] = error_message
    return errors

# Example usage
@view_config(route_name='form_validation', renderer='json')
def form_validator(request):
    # Example form data
    form_data = {
        "username": {
            "data": request.params.get("username"),
            "error_message": "Username is required."
        },
        "password": {
            "data": request.params.get("password"),
            "error_message": "Password is required."
        },
    }
    errors = validate_form(form_data)
    if errors:
        return {"success": False, "errors": errors}
    return {"success": True}