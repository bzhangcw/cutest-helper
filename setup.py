# change this file to do profiling

# un-picked methods in the following
# e.g. second-order method only...
# 0. HSODM Paper
# UNSELECT_METHOD = r"('\\lbfgs', '\\drsomh', '\\hsodmarc', '\\gd', '\\cg', '\\drsom', '\\utr', '\\newtontr', '\\iutr', '\\iutrhvp')"

# 1. HSODF Paper
UNSELECT_METHOD = r"('\\lbfgs', '\\drsomh', '\\hsodmarc', '\\hsodm', '\\gd', '\\cg', '\\drsom', '\\utr', '\\newtontr', '\\iutr', '\\iutrhvp')"

# 2. UTR Paper
# UNSELECT_METHOD = r"('\\lbfgs', '\\drsomh', '\\hsodmarc', '\\gd', '\\cg', '\\drsom', '\\hsodm', '\\hsodmhvp', '\\utr', '\\newtontr', '\\iutr')"

# filter the results satisfying the following condition...
OPTION = False
if OPTION:
    FILTER = f"""
    where n <= 200
        and `precision` = 1e-5
        and method not in {UNSELECT_METHOD}
        """
else:
    FILTER = f"""
        where `precision` = 1e-5
            and method not in {UNSELECT_METHOD}
            and n>=500
    """
    # FILTER = f"""
    #     where `precision` = 1e-5
    #         and method not in {UNSELECT_METHOD}
    # """
