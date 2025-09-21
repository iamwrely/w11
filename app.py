from __future__ import annotations

from datetime import datetime
from typing import Optional

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(database_uri: Optional[str] = None) -> Flask:
    """Application factory used for tests and production."""

    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="replace-this-secret-key",
        SQLALCHEMY_DATABASE_URI=database_uri or "sqlite:///clients.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    class Client(db.Model):
        __tablename__ = "clients"

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        phone = db.Column(db.String(50), nullable=True)
        company = db.Column(db.String(120), nullable=True)
        notes = db.Column(db.Text, nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self) -> str:  # pragma: no cover - debugging helper
            return f"<Client {self.name!r}>"

    @app.before_first_request
    def create_tables() -> None:
        db.create_all()

    @app.route("/")
    def index() -> str:
        search_query = request.args.get("search", "").strip()
        clients_query = Client.query.order_by(Client.created_at.desc())
        if search_query:
            like_query = f"%{search_query}%"
            clients_query = clients_query.filter(
                db.or_(
                    Client.name.ilike(like_query),
                    Client.email.ilike(like_query),
                    Client.phone.ilike(like_query),
                    Client.company.ilike(like_query),
                )
            )
        clients = clients_query.all()
        return render_template("index.html", clients=clients, search_query=search_query)

    @app.route("/clients/new", methods=["GET", "POST"])
    def create_client() -> str:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip() or None
            company = request.form.get("company", "").strip() or None
            notes = request.form.get("notes", "").strip() or None

            if not name or not email:
                flash("El nombre y el correo electrónico son obligatorios.", "error")
            else:
                existing = Client.query.filter_by(email=email).first()
                if existing:
                    flash("Ya existe un cliente con ese correo electrónico.", "error")
                else:
                    client = Client(
                        name=name,
                        email=email,
                        phone=phone,
                        company=company,
                        notes=notes,
                    )
                    db.session.add(client)
                    db.session.commit()
                    flash("Cliente creado correctamente.", "success")
                    return redirect(url_for("index"))

        return render_template("client_form.html", action="create")

    @app.route("/clients/<int:client_id>/edit", methods=["GET", "POST"])
    def edit_client(client_id: int) -> str:
        client = Client.query.get_or_404(client_id)

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip() or None
            company = request.form.get("company", "").strip() or None
            notes = request.form.get("notes", "").strip() or None

            if not name or not email:
                flash("El nombre y el correo electrónico son obligatorios.", "error")
            else:
                email_owner = Client.query.filter_by(email=email).first()
                if email_owner and email_owner.id != client.id:
                    flash("Otro cliente ya utiliza ese correo electrónico.", "error")
                else:
                    client.name = name
                    client.email = email
                    client.phone = phone
                    client.company = company
                    client.notes = notes
                    db.session.commit()
                    flash("Datos del cliente actualizados.", "success")
                    return redirect(url_for("index"))

        return render_template("client_form.html", action="edit", client=client)

    @app.route("/clients/<int:client_id>/delete", methods=["POST"])
    def delete_client(client_id: int) -> str:
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        flash("Cliente eliminado.", "success")
        return redirect(url_for("index"))

    @app.context_processor
    def inject_now() -> dict[str, datetime]:
        return {"now": datetime.utcnow()}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
