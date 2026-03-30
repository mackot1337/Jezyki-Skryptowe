def get_filtered_env_vars(env_vars, args):
    filtered_vars = []
    # Filtr powinien działać jako nieczuły na wielkość (case-insensitive)
    args_lower = [arg.lower() for arg in args]

    for key, value in env_vars:
        key_lower = key.lower()
        # Warunkiem wyświetlania jest istnienie parametru, którego wartość zawiera się w nazwie zmiennej
        if any(arg in key_lower for arg in args_lower):
            filtered_vars.append((key, value))

    return filtered_vars