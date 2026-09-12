from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from datetime import datetime, timedelta

from game.cases import CASES
from game.engine import InvestigationEngine


app = Flask(__name__)

app.secret_key = "change-this-secret-key"

engine = InvestigationEngine()


# =========================================================
# GAME STATE
# =========================================================

def reset_attempts_if_needed(case_id=None):

    """
    Reset attempts to 3 after the one-hour cooldown.

    Attempts are stored separately for every case.
    """

    if case_id is None:
        case_id = session.get("case_id")

    if not case_id:
        return

    case_progress = session.get(
        "case_progress",
        {}
    )

    if case_id not in case_progress:
        return

    progress = case_progress[case_id]

    reset_time = progress.get(
        "attempt_reset_time"
    )

    if not reset_time:
        return

    try:

        reset_time = datetime.fromisoformat(
            reset_time
        )

    except (ValueError, TypeError):

        progress["attempts"] = 3

        progress.pop(
            "attempt_reset_time",
            None
        )

        case_progress[case_id] = progress

        session["case_progress"] = case_progress

        session.modified = True

        return

    # -----------------------------------------------------
    # Cooldown finished
    # -----------------------------------------------------

    if datetime.now() >= reset_time:

        progress["attempts"] = 3

        progress.pop(
            "attempt_reset_time",
            None
        )

        case_progress[case_id] = progress

        session["case_progress"] = case_progress

        session.modified = True


# =========================================================
# CASE PROGRESS
# =========================================================

def initialize_case_progress(case_id):

    """
    Create progress storage for a case if it does not exist.
    """

    case_progress = session.get(
        "case_progress",
        {}
    )

    if case_id not in case_progress:

        case_progress[case_id] = {

            "score": 0,

            "attempts": 3,

            "found_clues": [],

            "unlocked_clues": [],

            "case_completed": False,

            "attempt_reset_time": None

        }

        session["case_progress"] = case_progress

        session.modified = True


def get_case_progress(case_id):

    """
    Return progress for the selected case.
    """

    initialize_case_progress(
        case_id
    )

    reset_attempts_if_needed(
        case_id
    )

    case_progress = session.get(
        "case_progress",
        {}
    )

    return case_progress.get(
        case_id,
        {
            "score": 0,
            "attempts": 3,
            "found_clues": [],
            "unlocked_clues": [],
            "case_completed": False,
            "attempt_reset_time": None
        }
    )


def save_case_progress(
    case_id,
    progress
):

    """
    Save progress for a specific case.
    """

    case_progress = session.get(
        "case_progress",
        {}
    )

    case_progress[case_id] = progress

    session["case_progress"] = case_progress

    session.modified = True


# =========================================================
# COMPLETED CASES
# =========================================================

def get_completed_cases():

    """
    Return the list of completed case IDs.

    completed_cases is the canonical unlock state.
    """

    completed_cases = session.get(
        "completed_cases",
        []
    )

    if not isinstance(
        completed_cases,
        list
    ):

        completed_cases = []

    return completed_cases


def complete_case(case_id):

    """
    Mark a case as completed.

    This updates BOTH:

    1. case_progress[case_id]["case_completed"]
    2. completed_cases

    Keeping both makes the system compatible with
    older sessions.
    """

    # -----------------------------------------------------
    # Update case progress
    # -----------------------------------------------------

    progress = get_case_progress(
        case_id
    )

    progress["case_completed"] = True

    save_case_progress(
        case_id,
        progress
    )

    # -----------------------------------------------------
    # Update canonical completed case list
    # -----------------------------------------------------

    completed_cases = get_completed_cases()

    if case_id not in completed_cases:

        completed_cases.append(
            case_id
        )

    session["completed_cases"] = (
        completed_cases
    )

    session.modified = True


def sync_completed_cases():

    """
    Synchronize old case_progress completion data
    into completed_cases.

    This is important for users who solved Case 1
    before the new unlock system was introduced.
    """

    completed_cases = get_completed_cases()

    changed = False

    for case in CASES:

        case_id = case["id"]

        progress = session.get(
            "case_progress",
            {}
        ).get(
            case_id
        )

        if not progress:
            continue

        if progress.get(
            "case_completed",
            False
        ):

            if case_id not in completed_cases:

                completed_cases.append(
                    case_id
                )

                changed = True

    if changed:

        session["completed_cases"] = (
            completed_cases
        )

        session.modified = True

    return completed_cases


