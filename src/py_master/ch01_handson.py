"""
Python Mastery for the Data + AI Engineer
Chapter 1 hands-on assessment: Python for the C# Developer
==========================================================

12 real-world problems covering the whole chapter:

    1.1  Running Python and environments          -> Problem 1
    1.2  Names, objects, mutability, copies       -> Problem 2
    1.3  Numbers, Decimal, strings, None          -> Problems 3, 4, 5
    1.4  Lists, tuples, sorting, unpacking        -> Problem 6
    1.5  Dicts, Counter, defaultdict, sets        -> Problems 7, 8
    1.6  Loops: enumerate, zip, for-else          -> Problem 9
    1.7  Comprehensions                           -> Problem 10
    All of it, under pressure                     -> Problems 11, 12 (capstones)

HOW TO WORK
-----------
1. Read a problem's docstring, then replace `raise NotImplementedError` with your code.
2. Run the checker:
       python ch01_handson.py            # all problems
       python ch01_handson.py 3 7        # only problems 3 and 7
   Each problem shows PASS, FAIL (with the first failing check) or TODO.
3. The checker also prints REVIEW notes when your code contains patterns that a
   senior Python reviewer would flag (index loops, `== None`, float for money).
   They do not fail the problem, but fix them.

RULES (like a real assessment)
------------------------------
* Standard library only. Allowed imports: sys, decimal, collections, csv, io, copy.
  No regular expressions (the `re` module comes in Chapter 4): use string methods.
* Do not change function names or signatures; the checker calls them.
* Never mutate the arguments you receive unless the problem says so.
* Time boxes are what a strong candidate needs. Track your own time honestly.

SCORING
-------
Easy problems are worth 5 points, medium 10, hard 15.  Total: 145.
  120+  ready for Chapter 2    90-119  revisit the sections you failed    < 90  re-read Chapter 1

Author: Vasu Shanmugam (solutions)  |  Problems: Python Mastery book, Chapter 1
"""

from __future__ import annotations

import sys
import re
from collections import Counter, defaultdict  # noqa: F401  (you will need these)
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation  # noqa: F401
import copy

CENT = Decimal("0.01")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


# =============================================================================
# PROBLEM 1 (easy, 5 points, 10 min) -- Section 1.1: know where your code runs
# =============================================================================
def environment_report() -> dict:
    """
    SCENARIO
    A production job failed because it ran with the system Python instead of the
    project's virtual environment, and picked up an old library. You are adding a
    start-up log line that records exactly which interpreter is running.

    TASK
    Return a dict with exactly these keys:
        "python"        -> version string like "3.13.1" (major.minor.micro)
        "major_minor"   -> tuple of ints, e.g. (3, 13)
        "in_virtualenv" -> True if running inside a virtual environment
        "executable"    -> full path of the running interpreter

    HINTS
    Look at sys.version_info, sys.executable, sys.prefix and sys.base_prefix.
    Inside a venv, sys.prefix and sys.base_prefix differ.

    STRETCH (not checked)
    Run the file once with `python ch01_handson.py 1` and once with
    `uv run python ch01_handson.py 1`, and compare "in_virtualenv" and "executable".
    """
    # print(
    #    f"sys.version_info : {sys.version_info} \n sys.executable : {sys.executable} \n sys.prefix : {sys.prefix} \n sys.base_prefix : {sys.base_prefix}"
    # )

    return {
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "major_minor": (sys.version_info.major, sys.version_info.minor),
        "in_virtualenv": sys.prefix != sys.base_prefix,
        "executable": sys.executable,
    }

    # raise NotImplementedError


# =============================================================================
# PROBLEM 2 (medium, 10 points, 20 min) -- Section 1.2: aliasing and copies
# =============================================================================
CART = [
    {
        "sku": "SOF-3S",
        "name": "3-seater sofa",
        "unit_price": Decimal("38500.00"),
        "qty": 1,
        "tags": ["festive", "sofas"],
    },
    {
        "sku": "LMP-BR",
        "name": "Brass floor lamp",
        "unit_price": Decimal("2499.00"),
        "qty": 2,
        "tags": ["clearance", "festive"],
    },
    {
        "sku": "RUG-WL",
        "name": "Wool rug",
        "unit_price": Decimal("6999.99"),
        "qty": 1,
        "tags": [],
    },
    {
        "sku": "CHR-TK",
        "name": "Teak chair",
        "unit_price": Decimal("4999.95"),
        "qty": 4,
        "tags": ["chairs", "festive"],
    },
]
DISCOUNT_RULES = {"festive": 10, "clearance": 35, "chairs": 15}  # tag -> percent off


def apply_discounts(cart: list[dict], rules: dict[str, int]) -> list[dict]:
    """
    SCENARIO
    The checkout service applies promotions to a shopping cart. A bug report says:
    "after viewing the cart twice, prices were discounted twice" -- the previous
    developer changed the cart items in place. The same cart object is shared by
    the pricing page, the order summary and the analytics event.

    TASK
    Return a NEW list of NEW item dicts where:
      * each item gets the single HIGHEST discount among its tags (no stacking);
        items with no matching tag get 0
      * "unit_price" becomes the discounted price, rounded to 2 places, ROUND_HALF_UP
      * a new key "discount_pct" (int) is added
      * every other key is kept, in the same order, items in the same order

    The input cart must be completely untouched -- including the nested "tags"
    lists. Changing a returned item's "tags" list must not change the input cart.
    (Trap: dict.copy() is a SHALLOW copy.)

    EXAMPLE
    Brass floor lamp, tags ["clearance", "festive"] -> 35% -> 2499.00 becomes 1624.35
    """

    # Add discount_pct property
    # From tag find the maximum discount rate and set it to discount_pct
    # Adjust the unit_price with discount %

    cart_clone = copy.deepcopy(cart)

    for i, c in enumerate(cart_clone):
        # print(i, c["tags"], c)
        c["discount_pct"] = max([rules[t] for t in c["tags"] if t in rules], default=0)
        c["unit_price"] = round(
            c["unit_price"]
            - Decimal(c["unit_price"] * Decimal(c["discount_pct"] / 100)),
            2,
        )

    # print(cart is cart_clone)
    # print(cart)
    # print(cart_clone)

    return cart_clone

    # raise NotImplementedError


