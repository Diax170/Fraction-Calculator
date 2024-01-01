import tkinter as tk
from tkinter.ttk import Checkbutton
from tkinter import font as tmp_font
from tkinter.messagebox import showerror, showinfo
from classes import *
from math import *
from fractions import Fraction


tk.font = tmp_font
del tmp_font


def error(msg): showerror('Error', msg)


def clear(inputs=(True, True, True, True, True, True, True)):
	if inputs[0]: input1.whole_num_input.delete(0, tk.END)
	if inputs[1]: input1.numerator_input.delete(0, tk.END)
	if inputs[2]: input1.denominator_input.delete(0, tk.END)
	if inputs[3]: input2.whole_num_input.delete(0, tk.END)
	if inputs[4]: input2.numerator_input.delete(0, tk.END)
	if inputs[5]: input2.denominator_input.delete(0, tk.END)
	if inputs[6]: eval_entry.delete(0, tk.END)


def forward():
	try:
		# Get the values
		numerator, denominator = input1.get_values()[1:]

		# Forward the fraction
		gcd_result = gcd(numerator, denominator)
		numerator //= gcd_result
		denominator //= gcd_result

		# Display the result	
		clear(inputs=(False, True, True, False, False, False, False))
		input1.numerator_input.insert(0, str(numerator))
		input1.denominator_input.insert(0, str(denominator))
	except: error('Invalid input')


def extract_wholes():
	try:
		# Get the values
		whole_num, numerator, denominator = input1.get_values()

		# Extract wholes
		if numerator >= denominator:
			whole_num += numerator // denominator
			numerator %= denominator

		# Display the result
		clear()
		if whole_num != 0:
			input1.whole_num_input.insert(0, str(whole_num))
		input1.numerator_input.insert(0, str(numerator))
		input1.denominator_input.insert(0, str(denominator))
	except: error('Invalid input')


def to_improper():
	try:
		# Get the values
		whole_num, numerator, denominator = input1.get_values()

		# Convert to improper fraction
		numerator += whole_num * denominator

		# Display the result
		clear(inputs=(True, True, False, False, False, False, False))
		input1.numerator_input.insert(0, str(numerator))
	except: error('Invalid input')


def extend():
	try:
		# Get the values
		whole_num, numerator, denominator = input1.get_values()

		# Ask for the factor
		factor = int(open_popup(root, "Input", "Enter the factor", font=default_font))

		# Calculate and check is the operation legal
		numerator *= factor
		denominator *= factor
		if factor <= 0:
			raise ValueError('Numerator or denominator can\'t be negative')

		# Display the result
		clear(inputs=(False, True, True, False, False, False, False))
		input1.numerator_input.insert(0, str(numerator))
		input1.denominator_input.insert(0, str(denominator))
	except: error('Invalid input')


def to_common_d():
	if to_common_d_button.cget('text') == 'To common denominator...':
		# Setup

		# Disable other buttons
		for button in [forward_button, extract_wholes_btn, to_improper_btn, extend_button, eval_button]:
			button.configure(state='disabled')

		# Show formatted input2
		clear(inputs=(False, False, False, True, True, True, False))
		input2.pack(side=tk.LEFT)

		# Configure the calculation button and the finish button
		to_common_d_button.configure(text='To common denominator')
		finish_button.pack()
	else:
		# Calculation

		try:
			# Get the values
			numerator1, denominator1 = input1.get_values()[1:]
			numerator2, denominator2 = input2.get_values()[1:]

			# Calculate
			numerator1, denominator1, numerator2, denominator2 = (
				to_common_denominator(numerator1, denominator1, numerator2, denominator2))

			# Display the result
			clear(inputs=(False, True, True, False, True, True, False))
			input1.numerator_input.insert(0, numerator1)
			input1.denominator_input.insert(0, denominator1)
			input2.numerator_input.insert(0, numerator2)
			input2.denominator_input.insert(0, denominator2)
		except: error('Invalid input')


def eval_calculator():
	# Setup

	# Disable some buttons
	for button in [forward_button, extract_wholes_btn, to_improper_btn, extend_button, eval_button, to_common_d_button]:
		button.configure(state='disabled')

	# Show formatted input2 and eval_frame and hide input1
	clear(inputs=(False, False, False, True, True, True, True))
	eval_frame.pack(side=tk.LEFT)
	input2.pack(side=tk.LEFT)
	input2.state('disabled')  # Disable input2
	input1.pack_forget()

	# Configure the finish button
	finish_button.pack()


def eval_solve(*args):
	input2.state('normal')
	clear(inputs=(False, False, False, True, True, True, False))
	try:
		# Solve
		result = float(eval(eval_entry.get()))
		if result == int(result): result = int(result)

		eval_result.configure(text='Result: ' + str(result))  # Display the result

		fraction = Fraction(result).limit_denominator(1000000)
		numerator = fraction.numerator
		denominator = fraction.denominator
		whole_num = 0

		# Extract wholes
		if numerator >= denominator and eval_check_var.get() == False:
			whole_num += numerator // denominator
			numerator %= denominator

		# Display the result as fraction

		input2.whole_num_input.insert(0, ('' if whole_num == 0 else str(whole_num)))
		input2.numerator_input.insert(0, numerator)
		input2.denominator_input.insert(0, denominator)
	except:
		eval_result.configure(text='Result: E')
	finally: input2.state('disabled')


