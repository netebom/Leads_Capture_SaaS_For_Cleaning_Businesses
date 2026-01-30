from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    abort
)

from .models import (
    create_business,
    get_business_by_token,
    save_lead,
    get_leads,
    update_lead_status,
    get_leads_for_csv
)

from .email_utils import send_new_lead_email
from flask import Response
import csv

main_bp = Blueprint("main", __name__)

# -------------------------------------------------
# LANDING PAGE
# -------------------------------------------------
@main_bp.route("/")
def landing():
    return render_template("landing.html")


# -------------------------------------------------
# EARLY ACCESS EMAIL CAPTURE
# -------------------------------------------------
@main_bp.route("/early-access", methods=["POST"])
def early_access():
    email = request.form.get("email")

    if not email:
        abort(400)

    # (Intentionally not saved yet — keeps system stable)
    return redirect("/setup")


# -------------------------------------------------
# BUSINESS SETUP
# -------------------------------------------------
@main_bp.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        country = request.form.get("country")

        if not name or not email or not country:
            abort(400)

        token = create_business(name, email, country)
        return redirect(f"/dashboard/{token}")

    return render_template("setup.html")


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
@main_bp.route("/dashboard/<token>")
def dashboard(token):
    business = get_business_by_token(token)
    if not business:
        abort(404)

    leads = get_leads(token)

    return render_template(
        "dashboard.html",
        business=business,
        leads=leads,
        token=token
    )


# -------------------------------------------------
# PUBLIC LEAD FORM (GET)
# -------------------------------------------------
@main_bp.route("/form/<token>")
def public_lead_form(token):
    business = get_business_by_token(token)
    if not business:
        abort(404)

    return render_template(
        "public_form.html",
        business=business,
        token=token
    )


# -------------------------------------------------
# CAPTURE LEAD (POST)
# -------------------------------------------------
@main_bp.route("/lead/<token>", methods=["POST"])
def capture_lead(token):
    business = get_business_by_token(token)
    if not business:
        abort(404)

    lead = save_lead(
        business_token=token,
        cleaning_type=request.form.get("cleaning_type"),
        city=request.form.get("city"),
        phone=request.form.get("phone")
    )

    # Email notification (fails silently if SMTP unavailable)
    try:
        send_new_lead_email(business["email"], lead)
    except Exception:
        pass

    return render_template("thank_you.html")


# -------------------------------------------------
# UPDATE LEAD STATUS
# -------------------------------------------------
@main_bp.route("/lead-status/<token>/<int:lead_id>", methods=["POST"])
def lead_status(token, lead_id):
    status = request.form.get("status")
    update_lead_status(lead_id, status)
    return redirect(f"/dashboard/{token}")


# -------------------------------------------------
# CSV EXPORT
# -------------------------------------------------
@main_bp.route("/export/<token>")
def export_csv(token):
    business = get_business_by_token(token)
    if not business:
        abort(404)

    leads = get_leads_for_csv(token)

    def generate():
        output = []
        header = ["Cleaning Type", "City", "Phone", "Status", "Created At"]
        output.append(header)

        for lead in leads:
            output.append([
                lead["cleaning_type"],
                lead["city"],
                lead["phone"],
                lead["status"],
                lead["created_at"]
            ])

        for row in output:
            yield ",".join(row) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=leads.csv"
        }
    )
