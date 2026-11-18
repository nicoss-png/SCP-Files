import json
import os

USER_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")

EASTER_EGG_NAME = "Reptor Tech Inc."
EASTER_EGG_PASSWORD = "Reptor"

# Easter egg: the 12 secret O5 accounts in plaintext.
O5_ACCOUNTS = {
    "O5-1":  {"pass": "EVE-01",        "title": "The Founder",        "site": "Site-01"},
    "O5-2":  {"pass": "NAZARENE-02",   "title": "The Nazarene",       "site": "Site-01"},
    "O5-3":  {"pass": "KID-03",        "title": "The All-Seeing Eye", "site": "Site-01"},
    "O5-4":  {"pass": "AMBASSADOR-04", "title": "The Ambassador",     "site": "Site-01"},
    "O5-5":  {"pass": "BLACKBIRD-05",  "title": "Blackbird",          "site": "Site-01"},
    "O5-6":  {"pass": "COWBOY-06",     "title": "The American",       "site": "Site-01"},
    "O5-7":  {"pass": "GREEN-07",      "title": "Green",              "site": "Site-01"},
    "O5-8":  {"pass": "DOGWOOD-08",    "title": "The Lesser",         "site": "Site-01"},
    "O5-9":  {"pass": "OUTSIDER-09",   "title": "The Outsider",       "site": "Site-01"},
    "O5-10": {"pass": "ARCHIVIST-10",  "title": "The Archivist",      "site": "Site-01"},
    "O5-11": {"pass": "LIAR-11",       "title": "The Liar",           "site": "Site-01"},
    "O5-12": {"pass": "ACCOUNTANT-12", "title": "The Accountant",     "site": "Site-01"},
}


def is_reptor_easter_egg(name, password):
    return name.strip().casefold() == EASTER_EGG_NAME.casefold() and password == EASTER_EGG_PASSWORD


def load_users() -> dict:
    if not os.path.exists(USER_DB):
        return {}
    try:
        with open(USER_DB, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return {}
            users = json.loads(content)
            return users if isinstance(users, dict) else {}
    except json.JSONDecodeError:
        return {}


def save_users(users: dict):
    with open(USER_DB, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def register_user(name, password, clearance, personnel, site, mtf="", committee=""):
    users = load_users()
    key = name.strip()

    if not key or not password:
        return False, "NAME AND PASSWORD ARE REQUIRED."
    if key.upper() in O5_ACCOUNTS or key.casefold() == EASTER_EGG_NAME.casefold() or key in users:
        return False, "USERNAME IS ALREADY TAKEN OR RESERVED."
    if clearance.strip() not in ["0", "1", "2", "3", "4", "5"]:
        return False, "INVALID CLEARANCE: PLEASE ENTER A LEVEL FROM 0 TO 5."

    users[key] = {
        "name": key,
        "password": password,
        "clearance": int(clearance.strip()),
        "personnel": personnel.strip() if personnel.strip() else "Researcher",
        "site": site.strip() if site.strip() else "Site-19",
        "mtf": mtf.strip() if mtf.strip() else "None",
        "committee": committee.strip() if committee.strip() else "None",
        "is_o5": False,
    }
    save_users(users)
    return True, users[key]


def login_user(name, password):
    key = name.strip()
    upper_key = key.upper()

    if is_reptor_easter_egg(key, password):
        return False, "ACCESS DENIED: THIS ACCOUNT HAS NO PERSONNEL ACCESS."

    # Check 1: one of the 12 O5 accounts (O5-1 through O5-12)
    if upper_key in O5_ACCOUNTS:
        o5 = O5_ACCOUNTS[upper_key]
        if password == o5["pass"]:
            return True, {
                "name": upper_key,
                "title": o5["title"],
                "clearance": 5,
                "personnel": "O5 Council Member",
                "site": o5["site"],
                "mtf": "Alpha-1 (Red Right Hand)",
                "committee": "Overseer Council",
                "is_o5": True,
            }
        return False, "INVALID O5 AUTHORIZATION CODE."

    # Check 2: regular personnel from users.json
    users = load_users()
    if key in users and users[key]["password"] == password:
        return True, users[key]

    return False, "ACCESS DENIED: INCORRECT USERNAME OR PASSWORD."


def promote_user(actor: dict, target_name: str, new_level: str):
    if actor.get("clearance", 0) < 5:
        return False, "[ACCESS DENIED] ONLY LEVEL-5 PERSONNEL OR O5 MAY CHANGE CLEARANCE."

    if new_level.strip() not in ["0", "1", "2", "3", "4", "5"]:
        return False, "[ERROR] TARGET CLEARANCE MUST BE BETWEEN LEVEL 0 AND 5."

    users = load_users()
    target = target_name.strip()

    if target.upper() in O5_ACCOUNTS:
        return False, "[ACCESS DENIED] O5 COUNCIL MEMBERS CANNOT BE MODIFIED."

    if target not in users:
        return False, f"[ERROR] PERSONNEL FILE '{target}' NOT FOUND."

    old_lvl = users[target]["clearance"]
    users[target]["clearance"] = int(new_level.strip())
    save_users(users)
    return True, f"[SUCCESS] {target} CLEARANCE CHANGED FROM LEVEL {old_lvl} TO LEVEL {new_level.strip()}."
