from flask import jsonify, make_response, Response
from loguru import logger


def get_response(status_code: int, content: str | dict | list) -> Response:
    if isinstance(content, str):
        logger.info(content)
        content = {"message": content}

    return make_response(jsonify(content), status_code)
