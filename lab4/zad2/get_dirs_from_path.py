import os

def get_directories_from_path(path_string):
    if not path_string:
        return []
    # os.pathsep to średnik (;) na Windows lub dwukropek (:) na Unix
    return [d for d in path_string.split(os.pathsep) if d]