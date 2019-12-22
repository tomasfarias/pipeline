import pipeline
import logging


def test_get_logger():
    logger_info = pipeline.logging.get_logger('test_info', debug=False)
    logger_debug = pipeline.logging.get_logger('test_debug', debug=True)

    assert logger_info.getEffectiveLevel() == 20
    assert logger_debug.getEffectiveLevel() == 10
