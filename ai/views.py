from django.shortcuts import render, redirect

from .assistant import ask_ai


SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are an AI Course Assistant. "
        "Answer clearly and accurately. "
        "If you don't know something, say so. "
        "Use Markdown when appropriate."
    )
}


def chat(request):

    question = ""

    messages = request.session.get("messages")

    if messages is None:

        messages = [SYSTEM_PROMPT.copy()]

    if request.method == "POST":

        question = request.POST.get("question", "").strip()

        if question:

            messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            answer = ask_ai(messages)

            messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            request.session["messages"] = messages

            question = ""

    display_messages = [
        message
        for message in messages
        if message["role"] != "system"
    ]

    return render(
        request,
        "ai/chat.html",
        {
            "messages": display_messages,
            "question": question,
        },
    )


def clear_chat(request):

    if "messages" in request.session:

        del request.session["messages"]

    return redirect("chat")