# =============================================================================
# PROBLEM 3 (medium, 10 points, 25 min) -- Section 1.3: Decimal money and parsing
# =============================================================================
INVOICE_LINES = [  # (description, qty, unit price as printed on the PO, GST rate %)
    ("Teak dining table", 1, "₹32,000.00", 18),
    ("Cushion covers", 6, "Rs. 349.50", 12),
    ("Assembly service", 1, "  1,499 ", 18),
    ("Delivery", 1, "0", 0),
    ("Wool rug", 2, "₹ 6,999.99", 12),
    ("Office desk (bulk)", 3, "1,00,000.10", 28),  # Indian digit grouping!
]
GST_RATES = {0, 5, 12, 18, 28}


def invoice_totals(lines: list[tuple[str, int, str, int]]) -> dict:
    """
    SCENARIO
    Purchase orders arrive from several suppliers with prices typed by hand:
    rupee symbols, "Rs.", Western and Indian comma grouping, stray spaces.
    Finance needs exact GST totals -- a float rounding error of one paisa makes
    the GST return fail reconciliation.

    TASK
    For each line:
      * parse the price: remove "₹", "Rs.", commas and spaces, then Decimal(...)
      * net  = qty * price, rounded to 2 places ROUND_HALF_UP
      * tax  = net * rate / 100, rounded to 2 places ROUND_HALF_UP (per line)
      * raise ValueError if qty <= 0 or the rate is not in GST_RATES
    Return:
      {
        "subtotal":    Decimal,             # sum of nets
        "tax_by_rate": {rate: Decimal},     # sorted by rate ascending, every rate used
        "tax":         Decimal,             # sum of taxes
        "grand_total": Decimal,
        "formatted":   "₹441,557.82"-style string of grand_total (2 decimals, commas)
      }
    Never use float anywhere in this function.

    STRETCH (not checked)
    Write format_inr(amount) that prints Indian grouping: ₹4,41,557.82
    """

    rates = []
    sum_net = 0
    sum_tax = 0
    sum_total = 0

    for line in lines:
        print(line)

        desc, qty, rate, gst = line

        if qty <= 0 or (gst in GST_RATES) == False:
            raise ValueError

        rate_new = Decimal(
            re.sub(r"[^\d.\-]", "", re.sub(r"Rs\.?", "", rate, flags=re.IGNORECASE))
        )
        net = Decimal(round((rate_new * qty), 2))
        tax = Decimal(round((net * Decimal(gst / 100)), 2))
        total = net + tax

        rates.append({gst: tax})
        sum_net += net
        sum_tax += tax
        sum_total += total

    rates_total = defaultdict(int)
    for i_rate in rates:
        for r, v in i_rate.items():
            rates_total[r] += v

    rates_total = {k: v for k, v in rates_total.items()}

    rates_total = dict(sorted(rates_total.items()))

    return {
        "subtotal": sum_net,
        "tax_by_rate": rates_total,
        "tax": sum_tax,
        "grand_total": sum_total,
        "formatted": f"₹{sum_total:,.2f}",
    }
    # raise NotImplementedError


# =============================================================================
# PROBLEM 4 (hard, 15 points, 35 min) -- Section 1.3: strings and None, for real
# =============================================================================
CONTACTS = [
    {
        "name": "  meena   krishnan ",
        "email": " Meena.K@Example.COM ",
        "phone": "+91 98765-43210",
    },
    {"name": "Ravi", "email": "ravi@@mail.com", "phone": "9876543210"},
    {"name": "", "email": "ghost@example.com", "phone": ""},
    {"name": "john o'brien", "email": None, "phone": "044-2345678"},
    {"name": "Asha  Devi", "email": "asha@example.in", "phone": "09845012345"},
    {"name": "MEENA K", "email": "meena.k@example.com", "phone": None},
    {"name": "Priya", "email": "priya@company", "phone": "919912345678"},
    {"name": "arun kumar", "email": "", "phone": "(0) 99123 45678"},
    {"name": "Lakshmi", "email": "lakshmi@example.org", "phone": "5551234567"},
]

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def clean_contacts(rows: list[dict]) -> tuple[list[dict], list[tuple[int, str]]]:
    """
    SCENARIO
    Marketing exported contacts from three CRMs into one list before a campaign.
    You must clean them before they are loaded into the warehouse: bad rows go to
    a rejects file with a reason, so the CRM owners can fix them.

    TASK
    Process rows in order. Row numbers in rejects start at 1. Check in this order
    and reject with the FIRST failing reason:
      1. name:  collapse repeated spaces, strip, Title Case ("meena  krishnan" ->
                "Meena Krishnan"). Empty or None -> reject "missing name"
      2. email: strip and lower-case. None or "" means "no email" (allowed, store None).
                Otherwise it is valid only if it has exactly one "@", a non-empty
                part before it, a "." in the domain that is not its first or last
                character, and no spaces. Otherwise reject "invalid email"
      3. phone: keep only the digits. None/"" means no phone (allowed, store None).
                12 digits starting "91" -> drop the "91"; 11 digits starting "0" ->
                drop the "0". The result must be 10 digits starting with 6, 7, 8 or 9,
                stored as "+91XXXXXXXXXX". Otherwise reject "invalid phone"
      4. duplicates: an email already accepted earlier -> reject "duplicate email"
    Return (clean_rows, rejects):
      clean_rows: list of {"name", "email", "phone"} dicts, in input order
      rejects:    list of (row_number, reason)

    Use string methods only (split, join, strip, lower, title, isdigit, count,
    partition, startswith...). No regular expressions.
    """
    clean_rows = []
    rejects = []
    # reject_row_count = 1

    for i, row in enumerate(rows, start=1):
        is_valid_row = False
        is_valid_name = is_valid_email = is_valid_phone = False
        valid_name = valid_email = valid_phone = ""

        if row["name"] == "" or row["name"] == None:
            rejects.append((i, "missing name"))
            # reject_row_count += 1
            continue
        else:
            is_valid_name, valid_name = is_valid_name_check(row["name"])

        if row["email"] == "" or row["email"] == None:
            # rejects.append((reject_row_count, "no email"))
            # reject_row_count += 1
            # continue
            valid_email = None
        else:
            is_valid_email, valid_email = is_valid_email_check(row["email"])
            if is_valid_email is not True:
                rejects.append((i, "invalid email"))
                # reject_row_count += 1
                continue
            else:
                if len(clean_rows) > 0 and any(
                    o["email"] == valid_email for o in clean_rows
                ):
                    rejects.append((i, "duplicate email"))
                    # reject_row_count += 1
                    continue

        if row["phone"] == "" or row["phone"] == None:
            rejects.append((i, "no phone"))
            # reject_row_count += 1
            continue
        else:
            is_valid_phone, valid_phone = is_valid_phone_check(row["phone"])
            if is_valid_phone is not True:
                rejects.append((i, "invalid phone"))
                # reject_row_count += 1
                continue

        valid_phone = "+91" + valid_phone
        clean_rows.append(
            {"name": valid_name, "email": valid_email, "phone": valid_phone}
        )

    return (clean_rows, rejects)
    # raise NotImplementedError


