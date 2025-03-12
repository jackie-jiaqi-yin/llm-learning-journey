import gradio as gr
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import argparse

# set the file's parent directory as the current working directory
import os
os.chdir(os.path.dirname(os.path.dirname(__file__)))

# Configuration settings
CONFIG = {
    # UI Configuration
    "ui": {
        "theme": gr.themes.Citrus(),
        "title": "# 🤖 Agent Chatbot",
        "placeholder": "Ask me anything?",
    },
    # Chatbot Configuration
    "chatbot": {
        "height": 600,
        "preview_max_length": 150,
    },
    # Logging Configuration
    "logging": {
        "log_dir": "chat_logs",
        "enable_undo_logging": True,
    },
    # Feedback Configuration
    "feedback": {
        "default_feedback": None,
        "like_label": "like",
        "dislike_label": "dislike",
    }
}


# you need import your retriver engine. for example, engine from LlamaIndex


class ChatLogger:
    def __init__(self):
        self.current_log = {"meta": "", "log": []}
        self.log_dir = os.path.join(CONFIG["logging"]["log_dir"], datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(self.log_dir, exist_ok=True)
        log_filename = f'{datetime.now().strftime("%H-%M-%S")}.json'
        self.log_filename = os.path.join(self.log_dir, log_filename)

    def save_log(self):
        with open(self.log_filename, "w") as f:
            json.dump(self.current_log, f, indent=2)

    def update_log(self, user_message: str, bot_message: str):
        self.current_log["log"].append({
            "user_message": user_message,
            "bot_message": bot_message,
            "feedback": CONFIG["feedback"]["default_feedback"],
            "note": "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_log()

    def delete_log_entry(self, index: int):
        """Delete a log entry at a specific index (for undo operations)"""
        if 0 <= index < len(self.current_log["log"]):
            deleted_entry = self.current_log["log"].pop(index)
            self.save_log()
            return f"Log entry deleted at index {index} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return f"Error: Invalid log index {index}"

    def save_metadata(self, metadata: str) -> str:
        self.current_log["meta"] = metadata
        self.save_log()
        return f"Metadata saved at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def handle_feedback(self, like_data: gr.LikeData) -> Optional[str]:
        """Handle feedback (like/dislike) for a message."""
        try:
            # Get the message index from the like_data
            msg_idx = like_data.index
            
            # Handle different types of indices
            if isinstance(msg_idx, tuple):
                msg_idx = msg_idx[0]
            elif isinstance(msg_idx, list):
                if len(msg_idx) > 0:
                    msg_idx = msg_idx[0]
                else:
                    return "Error: Empty index list"
            
            # Ensure msg_idx is an integer
            if not isinstance(msg_idx, int):
                try:
                    msg_idx = int(msg_idx)
                except (ValueError, TypeError):
                    return f"Error: Cannot convert index {msg_idx} to integer"
            
            # Calculate the log index based on the message index
            # For bot messages (odd indices), the log index is (msg_idx - 1) // 2
            # For user messages (even indices), the log index is msg_idx // 2
            is_bot_message = msg_idx % 2 == 1
            log_index = (msg_idx - 1) // 2 if is_bot_message else msg_idx // 2
            
            # Check if the index is valid
            if 0 <= log_index < len(self.current_log["log"]):
                # When a user unclicks, liked is None/empty
                # When a user clicks like, liked is True
                # When a user clicks dislike, liked is False
                if like_data.liked is None or like_data.liked == "":
                    # This is an unclick action, reset to default
                    feedback_value = CONFIG["feedback"]["default_feedback"]
                else:
                    # This is a click action
                    feedback_value = CONFIG["feedback"]["like_label"] if like_data.liked else CONFIG["feedback"]["dislike_label"]
                
                self.current_log["log"][log_index]["feedback"] = feedback_value
                self.save_log()
                feedback_display = "None" if feedback_value is None else feedback_value
                return f"Feedback '{feedback_display}' saved for message"
            
            return f"Error: Invalid message index {log_index}"
        except Exception as e:
            print(f"Error in handle_feedback: {str(e)}")
            return f"Error saving feedback: {str(e)}"

    def save_response_note(self, note: str, index: int) -> str:
        if 0 <= index < len(self.current_log["log"]):
            self.current_log["log"][index]["note"] = note
            self.save_log()
            return f"Note saved for message at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return f"Error: Invalid message index {index}"


class ChatBot:
    def __init__(self, use_placeholder=False):
        if not use_placeholder:
            raise ValueError("You need to provide your own query engine.")
        else:
            # Placeholder query engine that doesn't call LLM
            self.query_engine = self._placeholder_query_engine
        self.logger = ChatLogger()
        self.status_message = ""
        self.current_message_index = -1  # Track the current message index for undo

    def _placeholder_query_engine(self, query: str) -> str:
        """Placeholder query engine that returns mock responses without calling LLM."""
        responses = {
            "default": "This is a placeholder response. The real LLM is not being called to save costs during testing."
            # you can add more responses here
        }
        
        # Simple keyword matching for different responses
        for keyword, response in responses.items():
            if keyword.lower() in query.lower():
                return response
                
        return responses["default"]

    def chat(self, message: str, history: List[Tuple[str, str]]) -> str:
        """Process a message and return a response, while logging the interaction."""
        response = self.query_engine(message)
        response_str = str(response)
        
        # Log the conversation
        self.logger.update_log(message, response_str)
        self.current_message_index += 1
        
        return response_str

    def undo(self, index: int = None) -> str:
        """Handle undo operation by deleting the last message from the log."""
        # If index is not provided, use the current message index
        log_index = index if index is not None else self.current_message_index
        
        if CONFIG["logging"]["enable_undo_logging"]:
            self.status_message = self.logger.delete_log_entry(log_index)
            # Decrement the current message index
            if self.current_message_index > -1:
                self.current_message_index -= 1
        
        return self.status_message

    def vote_callback(self, data: gr.LikeData) -> None:
        """Handle upvote/downvote on messages."""
        self.status_message = self.logger.handle_feedback(data)


# UI Configuration
UI_CONFIG = CONFIG["ui"]


def create_interface(chatbot: ChatBot) -> gr.Blocks:
    # Custom CSS to hide retry buttons
    custom_css = """
    button[aria-label="Retry"] {
        display: none !important;
    }
    """
    
    with gr.Blocks(theme=UI_CONFIG["theme"], css=custom_css) as interface:
        # add a title
        gr.Markdown(UI_CONFIG["title"])
        with gr.Row():
            with gr.Column(scale=4):
                metadata = gr.Textbox(
                    label="Metadata/Notes", 
                    placeholder="Enter any metadata or notes for this session", 
                    lines=1,
                    container=True
                )
            with gr.Column(scale=1, min_width=100):
                save_btn = gr.Button("💾 Save", variant="secondary", size="sm")
                
        # Create a custom chatbot component
        chatbot_component = gr.Chatbot(
            type="messages",  # Use the recommended 'messages' format
            show_copy_button=True,
            height=CONFIG["chatbot"]["height"],
            container=True,
            show_copy_all_button=True,
            placeholder="Ask me about CDP data...",
        )
         
        # Note section (hidden by default)
        with gr.Group(visible=False) as note_section:
            gr.Markdown("### 📝 Add Feedback Note")
            message_preview = gr.Textbox(
                label="Message", 
                interactive=False, 
                lines=1,
                container=True
            )
            response_note = gr.Textbox(
                label="Your Note", 
                placeholder="Add detailed notes about this response", 
                lines=1,
                container=True
            )
            message_index = gr.Number(value=0, visible=False)  # Hidden field to store the message index
            with gr.Row():
                cancel_note = gr.Button("Cancel", variant="secondary", size="sm")
                save_note = gr.Button("Save Note", variant="primary", size="sm")

        # Create the ChatInterface
        chat_interface = gr.ChatInterface(
            fn=chatbot.chat,
            chatbot=chatbot_component,
            type="messages",
            textbox=gr.Textbox(
                placeholder=UI_CONFIG["placeholder"],
                container=True,
                submit_btn=True
            ),
            autoscroll=True,
        )
        
        status = gr.Textbox(
            label="Status", 
            interactive=False,
            container=True,
            visible=True,
            lines=1
        )
        
        # Function to handle clicking on a message
        def on_message_feedback(evt: gr.LikeData):
            try:
                # Get the message index
                msg_idx = evt.index
                
                # In ChatInterface, messages are displayed in pairs (user, bot)
                # The index in the UI might be different from the log index
                # For even indices (0, 2, 4...), it's a user message
                # For odd indices (1, 3, 5...), it's a bot message
                is_bot_message = msg_idx % 2 == 1
                
                # Calculate the log index based on the message index
                # For bot messages (odd indices), the log index is (msg_idx - 1) // 2
                # For user messages (even indices), the log index is msg_idx // 2
                log_index = (msg_idx - 1) // 2 if is_bot_message else msg_idx // 2
                
                # Check if the index is valid
                if 0 <= log_index < len(chatbot.logger.current_log["log"]):
                    # Get the message content for preview
                    if is_bot_message:
                        message_content = chatbot.logger.current_log["log"][log_index]["bot_message"]
                    else:
                        message_content = chatbot.logger.current_log["log"][log_index]["user_message"]
                    
                    # Truncate if too long for preview
                    preview = message_content
                    if len(preview) > CONFIG["chatbot"]["preview_max_length"]:
                        preview = preview[:CONFIG["chatbot"]["preview_max_length"]-1] + "..."
                    
                    # Update the feedback in the log
                    chatbot.vote_callback(evt)
                    
                    # Show the note section with message preview
                    return gr.update(visible=True), preview, "", log_index
                
                # Invalid index
                return gr.update(visible=True), f"Error: Invalid message index {log_index}", "", 0
            except Exception as e:
                import traceback
                print(f"Error in on_message_feedback: {str(e)}")
                print(traceback.format_exc())
                return gr.update(visible=True), f"Error: {str(e)}", "", 0
        
        # Set up the feedback handler
        chatbot_component.like(
            on_message_feedback, 
            None, 
            [note_section, message_preview, response_note, message_index]
        )
        
        # Handle undo event
        def on_undo(history):
            if history:
                # For undo, we always want to delete the most recent log entry
                # So we use the last index in the log
                log_index = len(chatbot.logger.current_log["log"]) - 1
                chatbot.undo(log_index)
                return chatbot.status_message
            return "No message to undo"
        
        # Connect only the undo event
        chatbot_component.undo(on_undo, chatbot_component, status)
        
        # Save note button functionality
        def save_note_callback(note, index):
            result = chatbot.logger.save_response_note(note, index)
            # Return all required values: status message, note section visibility, empty note, reset index
            return result, gr.update(visible=False), "", 0
        
        save_note.click(
            save_note_callback, 
            [response_note, message_index], 
            [status, note_section, response_note, message_index]
        )
        
        # Cancel button just hides the note section
        cancel_note.click(
            lambda: (gr.update(visible=False), "", "", 0), 
            None, 
            [note_section, response_note, message_index]
        )
        
        # Set up the metadata save handler
        save_btn.click(
            lambda metadata: chatbot.logger.save_metadata(metadata),
            metadata,
            status
        )
        
    return interface


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CDP Agent Chatbot")
    parser.add_argument("--use-placeholder", action="store_true", help="Use placeholder responses instead of calling the LLM")
    args = parser.parse_args()
    
    chatbot = ChatBot(use_placeholder=args.use_placeholder)
    interface = create_interface(chatbot)
    interface.launch()

