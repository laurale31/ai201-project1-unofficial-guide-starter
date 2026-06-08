import gradio as gr
from rag import ask


def handle_query(question):

    answer, sources = ask(question)

    source_text = "\n".join(
        f"• {s}" for s in sorted(set(sources))
    )

    return answer, source_text


with gr.Blocks() as demo:

    gr.Markdown("# DePauw Professor Review Search")

    question = gr.Textbox(
        label="Ask a question"
    )

    answer = gr.Textbox(
        label="Answer",
        lines=10
    )

    sources = gr.Textbox(
        label="Sources",
        lines=5
    )

    ask_button = gr.Button("Ask")

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources]
    )

demo.launch()