def is_valid_name_check(s: str) -> tuple(bool, str):
    if not s or s is None:
        return (False, "")

    formatted_name = s

    # unwanted space check => trim (start, end, middle)
    formatted_name = formatted_name.strip()
    formatted_name = " ".join(s.split())
    # print(s, formatted_name)

    # case check => first character upper case
    formatted_name = formatted_name.title()
    # if all(word[0].isupper() for word in formatted_name.split()):

    # print(s, formatted_name)

    return (formatted_name is s, formatted_name)


def is_valid_email_check(email: str | None) -> tuple(bool, str):
    if not email or email is None:
        return (False, "")

    f_email = email

    f_email = f_email.strip()
    f_email = f_email.lower()
    if ".." in f_email or len(f_email) > 254:
        return (False, "")
    return (bool(EMAIL_RE.fullmatch(f_email)), f_email)


def is_valid_phone_check(mobile: str | None) -> tuple(bool, str):
    if not mobile or mobile is None:
        return (False, "")

    f_mobile = mobile
    f_mobile = re.sub(r"\D", "", f_mobile)

    valid_start_with = ["6", "7", "8", "9"]
    if len(f_mobile) == 12 and f_mobile.startswith("91"):
        f_mobile = f_mobile.removeprefix("91")
    elif len(f_mobile) == 11 and f_mobile.startswith("0"):
        f_mobile = f_mobile.removeprefix("0")

    if any(f_mobile.startswith(o) for o in valid_start_with):
        return (True, f_mobile)
    else:
        return (False, f_mobile)


# =============================================================================
# PROBLEM 5 (hard, 15 points, 30 min) -- Section 1.3: None vs falsy, in config
# =============================================================================
DEFAULTS = {
    "env": "dev",
    "debug": True,
    "workers": 4,
    "retries": 3,
    "tags": ["core"],
    "db": {"host": "localhost", "port": 5432, "pool": 5},
    "llm": {"model": "claude-haiku-5-5", "max_tokens": 500},
}
FILE_CFG = {
    "debug": False,
    "workers": None,
    "db": {"host": "db.internal", "pool": 0},
    "llm": {"max_tokens": None},
    "feature_x": "",
}
ENV_CFG = {
    "env": "prod",
    "retries": 0,
    "db": {"port": None, "password": "s3cret"},
    "llm": {"model": None},
    "tags": [],
}


def merge_config(defaults: dict, file_cfg: dict, env_cfg: dict) -> tuple[dict, dict]:
    """
    SCENARIO
    A data pipeline reads settings from three layers: built-in defaults, a YAML
    file, and environment variables. An incident: production ran with 3 retries
    although the ops team set RETRIES=0, because the old code used
    `env.get("retries") or file.get("retries") or default` -- and 0 is falsy.

    TASK
    Merge the layers with precedence env > file > defaults:
      * None in a higher layer means "not set": fall through to the lower layer
      * 0, False, "" and [] are REAL values and must win
      * if both the existing value and the new value are dicts, merge them with the
        same rules (nesting can be any depth); keys new in a higher layer are added
      * lists in the result must not be the same objects as in the inputs
      * do not mutate any input
    Return (merged, sources):
      merged:  the merged dict
      sources: {"dotted.key": "default" | "file" | "env"} for every leaf value in
               merged, sorted by key. Example: "db.host": "file", "retries": "env"
    """
    raise NotImplementedError


# =============================================================================
# PROBLEM 6 (medium, 10 points, 25 min) -- Section 1.4: sorting with tuple keys
# =============================================================================
REPS = [  # (name, region, deals closed, revenue as text from the CRM export)
    ("Asha", "South", 12, "1250000.00"),
    ("ravi", "South", 15, "1250000"),
    ("Meena", "West", 15, "1250000.00"),
    ("John", "North", 9, "980000.50"),
    ("Priya", "West", 9, "980000.5"),
    ("Arun", "North", 0, "0"),
    ("Lakshmi", "South", 20, "760000"),
    ("David", "North", 11, "1310000"),
    ("anand", "West", 9, "980000.50"),
]


def leaderboard(
    reps: list[tuple[str, str, int, str]],
) -> list[tuple[int, str, Decimal, int]]:
    """
    SCENARIO
    Sales leadership wants a quarterly leaderboard. Last quarter's version ranked
    "1250000" and "1250000.00" differently (string comparison) and sorted names
    case-sensitively, so "ravi" appeared after "Priya". Two people complained.

    TASK
    * Exclude reps with 0 deals.
    * Order by revenue (numeric) descending, then deals descending, then name
      ascending ignoring case.
    * Dense ranking: reps with equal (revenue, deals) share a rank, and the next
      rank is +1 (1, 2, 2, 3 -- not 1, 2, 2, 4).
    * Return a list of (rank, name, revenue as Decimal, deals).
    """
    raise NotImplementedError


