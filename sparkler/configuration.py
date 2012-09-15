from configparser import SafeConfigParser

class Configuration():
    def __init__(self, options_dict=None):
        self.config = None
        self.reset()
        self.load_dict(options_dict)

    def load_dict(self, options_dict):
        if options_dict == None:
            return None

        for key in options_dict:
            self.config[key] = options_dict[key]

        self._detect_defaults()

        return self.config

    def reset(self):
        self.config = {
                "key" : None,
                "secret" : None,
                "auth_mode": "hybrid",
                "api_version": "v1",
                "api_endpoint_uri": "https://sparkapi.com",
                "auth_endpoint_uri": "https://sparkplatform.com/openid",
                "auth_callback_uri": None,
                "data_access_version": "v1"
        }
        return self.config

    def _detect_defaults(self):
        auth_mode = self.config["auth_mode"]
        if self.config.get("auth_enpoint_uri") == None:
            if auth_mode == "openid":
                self.config["auth_endpoint_uri"] = "https://sparkplatform.com/oauth2"
            elif auth_mode == "spark_auth":
                self.config["auth_endpoint_uri"] = "https://sparkapi.com/v1/session"
