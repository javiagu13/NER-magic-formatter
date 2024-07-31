import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess
import os
import sys

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("File Processing App")
        self.geometry("1200x900")

        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Helvetica', 12))
        self.style.configure('TLabel', font=('Helvetica', 12), background="lightgray")

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=(20, 10))  # Adjust the bottom padding for consistency

        # Set the width of the buttons based on the longest text
        button_width = 30

        self.button1 = ttk.Button(self.button_frame, text="KULLM tsv to doccano - human", command=self.load_drag_drop_screen_1, width=button_width)
        self.button1.pack(side=tk.LEFT, padx=10)

        self.button2 = ttk.Button(self.button_frame, text="KULLM tsv to doccano - ai", command=self.load_drag_drop_screen_2, width=button_width)
        self.button2.pack(side=tk.LEFT, padx=10)

        self.button3 = ttk.Button(self.button_frame, text="JSONL to Markup", command=self.load_drag_drop_screen_3, width=button_width)
        self.button3.pack(side=tk.LEFT, padx=10)

        self.button4 = ttk.Button(self.button_frame, text="Markup to JSONL", command=self.load_drag_drop_screen_4, width=button_width)
        self.button4.pack(side=tk.LEFT, padx=10)

        # Adding a new frame for the "Undefined" buttons below the initial buttons
        self.undefined_buttons_frame = ttk.Frame(self)
        self.undefined_buttons_frame.pack(pady=10)  # Adjust the top padding for consistency

        self.row1_frame = ttk.Frame(self.undefined_buttons_frame)
        self.row1_frame.pack(pady=10)
        self.button5 = ttk.Button(self.row1_frame, text="Number the Markup", command=self.load_drag_drop_screen_5, width=button_width)
        self.button5.pack(side=tk.LEFT, padx=10)
        self.button6 = ttk.Button(self.row1_frame, text="Number the Json", command=self.load_drag_drop_screen_6, width=button_width)
        self.button6.pack(side=tk.LEFT, padx=10)
        self.button7 = ttk.Button(self.row1_frame, text="Undefined", command=self.load_execute_screen_7, width=button_width)
        self.button7.pack(side=tk.LEFT, padx=10)
        self.button8 = ttk.Button(self.row1_frame, text="Undefined", command=self.load_execute_screen_8, width=button_width)
        self.button8.pack(side=tk.LEFT, padx=10)

        self.row2_frame = ttk.Frame(self.undefined_buttons_frame)
        self.row2_frame.pack(pady=10)
        self.button9 = ttk.Button(self.row2_frame, text="Undefined", width=button_width)
        self.button9.pack(side=tk.LEFT, padx=10)
        self.button10 = ttk.Button(self.row2_frame, text="Undefined", width=button_width)
        self.button10.pack(side=tk.LEFT, padx=10)
        self.button11 = ttk.Button(self.row2_frame, text="Undefined", width=button_width)
        self.button11.pack(side=tk.LEFT, padx=10)
        self.button12 = ttk.Button(self.row2_frame, text="Undefined", width=button_width)
        self.button12.pack(side=tk.LEFT, padx=10)

        self.row3_frame = ttk.Frame(self.undefined_buttons_frame)
        self.row3_frame.pack(pady=10)
        self.button13 = ttk.Button(self.row3_frame, text="Undefined", width=button_width)
        self.button13.pack(side=tk.LEFT, padx=10)
        self.button14 = ttk.Button(self.row3_frame, text="Undefined", width=button_width)
        self.button14.pack(side=tk.LEFT, padx=10)
        self.button15 = ttk.Button(self.row3_frame, text="Undefined", width=button_width)
        self.button15.pack(side=tk.LEFT, padx=10)
        self.button16 = ttk.Button(self.row3_frame, text="Undefined", width=button_width)
        self.button16.pack(side=tk.LEFT, padx=10)

        self.row4_frame = ttk.Frame(self.undefined_buttons_frame)
        self.row4_frame.pack(pady=10)
        self.button17 = ttk.Button(self.row4_frame, text="Undefined", width=button_width)
        self.button17.pack(side=tk.LEFT, padx=10)
        self.button18 = ttk.Button(self.row4_frame, text="Undefined", width=button_width)
        self.button18.pack(side=tk.LEFT, padx=10)
        self.button19 = ttk.Button(self.row4_frame, text="Undefined", width=button_width)
        self.button19.pack(side=tk.LEFT, padx=10)
        self.button20 = ttk.Button(self.row4_frame, text="Undefined", width=button_width)
        self.button20.pack(side=tk.LEFT, padx=10)

        self.drag_drop_frame = ttk.Frame(self)
        self.execute_frame = ttk.Frame(self)
        self.proceed_button = None
        self.dropped_file = None
        self.selected_script = None
        self.description_label = None

    def load_drag_drop_screen(self, script_name, description):
        self.button_frame.pack_forget()
        self.undefined_buttons_frame.pack_forget()
        self.drag_drop_frame.pack(pady=20)
        self.selected_script = script_name

        self.description_label = ttk.Label(self.drag_drop_frame, text=description, anchor="center", wraplength=600)
        self.description_label.pack(pady=10)

        self.drop_label = ttk.Label(self.drag_drop_frame, text="Drag and drop a file here", anchor="center", relief="solid")
        self.drop_label.pack(fill=tk.BOTH, expand=True, padx=100, pady=200)

        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_file_drop)

        self.proceed_button = ttk.Button(self.drag_drop_frame, text="Proceed", command=self.process_file, state=tk.DISABLED)
        self.proceed_button.pack(pady=10)

    def load_execute_screen(self, script_name, description):
        self.button_frame.pack_forget()
        self.undefined_buttons_frame.pack_forget()
        self.execute_frame.pack(pady=20)
        self.selected_script = script_name

        #self.description_label = ttk.Label(self.drag_drop_frame, text=description, anchor="center", wraplength=600)
        #self.description_label.pack(pady=10)

        #self.drop_label = ttk.Label(self.drag_drop_frame, text="Drag and drop a file here", anchor="center", relief="solid")
        #self.drop_label.pack(fill=tk.BOTH, expand=True, padx=100, pady=200)

        #self.drop_label.drop_target_register(DND_FILES)
        #self.drop_label.dnd_bind('<<Drop>>', self.on_file_drop)

        self.proceed_button = ttk.Button(self.execute_frame, text="Proceed", command=self.process_script)
        self.proceed_button.pack(pady=10)

    def load_drag_drop_screen_1(self):
        self.load_drag_drop_screen('script1.py', "It takes a tsv file and generates a doccano jsonl file for each line. The input should be '[INST] Please output all medical terminologies related to the following medical record:' then ending the text with '[/INST]'. Finally the code will automatically erase anything after the '}]}' pattern \n\n An example: \n\n <s>[INST] Please output all medical terminologies related to the following medical record: F/28 Prev. healthy 2018-09-12 내원 1시간전에 갑작스럽게 우측 귀 청력저하 발생하여 ER 내원함 [/INST] {'DEMOGRAPHIC': [{'type': 'F/28', 'start_offset': 0, 'end_offset': 4}], 'TEMPORAL': [{'type': '2018-09-12', 'start_offset': 19, 'end_offset': 29}, {'type': '내원 1시간전', 'start_offset': 30, 'end_offset': 37}], 'SYMPTOM': [{'type': '우측 귀 청력저하', 'start_offset': 45, 'end_offset': 54}]} </s>")

    def load_drag_drop_screen_2(self):
        self.load_drag_drop_screen('script2.py', "It takes a tsv file and generates a doccano jsonl file for each line. The input should be '[INST] Please output all medical terminologies related to the following medical record:' then ending the text with '[/INST]'. Finally the code will automatically erase anything after the '}]}' pattern \n\n An example: \n\n <s>[INST] Please output all medical terminologies related to the following medical record: F/28 Prev. healthy 2018-09-12 내원 1시간전에 갑작스럽게 우측 귀 청력저하 발생하여 ER 내원함 [/INST] {'DEMOGRAPHIC': [{'type': 'F/28', 'start_offset': 0, 'end_offset': 4}], 'TEMPORAL': [{'type': '2018-09-12', 'start_offset': 19, 'end_offset': 29}, {'type': '내원 1시간전', 'start_offset': 30, 'end_offset': 37}], 'SYMPTOM': [{'type': '우측 귀 청력저하', 'start_offset': 45, 'end_offset': 54}]} </s>")

    def load_drag_drop_screen_3(self):
        self.load_drag_drop_screen('script3.py', "To transform JSONL to Markup copy all the desired files in a folder and drag and drop the folder full of JSONL here. It will transform all to Markup format.")
    
    def load_drag_drop_screen_4(self):
        self.load_drag_drop_screen('script4.py', "To transform Markup to JSONL copy all the desired files in a folder and drag and drop the folder full of Markup here. It will transform all to JSONL format ready to load in doccano.")

    def load_drag_drop_screen_5(self):
        self.load_drag_drop_screen('script5.py', "It loads a list of txt files and numbers them taking the number in the original txt. Id adds No. NUMBER at the beginning of each txt file.")

    def load_drag_drop_screen_6(self):
        self.load_drag_drop_screen('script6.py', "It loads a list of jsonl files and numbers them taking the number in the original txt. Id adds No. NUMBER after the '{\"text\": pattern at the beginning of each txt file.")

    def load_execute_screen_6(self):
        self.load_execute_screen('script6.py', "This code generates a template to ask chatGPT about the guidelines to create a blog, you just have to give the topic")

    def load_execute_screen_7(self):
        self.load_execute_screen('script7.py', "This code copies the prompt regarding the addition of image suggestion to the current blog")

    def load_execute_screen_8(self):
        self.load_execute_screen('script8.py', "This code copies the prompt regarding the FAQ blog to the current blog")


    def on_file_drop(self, event):
        self.dropped_file = event.data
        self.drop_label.config(text=f"File dropped: {self.dropped_file}", background="lightgreen")
        self.proceed_button.config(state=tk.NORMAL)

    def process_file(self):
        if self.dropped_file and self.selected_script:
            self.drop_label.config(text="Processing...", background="lightblue")
            self.proceed_button.config(state=tk.DISABLED)
            try:
                subprocess.run(['python', self.selected_script, self.dropped_file], check=True)
                
                file_directory = os.path.dirname(__file__)

                if sys.platform.startswith('darwin'):  # macOS
                    subprocess.run(['open', file_directory])
                elif os.name == 'nt':  # Windows
                    subprocess.run(['explorer', file_directory])
                elif os.name == 'posix':  # Linux
                    subprocess.run(['xdg-open', file_directory])
                messagebox.showinfo("Success", "File processed successfully!")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to process file: {e}")
            self.reset_screen()

    def process_script(self):
        self.proceed_button.config(state=tk.DISABLED)
        try:
            subprocess.run(['python', self.selected_script], check=True)
            
            file_directory = os.path.dirname(__file__)

            if sys.platform.startswith('darwin'):  # macOS
                subprocess.run(['open', file_directory])
            elif os.name == 'nt':  # Windows
                subprocess.run(['explorer', file_directory])
            elif os.name == 'posix':  # Linux
                subprocess.run(['xdg-open', file_directory])
            messagebox.showinfo("Success", "File processed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")
        self.reset_screen()

    def reset_screen(self):
        self.drag_drop_frame.pack_forget()
        self.button_frame.pack(pady=(20, 10))  # Adjust the bottom padding for consistency
        self.undefined_buttons_frame.pack(pady=10)  # Adjust the top padding for consistency
        self.dropped_file = None
        self.selected_script = None
        if self.description_label:
            self.description_label.pack_forget()
            self.description_label = None

if __name__ == "__main__":
    app = App()
    app.mainloop()
