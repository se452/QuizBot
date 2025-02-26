from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found",
            "status": 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status": 500
        }), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": "The method is not allowed for this endpoint",
            "status": 405
        }), 405 