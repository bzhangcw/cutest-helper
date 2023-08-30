# change this file to do profiling

# un-picked methods in the following
# e.g. second-order method only...
# 1. HSODF Paper
# UNSELECT_METHOD = r"('\\lbfgs', '\\drsomh', '\\hsodmarc', '\\gd', '\\cg', '\\drsom')"
# 2. UTR Paper
UNSELECT_METHOD = r"('\\lbfgs', '\\drsomh', '\\hsodmarc', '\\gd', '\\cg', '\\drsom', '\\hsodm', '\\hsodmhvp', '\\utr', '\\newtontr')"

# filter the results satisfying the following condition...
OPTION = int(input("small: 1; large: 0\n"))
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
    """
