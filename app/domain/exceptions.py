class DomainException(Exception):
    pass


class InvalidUrlError(DomainException):
    def __init__(self, url: str, reason: str = ""):
        self.url = url
        self.reason = reason
        message = f"Invalid URL: {url}"
        if reason:
            message += f" - {reason}"
        super().__init__(message)


class CrawlError(DomainException):
    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        super().__init__(f"Failed to crawl {url}: {reason}")