# =========================================================
# GAME STATE
# =========================================================

def get_game_state():

    """
    Return current case + overall game state.
    """

    case_id = session.get(
        "case_id"
    )

    # -----------------------------------------------------
    # Sync completion state
    # -----------------------------------------------------

    sync_completed_cases()

    # -----------------------------------------------------
    # Overall XP
    # -----------------------------------------------------

    if "xp" not in session:

        session["xp"] = 0

    # -----------------------------------------------------
    # Overall score
    # -----------------------------------------------------

    if "score" not in session:

        session["score"] = 0

    # -----------------------------------------------------
    # No active case
    # -----------------------------------------------------

    if not case_id:

        return {

            "score":
                session.get(
                    "score",
                    0
                ),

            "xp":
                session.get(
                    "xp",
                    0
                ),

            "attempts":
                3,

            "unlocked_clues":
                [],

            "case_completed":
                False,

            "reset_time":
                None

        }

    # -----------------------------------------------------
    # Case progress
    # -----------------------------------------------------

    progress = get_case_progress(
        case_id
    )

    completed_cases = (
        get_completed_cases()
    )

    case_completed = (

        progress.get(
            "case_completed",
            False
        )

        or

        case_id in completed_cases

    )

    return {

        "score":
            progress.get(
                "score",
                0
            ),

        "xp":
            session.get(
                "xp",
                0
            ),

        "attempts":
            progress.get(
                "attempts",
                3
            ),

        "unlocked_clues":
            progress.get(
                "unlocked_clues",
                []
            ),

        "case_completed":
            case_completed,

        "reset_time":
            progress.get(
                "attempt_reset_time"
            )

    }


# =========================================================
# POINTS
# =========================================================

def add_game_points(
    points,
    case_id=None
):

    """
    Add points to:

    1. Current case score
    2. Overall score
    3. Overall XP
    """

    if case_id is None:

        case_id = session.get(
            "case_id"
        )

    # -----------------------------------------------------
    # Case score
    # -----------------------------------------------------

    if case_id:

        progress = get_case_progress(
            case_id
        )

        progress["score"] = (

            progress.get(
                "score",
                0
            )

            + points

        )

        save_case_progress(
            case_id,
            progress
        )

    # -----------------------------------------------------
    # Overall score
    # -----------------------------------------------------

    session["score"] = (

        session.get(
            "score",
            0
        )

        + points

    )

    # -----------------------------------------------------
    # Overall XP
    # -----------------------------------------------------

    session["xp"] = (

        session.get(
            "xp",
            0
        )

        + points

    )

    session.modified = True


# =========================================================
# DETECTIVE LEVEL
# =========================================================

def get_detective_level(xp):

    if xp >= 2000:
        return "MASTER DETECTIVE"

    if xp >= 1200:
        return "SENIOR DETECTIVE"

    if xp >= 600:
        return "INVESTIGATOR"

    if xp >= 250:
        return "JUNIOR INVESTIGATOR"

    return "TRAINEE"


# =========================================================
# CASE ACCESS CONTROL
# =========================================================

def is_case_unlocked(case_id):

    """
    Sequential case unlocking.

    Case 1:
        Always unlocked.

    Case 2:
        Requires Case 1 completion.

    Case 3:
        Requires Case 2 completion.

    Case 4:
        Requires Case 3 completion.

    etc.

    completed_cases is used as the primary unlock state.
    Existing case_progress completion is also supported.
    """

    # -----------------------------------------------------
    # Find requested case
    # -----------------------------------------------------

    try:

        current_index = next(

            index

            for index, case in enumerate(CASES)

            if case["id"] == case_id

        )

    except StopIteration:

        return False

    # -----------------------------------------------------
    # Case 1 always unlocked
    # -----------------------------------------------------

    if current_index == 0:

        return True

    # -----------------------------------------------------
    # Synchronize old completion data
    # -----------------------------------------------------

    completed_cases = (
        sync_completed_cases()
    )

    # -----------------------------------------------------
    # Previous case
    # -----------------------------------------------------

    previous_case = CASES[
        current_index - 1
    ]

    previous_case_id = (
        previous_case["id"]
    )

    # -----------------------------------------------------
    # Primary check
    # -----------------------------------------------------

    if previous_case_id in completed_cases:

        return True

    # -----------------------------------------------------
    # Backward-compatible check
    # -----------------------------------------------------

    previous_progress = get_case_progress(
        previous_case_id
    )

    if previous_progress.get(
        "case_completed",
        False
    ):

        # Repair completion state

        complete_case(
            previous_case_id
        )

        return True

    return False

