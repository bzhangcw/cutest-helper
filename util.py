import numpy as np
import pandas as pd
from scipy import stats
from sqlalchemy import create_engine


# utility funcs
def convert_to_int_else_slash(x):
    try:
        return "\\texttt{" + int(np.floor(x)).__str__() + "}"
    except:
        return "-"


def scaled_gmean(arr, scale=10):
    """compute scaled geometric mean,
    the scale=10 mimics the Hans's benchmark
    """
    return stats.gmean(arr + scale) - scale


# constants
class CUTEST_UTIL:
    @staticmethod
    def establish_connection():
        # engine = create_engine("mysql+pymysql://root@127.0.0.1:3306", echo=True)
        engine = create_engine(
            "mysql+pymysql://chuwen:931017@127.0.0.1:3306", echo=True
        )

        trans = engine.begin()
        return engine, trans


class INFO_CUTEST(object):
    NAME_SCHEMA = "cutest"


class INFO_CUTEST_RESULT(INFO_CUTEST):
    PARAM_GEOMETRIC_SCALER = 1
    NAME_TABLE = "result"
    PRIMARY_KEY = "id"
    COLUMNS = [
        "precision",
        "name",
        "param",
        "n",
        "method",
        "k",
        "kf",
        "kg",
        "kh",
        "df",
        "fx",
        "t",
        "status",
    ]
    COLUMNS_PERF = ["k", "kf", "kg", "kh", "df", "fx", "t", "status"]
    COLUMNS_RENAMING = {
        "n": "$n$",
        "k": "$k$",
        "t": "$t$",
        "df": "$\|g\|$",
        "fx": "$f$",
        # agg
        "kf": "$\\overline k$",
        "kff": "$\\overline k^f$",
        "kfg": "$\\overline k^g$",
        "kfh": "$\\overline k^H$",
        "tf": "$\\overline t$",
        "nf": "$\\mathcal K$",
        "kg": "$\\overline k_G$",
        "kgf": "$\\overline k_G^f$",
        "kgg": "$\\overline k_G^g$",
        "kgh": "$\\overline k_G^H$",
        "tg": "$\\overline t_G$",
    }
    COLUMNS_FULL_TABLE_LATEX_WT_FORMATTER = {
        # "name": lambda x: "\\texttt{" + x + "}",
        # "n": convert_to_int_else_slash,
        "k": convert_to_int_else_slash,
        "kg": convert_to_int_else_slash,
        "df": lambda x: "\\texttt{" + f"{np.nan_to_num(x, np.inf):.1e}" + "}",
        "fx": lambda x: "\\texttt{" + f"{np.nan_to_num(x, np.inf):+.1e}" + "}",
        "t": lambda x: "\\texttt{" + f"{np.nan_to_num(x, np.inf):.1e}" + "}",
    }
    METHODS_RENAMING = {
        "DRSOM": r"\drsom",
        "NewtonTR": r"\newtontr",
        "TRST": r"\newtontrst",
        "HSODM": r"\hsodm",
        "HSODMhvp": r"\hsodmhvp",
        "UTR": r"\utr",
        "iUTR": r"\iutr",
        "iUTRhvp": r"\iutrhvp",
        "DRSOMHomo": r"\drsomh",
        "HSODMArC": r"\hsodmarc",
        "LBFGS": r"\lbfgs",
        "CG": r"\cg",
        "ARC": r"\arc",
        "GD": r"\gd",
        "TRACE": r"\itrace",  # avoid conflicts with amsmath
    }
    METHODS_RENAMING_REV = {
        "\\drsom": "DRSOM",
        "\\newtontr": "Newton-TR",
        "\\newtontrst": "Newton-TR-STCG",
        "\\hsodm": "HSODM",
        "\\hsodmhvp": "Adaptive-HSODM",
        # "\\hsodmhvp": "HSODM-HVP",
        "\\utr": "UTR",
        "\\iutr": "iUTR(Hessian)",
        "\\iutrhvp": "iUTR",
        "\\lbfgs": "LBFGS",
        "\\cg": "CG",
        # "\\arc": "ARC",
        "\\arc": "Cubic-Reg",
        "\\gd": "GD",
    }

    @staticmethod
    def produce_latex_long_table(df: pd.DataFrame, keys, caption, label, path):
        return (
            df[keys]
            .rename(
                index=INFO_CUTEST_RESULT.COLUMNS_RENAMING,
                columns=INFO_CUTEST_RESULT.COLUMNS_RENAMING,
            )
            .swaplevel(0, 1, 1)
            .sort_index()
            .fillna("-")
            .to_latex(
                longtable=True,
                escape=False,
                caption=caption,
                multicolumn=True,
                label=label,
                buf=path,
                float_format="\texttt{%+.2f}",
            )
        )

    QUICK_VIEW = r"""
\documentclass{article}
\usepackage{lscape,longtable,multirow}
\usepackage{booktabs,caption}

\newcommand{\hsodm}{\textrm{HSODM}}
\newcommand{\hsodmarc}{\textrm{HSODMArC}}
\newcommand{\hsodmhvp}{\textrm{HSODM-HVP}}
\newcommand{\drsom}{\textrm{DRSOM}}
\newcommand{\drsomh}{\textrm{DRSOM-H}}
\newcommand{\lbfgs}{\textrm{LBFGS}}
\newcommand{\newtontr}{\textrm{Newton-TR}}
\newcommand{\newtontrst}{\textrm{Newton-TR-STCG}}
\newcommand{\cg}{\textrm{CG}}
\newcommand{\arc}{\textrm{ARC}}
\newcommand{\itrace}{\textrm{TRACE}}
\newcommand{\gd}{\textrm{GD}}
\newcommand{\utr}{\textrm{UTR}}
\newcommand{\iutr}{\textrm{iUTR(Hessian)}}
\newcommand{\iutrhvp}{\textrm{iUTR}}

\begin{document}

\begin{landscape}
    \input{perf.alg}
    \input{perf.geo}
    \clearpage
    \input{perf}
    \clearpage
    \input{perf.history}
    \scriptsize
    \clearpage
    \input{complete.kt}
    \input{complete.fg}
\end{landscape}
\end{document}
    """
