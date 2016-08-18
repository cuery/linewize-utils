import json
from flask import jsonify


class InterApplicationException(Exception):
    def __init__(self, causing_application, exception, from_url=None, to_url=None, to_status_code=None, message=None, device_id=None):
        self.causing_application = causing_application
        self.exception = exception
        self.from_url = from_url
        self.to_url = to_url
        self.to_status_code = to_status_code
        self.message = message
        self.device_id = device_id
        self.stack_trace = None

    def __str__(self):
        return json.dumps(self.__dict__)


def error_handled_response(current_app, response_obj):
    if response_obj.status_code / 500 == 1:
        try:
            response_json = json.loads(response_obj.text)
            if 'error' in response_json:
                ex = InterApplicationException(
                    response_json['error']['causing_application'], response_json['error']['exception'],
                    response_json['error']['from_url'], response_json['error']['to_url'],
                    response_json['error']['to_status_code'], response_json['error']['message'],
                    response_json['error']['device_id']
                )

                if not ex.to_url:
                    ex.to_url = ex.from_url
                if not ex.to_status_code:
                    ex.to_status_code = response_obj.status_code
                raise ex
            else:
                raise InterApplicationException(
                    current_app, response_obj.text, to_url=response_obj.url,
                    to_status_code=response_obj.status_code, message='Malformed error handling JSON response'
                )
        except ValueError:
            raise InterApplicationException(
                current_app, response_obj.text, to_url=response_obj.url,
                to_status_code=response_obj.status_code, message='Unknown root cause, json.loads failed'
            )

    elif response_obj.status_code == 403:
        return response_obj

    elif response_obj.status_code == 401:
        return response_obj

    elif response_obj.status_code / 400 == 1:
        raise InterApplicationException(
            current_app, str(response_obj.status_code), to_url=response_obj.url,
            to_status_code=response_obj.status_code
        )

    return response_obj

def is_exposable(msg):
    msg = str(msg).lower()
    if 'line' in msg or 'exception' in msg:
        return False
    return True


def catch_inter_application_exception(exception, from_url, logger=None, redirect_url=None):
    exception.from_url = from_url
    if logger:
        logger.error(exception)

    if redirect_url:
        from flask import redirect
        from flask.helpers import flash
        if exception.message and is_exposable(exception.message):
            flash(exception.message)
        else:
            flash('An error occurred.')
        return redirect(redirect_url)

    response = jsonify({"error": exception.__dict__})
    response.status_code = 500
    return response


def catch_application_exception(causing_application, exception, from_url=None, logger=None, new_relic_agent=None,
                                redirect_url=None, stacktrace=None, device_id=None, message=None):
    inter_app_exception = InterApplicationException(causing_application, str(exception), from_url=from_url)

    if not inter_app_exception.exception and exception.message:
        inter_app_exception.exception = exception.message

    if message:
        inter_app_exception.message = message

    if device_id:
        inter_app_exception.device_id = device_id

    if logger:
        if stacktrace:
            inter_app_exception.stack_trace = stacktrace
            if len(str(inter_app_exception)) >= 2000:
                inter_app_exception.stack_trace = "Too long for syslog."

        logger.error(inter_app_exception)

    if new_relic_agent:
        new_relic_agent.record_exception()

    if redirect_url:
        from flask import redirect
        from flask.helpers import flash
        # if inter_app_exception.message:
        #     flash(inter_app_exception.message)
        # else:
        flash('An error occurred.')

        return redirect(redirect_url)

    response = jsonify({"error": inter_app_exception.__dict__})
    response.status_code = 500
    return response
