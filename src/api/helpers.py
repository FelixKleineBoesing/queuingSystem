import traceback


def statuscode_endpoint_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            status_code = 200
            message = "Successfully calculated"
        except Exception as e:
            res = {}
            status_code = 400
            message = "Raised error {} with traceback: {}".format(e, traceback.format_exc())
        return {"result": res, "status_code": status_code, "message": message}
    return wrapper
