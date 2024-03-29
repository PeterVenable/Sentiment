from sentiment_classifier import SentimentClassifier


def get_remote_client() -> SentimentClassifier:
    import clients
    from settings import settings
    if "client" not in settings:
        raise ValueError("No client specified in settings")
    client_settings = settings["client"]
    class_name = client_settings["class"]
    # import the class from the client module
    klass = getattr(clients, class_name, None)
    if not issubclass(klass, clients.GenericTextClassificationClient):
        raise ValueError(f"Unsupported client: {class_name}")
    return klass(
        url=client_settings["url"],
        headers=client_settings["headers"],
        method=client_settings["method"],
        timeout=int(client_settings.get("timeout", 5)),
    )


def get_local_classifier() -> SentimentClassifier:
    from huggingface import HuggingFaceSentimentClassifier
    from settings import settings
    try:
        kwargs = {"model": settings["model"]["name"]}
    except (KeyError, TypeError):
        raise ValueError("No model specified in settings")
    return HuggingFaceSentimentClassifier(**kwargs)


def get_fallback_classifier() -> SentimentClassifier:
    from fallback import FallBackSentimentClassifier
    from settings import settings
    primary = get_remote_client()
    secondary = get_local_classifier()
    fallback_settings = settings.get("fallback", {})
    kwargs = {
        k: v for k, v in fallback_settings.items()
        if k in ("retry_after", "increase_retry", "max_wait") and isinstance(v, (int, float))
    } if isinstance(fallback_settings, dict) else {}
    return FallBackSentimentClassifier(primary=primary, secondary=secondary, **kwargs)


def configure_logging():
    from logging.config import dictConfig
    from settings import settings
    log_settings = settings.get("logging")
    if log_settings:
        dictConfig(log_settings)
