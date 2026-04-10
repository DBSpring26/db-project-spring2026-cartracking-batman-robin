def validate_limit_offset(limit: int, offset: int):
    if limit < 0 or offset < 0:
        raise ValueError("limit and offset must be non-negative integers.")