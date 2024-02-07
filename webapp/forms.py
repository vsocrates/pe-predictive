"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class PEPredictionForm(FlaskForm):
    """User Sign-up Form."""

    reports = StringField("Reports Path",validators=[DataRequired()],
                          description="Path to folder of reports, or tab separated text file")

    report_field = StringField(
        "Report Text Field",
        validators=[
            Optional(),
        ],
        description="the header column that contains the text of interest (default is report_text)",
        default="report_text"
    )
    id_field = StringField(
        "Report ID Field",
        validators=[
            Optional()
        ],
        description="the header column that contains the id of the report (default is report_id)",
        default="report_id"

    )
    result_field = StringField(
        "PEFinder Result Field",
        validators=[
            Optional()
        ],
        description="the field to save pefinder (chapman) result to.",
    )
    delim = StringField(
        "Delimiter",
        validators=[
            Optional()
        ],
        description="the delimiter separating the input reports data. Default is tab (\\t)",
        default=r"\t"
    )
    output = StringField(
        "Output File Name",
        validators=[
            DataRequired()
        ],
        description="Desired output file (.tsv)"
    )
    verbose = SelectField(
        "Verbose",
        choices=[(1, 'Yes'), (0, 'No')],
        validators=[
            Optional()
        ],
        description="Print more verbose output (useful for analyzing more reports)",
        default=1,
        coerce=int
    )
    remap = SelectField(
        "Remap PEFidner to Stanford",
        choices=[(1, 'Yes'), (0, 'No')],
        validators=[
            Optional()
        ],
        description="don't remap multilabel PEFinder result to Stanford labels",
        default=1,
        coerce=int
    )
    run = SelectField(
        "Mark or Classify Reports",
        choices=[("mark", "Mark"), ("classify", "Classify")],
        validators=[
            Optional()
        ],
        description="mark (mark), or classify (classify) reports. Default is (classify).",
        default="classify"
    )

    submit = SubmitField("Predict")