def get_case_data_path(case_id, data_type):
    """
    Return the appropriate dataset for the active case.

    Existing cases continue using the original shared files.
    Case 4 uses dedicated datasets.
    """

    if case_id == "case_004":
        if data_type == "transactions":
            return "data/case_004_transactions.csv"

        if data_type == "movements":
            return "data/case_004_movements.csv"

    if data_type == "transactions":
        return "data/transactions.csv"

    if data_type == "movements":
        return "data/movements.csv"

    raise ValueError("Unsupported data type")

# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# CASE SELECTION
# =========================================================

@app.route("/cases")
def cases():

    # -----------------------------------------------------
    # Repair / synchronize completion state
    # -----------------------------------------------------

    sync_completed_cases()

    case_data = []

    for index, case in enumerate(CASES):

        progress = get_case_progress(
            case["id"]
        )

        unlocked = is_case_unlocked(
            case["id"]
        )

        completed_cases = (
            get_completed_cases()
        )

        completed = (

            progress.get(
                "case_completed",
                False
            )

            or

            case["id"] in completed_cases

        )

        case_data.append({

            "case":
                case,

            "unlocked":
                unlocked,

            "completed":
                completed,

            "score":
                progress.get(
                    "score",
                    0
                ),

            "attempts":
                progress.get(
                    "attempts",
                    3
                )

        })

    return render_template(

        "cases.html",

        cases=CASES,

        case_data=case_data

    )


# =========================================================
# START CASE
# =========================================================

@app.route("/start/<case_id>")
def start_case(case_id):

    # -----------------------------------------------------
    # Find case
    # -----------------------------------------------------

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return "Case not found", 404

    # -----------------------------------------------------
    # Check unlock
    # -----------------------------------------------------

    if not is_case_unlocked(
        case_id
    ):

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Initialize existing progress
    # -----------------------------------------------------

    initialize_case_progress(
        case_id
    )

    reset_attempts_if_needed(
        case_id
    )

    # -----------------------------------------------------
    # Set active case
    # -----------------------------------------------------

    session["case_id"] = (
        case_id
    )

    session.modified = True

    return redirect(
        url_for("investigation")
    )


# =========================================================
# INVESTIGATION
# =========================================================

@app.route("/investigation")
def investigation():

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Find case
    # -----------------------------------------------------

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Verify access
    # -----------------------------------------------------

    if not is_case_unlocked(
        case_id
    ):

        return redirect(
            url_for("cases")
        )

    progress = get_case_progress(
        case_id
    )

    return render_template(

        "investigation.html",

        case=case,

        score=progress.get(
            "score",
            0
        ),

        found_clues=progress.get(
            "found_clues",
            []
        )

    )


# =========================================================
# INVESTIGATE CLUE
# =========================================================

@app.route("/clue/<clue_id>")
def investigate_clue(clue_id):

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    if not is_case_unlocked(
        case_id
    ):

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Find current case
    # -----------------------------------------------------

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Make sure clue belongs to current case
    # -----------------------------------------------------

    valid_clue = any(

        clue["id"] == clue_id

        for clue in case.get(
            "clues",
            []
        )

    )

    if not valid_clue:

        return redirect(
            url_for("investigation")
        )

    # -----------------------------------------------------
    # Progress
    # -----------------------------------------------------

    progress = get_case_progress(
        case_id
    )

    found_clues = progress.get(
        "found_clues",
        []
    )

    # -----------------------------------------------------
    # Prevent duplicate clue points
    # -----------------------------------------------------

    if clue_id not in found_clues:

        found_clues.append(
            clue_id
        )

        progress["found_clues"] = (
            found_clues
        )

        progress["score"] = (

            progress.get(
                "score",
                0
            )

            + 100

        )

        save_case_progress(
            case_id,
            progress
        )

        # Overall score

        session["score"] = (

            session.get(
                "score",
                0
            )

            + 100

        )

        # Overall XP

        session["xp"] = (

            session.get(
                "xp",
                0
            )

            + 100

        )

        session.modified = True

    return redirect(
        url_for("investigation")
    )