def top_per_region(
    reps: list[tuple[str, str, int, str]], n: int
) -> dict[str, list[str]]:
    """
    TASK
    Using the same exclusion and ordering rules as leaderboard(), return
    {region: [names of the top n reps]} with regions in alphabetical order.
    """
    raise NotImplementedError


# =============================================================================
# PROBLEM 7 (hard, 15 points, 35 min) -- Section 1.5: dicts as state machines
# =============================================================================
EVENTS = [  # (ISO timestamp, order_id, event) -- arrives out of order, with redeliveries
    ("2026-11-01T10:00:00", "O-1", "created"),
    ("2026-11-01T10:05:00", "O-1", "paid"),
    ("2026-11-02T09:00:00", "O-1", "shipped"),
    ("2026-11-01T11:00:00", "O-2", "created"),
    ("2026-11-01T11:00:00", "O-2", "paid"),
    ("2026-11-03T08:00:00", "O-2", "refunded"),
    ("2026-11-01T12:00:00", "O-3", "paid"),
    ("2026-11-01T12:30:00", "O-3", "created"),
    ("2026-11-02T12:00:00", "O-3", "cancelled"),
    ("2026-11-01T10:05:00", "O-1", "paid"),
    ("2026-11-04T10:00:00", "O-1", "delivered"),
    ("2026-11-05T10:00:00", "O-1", "returned"),
    ("2026-11-06T10:00:00", "O-1", "refunded"),
    ("2026-11-02T10:00:00", "O-4", "created"),
    ("2026-11-02T11:00:00", "O-4", "shipped"),
    ("2026-11-02T12:00:00", "O-5", "created"),
    ("2026-11-02T12:01:00", "O-5", "paid"),
    ("2026-11-03T12:00:00", "O-2", "shipped"),
]
ALLOWED = {  # current status -> events allowed next (None = order not seen yet)
    None: {"created"},
    "created": {"paid", "cancelled"},
    "paid": {"shipped", "refunded"},
    "shipped": {"delivered"},
    "delivered": {"returned"},
    "returned": {"refunded"},
}


def order_status(events: list[tuple[str, str, str]]) -> tuple[dict, list, dict]:
    """
    SCENARIO
    Order events come from a message queue (like RabbitMQ). Messages can arrive out
    of order and can be delivered twice. You must rebuild each order's status and
    flag impossible transitions for the support team.

    TASK
    * Process events sorted by timestamp. ISO timestamps sort correctly as strings.
      Events with the SAME timestamp keep their original relative order.
    * If the event equals the order's current status, it is a redelivery: ignore it
      silently.
    * If the event is allowed from the current status (see ALLOWED), apply it.
    * Otherwise record an anomaly (order_id, current_status, event) and ignore it.
    Return (final, anomalies, counts):
      final:     {order_id: status}, sorted by order_id
      anomalies: list of tuples in processing order
      counts:    {status: number of orders}, sorted by count desc, then status name
    """
    raise NotImplementedError


# =============================================================================
# PROBLEM 8 (hard, 15 points, 30 min) -- Section 1.5: set-based reconciliation
# =============================================================================
SOURCE_ROWS = [
    ("A-100", "1500.00"),
    ("a-101 ", "200"),
    ("A-102", "999.99"),
    ("A-103", "50.00"),
    ("A-101", "250.00"),
    ("A-104", "75.10"),
    ("A-105", "0.00"),
    ("A-102", "999.99"),
]
TARGET_ROWS = [
    ("A-100", "1500"),
    ("A-101", "250.0"),
    ("A-102", "1000.00"),
    ("A-104", "75.1"),
    ("A-106", "300.00"),
    ("A-105", "0"),
    ("A-106", "310.00"),
]


def reconcile(
    source_rows: list[tuple[str, str]], target_rows: list[tuple[str, str]]
) -> dict:
    """
    SCENARIO
    Every night a CDC job copies orders from the ERP (source) to Snowflake (target).
    Finance signs off only if the two agree. Your reconciliation report goes to the
    change-approval board when they do not.

    TASK
    * Normalise ids: strip spaces, upper-case ("a-101 " is "A-101").
    * Amounts are compared as Decimal ("1500" equals "1500.00").
    * An id can appear more than once (CDC replays): the LAST occurrence wins.
    Return a dict with these keys:
      "missing_in_target":       sorted ids in source but not in target
      "unexpected_in_target":    sorted ids in target but not in source
      "amount_mismatches":       sorted list of (id, source_amount, target_amount)
      "matched_count":           ids in both with equal amounts
      "duplicate_ids_in_source": sorted ids that appeared more than once in source
      "source_total", "target_total": Decimal sums of the winning rows
      "difference":              target_total - source_total
    Use set operations for the id comparisons.
    """
    raise NotImplementedError


# =============================================================================
# PROBLEM 9 (medium, 10 points, 25 min) -- Section 1.6: enumerate, zip, for-else
# =============================================================================
BATCH = """order_id, Customer ,AMOUNT,currency
1001,Arhaus,1200.50,USD

1002,Elite Parking,abc,USD
1003,Arhaus,99.99
1004,Fujitec,15000,SGD
1005,NCS,7500.00,SGD,extra
1006,Arhaus,25000.00,USD
"""


