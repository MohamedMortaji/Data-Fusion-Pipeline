def match_cases(mosaiq_data, myoncare_data):
    """
    Match cases between Mosaiq and Myoncare using IDA.
    """

    mosaiq_ids = set(mosaiq_data["IDA"])
    myoncare_ids = set(myoncare_data["IDA"])

    return {
        "matched_ids": sorted(mosaiq_ids & myoncare_ids),
        "mosaiq_only_ids": sorted(mosaiq_ids - myoncare_ids),
        "myoncare_only_ids": sorted(myoncare_ids - mosaiq_ids),
    }