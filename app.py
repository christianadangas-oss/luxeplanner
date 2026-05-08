import os
import json
import tempfile
import traceback

import anthropic
import fitz
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

MAX_PDF_BYTES = 15 * 1024 * 1024  # 15 MB
MAX_CONTRACT_CHARS = 50_000
MODEL = "claude-opus-4-7"

SYSTEM = """You are an expert luxury wedding planning contract analyst for LuxePlanner AI.
Extract structured data from vendor contracts to build production bible entries.

Be thorough but precise:
- If a field is genuinely not specified in the contract, use null (for strings) or [] (for arrays).
- Do not invent values. Do not paraphrase legal terms loosely.
- For risk_flags, surface real issues a wedding planner needs to know: vague cancellation terms,
  missing liability/insurance, exclusivity restrictions, unusual overtime rates, payment timing risk,
  ambiguous force majeure, and similar concrete concerns.
- Cancellation policy summaries should be in plain English a planner can read aloud to a client."""

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "vendor_name": {"type": "string"},
        "vendor_type": {"type": "string"},
        "event_date": {"type": ["string", "null"]},
        "total_value": {"type": "string"},
        "deposit_amount": {"type": ["string", "null"]},
        "deposit_due_date": {"type": ["string", "null"]},
        "final_payment_due": {"type": ["string", "null"]},
        "payment_schedule": {"type": "array", "items": {"type": "string"}},
        "services_included": {"type": "array", "items": {"type": "string"}},
        "setup_time": {"type": ["string", "null"]},
        "breakdown_time": {"type": ["string", "null"]},
        "staff_count": {"type": ["string", "null"]},
        "cancellation_policy": {"type": "string"},
        "cancellation_deadlines": {"type": "array", "items": {"type": "string"}},
        "force_majeure": {"type": ["string", "null"]},
        "overtime_policy": {"type": ["string", "null"]},
        "liability_insurance": {"type": ["string", "null"]},
        "exclusivity": {"type": ["string", "null"]},
        "key_dates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["date", "description"],
                "additionalProperties": False,
            },
        },
        "vendor_contact": {"type": ["string", "null"]},
        "risk_flags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["high", "medium", "low"]},
                    "title": {"type": "string"},
                    "detail": {"type": "string"},
                },
                "required": ["severity", "title", "detail"],
                "additionalProperties": False,
            },
        },
        "notes": {"type": ["string", "null"]},
    },
    "required": [
        "vendor_name", "vendor_type", "event_date", "total_value",
        "deposit_amount", "deposit_due_date", "final_payment_due",
        "payment_schedule", "services_included", "setup_time", "breakdown_time",
        "staff_count", "cancellation_policy", "cancellation_deadlines",
        "force_majeure", "overtime_policy", "liability_insurance", "exclusivity",
        "key_dates", "vendor_contact", "risk_flags", "notes",
    ],
    "additionalProperties": False,
}


def _extract_pdf_text(pdf_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name
    try:
        doc = fitz.open(tmp_path)
        try:
            return "".join(page.get_text() for page in doc)
        finally:
            doc.close()
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(Exception)
def handle_unexpected(e):
    app.logger.error("Unhandled error: %s\n%s", e, traceback.format_exc())
    return jsonify({"error": "Server error. Please try again."}), 500


@app.route("/extract", methods=["POST"])
def extract():
    try:
        if "pdf" not in request.files:
            return jsonify({"error": "No PDF uploaded"}), 400

        pdf_file = request.files["pdf"]
        if not pdf_file.filename:
            return jsonify({"error": "No PDF selected"}), 400
        if not pdf_file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "File must be a PDF"}), 400

        pdf_bytes = pdf_file.read()
        if not pdf_bytes:
            return jsonify({"error": "Uploaded PDF is empty"}), 400
        if len(pdf_bytes) > MAX_PDF_BYTES:
            return jsonify({"error": f"PDF too large (max {MAX_PDF_BYTES // (1024*1024)} MB)"}), 400

        try:
            text = _extract_pdf_text(pdf_bytes)
        except Exception as e:
            app.logger.warning("PDF parse failed: %s", e)
            return jsonify({"error": "Could not read PDF (corrupt or password-protected?)"}), 400

        if not text.strip():
            return jsonify({"error": "PDF appears to contain no extractable text (scanned image?)"}), 400

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return jsonify({"error": "Server is missing ANTHROPIC_API_KEY"}), 500

        client = anthropic.Anthropic(api_key=api_key)

        try:
            message = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                thinking={"type": "adaptive"},
                system=SYSTEM,
                output_config={
                    "format": {
                        "type": "json_schema",
                        "schema": EXTRACTION_SCHEMA,
                    }
                },
                messages=[{
                    "role": "user",
                    "content": (
                        "Extract all production bible data from this vendor contract.\n\n"
                        f"--- CONTRACT TEXT ---\n{text[:MAX_CONTRACT_CHARS]}"
                    ),
                }],
            )
        except anthropic.AuthenticationError:
            return jsonify({"error": "Invalid API key on server"}), 500
        except anthropic.RateLimitError:
            return jsonify({"error": "Rate limited. Please try again in a minute."}), 429
        except anthropic.BadRequestError as e:
            app.logger.error("Anthropic bad request: %s", e)
            return jsonify({"error": "Extraction request was rejected by the model API"}), 502
        except anthropic.APIStatusError as e:
            app.logger.error("Anthropic API error %s: %s", e.status_code, e)
            return jsonify({"error": "Model API error. Please try again."}), 502
        except anthropic.APIConnectionError:
            return jsonify({"error": "Could not reach the model API. Check your connection."}), 503

        if message.stop_reason == "refusal":
            return jsonify({"error": "Model declined to process this contract"}), 422

        text_block = next(
            (b.text for b in message.content if getattr(b, "type", None) == "text"),
            None,
        )
        if not text_block:
            return jsonify({"error": "Model returned no text output"}), 502

        try:
            data = json.loads(text_block)
        except json.JSONDecodeError as e:
            app.logger.error("JSON parse failed: %s | raw=%s", e, text_block[:500])
            return jsonify({"error": "Model returned malformed JSON"}), 502

        return jsonify(data)

    except Exception as e:
        app.logger.error("Unexpected error in /extract: %s\n%s", e, traceback.format_exc())
        return jsonify({"error": "Unexpected server error"}), 500


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    print("\n◈ LuxePlanner AI running at http://127.0.0.1:5000\n")
    app.run(debug=debug, port=5000)