# =========================================================
# ANALYSIS
# =========================================================

@app.route("/analysis")
def analysis():

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Transactions
    # -----------------------------------------------------

    df = engine.load_transactions(
        get_case_data_path(
            case_id,
            "transactions"
        ),
        case_id=case_id
    )

    df = engine.clean_transactions(
        df
    )

    analyzed_data = (
        engine.detect_anomalies(
            df
        )
    )

    # -----------------------------------------------------
    # Suspicion
    # -----------------------------------------------------

    suspicion_scores = (
        engine.calculate_suspicion(
            case["suspects"],
            analyzed_data
        )
    )

    insights = engine.generate_insight(
        analyzed_data,
        suspicion_scores
    )

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    total_transactions = len(
        analyzed_data
    )

    total_amount = (
        analyzed_data["amount"].sum()
    )

    anomaly_count = int(
        analyzed_data["anomaly"].sum()
    )

    average_transaction = (
        analyzed_data["amount"].mean()
    )

    highest_transaction = (
        analyzed_data["amount"].max()
    )

    # -----------------------------------------------------
    # Highest risk
    # -----------------------------------------------------

    highest_risk_id = max(

        suspicion_scores,

        key=suspicion_scores.get

    )

    highest_risk_score = (
        suspicion_scores[
            highest_risk_id
        ]
    )

    highest_risk_suspect = next(

        (

            suspect

            for suspect in case["suspects"]

            if suspect["id"]
            == highest_risk_id

        ),

        None

    )

    # -----------------------------------------------------
    # Chart data
    # -----------------------------------------------------

    chart_transactions = (

        analyzed_data[

            [
                "transaction_id",
                "suspect_id",
                "amount",
                "anomaly"
            ]

        ]

        .to_dict(
            orient="records"
        )

    )

    # -----------------------------------------------------
    # Suspect spending
    # -----------------------------------------------------

    suspect_spending = (

        analyzed_data

        .groupby(
            "suspect_id"
        )["amount"]

        .sum()

        .to_dict()

    )

    # -----------------------------------------------------
    # Anomalies
    # -----------------------------------------------------

    anomalies = analyzed_data[
        analyzed_data["anomaly"] == True
    ]

    return render_template(

        "analysis.html",

        case=case,

        transactions=(
            analyzed_data
            .to_dict(
                orient="records"
            )
        ),

        anomalies=(
            anomalies
            .to_dict(
                orient="records"
            )
        ),

        suspicion_scores=
            suspicion_scores,

        insights=
            insights,

        total_transactions=
            total_transactions,

        total_amount=
            total_amount,

        anomaly_count=
            anomaly_count,

        average_transaction=
            average_transaction,

        highest_transaction=
            highest_transaction,

        highest_risk_suspect=
            highest_risk_suspect,

        highest_risk_score=
            highest_risk_score,

        chart_transactions=
            chart_transactions,

        suspect_spending=
            suspect_spending

    )


# =========================================================
# TIMELINE
# =========================================================

@app.route("/timeline")
def timeline():

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    df = engine.load_movements(
        get_case_data_path(
            case_id,
            "movements"
        ),
        case_id=case_id
    )

    df = engine.clean_movements(
        df
    )

    selected_suspect = request.args.get(
        "suspect",
        "ALL"
    )

    selected_location = request.args.get(
        "location",
        "ALL"
    )

    filtered_df = engine.filter_movements(

        df,

        suspect=selected_suspect,

        location=selected_location

    )

    timeline_events = (
        engine.build_timeline(
            filtered_df
        )
    )

    suspects = case["suspects"]

    locations = sorted(
        df["location"]
        .unique()
        .tolist()
    )

    return render_template(

        "timeline.html",

        case=case,

        events=timeline_events,

        suspects=suspects,

        locations=locations,

        selected_suspect=
            selected_suspect,

        selected_location=
            selected_location

    )


