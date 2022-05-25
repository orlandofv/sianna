# This file contains common functions for apps 

def get_model_field(model, model_field, search_field, return_field):
    """
    Returns the a field given the a field
    """

    try:
        model = model.objects.get(model_field=search_field)
        return model.return_field
    except model.DoesNotExist:
        return None