def validate_batch(text: str, required: list[str], max_amount: Decimal) -> dict:
    """
    SCENARIO
    A partner uploads order batches as comma-separated text (no quoted fields).
    Before loading, you validate the batch and return errors that point to the
    exact line in THEIR file, so they can fix it themselves.

    TASK
    * Line 1 is the header. Normalise header names: strip and lower-case.
    * If any `required` column is missing, return immediately with
      errors [(1, "missing columns: a, b")] (in the order given in `required`),
      ok False, rows 0, first_over_limit None.
    * Skip blank lines, but keep counting lines (line numbers match the file).
    * For each data line (values stripped):
        - wrong number of fields -> (line, "expected 4 fields, got 3")
        - "amount" not a valid Decimal -> (line, "bad amount 'abc'")
        - otherwise it is a valid row
    * first_over_limit: line number of the first VALID row whose amount is greater
      than max_amount, or None. Write this search with a for ... else.
    Return {"ok": bool (no errors), "rows": number of valid rows,
            "errors": list of (line, message), "first_over_limit": int | None}
    Use enumerate for line numbers and zip to pair header names with values.
    """
    raise NotImplementedError


# =============================================================================
# PROBLEM 10 (medium, 10 points, 30 min) -- Section 1.7: comprehensions
# =============================================================================
CUSTOMERS = [
    {
        "id": 1,
        "name": "Arhaus",
        "tier": "gold",
        "orders": [
            {
                "order_id": "A1",
                "status": "paid",
                "items": [
                    {"product": "sofa", "qty": 1, "price": "38500"},
                    {"product": "lamp", "qty": 2, "price": "2499"},
                ],
            },
            {
                "order_id": "A2",
                "status": "cancelled",
                "items": [{"product": "desk", "qty": 1, "price": "12999"}],
            },
            {
                "order_id": "A3",
                "status": "paid",
                "items": [{"product": "rug", "qty": 1, "price": "4999.50"}],
            },
        ],
    },
    {
        "id": 2,
        "name": "Elite",
        "tier": "silver",
        "orders": [
            {
                "order_id": "E1",
                "status": "paid",
                "items": [
                    {"product": "chair", "qty": 4, "price": "4999"},
                    {"product": "lamp", "qty": 1, "price": "2499"},
                ],
            }
        ],
    },
    {
        "id": 3,
        "name": "Fujitec",
        "tier": "gold",
        "orders": [
            {
                "order_id": "F1",
                "status": "pending",
                "items": [{"product": "table", "qty": 1, "price": "32000"}],
            }
        ],
    },
    {
        "id": 4,
        "name": "NCS",
        "tier": "gold",
        "orders": [
            {
                "order_id": "N1",
                "status": "paid",
                "items": [{"product": "desk", "qty": 2, "price": "12999"}],
            },
            {
                "order_id": "N2",
                "status": "paid",
                "items": [{"product": "lamp", "qty": 1, "price": "2499"}],
            },
        ],
    },
    {"id": 5, "name": "Qantler", "tier": "bronze", "orders": []},
]


def customer_insights(customers: list[dict]) -> dict:
    """
    SCENARIO
    An API returns customers with nested orders and items (typical JSON). The
    account team wants a few numbers for a quarterly business review. Only orders
    with status "paid" count anywhere in this problem. Prices are strings; use Decimal.

    TASK  (each value should be ONE comprehension, or a comprehension plus sorted();
           product_buyers may use a defaultdict loop)
      "paid_totals":    {customer name: Decimal total of paid orders}, all customers
                        (0 for none), in input order
      "gold_products":  sorted list of unique products bought by "gold" customers
      "big_orders":     [(customer name, order_id)] for paid orders with total > 5000,
                        sorted by order total, largest first
      "product_buyers": {product: sorted unique customer names}, products sorted
      "inactive":       sorted names of customers with no paid orders
    """
    raise NotImplementedError


# =============================================================================
# PROBLEM 11 (hard, 15 points, 40 min) -- capstone: production log triage
# =============================================================================
LOG_LINES = [
    "2026-11-20 10:15:02 ERROR [payments] Card declined for order 1042",
    "2026-11-20 10:15:09 INFO [payments] Payment captured for order 1043",
    "2026-11-20 10:16:00 ERROR [payments] Card declined for order 1050",
    "2026-11-20 10:16:30 WARNING [delivery] Courier delayed 2 days",
    "2026-11-20 10:17:00 ERROR [delivery] Address not found for pin 641001",
    "garbage line without structure",
    "2026-11-20 10:18:00 CRITICAL [payments] Gateway timeout after 30000 ms",
    "2026-11-20 10:18:05 INFO [catalog] Indexed 1200 products",
    "2026-11-20 10:18:06 NOTICE [catalog] Unknown level line",
    "2026-11-20 10:19:00 ERROR [search] Card declined for order 77",
    "2026-11-20 10:19:30 INFO [search] Query served in 45 ms",
    "2026-11-20 10:20:00 ERROR delivery Address not found for pin 641002",
    "2026-11-20 10:21:00 ERROR [delivery] Address not found for pin 600001",
    "2026-11-20 10:22:00 DEBUG [catalog] Cache warm",
]
LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def log_report(lines: list[str]) -> str:
    """
    SCENARIO
    You are on call. The incident channel asks "which module is failing, and with
    what?". Write the triage report you would paste into the channel.

    TASK
    A valid line is "DATE TIME LEVEL [module] message": at least 5 space-separated
    parts (the message keeps its spaces), LEVEL in LEVELS, module in square brackets.
    Anything else is skipped. ERROR and CRITICAL count as errors.
    Error messages are grouped after replacing every RUN of digits with one "#"
    ("order 1042" and "order 77" -> "order #").

    Return exactly this text (lines joined with "\\n", no trailing newline):
        lines: 11 parsed, 3 skipped
        module       total  errors  error_rate
        payments         4       3       75.0%
        ...
        top errors:
          3 x Card declined for order #
          ...
    Formatting:
      header row:  f"{'module':<12}{'total':>6}{'errors':>8}{'error_rate':>12}"
      module rows: f"{module:<12}{total:>6}{errors:>8}{rate:>12.1%}"
                   sorted by error rate desc, then module name
      top errors:  at most 3, by count desc then message; "  {count} x {message}"
    """
    raise NotImplementedError


