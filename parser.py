import re

def parse_instruction(text: str) -> list:
    text = text.lower().strip()
    commands = []

   
    if "login" in text:
        username = re.search(r"login with (\w+)", text)

        if username:
            commands.append({
                "action": "type",
                "target": "username_field",
                "value": username.group(1)
            })

        commands.append({
            "action": "click",
            "target": "submit_button",
            "value": None
        })

    
    if "form" in text or "fill" in text:
        name = re.search(r"name as (\w+)", text)
        email = re.search(r"email as ([\w@.]+)", text)

        if name:
            commands.append({
                "action": "type",
                "target": "name_field",
                "value": name.group(1)
            })

        if email:
            commands.append({
                "action": "type",
                "target": "email_field",
                "value": email.group(1)
            })

        if "male" in text:
            commands.append({
                "action": "click",
                "target": "gender_male",
                "value": None
            })

        if "female" in text:
            commands.append({
                "action": "click",
                "target": "gender_female",
                "value": None
            })

        if "student" in text:
            commands.append({
                "action": "type",
                "target": "role_select",
                "value": "student"
            })

        if "developer" in text:
            commands.append({
                "action": "type",
                "target": "role_select",
                "value": "developer"
            })

        if "tester" in text:
            commands.append({
                "action": "type",
                "target": "role_select",
                "value": "tester"
            })

        commands.append({
            "action": "click",
            "target": "submit_button",
            "value": None
        })

    return commands
