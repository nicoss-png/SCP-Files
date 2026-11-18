import textwrap

LORE_ENTRIES = {
    "mtf": [
        "=== MOBILE TASK FORCES (MTF) - SPECIAL OPERATIONS UNITS ===",
        "",
        "[Alpha-1 'Red Right Hand'] -> Reports directly to the O5 Council and conducts highly classified operations.",
        "[Epsilon-11 'Nine-Tailed Fox'] -> Internal security and containment during major containment breaches.",
        "[Nu-7 'Hammer Down'] -> Heavy battalion with tanks and air support for large-scale assaults.",
        "[Beta-7 'Maz Hatters'] -> Specializes in biological, chemical, and radiological anomalies.",
        "[Eta-10 'See No Evil'] -> Counters visual cognitohazards and memetic anomalies.",
        "[Mu-13 'Ghostbusters'] -> Locates and contains spectral and ghostlike entities.",
        "[Tau-5 'Samsara'] -> Immortal cyborg clones made from the flesh of a dead god.",
        "[Omega-7 'Pandora's Box'] -> Former unit that worked with humanoid SCPs (SCP-076 and SCP-105).",
        "[Lambda-5 'White Rabbits'] -> Specializes in traversing unstable realities and spacetime rifts.",
        "[Pi-1 'City Slickers'] -> Conducts covert operations and containment in densely populated cities.",
    ],
    "sites": [
        "=== IMPORTANT FOUNDATION LOCATIONS (SITES & AREAS) ===",
        "",
        "[Site-01] -> Highly classified headquarters of the O5 Council and the Administrator.",
        "[Site-19] -> The Foundation's largest active site; houses SCP-173, SCP-096, SCP-682, among others.",
        "[Site-02] -> High-security complex for Keter anomalies and memetic research.",
        "[Site-17] -> Specializes in containing and studying humanoid SCPs.",
        "[Area-12] -> Biological research facility for highly infectious and biological anomalies.",
        "[Area-14] -> Remote military and containment zone for extremely destructive entities.",
        "[Site-64] -> Facility for electronic, mechanical, and anomalous technological objects.",
        "[Site-77] -> One of Europe's largest sites for historical and religious artifacts.",
    ],
    "ranks": [
        "=== ORGANIZATION & PERSONNEL CLASSIFICATION ===",
        "",
        "[O5 Council (Overseer Council)] -> The highest authority (O5-1 through O5-12/13). No direct SCP contact.",
        "[The Administrator] -> Mysterious founder figure, formally above or alongside the O5 Council.",
        "[Site Director] -> Leads an individual site (e.g. the director of Site-19).",
        "[Senior Researcher] -> Leads complex or dangerous SCP research projects.",
        "[Researcher / Junior Researcher] -> Conducts tests, analysis, and documentation.",
        "[Containment Specialist] -> Engineers and strategists who design secure containment chambers.",
        "[Field Agent] -> Covert investigators who locate new anomalies in the outside world.",
        "[Security Officer] -> Guards sectors and protects personnel.",
        "[Class A personnel] -> Irreplaceable leadership (O5 Council); must not be exposed to risk.",
        "[Class B personnel] -> Important site leaders and specialists; evacuation takes priority during breaches.",
        "[Class C personnel] -> Regular personnel with access to non-lethal anomalies.",
        "[Class D personnel] -> Expendable test subjects (usually convicted criminals) for dangerous tests.",
        "[Class E personnel] -> Provisional classification for personnel potentially contaminated by an anomaly.",
    ],
    "clearance": [
        "=== SECURITY CLEARANCE LEVELS ===",
        "",
        "[Level 0 - For official use only] -> Non-critical support staff (cleaning, logistics). No SCP file access.",
        "[Level 1 - Confidential] -> Personnel near anomalies without direct access to files.",
        "[Level 2 - Restricted] -> Standard clearance for researchers, security staff, and agents.",
        "[Level 3 - Secret] -> Senior personnel; access to detailed containment and testing data.",
        "[Level 4 - Top Secret] -> Site directors and MTF commanders; access to strategic data.",
        "[Level 5 - Thaumiel / O5] -> Highest regular clearance; O5 Council members also have SCP-001 access.",
    ],
    "classes": [
        "=== OBJECT CLASSES (CONTAINMENT CLASSES) ===",
        "",
        "[Safe] -> Easily and reliably contained (this does NOT mean the object is harmless!).",
        "[Euclid] -> Unpredictable or incompletely understood (often autonomous or living SCPs).",
        "[Keter] -> Extremely difficult to contain; requires complex measures or poses a major threat.",
        "[Thaumiel] -> Highly classified anomalies used to contain other SCPs.",
        "[Neutralized] -> No longer anomalous, destroyed, or permanently deactivated.",
        "[Apollyon] -> Uncontainable anomaly that triggers a K-Class scenario.",
        "[Archon] -> Anomaly that COULD be contained but must remain free for safety reasons.",
    ],
    "meds": [
        "=== FOUNDATION MEDICATIONS & AMNESTICS ===",
        "",
        "[Class A amnestics] -> Erase memories from the past few hours (standard after minor incidents).",
        "[Class B amnestics] -> Erase memories from the past days or weeks (liquid or gas).",
        "[Class C amnestics] -> Targeted erasure of specific memories or several months of memory.",
        "[Class D amnestics] -> Potent amnestics that erase years of memory (risk of brain damage).",
        "[Class E amnestics] -> Induce permanent amnesia or personality loss (for extreme cases).",
        "[Class F amnestics] -> Completely overwrite an identity (for witnesses or defectors).",
        "[Mnestic drugs (Classes W, X, Y, Z)] -> Counter amnestics and strengthen memory against antimemes.",
        "[SCP-500 ('Panacea')] -> Red pills that immediately cure EVERY known disease or infection.",
    ],
    "kclass": [
        "=== K-CLASS END-OF-THE-WORLD SCENARIOS ===",
        "",
        "[XK-Class] -> End of the world (a classic apocalypse involving the extinction of humanity or destruction of Earth).",
        "[ZK-Class] -> End of reality (collapse of spacetime or the fundamental laws of physics).",
        "[CK-Class] -> Restructuring of reality (history or the world is altered by reality benders).",
        "[NK-Class] -> 'Grey Goo' scenario (uncontrolled self-replication consumes all matter).",
        "[SK-Class] -> Dominance shift (another species or entity replaces humanity).",
        "[GH-Class] -> 'Dead Greenhouse' (ecological collapse makes Earth uninhabitable).",
        "[IK-Class] -> Collapse of global civilization (the end of modern society).",
        "[AK-Class] -> Endogenous madness (a global, incurable psychological or memetic infection).",
    ],
}


def get_lore_topic(topic: str) -> list[str]:
    key = topic.lower().strip()
    aliases = {
        "sites": "sites",
        "ranks": "ranks",
        "rank": "ranks",
        "clearance": "clearance",
        "classes": "classes",
        "object classes": "classes",
        "medications": "meds",
        "amnestics": "meds",
        "scenarios": "kclass",
        "k-class": "kclass",
        "standorte": "sites",
        "site": "sites",
        "sites": "sites",
        "rang": "ranks",
        "ränge": "ranks",
        "rangordnung": "ranks",
        "personal": "ranks",
        "personalerklärung": "ranks",
        "freigabe": "clearance",
        "freigaben": "clearance",
        "klassen": "classes",
        "objektklassen": "classes",
        "medikamente": "meds",
        "amnestika": "meds",
        "szenarien": "kclass",
        "k-klasse": "kclass",
    }
    resolved = aliases.get(key, key)
    if resolved not in LORE_ENTRIES:
        return [
            "=== AVAILABLE FOUNDATION DATABASES ===",
            "Use: info <topic> with one of these terms:",
            "  info mtf          -> Mobile Task Forces",
            "  info sites        -> Sites & Areas",
            "  info ranks        -> Organization & personnel classes (A-E)",
            "  info clearance   -> Security clearance (Level 0-5)",
            "  info classes      -> Object classes (Safe to Apollyon)",
            "  info medications  -> Amnestics, mnestics & SCP-500",
            "  info scenarios    -> K-Class end-of-the-world scenarios",
        ]

    wrapped = []
    for line in LORE_ENTRIES[resolved]:
        if line == "":
            wrapped.append("")
        else:
            wrapped.extend(textwrap.wrap(line, width=82))
    return wrapped
