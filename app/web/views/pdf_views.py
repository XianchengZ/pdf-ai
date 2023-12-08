from flask import Blueprint, g, jsonify
from app.web.hooks import login_required, handle_file_upload, load_model
from app.web.db.models import Pdf
from app.web.tasks.embeddings import process_document
from app.web import files
from app.web.config import Config

bp = Blueprint("pdf", __name__, url_prefix="/api/pdfs")


@bp.route("/", methods=["GET"])
@login_required
def list():
    pdfs = Pdf.where(user_id=g.user.id)

    return Pdf.as_dicts(pdfs)


@bp.route("/", methods=["POST"])
@login_required
@handle_file_upload
def upload_file(file_id, file_path, file_name):
    status_code = files.upload(file_path, file_id)
    if status_code >= 400:
        return status_code

    pdf = Pdf.create(id=file_id, name=file_name, user_id=g.user.id)

    process_document.delay(pdf.id)

    return pdf.as_dict()


@bp.route("/<string:pdf_id>", methods=["GET"])
@login_required
@load_model(Pdf)
def show(pdf):
    s3_client = files.get_s3_client()
    bucket_name = Config.AWS_S3_BUCKET_NAME
    object_key = pdf.id

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
             Params={
                'Bucket': bucket_name,
                'Key': object_key
             },
            ExpiresIn=12 * 3600
        )  # URL expires in 12 hour
        print(presigned_url)
        return jsonify(
            {
                "pdf": pdf.as_dict(),
                "download_url": presigned_url,
            }
        )
    except s3_client.exceptions.NoSuchKey:
        return jsonify({"message": "File not found"}), 404
    except Exception:
        return jsonify({"message": "Error fetching file"}), 500
