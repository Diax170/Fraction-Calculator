import tkinter as tk
from math import gcd


class FractionInput(tk.Frame):
	def __init__(self, master=None, **kwargs):
		self.font = kwargs.pop('font', None)
		super().__init__(master, **kwargs)
		self._validate_cmd = self.register(self._validate)
		self._n_d_frame = tk.Frame(self)  # Create a frame for numerator, denominator and dash

		# Whole number
		self._whole_num_var = tk.StringVar()
		self._whole_num_var.trace_add("write", self._update_length)
		self.whole_num_input = tk.Entry(self, width=1, textvariable=self._whole_num_var, validate="key",
										validatecommand=(self._validate_cmd, '%S'), font=self.font, justify="center")

		# Numerator
		self._numerator_var = tk.StringVar()
		self._numerator_var.trace_add("write", self._update_length)
		self.numerator_input = tk.Entry(self._n_d_frame, width=1, textvariable=self._numerator_var, validate="key",
										validatecommand=(self._validate_cmd, '%S'), font=self.font, justify="center")

		# Denominator
		self._denominator_var = tk.StringVar()
		self._denominator_var.trace_add("write", self._update_length)
		self.denominator_input = tk.Entry(self._n_d_frame, width=1, textvariable=self._denominator_var, validate="key",
										validatecommand=(self._validate_cmd, '%S'), font=self.font, justify="center")

		# Dash
		self.dash = tk.Label(self._n_d_frame, text='-', font=self.font)

		# Pack all the widgets
		self.whole_num_input.pack(side=tk.LEFT)
		self.numerator_input.grid(row=0, column=0)
		self.dash.grid(row=1, column=0)
		self.denominator_input.grid(row=2, column=0)
		self._n_d_frame.pack(side=tk.RIGHT)

	def _validate(self, char):
		# Allow only digits (0-9) and backspace
		return char.isdigit() or char == '\b'

	def _update_length(self, *args):
		length = max(len(self.numerator_input.get()), len(self.denominator_input.get()))
		if length < 1: length = 1  # Minimal length

		denominator_len = len(self.whole_num_input.get())
		if denominator_len < 1: denominator_len = 1

		self.whole_num_input.config(width=denominator_len)
		self.numerator_input.config(width=length)
		self.denominator_input.config(width=length)
		self.dash.configure(text='-' * length)

	def state(self, state=None):
		# Disable/enable inputs
		if state is None:
			actual_state = self.whole_num_input.cget('state')
			new_state = 'normal' if actual_state == 'disabled' else 'disabled'
		elif type(state) is bool:
			if state: new_state = 'normal'
			else: new_state = 'disabled'
		else: new_state = state

		for widget in [self.whole_num_input, self.numerator_input, self.denominator_input]:
			widget.configure(state=new_state)

	def get_values(self):
		whole_num = self.whole_num_input.get()
		if not whole_num:  # If 'whole_num' string is empty
			whole_num = 0
		else:
			whole_num = int(whole_num)

		numerator = int(self.numerator_input.get())
		denominator = int(self.denominator_input.get())

		return whole_num, numerator, denominator


# All code below is written by AI, modified by me
class _CustomPopup:
	def __init__(self, parent, title, prompt, font):
		self.parent = parent
		self.popup = tk.Toplevel(parent)
		self.popup.title(title)

		# Set a custom font for the popup
		self.font = font

		# Disable other windows
		self.popup.grab_set()

		# Label for displaying the prompt text
		self.label = tk.Label(self.popup, text=prompt, font=self.font)
		self.label.pack(padx=5, pady=10)

		# Entry widget for user input
		self.entry_var = tk.StringVar()
		self.entry = tk.Entry(self.popup, textvariable=self.entry_var, font=self.font)
		self.entry.pack(padx=5, pady=5, side=tk.LEFT)

		# OK button to submit the entry
		self.ok_button = tk.Button(self.popup, text="OK", command=self.submit, font=self.font)
		self.ok_button.pack(padx=5, pady=5, side=tk.LEFT)

		# Variable to store the entered value
		self.result = None

	def submit(self):
		self.result = self.entry_var.get()
		self.popup.grab_release()  # Release the grab
		self.popup.destroy()  # Close the popup

	def show(self):
		self.popup.geometry("")  # Reset geometry to allow resizing
		self.popup.update_idletasks()  # Update the geometry
		self.popup.resizable(False, False)  # Make the popup un-resizable
		self.popup.grab_set()  # Set the grab
		self.parent.wait_window(self.popup)  # Wait for the popup to be closed


def open_popup(master, title, prompt, font=None):
	popup = _CustomPopup(master, title, prompt, font)
	popup.show()
	result = popup.result
	del popup  # Clear the memory
	return result


def find_lcm(x, y): return x * y // gcd(x, y)


def to_common_denominator(num1, den1, num2, den2):

	# Find the common denominator
	common_denominator = find_lcm(den1, den2)

	# Modify fractions to the common denominator
	new_num1 = num1 * (common_denominator // den1)
	new_num2 = num2 * (common_denominator // den2)

	# Return modified fractions
	return new_num1, common_denominator, new_num2, common_denominator
