class AssertionGenerator:
    def generate(self, actions):
        """
        Generate assertions based on actions.
        """
        assertions = []

        for action in actions:
            if action["action"] == "navigate":
                # Assert that the page URL contains the expected domain or path
                url = action["url"]
                if "youtube" in url:
                    assertions.append({
                        "type": "url_contains",
                        "value": "youtube"
                    })
                elif "google" in url:
                    assertions.append({
                        "type": "url_contains",
                        "value": "google"
                    })
                elif "github" in url:
                    assertions.append({
                        "type": "url_contains",
                        "value": "github"
                    })
                elif "linkedin" in url:
                    assertions.append({
                        "type": "url_contains",
                        "value": "linkedin"
                    })
                elif "login" in url.lower():
                    assertions.append({
                        "type": "url_contains",
                        "value": "login"
                    })
                else:
                    # For other sites, check the domain
                    if "://" in url:
                        domain = url.split("://")[1].split("/")[0]
                        if "." in domain:
                            site_name = domain.split(".")[-2]  # e.g., github from github.com
                            assertions.append({
                                "type": "url_contains",
                                "value": site_name
                            })
            elif action["action"] == "click" and action["element"].lower() == "login":
                assertions.append({
                    "type": "url_contains",
                    "value": "agent"
                })
            elif action["action"] == "fill":
                # Assert that the field has the entered value
                # Use the mapped field name (username, password) as that's what gets filled
                assertions.append({
                    "type": "field_value",
                    "field": action["field"],
                    "value": action["value"]
                })
            elif action["action"] == "assert":
                # Assert that specific text is present on the page
                assertions.append({
                    "type": "text_contains",
                    "value": action["text"]
                })

        return assertions
