import json
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import dashboard_bp
from ..services.analyzer import ResumeAnalyzer
from ..services.scorer import ResumeScorer
from ..services.suggestions import SuggestionEngine
from ..services.graph_generator import GraphGenerator
from ..models import ResumeAnalysis
from ..extensions import db
from ..utils import allowed_file, safe_store_name, ensure_folder
from config import Config

dashboard_bp = Blueprint("dashboard", __name__)

analyzer = ResumeAnalyzer()
scorer = ResumeScorer()
suggester = SuggestionEngine()
graphger = GraphGenerator(Config.GRAPH_FOLDER)

ensure_folder(Config.UPLOAD_FOLDER)
ensure_folder(Config.GRAPH_FOLDER)

@dashboard_bp.route("/")
def home():
    return render_template("dashboard/index.html")

@dashboard_bp.route("/analyze", methods=["POST"])
def analyze():
    pdf_file = request.files.get("resume_file")
    image_file = request.files.get("resume_image")
    camera_file = request.files.get("camera_image")
    resume_url = request.form.get("resume_url", "").strip()

    uploaded_name = None
    text_data = ""

    if pdf_file and pdf_file.filename:
        if not allowed_file(pdf_file.filename, Config.ALLOWED_PDF):
            flash("Only PDF files are allowed for PDF analysis.")
            return redirect(url_for("dashboard.home"))
        uploaded_name = safe_store_name(pdf_file.filename)
        save_path = Path(Config.UPLOAD_FOLDER) / uploaded_name
        pdf_file.save(save_path)
        text_data = analyzer.extract_pdf_text(save_path)

    elif image_file and image_file.filename:
        flash("Image upload received. OCR can be added next for image text extraction.")
        return redirect(url_for("dashboard.home"))

    elif camera_file and camera_file.filename:
        flash("Camera capture received. OCR can be added next for camera image text extraction.")
        return redirect(url_for("dashboard.home"))

    elif resume_url:
        flash("Resume URL input received. URL fetch parsing can be added next.")
        return redirect(url_for("dashboard.home"))

    else:
        flash("Please upload a PDF, image, camera capture, or enter a resume URL.")
        return redirect(url_for("dashboard.home"))

    if not text_data:
        flash("No text could be extracted from the resume PDF.")
        return redirect(url_for("dashboard.home"))

    analysis_df = analyzer.analyze_keywords(text_data)
    ats_report = analyzer.ats_check(text_data)
    final_score = scorer.score(analysis_df)
    breakdown = scorer.breakdown(analysis_df)
    suggestions = suggester.build(analysis_df, ats_report)
    graph_path = graphger.save_bar(breakdown)

    payload = {
        "score": final_score,
        "ats": ats_report,
        "suggestions": suggestions,
        "rows": analysis_df.to_dict(orient="records"),
    }

    if current_user.is_authenticated:
        record = ResumeAnalysis(
            user_id=current_user.id,
            filename=uploaded_name or "uploaded_resume",
            score=final_score,
            summary_json=json.dumps(payload)
        )
        db.session.add(record)
        db.session.commit()

    return render_template(
        "dashboard/result.html",
        score=final_score,
        ats=ats_report,
        suggestions=suggestions,
        table_rows=analysis_df.to_dict(orient="records"),
        graph_url=url_for("static", filename=f"graphs/{Path(graph_path).name}")
    )