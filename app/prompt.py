def build_prompt(question, chunks, history):
    context = "\n".join([f"[{c['file']}] {c['text']}" for c in chunks])
    hist = "\n".join(f"{t['role']}: {t['content']}" for t in history)
    return f"Context:\n{context}\n\nHistory:\n{hist}\nUser: {question}\nAssistant:"
 
