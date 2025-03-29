import tkinter as tk
from openai import OpenAI
import json

client = OpenAI(api_key="YOUR_KEY_HERE")

root = tk.Tk()
root_width = 600
root_height = 360
root.title("ChatGPT")
root.geometry(f"{root_width}x{root_height}")
root.minsize(500, 300)

#Sidebar
setting_sidebar_width = 150
sb = tk.Frame(width=setting_sidebar_width, relief=tk.RIDGE, bd=2)
sb.pack(side="left", fill="y")
sb.pack_propagate(False)

sidebar_visible = True
def animate_sidebar(opening):
	global sidebar_visible
	max_width = setting_sidebar_width
	current_width = sb.winfo_width()

	if opening:
		current_width += 8
		if current_width > max_width:
			current_width = max_width
			sb.config(width=current_width)
			ms.config(width=root.winfo_width()-current_width)
		else:
			sb.config(width=current_width)
			ms.config(width=root.winfo_width()-current_width)
			sb.after(10, animate_sidebar, True)
	elif not opening:
		current_width -= 8
		if current_width < 0:
			current_width = 0
			sb.config(width=current_width)
			ms.config(width=root.winfo_width()-current_width)
			sidebar_visible = False
			sb.pack_forget()
		else:
			sb.config(width=current_width)
			ms.config(width=root.winfo_width()-current_width)
			sb.after(10, animate_sidebar, False)

#Sidebar.Top Buttons
sb_top_buttons = tk.Frame(sb, height=30)
sb_top_buttons.pack(side="top", fill="x")
sb_top_buttons_close_sidebar = tk.Button(sb_top_buttons, width=2, text="X", command=lambda: animate_sidebar(False))
sb_top_buttons_close_sidebar.pack(side="left", fill="x")
sb_top_buttons_new = tk.Button(sb_top_buttons, text="+", width=2)
sb_top_buttons_new.pack(side="right", fill="x")
sb_top_buttons_search = tk.Button(sb_top_buttons, text="o", width=2)
sb_top_buttons_search.pack(side="right", fill="x")
#Sidebar.Explore GPTS
sb_explore = tk.Frame(sb, height=60)
sb_explore.pack(side="top", fill="x", pady=5)
sb_explore_chatgpt = tk.Button(sb_explore, text="ChatGPT")
sb_explore_chatgpt.pack(fill="x", padx=5)
sb_explore_gpts = tk.Button(sb_explore, text="Explore Models")
sb_explore_gpts.pack(fill="x", padx=5)
#Sidebar.Today Conversations
sb_today_conversations = tk.Frame(sb)
sb_today_conversations.pack(side="top", fill="x")
sb_today_conversations_header = tk.Label(sb_today_conversations, text="Today's Conversations", font=("Arial", 7, "bold"))
sb_today_conversations_header.pack(side="top", fill="x")
#Sidebar.Previous Conversations
sb_previous_conversations = tk.Frame(sb)
sb_previous_conversations.pack(side="top", fill="x")
sb_previous_conversations_header = tk.Label(sb_today_conversations, text="Previous Conversations", font=("Arial", 7, "bold"))
sb_previous_conversations_header.pack(side="top", fill="x")
#Sidebar.Renew Plus
sb_renew_plus = tk.Frame(sb, height=30)
sb_renew_plus.pack(side="bottom", fill="x")
sb_renew_plus_button = tk.Button(sb_renew_plus, text="Renew Plus")
sb_renew_plus_button.pack()

#Main Screen
ms = tk.Frame(bg="white", width=root_width-setting_sidebar_width)
ms.pack(side="right", fill="y")
ms.pack_propagate(False)

#Main Screen.Top Bar
ms_top_bar = tk.Frame(ms, bg="white", height=40)
ms_top_bar.pack(side="top", fill="x")
ms_top_bar_change_model = tk.Label(ms_top_bar, text="ChatGPT v", bg="white")
ms_top_bar_change_model.pack(side="left", padx=15, pady=5)
ms_top_bar_profile = tk.Button(ms_top_bar, bg="lightblue", width=2, relief=tk.FLAT)
ms_top_bar_profile.pack(side="right")

#Chat Screen
ms_chat_screen = tk.Frame(ms, bg="white", relief=tk.RIDGE, bd=2)
ms_chat_screen.pack(fill="both", expand=True, padx=15, pady=10)

#Main Screen.Bottom Text
ms_bottom_text = tk.Label(ms, text="ChatGPT can make mistakes. Check important info.", bg="white", font=("Arial", 6))
ms_bottom_text.pack(side="bottom")
ms_center = tk.Frame(ms, bg="white")
ms_center.pack(side="bottom", fill="x")
#Main Screen.Title
ms_title = tk.Label(ms_center, text="What can I help you with?", bg="white", font=("Arial", 12, "bold"))
ms_title.pack(expand=True)
#Main Screen.Chatbox
ms_chatbox = tk.Frame(ms_center, bg="white", height=75, relief=tk.RIDGE, bd=2)
ms_chatbox.pack(expand=True, fill="x", padx=50)
ms_chatbox.pack_propagate(False)
ms_chatbox_text = tk.Text(ms_chatbox, wrap="word")
ms_chatbox_text.pack(fill="x")

messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def clear_widgets():
    for widget in ms_chat_screen.winfo_children():
        widget.destroy()

def refresh_chat():
	global messages
	clear_widgets()
	for message in messages:
		msg = tk.Label(ms_chat_screen, text=message["content"], wraplength=150, justify="left")
		if message["role"] == "assistant":
			msg.config(bg="lightgray")
			msg.pack(anchor="w", fill=tk.NONE)
		elif message["role"] == "user":
			msg.pack(anchor="e", fill=tk.NONE)
	print(messages)

def submit_text(event):
	if event.state != 0x1:
		messages.append({"role": "user", "content": ms_chatbox_text.get("1.0", "end")[:-1]})
		ms_chatbox_text.delete("1.0", "end")
		response = client.responses.create(
    		model="gpt-4o-mini",
    		input=messages
		)
		messages.append({"role": "assistant", "content": response.output_text})
		refresh_chat()
		return "break"
	else:
		refresh_chat()

ms_chatbox_text.bind("<Return>", submit_text)
#Main Screen.Chatbox.Bottom Bar
#Main Screen.Buttons
ms_buttons = tk.Frame(ms_center, bg="green")

def on_resize(event):
	global sidebar_visible
	if (event.width != root.winfo_width() or event.height != root.winfo_height()):
		if sidebar_visible:
			ms.config(width=root.winfo_width() - sb.winfo_width())
		elif not sidebar_visible:
			ms.config(width=root.winfo_width())

root.bind("<Configure>", on_resize)

root.mainloop()