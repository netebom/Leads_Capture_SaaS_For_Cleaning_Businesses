from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    abort,
    Response
)
import csv
import io

from .models import (
    create_business,
    get_business_by_token,
    save_lead,
    get_leads,
    get_leads_for_csv,
    update_lead_status
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        country = request.form["country"]

        token = create_business(name, email, country)
        return redirect(f"/dashboard/{token}")

    return render_template("setup.html")


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


@main_bp.route("/lead/<token>", methods=["POST"])
def capture_lead(token):
    business = get_business_by_token(token)
    if not business:
        abort(404)

    save_lead(
        business_token=token,
        cleaning_type=request.form.get("cleaning_type"),
        city=request.form.get("city"),
        phone=request.form.get("phone")
    )

    return render_template("thank_you.html")


@main_bp.route("/lead-status/<token>/<int:lead_id>", methods=["POST"])
def lead_status(token, lead_id):
    business = get_business_by_token(token)
    if not business:
        abort(404)

    status = request.form.get("status")
    update_lead_status(lead_id, status)

    return redirect(f"/dashboard/{token}")


@main_bp.route("/export/<token>")
def export_csv(token):
    business = get_business_by_token(token)
    if not business:
        abort(404)

    leads = get_leads_for_csv(token)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Cleaning Type",
        "City",
        "Phone",
        "Status",
        "Created At"
    ])

    for lead in leads:
        writer.writerow([
            lead["cleaning_type"],
            lead["city"],
            lead["phone"],
            lead["status"],
            lead["created_at"]
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        f"attachment; filename=leads_{token}.csv"
    )

    return response
