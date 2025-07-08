import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import (
    db,
    Prospect,
    STATUS_FOUND,
    STATUS_QUALIFIED,
    STATUS_CONVERTED,
)

# ------------------------------------------------------------------
# Factory pattern keeps things neat and testable
# ------------------------------------------------------------------
def create_app():
    app = Flask(__name__)

    # ----------------------------------------------------------------
    # Configuration
    # ----------------------------------------------------------------
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    # Persisted SQLite DB lives in /data (mounted from host ./data)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URI", "sqlite:////data/prospects.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialise SQLAlchemy
    db.init_app(app)
    return app


app = create_app()

# ------------------------------------------------------------------
# Ensure tables exist every time the app (or a new container) starts
# ------------------------------------------------------------------
with app.app_context():
    db.create_all()

# ------------------------------------------------------------------
# Optional CLI helper to drop & recreate the schema manually
#   > flask --app app.py init-db
# ------------------------------------------------------------------
@app.cli.command("init-db")
def init_db():
    """Drop ALL tables and recreate them (useful for a clean slate)."""
    db.drop_all()
    db.create_all()
    print("Database initialised.")


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@app.route("/")
def dashboard():
    total_found = Prospect.query.filter_by(status=STATUS_FOUND).count()
    total_qualified = Prospect.query.filter_by(status=STATUS_QUALIFIED).count()
    total_converted = Prospect.query.filter_by(status=STATUS_CONVERTED).count()

    total_sales = (
        db.session.query(db.func.sum(Prospect.opportunity_size))
        .filter(Prospect.status == STATUS_CONVERTED, Prospect.success.is_(True))
        .scalar()
        or 0
    )

    return render_template(
        "dashboard.html",
        total_found=total_found,
        total_qualified=total_qualified,
        total_converted=total_converted,
        total_sales=round(total_sales, 2),
    )


@app.route("/prospects", methods=["GET", "POST"])
def prospects():
    if request.method == "POST":
        name = request.form["name"].strip()
        contact = request.form.get("contact", "").strip()
        if not name:
            flash("Prospect name is required.", "danger")
        else:
            db.session.add(Prospect(name=name, contact_info=contact))
            db.session.commit()
            flash("Prospect added!", "success")
        return redirect(url_for("prospects"))

    items = Prospect.query.all()
    return render_template("prospects.html", items=items)


@app.route("/qualify/<int:pid>", methods=["POST"])
def qualify(pid):
    prospect = Prospect.query.get_or_404(pid)
    decision = request.form.get("decision")
    notes = request.form.get("notes")

    prospect.qualifying_notes = notes
    prospect.status = STATUS_QUALIFIED if decision == "qualify" else "disqualified"
    db.session.commit()
    return redirect(url_for("prospects"))


@app.route("/qualified")
def qualified():
    items = Prospect.query.filter_by(status=STATUS_QUALIFIED).all()
    return render_template("qualified.html", items=items)

@app.route("/disqualified")
def disqualified():
    items = Prospect.query.filter_by(status="disqualified").all()
    return render_template("disqualified.html", items=items)



@app.route("/convert/<int:pid>", methods=["POST"])
def convert(pid):
    prospect = Prospect.query.get_or_404(pid)
    amount = float(request.form.get("amount", 0))
    success = request.form.get("success") == "true"
    notes = request.form.get("notes")

    prospect.opportunity_size = amount
    prospect.conversion_notes = notes
    prospect.success = success
    prospect.status = STATUS_CONVERTED
    db.session.commit()
    return redirect(url_for("qualified"))


# ------------------------------------------------------------------
# Run the development server if you do: python app.py
# In Docker you'll normally use `flask run` (see Dockerfile/entrypoint),
# but this keeps local testing super-simple.
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
