import sys
from pathlib import Path

import gradio as gr

sys.path.append(str(Path(__file__).parent / "src"))

from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    sources_text = "\n".join(f"• {source}" for source in result["sources"])

    return result["answer"], sources_text


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide")
    gr.Markdown("Ask questions about professor reviews. Answers are grounded in retrieved review chunks.")

    question = gr.Textbox(label="Your question", placeholder="Example: Which professor gives helpful feedback?")
    button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved Sources", lines=6)

    button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])

demo.launch()