def frac(arg1, arg2, arg3=None):
	# Function for eval calculator

	negative = any(x < 0 for x in (arg1, arg2, (0 if arg3 is None else arg3)))
	arg1 = abs(int(arg1))
	arg2 = abs(int(arg2))
	if arg3 is not None: arg3 = abs(int(arg3))

	if arg3 is None:
		if negative: arg1 = -arg1
		return Fraction(arg1, arg2)
	else:
		arg2 += arg1 * arg3  # numerator += whole number * denominator
		if negative: arg2 = -arg2
		return Fraction(arg2, arg3)


def finish():
	if to_common_d_button.cget('text') == 'To common denominator':  # If common denominator mode is opened
		to_common_d_button.configure(text='To common denominator...')
	else:  # If eval calculator mode is opened
		eval_frame.pack_forget()  # Hide the eval calculator frame
		input1.pack(side=tk.LEFT)  # Show the input1
		input2.state('normal')  # Enable input2 back

	# Enable the buttons
	for button in [forward_button, extract_wholes_btn, to_improper_btn, extend_button, eval_button, to_common_d_button]:
		button.configure(state='normal')

	# Hide the finish button and input2
	finish_button.pack_forget()
	input2.pack_forget()


def copy_eval_result():
	try:  # Try to copy result to clipboard, if failed inform user about an error
		root.clipboard_clear()
		root.clipboard_append(eval_result.cget('text')[8:])
		root.update()  # Update clipboard content
		showinfo("Copied", "Result copied to clipboard!")
	except Exception: error('Failed to copy')


root = tk.Tk()
root.title('Fraction Calculator')

# Set the default font size
default_font = tk.font.nametofont("TkDefaultFont")
default_font.configure(size=15)

main_label = tk.Label(root, text="Fraction Calculator")
main_label.pack()

# FractionInput
input_frame = tk.Frame(root)
input1 = FractionInput(input_frame, font=default_font, padx=20, pady=10)
input1.pack(side=tk.LEFT)


# Eval calculator
eval_frame = tk.Frame(input_frame)

eval_variable = tk.StringVar()
eval_variable.trace_add('write', eval_solve)
eval_entry = tk.Entry(eval_frame, font=default_font, textvariable=eval_variable)
eval_entry.pack(pady=5)

eval_result_frame = tk.Frame(eval_frame)
eval_result = tk.Label(eval_result_frame, font=default_font, padx=5, pady=5, text='Result: E')
eval_result.pack(side=tk.LEFT)
eval_copy_button = tk.Button(eval_result_frame, text='Copy', command=copy_eval_result)
eval_copy_button.pack(side=tk.LEFT)
eval_help_button = tk.Button(eval_result_frame, text='?', command=(
	lambda: showinfo('Help',
	'Insert your math problem in Python syntax.\nReplace fractions with \'frac(wholes, num, denom)\' or \'frac(num, denom)\'.\nCalculator isn\'t 100% accurate!')))
eval_help_button.pack(side=tk.LEFT)
eval_result_frame.pack()

eval_check_frame = tk.Frame(eval_frame)
eval_check_label = tk.Label(eval_check_frame, text='Show as improper', padx=5, pady=5)
eval_check_label.pack(side=tk.LEFT)
eval_check_var = tk.BooleanVar(value=True)
eval_check_var.trace_add('write', eval_solve)
eval_check = Checkbutton(eval_check_frame, variable=eval_check_var)
eval_check.pack(side=tk.LEFT, pady=5)
eval_check_frame.pack()

eval_frame.pack(side=tk.LEFT)


# Second FractionInput
input2 = FractionInput(input_frame, font=default_font, padx=20, pady=10)
input2.pack(side=tk.LEFT)
input_frame.pack()

# Menu buttons
button_frame1 = tk.Frame(root)
forward_button = tk.Button(button_frame1, text='Forward', command=forward)
forward_button.pack(side=tk.LEFT)
extract_wholes_btn = tk.Button(button_frame1, text='Extract wholes', command=extract_wholes)
extract_wholes_btn.pack(side=tk.LEFT)
to_improper_btn = tk.Button(button_frame1, text='To improper', command=to_improper)
to_improper_btn.pack(side=tk.LEFT)
extend_button = tk.Button(button_frame1, text='Extend...', command=extend)
extend_button.pack(side=tk.LEFT)
button_frame1.pack()

button_frame2 = tk.Frame(root)
to_common_d_button = tk.Button(button_frame2, text='To common denominator...', command=to_common_d)
to_common_d_button.pack(side=tk.LEFT)
eval_button = tk.Button(button_frame2, text='Eval calculator...', command=eval_calculator)
eval_button.pack(side=tk.LEFT)
clear_button = tk.Button(button_frame2, text='Clear', command=clear)
clear_button.pack(side=tk.LEFT)
finish_button = tk.Button(button_frame2, text="Finish", command=finish)  # Button to exit modes like eval calculator
finish_button.pack(side=tk.LEFT)
button_frame2.pack()

# Disable window resize
root.update_idletasks()
root.resizable(False, False)

# Temporarily hide eval frame, input2 and finish button
eval_frame.pack_forget()
input2.pack_forget()
finish_button.pack_forget()

root.mainloop()
