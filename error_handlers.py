from flask import render_template


def page_not_found(error):
    return render_template("page_not_found_error_page.html"), 404


def internal_server_error(error):
    return render_template("internal_server_error_page.html"), 500


def bad_request_error(error):
    return render_template("bad_request_error_page.html"), 400
