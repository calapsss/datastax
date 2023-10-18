def is_valid_query(query):
    """
    Check if a query is valid.

    Args:
        query (str): The query to check.

    Returns:
        bool: True if the query is valid, False otherwise.
    """
    # Replace this with your own validation logic
    if query is None or len(query.strip()) == 0 or query is not str:
        return False
    return True
