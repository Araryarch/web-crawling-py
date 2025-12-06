from flask import Blueprint, request, jsonify
from app.presentation.schemas import CrawlRequest, ErrorResponse
from app.domain.exceptions import InvalidUrlError, DomainException
from app.container.service_container import get_container
from flask import current_app


bp = Blueprint('api', __name__)


@bp.route('/', methods=['GET'])
def index():
    return jsonify({
        "service": "DFS Web Crawler API",
        "version": "2.0.0",
        "architecture": "Clean Architecture + Microservice Pattern",
        "endpoints": {
            "/crawl": {
                "method": "POST",
                "description": "Crawl website menggunakan DFS",
                "body": {"url": "https://example.com"}
            },
            "/health": {
                "method": "GET",
                "description": "Health check endpoint"
            }
        }
    }), 200


@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "DFS Web Crawler API",
        "version": "2.0.0"
    }), 200


@bp.route('/crawl', methods=['POST'])
def crawl():
    try:
        crawl_request = CrawlRequest.from_dict(request.get_json())
        container = get_container()
        crawler_service = container.get_crawler_service()
        result = crawler_service.crawl_website(crawl_request.url)
        return jsonify(result), 200
    
    except ValueError as e:
        error = ErrorResponse(error="Invalid request", details=str(e))
        return jsonify(error.to_dict()), 400
    
    except InvalidUrlError as e:
        error = ErrorResponse(error="Invalid URL", details=str(e))
        return jsonify(error.to_dict()), 400
    
    except DomainException as e:
        error = ErrorResponse(error="Domain error", details=str(e))
        return jsonify(error.to_dict()), 400
    
    except Exception as e:
        error = ErrorResponse(
            error="Internal server error",
            details=str(e) if current_app.config['DEBUG'] else None
        )
        return jsonify(error.to_dict()), 500