# =============================================================================
# PROBLEM 12 (hard, 15 points, 45 min) -- capstone: the month-end sales report
# =============================================================================
SALES_CSV = """
order_id, date, customer, region, amount, status
S-001, 2026-10-02, Arhaus, US, 1200.50, PAID
S-002, 2026-10-03, Elite Parking, US, 450.00, pending
S-003, 2026-10-05, Fujitec, SG, 980.00, paid

S-004, 2026-10-07, NCS, SG, abc, paid
S-005, 2026-10-09, Arhaus, US, 300.005, Paid
S-006, 2026-09-30, Arhaus, US, 999.00, paid
S-003, 2026-10-05, Fujitec, SG, 1080.00, paid
S-007, 2026-10-11, Qantler, IN, 2500.00, paid
S-008, 2026-10-12, Elite Parking, US, 1780.25, paid
S-009, 2026-10-15, Sparkle, IN, 120.00, refunded
S-010, 2026-10-20, Qantler, IN, 1200.50, paid
"""


def monthly_sales_report(csv_text: str, month: str) -> str:
    """
    SCENARIO
    The CFO's month-end pack needs a sales summary from a CSV export that is never
    quite clean: blank lines, spaces around values, mixed-case status, re-exported
    rows with the same order_id, and the odd typo in an amount.

    TASK
    * Ignore blank lines. Strip every header name and value; header is lower-cased.
    * Amounts: Decimal, rounded to 2 places ROUND_HALF_UP ("300.005" -> 300.01).
      Rows with an invalid amount are dropped and counted as "bad amounts".
    * Duplicate order_id: the LAST valid row wins; count each repeat as a duplicate.
    * Keep rows whose status is "paid" (any case) and whose date starts with `month`.
    Return exactly this text (no trailing newline):
        SALES REPORT 2026-10
        Paid orders: 6
        Revenue: 8,061.26
        Average order: 1,343.54
        By region:
          IN          3,700.50   45.9%
          ...
        Top customers:
          1. Qantler (3,700.50)
          ...
        Data issues: 1 duplicate ids, 1 bad amounts
    Formatting:
      average:      total / count, rounded ROUND_HALF_UP to 2 places
      region rows:  f"  {region:<8}{amount:>12,.2f}{share:>8.1%}"  (share = amount/total
                    as a float), sorted by amount desc then region
      top customers: top 3 by amount desc then name, f"  {i}. {name} ({amount:,.2f})"
    """
    raise NotImplementedError


# =============================================================================
#                         CHECKER -- no need to read below
# =============================================================================
import copy
import inspect


class CheckFailed(Exception):
    pass


def expect(actual, expected, what):
    if actual != expected:
        raise CheckFailed(
            f"{what}\n        expected: {expected!r}\n        got:      {actual!r}"
        )


def check_1(f):
    r = f["environment_report"]()
    expect(sorted(r), ["executable", "in_virtualenv", "major_minor", "python"], "keys")
    v = sys.version_info
    expect(r["python"], f"{v.major}.{v.minor}.{v.micro}", "python")
    expect(r["major_minor"], (v.major, v.minor), "major_minor")
    expect(r["in_virtualenv"], sys.prefix != sys.base_prefix, "in_virtualenv")
    expect(r["executable"], sys.executable, "executable")


def check_2(f):
    before = copy.deepcopy(CART)
    out = f["apply_discounts"](CART, DISCOUNT_RULES)
    expect(
        [(i["sku"], i["unit_price"], i["discount_pct"]) for i in out],
        [
            ("SOF-3S", Decimal("34650.00"), 10),
            ("LMP-BR", Decimal("1624.35"), 35),
            ("RUG-WL", Decimal("6999.99"), 0),
            ("CHR-TK", Decimal("4249.96"), 15),
        ],
        "prices",
    )
    expect(
        list(out[0]),
        ["sku", "name", "unit_price", "qty", "tags", "discount_pct"],
        "key order",
    )
    expect(CART, before, "input cart must not change")
    out[1]["tags"].append("hacked")
    expect(CART, before, "returned tags list is shared with the input (shallow copy?)")
    again = f["apply_discounts"](CART, DISCOUNT_RULES)
    expect(
        again[1]["unit_price"],
        Decimal("1624.35"),
        "second call must give the same price",
    )


def check_3(f):
    r = f["invoice_totals"](INVOICE_LINES)
    expect(r["subtotal"], Decimal("349596.28"), "subtotal")
    expect(
        r["tax_by_rate"],
        {
            0: Decimal("0.00"),
            12: Decimal("1931.64"),
            18: Decimal("6029.82"),
            28: Decimal("84000.08"),
        },
        "tax_by_rate",
    )
    expect(list(r["tax_by_rate"]), [0, 12, 18, 28], "tax_by_rate order")
    expect(r["tax"], Decimal("91961.54"), "tax")
    expect(r["grand_total"], Decimal("441557.82"), "grand_total")
    expect(r["formatted"], "₹441,557.82", "formatted")
    expect(
        all(
            isinstance(v, Decimal) for v in (r["subtotal"], r["tax"], r["grand_total"])
        ),
        True,
        "money values must be Decimal",
    )
    for bad in ([("x", 0, "10", 18)], [("x", 1, "10", 15)]):
        try:
            f["invoice_totals"](bad)
        except ValueError:
            continue
        raise CheckFailed(f"expected ValueError for {bad}")


def check_4(f):
    before = copy.deepcopy(CONTACTS)
    clean, rejects = f["clean_contacts"](CONTACTS)
    expect(
        clean,
        [
            {
                "name": "Meena Krishnan",
                "email": "meena.k@example.com",
                "phone": "+919876543210",
            },
            {"name": "Asha Devi", "email": "asha@example.in", "phone": "+919845012345"},
            {"name": "Arun Kumar", "email": None, "phone": "+919912345678"},
        ],
        "clean rows",
    )
    expect(
        rejects,
        [
            (2, "invalid email"),
            (3, "missing name"),
            (4, "invalid phone"),
            (6, "duplicate email"),
            (7, "invalid email"),
            (9, "invalid phone"),
        ],
        "rejects",
    )
    expect(CONTACTS, before, "input must not change")


