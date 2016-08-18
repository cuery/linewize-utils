def init_new_relic(license_key, application_name):
    from newrelic import agent
    settings = agent.global_settings()

    settings.license_key = license_key
    settings.app_name = application_name
    settings.transaction_tracer.enabled = False
    settings.error_collector.enabled = False
    settings.slow_sql.enabled = False
    settings.browser_monitoring.auto_instrument = False
    agent.initialize()
