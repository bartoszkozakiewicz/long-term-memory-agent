from PIL import Image

def save_graph_structure(graph, filename):
    img_data = graph.get_graph(xray=True).draw_mermaid_png()
    with open(filename, "wb") as img_file:
        img_file.write(img_data)
    img = Image.open(filename)
    img.save(filename, "PNG")
    print("Graph structure image saved.")

def print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_stack")
    if current_state:
        print(f"Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)