# =========================================================
# CONNECTIONS
# =========================================================

@app.route("/connections")
def connections():

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    df = engine.load_movements(
        "data/movements.csv"
    )

    df = engine.clean_movements(
        df
    )

    connected_events = (
        engine.find_connected_events(
            df,
            max_minutes=10
        )
    )

    return render_template(

        "connections.html",

        case=case,

        connections=
            connected_events

    )


# =========================================================
# EVIDENCE BOARD
# =========================================================

@app.route("/evidence-board")
def evidence_board():

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    progress = get_case_progress(
        case_id
    )

    return render_template(

        "evidence_board.html",

        case=case,

        score=progress.get(
            "score",
            0
        )

    )


# =========================================================
# INTELLIGENCE
# =========================================================

@app.route("/intelligence")
def intelligence():

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Transactions
    # -----------------------------------------------------

    transactions = (
        engine.load_transactions(
            "data/transactions.csv"
        )
    )

    transactions = (
        engine.clean_transactions(
            transactions
        )
    )

    transactions = (
        engine.detect_anomalies(
            transactions
        )
    )

    # -----------------------------------------------------
    # Movements
    # -----------------------------------------------------

    movements = (
        engine.load_movements(
            "data/movements.csv"
        )
    )

    movements = (
        engine.clean_movements(
            movements
        )
    )

    # -----------------------------------------------------
    # Intelligence report
    # -----------------------------------------------------

    intelligence_report = (
        engine.build_intelligence_report(

            transactions,

            movements,

            case["suspects"]

        )
    )

    return render_template(

        "intelligence.html",

        case=case,

        intelligence=
            intelligence_report

    )


# =========================================================
# ACCUSATION
# =========================================================

@app.route(
    "/accuse",
    methods=["GET", "POST"]
)
def accuse():

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    case = next(

        (

            case

            for case in CASES

            if case["id"] == case_id

        ),

        None

    )

    if not case:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Check access
    # -----------------------------------------------------

    if not is_case_unlocked(
        case_id
    ):

        return redirect(
            url_for("cases")
        )

    reset_attempts_if_needed(
        case_id
    )

    progress = get_case_progress(
        case_id
    )

    # =====================================================
    # GET
    # =====================================================

    if request.method == "GET":

        return render_template(

            "accuse.html",

            case=case,

            suspects=case["suspects"],

            game=get_game_state(),

            reset_time=
                progress.get(
                    "attempt_reset_time"
                )

        )

    # =====================================================
    # POST
    # =====================================================

    suspect_id = request.form.get(
        "suspect_id"
    )

    explanation = request.form.get(
        "explanation",
        ""
    ).strip()

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    if not suspect_id:

        return render_template(

            "accuse.html",

            case=case,

            suspects=case["suspects"],

            game=get_game_state(),

            reset_time=
                progress.get(
                    "attempt_reset_time"
                ),

            error="Select a suspect."

        )

    if len(explanation) < 30:

        return render_template(

            "accuse.html",

            case=case,

            suspects=case["suspects"],

            game=get_game_state(),

            reset_time=
                progress.get(
                    "attempt_reset_time"
                ),

            error=(
                "Your explanation must contain "
                "at least 30 characters."
            )

        )

    # -----------------------------------------------------
    # Attempts
    # -----------------------------------------------------

    attempts = progress.get(
        "attempts",
        3
    )

    if attempts <= 0:

        return render_template(

            "accuse.html",

            case=case,

            suspects=case["suspects"],

            game=get_game_state(),

            reset_time=
                progress.get(
                    "attempt_reset_time"
                ),

            error=(
                "No investigation attempts "
                "remaining. Your attempts will "
                "reset after one hour."
            )

        )

    # -----------------------------------------------------
    # Consume attempt
    # -----------------------------------------------------

    progress["attempts"] = (
        attempts - 1
    )

    # -----------------------------------------------------
    # Start cooldown
    # -----------------------------------------------------

    if progress["attempts"] == 0:

        reset_time = (

            datetime.now()

            + timedelta(
                hours=1
            )

        )

        progress["attempt_reset_time"] = (
            reset_time.isoformat()
        )

    save_case_progress(
        case_id,
        progress
    )

    # =====================================================
    # CHECK ANSWER
    # =====================================================

    correct_suspect = case.get(
        "culprit_id"
    )

    # =====================================================
    # CORRECT
    # =====================================================

    if suspect_id == correct_suspect:

        base_points = 500

        remaining_attempt_bonus = (

            progress["attempts"]
            * 100

        )

        explanation_bonus = (

            150
            if len(explanation) >= 100
            else 50

        )

        total_points = (

            base_points

            + remaining_attempt_bonus

            + explanation_bonus

        )

        # -------------------------------------------------
        # Add score + XP
        # -------------------------------------------------

        add_game_points(

            total_points,

            case_id=case_id

        )

        # -------------------------------------------------
        # IMPORTANT:
        #
        # Explicitly mark the case completed.
        # This is what unlocks the next case.
        # -------------------------------------------------

        complete_case(
            case_id
        )

        # -------------------------------------------------
        # Save session
        # -------------------------------------------------

        session.modified = True

        return redirect(

            url_for(

                "case_result",

                result="success"

            )

        )

    # =====================================================
    # WRONG
    # =====================================================

    return redirect(

        url_for(

            "case_result",

            result="failure"

        )

    )