def check_5(f):
    inputs = copy.deepcopy((DEFAULTS, FILE_CFG, ENV_CFG))
    merged, sources = f["merge_config"](DEFAULTS, FILE_CFG, ENV_CFG)
    expect(
        merged,
        {
            "env": "prod",
            "debug": False,
            "workers": 4,
            "retries": 0,
            "tags": [],
            "db": {
                "host": "db.internal",
                "port": 5432,
                "pool": 0,
                "password": "s3cret",
            },
            "llm": {"model": "claude-haiku-5-5", "max_tokens": 500},
            "feature_x": "",
        },
        "merged",
    )
    expect(
        sources,
        {
            "db.host": "file",
            "db.password": "env",
            "db.pool": "file",
            "db.port": "default",
            "debug": "file",
            "env": "env",
            "feature_x": "file",
            "llm.max_tokens": "default",
            "llm.model": "default",
            "retries": "env",
            "tags": "env",
            "workers": "default",
        },
        "sources",
    )
    expect(list(sources), sorted(sources), "sources must be sorted by key")
    expect((DEFAULTS, FILE_CFG, ENV_CFG), inputs, "inputs must not change")
    merged2, _ = f["merge_config"](
        {"tags": ["a"], "x": {"y": {"z": 1}}}, {"x": {"y": {"w": 2}}}, {}
    )
    merged2["tags"].append("b")
    expect(merged2["x"], {"y": {"z": 1, "w": 2}}, "deep nesting must merge")
    merged3, _ = f["merge_config"]({"tags": ["a"]}, {}, {})
    expect(merged3["tags"], ["a"], "result lists must be copies (mutating one leaked)")


def check_6(f):
    expect(
        f["leaderboard"](REPS),
        [
            (1, "David", Decimal(1310000), 11),
            (2, "Meena", Decimal("1250000.00"), 15),
            (2, "ravi", Decimal(1250000), 15),
            (3, "Asha", Decimal("1250000.00"), 12),
            (4, "anand", Decimal("980000.50"), 9),
            (4, "John", Decimal("980000.50"), 9),
            (4, "Priya", Decimal("980000.5"), 9),
            (5, "Lakshmi", Decimal(760000), 20),
        ],
        "leaderboard",
    )
    expect(
        f["top_per_region"](REPS, 2),
        {
            "North": ["David", "John"],
            "South": ["ravi", "Asha"],
            "West": ["Meena", "anand"],
        },
        "top_per_region",
    )
    expect(
        list(f["top_per_region"](REPS, 1)), ["North", "South", "West"], "region order"
    )


def check_7(f):
    final, anomalies, counts = f["order_status"](EVENTS)
    expect(
        final,
        {
            "O-1": "refunded",
            "O-2": "refunded",
            "O-3": "cancelled",
            "O-4": "created",
            "O-5": "paid",
        },
        "final",
    )
    expect(list(final), ["O-1", "O-2", "O-3", "O-4", "O-5"], "final order")
    expect(
        anomalies,
        [
            ("O-3", None, "paid"),
            ("O-4", "created", "shipped"),
            ("O-2", "refunded", "shipped"),
        ],
        "anomalies",
    )
    expect(
        list(counts.items()),
        [("refunded", 2), ("cancelled", 1), ("created", 1), ("paid", 1)],
        "counts and their order",
    )


def check_8(f):
    r = f["reconcile"](SOURCE_ROWS, TARGET_ROWS)
    expect(r["missing_in_target"], ["A-103"], "missing_in_target")
    expect(r["unexpected_in_target"], ["A-106"], "unexpected_in_target")
    expect(
        r["amount_mismatches"],
        [("A-102", Decimal("999.99"), Decimal("1000.00"))],
        "amount_mismatches",
    )
    expect(r["matched_count"], 4, "matched_count")
    expect(r["duplicate_ids_in_source"], ["A-101", "A-102"], "duplicate_ids_in_source")
    expect(
        (r["source_total"], r["target_total"], r["difference"]),
        (Decimal("2875.09"), Decimal("3135.10"), Decimal("260.01")),
        "totals",
    )


def check_9(f):
    r = f["validate_batch"](BATCH, ["order_id", "customer", "amount"], Decimal(10000))
    expect(
        r,
        {
            "ok": False,
            "rows": 3,
            "first_over_limit": 6,
            "errors": [
                (4, "bad amount 'abc'"),
                (5, "expected 4 fields, got 3"),
                (7, "expected 4 fields, got 5"),
            ],
        },
        "result",
    )
    r = f["validate_batch"](
        BATCH, ["order_id", "region", "amount", "store"], Decimal(10000)
    )
    expect(
        r,
        {
            "ok": False,
            "rows": 0,
            "errors": [(1, "missing columns: region, store")],
            "first_over_limit": None,
        },
        "missing columns",
    )
    r = f["validate_batch"]("id,amount\n1,5\n2,7\n", ["amount"], Decimal(100))
    expect(
        r,
        {"ok": True, "rows": 2, "errors": [], "first_over_limit": None},
        "clean batch",
    )


def check_10(f):
    r = f["customer_insights"](CUSTOMERS)
    expect(
        r["paid_totals"],
        {
            "Arhaus": Decimal("48497.50"),
            "Elite": Decimal(22495),
            "Fujitec": Decimal(0),
            "NCS": Decimal(28497),
            "Qantler": Decimal(0),
        },
        "paid_totals",
    )
    expect(
        list(r["paid_totals"]),
        ["Arhaus", "Elite", "Fujitec", "NCS", "Qantler"],
        "paid_totals order",
    )
    expect(r["gold_products"], ["desk", "lamp", "rug", "sofa"], "gold_products")
    expect(
        r["big_orders"],
        [("Arhaus", "A1"), ("NCS", "N1"), ("Elite", "E1")],
        "big_orders",
    )
    expect(
        r["product_buyers"],
        {
            "chair": ["Elite"],
            "desk": ["NCS"],
            "lamp": ["Arhaus", "Elite", "NCS"],
            "rug": ["Arhaus"],
            "sofa": ["Arhaus"],
        },
        "product_buyers",
    )
    expect(
        list(r["product_buyers"]),
        ["chair", "desk", "lamp", "rug", "sofa"],
        "product order",
    )
    expect(r["inactive"], ["Fujitec", "Qantler"], "inactive")


