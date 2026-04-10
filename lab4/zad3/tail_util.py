def tail_logic(lines, n):
    # Jeżeli n jest mniejsze lub równe 0, zwracamy pustą listę
    if n <= 0:
        return []
    # W przeciwnym razie zwracamy n ostatnich elementów z listy. Jeśli lista ma mniej niż n elementów, zwracamy całą listę
    return lines[-n:]