__author__ = 'Cody Harrington'
__email__ = 'cody.harrington@linewize.com'


# HONESTLY, this is fucking ridiculous
class HTTPStatusCodes(object):
    OK = 200
    CREATED = 200
    # Used after a DELETE request
    NO_CONTENT = 200

    BAD_REQUEST = 400
    UNAUTHORISED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404

    # This one means that the request is syntactically valid but semantically invalid
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