# =========================================================
# CASE RESULT
# =========================================================

@app.route(
    "/case-result/<result>"
)
def case_result(result):

    if result not in [
        "success",
        "failure"
    ]:

        return redirect(
            url_for("cases")
        )

    case_id = session.get(
        "case_id"
    )

    if not case_id:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Find case index
    # -----------------------------------------------------

    case_index = next(

        (

            index

            for index, case in enumerate(CASES)

            if case["id"] == case_id

        ),

        None

    )

    if case_index is None:

        return redirect(
            url_for("cases")
        )

    case = CASES[
        case_index
    ]

    # -----------------------------------------------------
    # If successful, make absolutely sure completion
    # state is stored.
    # -----------------------------------------------------

    if result == "success":

        complete_case(
            case_id
        )

    # -----------------------------------------------------
    # Game state
    # -----------------------------------------------------

    game = get_game_state()

    level = get_detective_level(
        game["xp"]
    )

    # -----------------------------------------------------
    # Next case
    # -----------------------------------------------------

    next_case = None

    if result == "success":

        if case_index + 1 < len(CASES):

            next_case = CASES[
                case_index + 1
            ]

    return render_template(

        "case_result.html",

        case=case,

        result=result,

        game=game,

        level=level,

        next_case=next_case

    )


# =========================================================
# CONTINUE TO NEXT CASE
# =========================================================

@app.route("/next-case")
def next_case():

    """
    Automatically move the player to the next
    unlocked case after completing the current case.
    """

    current_case_id = session.get(
        "case_id"
    )

    if not current_case_id:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Find current case
    # -----------------------------------------------------

    current_index = next(

        (

            index

            for index, case in enumerate(CASES)

            if case["id"] == current_case_id

        ),

        None

    )

    if current_index is None:

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # No next case
    # -----------------------------------------------------

    if current_index + 1 >= len(CASES):

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Next case
    # -----------------------------------------------------

    next_case = CASES[
        current_index + 1
    ]

    next_case_id = next_case[
        "id"
    ]

    # -----------------------------------------------------
    # Check unlock
    # -----------------------------------------------------

    if not is_case_unlocked(
        next_case_id
    ):

        return redirect(
            url_for("cases")
        )

    # -----------------------------------------------------
    # Start next case
    # -----------------------------------------------------

    initialize_case_progress(
        next_case_id
    )

    reset_attempts_if_needed(
        next_case_id
    )

    session["case_id"] = (
        next_case_id
    )

    session.modified = True

    return redirect(
        url_for("investigation")
    )


# =========================================================
# OPTIONAL DEBUG / SESSION RESET
# =========================================================

@app.route("/reset-game")
def reset_game():

    """
    Reset the entire game session.

    Use this only when you intentionally want
    to start the investigation from Case 1 again.
    """

    session.clear()

    return redirect(
        url_for("cases")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )