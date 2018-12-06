import re

#
# ----------------------------------------------------------
# boolean intent

def __determine_intent(patterns, phrase):
    check_phrase = phrase.lower()
    for p in patterns:
        if re.search(p.lower(), check_phrase):
            return True
    return False

def yes(phrase):
    patterns = [
        r"yes",
        r"yep",
    ]
    return __determine_intent(patterns, phrase)

def program_command(phrase):
    patterns = [
        r"program",
    ]
    return __determine_intent(patterns, phrase)

def scan_new_widgets(phrase):
    patterns = [
        r"scan",
        r"scan new widgets",
    ]
    return __determine_intent(patterns, phrase)

def share_current_widgets(phrase):
    patterns = [
        r"current widgets",
        r"share widgets",
        r"registered widgets",
    ]
    return __determine_intent(patterns, phrase)

def build_new_command(phrase):
    patterns = [
        r"new command",
    ]
    return __determine_intent(patterns, phrase)

def send_command(phrase):
    patterns = [
        r"send command",
    ]
    return __determine_intent(patterns, phrase)

def party(phrase):
    patterns = [
        r"party",
    ]
    return __determine_intent(patterns, phrase)

#
# ----------------------------------------------------------
# intent and return blocks

def __chomp_blocks(pattern, phrase):
    # find matches
    check_phrase = phrase.lower()
    matched = []
    # print(pattern)
    for p in pattern.split("_"):
        re_obj = re.search(p.lower(), check_phrase)
        if not re_obj:
            return []
        else:
            start, end = re_obj.start(), re_obj.end()
            if start < end:
                matched.append((start, end))

    # parse out unused blocks
    previous_end = 0
    unused_blocks = []
    for match in matched:
        start, end = match
        block = phrase[previous_end:start]
        if block:
            unused_blocks.append(block)
        previous_end = end
    block = phrase[previous_end:]
    if block:
        unused_blocks.append(block)
    return unused_blocks

def execute_command(phrase):
    patterns = [
        r"execute _",
    ]

    for pattern in patterns:
        movie = __chomp_blocks(pattern, phrase)
        if movie:
            return movie[0]
    return ""

def get_hostnames(phrase):
    pattern = r"Nmap scan report for _ \(_\)"
    hostnames = __chomp_blocks(pattern, phrase)
    if hostnames:
        return hostnames[0], hostnames[1]
    return None, None