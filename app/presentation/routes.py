import json
from flask import Blueprint, request, jsonify, Response, stream_with_context, render_template
from app.presentation.schemas import CrawlRequest, ErrorResponse
from app.domain.exceptions import InvalidUrlError, DomainException
from app.container.service_container import get_container
from flask import current_app


bp = Blueprint('api', __name__)


@bp.route('/', methods=['GET'])
def index():
    """Serve the UI"""
    return render_template('index.html')


@bp.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        "service": "DFS Web Crawler API",
        "version": "2.1.0",
        "architecture": "Clean Architecture + Microservice Pattern",
        "endpoints": {
            "/crawl": {
                "method": "POST",
                "description": "Crawl website menggunakan DFS (non-streaming)",
                "body": {"url": "https://example.com"}
            },
            "/crawl/stream": {
                "method": "POST",
                "description": "Crawl website dengan streaming progress (SSE)",
                "body": {"url": "https://example.com"},
                "response": "Server-Sent Events stream"
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
        "version": "2.1.0"
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


@bp.route('/crawl/stream', methods=['POST'])
def crawl_stream():
    """
    Streaming endpoint menggunakan Server-Sent Events (SSE).
    
    Frontend bisa menggunakan EventSource untuk menerima progress:
    
    ```javascript
    const eventSource = new EventSource('/crawl/stream');
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data);
    };
    ```
    
    Atau dengan fetch:
    
    ```javascript
    const response = await fetch('/crawl/stream', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: 'https://example.com'})
    });
    const reader = response.body.getReader();
    // ... read stream
    ```
    """
    try:
        crawl_request = CrawlRequest.from_dict(request.get_json())
        container = get_container()
        
        # Validate URL first
        url_parser = container.get_url_parser()
        from app.use_cases.crawl_website import CrawlWebsiteUseCase
        use_case = CrawlWebsiteUseCase(container.get_crawler(), url_parser)
        use_case._validate_url(crawl_request.url)
        
        def generate():
            crawler = container.get_crawler()
            
            for event in crawler.crawl_stream(crawl_request.url):
                if event['type'] == 'complete':
                    # Convert CrawlResult to dict for JSON serialization
                    event = {
                        'type': 'complete',
                        'result': event['result'].to_dict()
                    }
                
                # Format as SSE
                yield f"data: {json.dumps(event)}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no',  # Disable nginx buffering
                'Access-Control-Allow-Origin': '*'
            }
        )
    
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
