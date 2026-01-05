# app.py
import os
from flask import Flask, render_template, request, send_from_directory, current_app
# from config import UPLOAD_FOLDER, PORT
from extensions import init_services
from errors.handlers import register_error_handlers
from config import get_config

def create_app():
    app = Flask(__name__)

    config_class = get_config()
    config_class.validate()

    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    init_services(app)
    register_error_handlers(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/process", methods=["POST"])
    def process():
        file = request.files.get("pdf")
        if not file:
            return "No file uploaded!", 400

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        doc = current_app.document_service.process_pdf(filepath)
        current_app.rag_service.index(doc["json"], doc_id=file.filename)

        return render_template(
            "result.html",
            filename=file.filename,
            extracted_text=doc["text"]
        )

    @app.route("/ask", methods=["POST"])
    def ask():
        question = request.form.get("question", "").strip()

        if not question:
            return {"answer": "No question provided."}

        # 🔥 NEW: use Self-Verifying RAG
        result = current_app.rag_service.answer_question(question)

        return result



    @app.route("/summarize", methods=["POST"])
    def summarize():
        text = request.form.get("text", "").strip()
        if not text:
            return {"summary": "No text provided."}

        return {"summary": current_app.llm_service.summarize(text)}

    @app.route("/mindmap", methods=["POST"])
    def mindmap():
        text = request.form.get("text", "").strip()
        if not text:
            return {"mindmap": "No text provided."}

        return {"mindmap": current_app.llm_service.generate_mindmap(text)}

    @app.route("/uploads/<filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=app.config.get("DEBUG", False),
        port=app.config["PORT"]
    )