EXPECTED_LOG = """lines: 11 parsed, 3 skipped
module       total  errors  error_rate
payments         4       3       75.0%
delivery         3       2       66.7%
search           2       1       50.0%
catalog          2       0        0.0%
top errors:
  3 x Card declined for order #
  2 x Address not found for pin #
  1 x Gateway timeout after # ms"""

EXPECTED_SALES = """SALES REPORT 2026-10
Paid orders: 6
Revenue: 8,061.26
Average order: 1,343.54
By region:
  IN          3,700.50   45.9%
  US          3,280.76   40.7%
  SG          1,080.00   13.4%
Top customers:
  1. Qantler (3,700.50)
  2. Elite Parking (1,780.25)
  3. Arhaus (1,500.51)
Data issues: 1 duplicate ids, 1 bad amounts"""


def _compare_text(actual, expected, what):
    if actual == expected:
        return
    for n, (a, e) in enumerate(
        zip(actual.splitlines(), expected.splitlines()), start=1
    ):
        if a != e:
            raise CheckFailed(
                f"{what}: line {n} differs\n        expected: {e!r}\n        got:      {a!r}"
            )
    expect(
        len(actual.splitlines()), len(expected.splitlines()), f"{what}: number of lines"
    )
    expect(actual, expected, what)


def check_11(f):
    _compare_text(f["log_report"](LOG_LINES), EXPECTED_LOG, "report")
    expect(
        f["log_report"]([]).splitlines()[0], "lines: 0 parsed, 0 skipped", "empty input"
    )


def check_12(f):
    _compare_text(
        f["monthly_sales_report"](SALES_CSV, "2026-10"), EXPECTED_SALES, "report"
    )
    sept = f["monthly_sales_report"](SALES_CSV, "2026-09").splitlines()
    expect(
        sept[1:4],
        ["Paid orders: 1", "Revenue: 999.00", "Average order: 999.00"],
        "September",
    )


PROBLEMS = {  # number: (title, points, check, function names)
    1: ("Environment report", 5, check_1, ["environment_report"]),
    2: ("Discounts without side effects", 10, check_2, ["apply_discounts"]),
    3: ("GST invoice with Decimal", 10, check_3, ["invoice_totals"]),
    4: ("Contact cleaning", 15, check_4, ["clean_contacts"]),
    5: ("Layered configuration", 15, check_5, ["merge_config"]),
    6: ("Sales leaderboard", 10, check_6, ["leaderboard", "top_per_region"]),
    7: ("Order event state machine", 15, check_7, ["order_status"]),
    8: ("CDC reconciliation", 15, check_8, ["reconcile"]),
    9: ("Batch file validation", 10, check_9, ["validate_batch"]),
    10: ("Customer insights", 10, check_10, ["customer_insights"]),
    11: ("Log triage report", 15, check_11, ["log_report"]),
    12: ("Month-end sales report", 15, check_12, ["monthly_sales_report"]),
}

REVIEW_PATTERNS = [
    ("range(len(", "index loop: use enumerate() or loop over items"),
    ("== None", "use 'is None'"),
    ("!= None", "use 'is not None'"),
    ("import re", "regular expressions are not allowed in this chapter"),
]
MONEY_FUNCTIONS = {"apply_discounts", "invoice_totals", "reconcile"}


def review(func) -> list[str]:
    try:
        source = inspect.getsource(func)
    except (OSError, TypeError):
        return []
    body = source.split('"""')[-1] if source.count('"""') >= 2 else source
    notes = [msg for pattern, msg in REVIEW_PATTERNS if pattern in body]
    if func.__name__ in MONEY_FUNCTIONS and "float(" in body:
        notes.append("float in a money calculation: use Decimal")
    return notes


def run(impl: dict, selected: list[int] | None = None) -> int:
    selected = selected or list(PROBLEMS)
    score = total = 0
    print(f"\nChapter 1 hands-on  |  Python {sys.version.split()[0]}\n")
    for n in selected:
        title, points, check, names = PROBLEMS[n]
        total += points
        try:
            check(impl)
            status = "PASS"
            score += points
            detail = ""
        except NotImplementedError:
            status, detail = "TODO", ""
        except CheckFailed as e:
            status, detail = "FAIL", f"    -> {e}"
        except Exception as e:  # noqa: BLE001 - show any crash to the learner
            tb = e.__traceback__
            while tb.tb_next:  # walk to the last frame
                tb = tb.tb_next

            status, detail = (
                "FAIL",
                f"    -> crashed: Line: {tb.tb_lineno} : {type(e).__name__}: {e}",
            )
        print(
            f"  {status:<5} P{n:<3}{title:<34}{points if status == 'PASS' else 0:>3}/{points}"
        )
        if detail:
            print(detail)
        for name in names:
            for note in review(impl[name]):
                print(f"        REVIEW {name}: {note}")
    print(f"\n  SCORE {score}/{total}")
    if selected == list(PROBLEMS):
        verdict = (
            "ready for Chapter 2"
            if score >= 120
            else "revisit the sections you failed"
            if score >= 90
            else "re-read Chapter 1"
        )
        print(f"  {verdict}")
    return 0 if score == total else 1


if __name__ == "__main__":
    picks = [int(a) for a in sys.argv[1:] if a.isdigit() and int(a) in PROBLEMS]
    print(picks)
    sys.exit(run(globals(), picks or None))
    # environment_report()
