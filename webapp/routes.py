"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, url_for, jsonify, flash
from .forms import PEPredictionForm
from .pefinder.pefinder import analyze_reports, label_remapping, mark_reports
from .pefinder.utils import load_reports
from .pefinder.logman import logger

# Blueprint Configuration
main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder="static")

@main_bp.route("/", methods=["GET", "POST"])
def index():
    """Open the main page."""
    form = PEPredictionForm()
    if form.validate_on_submit():
        # form_fields = form._fields
        # for x, y in form_fields.items():
        #     print(x, Markup(y))

        verbose = bool(form['verbose'].data)
        remap = bool(form['remap'].data)

        # Load the reports
        reports = load_reports(reports_path=form['reports'].data,
                            report_field=form['report_field'].data,
                            id_field=form['id_field'].data,
                            delim=form['delim'].data)

        # What actions does the user want to run?
        if "classify" == form['run'].data:
            reports = analyze_reports(reports,
                                    report_field=form['report_field'].data,
                                    result_field=form['result_field'].data,
                                    verbose=verbose)

            # Remap to Stanford labels (default True)
            if remap == True:
                reports = label_remapping(reports=reports,
                                        result_field=form['result_field'].data,
                                        drop_result=True)

        elif "mark" == form['run'].data:
            reports = mark_reports(reports,
                                report_field=form['report_field'].data,
                                result_field=form['result_field'].data,                                   
                                verbose=verbose)

        # Parse result in some format, provide visualization? 
        reports.to_csv(form['output'].data, sep="\t",index=False)
        logger.info("Result for %s saved to %s", form['run'].data, form['output'].data)    
        flash("Reports processed sucessfully and written to file!")
    return render_template(
        "index.html",
        form=form,
    )
