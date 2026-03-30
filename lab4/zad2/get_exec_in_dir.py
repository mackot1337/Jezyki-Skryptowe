import os

def is_executable(filepath):
    if not os.path.isfile(filepath):
        return False
        
    if os.name == 'nt':  # Windows
        return filepath.lower().endswith(('.exe', '.bat', '.cmd'))
    else:  # Unix / Linux / Mac OS X
        return os.access(filepath, os.X_OK)

def get_executables_in_dir(directory):
    executables = []
    try:
        # Pobieramy listę plików, ignorując błędy dostępu lub nieistniejące katalogi
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if is_executable(filepath):
                executables.append(filename)
    except (FileNotFoundError, PermissionError, NotADirectoryError):
        pass
    return executables