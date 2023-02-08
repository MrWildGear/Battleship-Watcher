def count_for_list_items_in_list(searched_data: list, search_keys: list) -> int:
    """
    counts how many times all the items in searched keys are repeated in searched data
    :param searched_data: list of strings
    :param search_keys: list of strings
    :returns integer count of the repeats
    """
    count = 0
    for keyword in search_keys:
        for entry in searched_data:
            if entry.__contains__(keyword):
                count += 1
    return count
