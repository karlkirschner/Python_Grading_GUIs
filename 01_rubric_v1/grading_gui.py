import bisect
import tkinter

from tkinter import (Checkbutton, END, Entry, filedialog, Label, Button, IntVar, HORIZONTAL,Scrollbar, StringVar, Text, WORD)


def show_entry_fields():
    ''' Print to screen the values of the filled in fields and
            the computed final score and mark.
    '''

    data = grab_form_data()

    final_score = compute_final_score()
    final_mark = score2mark(score=final_score)
    
    if data['feedback'] != '':
        feedback = f"\nFeedback:\n{data['feedback']}\n\n"
    else:
        feedback = ''

    print(f"Student Name:                         {data['name']}\n"
          f"Assignment:                           {data['assignment']}\n"
          f"Code Quality (x6):                    {data['code_qual']}\n"
          f"Scientific & Scholarly Concepts (x6): {data['sci_conc']}\n"
          f"Code Execution & Results (x4):        {data['execution']}\n"
          f"Assignment Completed (x2):            {data['completed']}\n"
          f"Followed Instructions (x10):          {data['follow_inst']}\n\n"
          f"{feedback}"
          f"Total Score: {final_score}\n"
          f"Final Mark:  {final_mark}\n"
          )


def score2mark(score: float) -> float:
    ''' Convert final score (i.e. a perctage) to a mark grade.

        Args:
            score: a percentage value out of 100 (e.g., 0.0, 50.5, 88.3, 100.0)
        Return:
            mark

        Dependencies:
            bisect
    '''

    if not isinstance(score, float):
        raise TypeError("score is not a float.")
    else:
        point_cutoffs = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
        marks = ['5.0', '4.0', '3.7', '3.3', '3.0', '2.7', '2.3', '2.0', '1.7', '1.3', '1.0']

        index = bisect.bisect(point_cutoffs, score)

        return marks[index]


def compute_final_score() -> float:
    ''' Compute the total score from filled-in values.

        Here is where the assigned values are multiplied by their weighting factors.

            code_quality (0-5) * 6           (30% of total points)
            scientific_concepts (0-5) * 6    (30% of total points)
            code_execution_results (0-5) * 4 (20% of total points)
            assign_completed (0-5) * 2       (10% of total points)
            follow_instructions (0-1) * 10   (10% of total points)

        Return:
            final_score (0-100)              (out of 100%)
    '''

    data = grab_form_data()

    code_quality = float(data['code_qual']) * 6
    scientific_concepts = float(data['sci_conc']) * 6
    code_execution_results = float(data['execution']) * 4
    assign_completed = float(data['completed']) * 2
    follow_instructions = float(data['follow_inst']) * 10

    final_score = sum([code_quality, scientific_concepts,
                       code_execution_results, assign_completed,
                       follow_instructions])

    return final_score 


def save_grade():
    ''' Save the data to a text file.
    '''
    data = grab_form_data()
    final_score = compute_final_score()
    final_mark = score2mark(score=final_score)

    if data['feedback'] != '':
        feedback = f"\nFeedback:\n{data['feedback']}\n\n"
    else:
        feedback = ''

    show_entry_fields()

    with open(f"{data['name']}.txt", "w") as text_file:
        text_file.write(f"Student:                                    {data['name']}\n")
        text_file.write(f"Assignment:                                 {data['assignment']}\n")
        text_file.write(f"Code Quality (x6):                          {data['code_qual']}\n")
        text_file.write(f"Scientific & Scholarly Concepts Score (x6): {data['sci_conc']}\n")
        text_file.write(f"Code Execution & Results Score (x4):        {data['execution']}\n")
        text_file.write(f"Assignment Completed Score(x2):             {data['completed']}\n")
        text_file.write(f"Followed Instructions Score (x10):          {data['follow_inst']}\n\n")
        text_file.write(f"{feedback}")
        text_file.write(f"Total Points: {final_score}\n")
        text_file.write(f"Final Mark:   {final_mark}")


def grab_form_data():
    ''' Grad values from the filled out form.

        Variables:
            student_name (tkinter.Entry)
            assignment (tkinter.Entry)
            code_quality (tkinter.Entry)
            scientific_concepts (tkinter.Entry)
            code_execution_results (tkinter.Entry)
            assign_completed (tkinter.Entry)
            follow_instructions_yes (tkinter.IntVar)
            follow_instructions_partially (tkinter.IntVar)
            personalize_text (tkinter.Text)

    '''
    data_dict = {}

    data_dict['name'] = student_name.get()
    data_dict['assignment'] = assignment_form.get()
    data_dict['code_qual'] = float(code_quality_form.get())
    data_dict['sci_conc'] = float(scientific_concepts_form.get())
    data_dict['execution'] = float(code_execution_results_form.get())
    data_dict['completed'] = float(assign_completed_form.get())

    if (follow_instructions_yes.get() == 1) and (follow_instructions_partially.get() == 1):
        sys.exit('ERROR: both instruction buttons cannot be checked at the same time.')
    elif (follow_instructions_yes.get() == 1) and (follow_instructions_partially.get() == 0):
        data_dict['follow_inst'] = 1
    elif (follow_instructions_yes.get() == 0) and (follow_instructions_partially.get() == 1):
        data_dict['follow_inst'] = 0.5
    elif (follow_instructions_yes.get() == 0) and (follow_instructions_partially.get() == 0):
        data_dict['follow_inst'] = 0.0

    data_dict['feedback'] = personalize_text.get("1.0", "end-1c")

    return data_dict


def read_saved_file(my_file):

    clear_form()

    data_dict = {}
    import re
    # print('KNK', read_file.get())
    # my_file = read_file.get()

    # my_file = read_file.get()
    # print('KNK', type(my_file), my_file)
    e = open(my_file, 'r')

    for line in e:
        if "Student:" in line:
            name = line.split()
            data_dict['name'] = name[-1]

        elif "Assignment:" in line:
            assignment = line.split()
            assignment = assignment[1:]
            data_dict['assignment'] = ' '.join(assignment)

        elif "Code Quality (x6):" in line:
            code_quality = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            data_dict['code_qual'] = code_quality[-1]

        elif "Scientific & Scholarly Concepts Score (x6):" in line:
            scientific_concepts = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            data_dict['sci_conc'] = scientific_concepts[-1]

        elif "Code Execution & Results Score (x4):" in line:
            code_execution_results = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            data_dict['execution'] = code_execution_results[-1]

        elif "Assignment Completed Score(x2):" in line:
            assign_completed = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            data_dict['completed'] = assign_completed[-1]

        elif "Followed Instructions Score (x10):" in line:
            follow_inst = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            if follow_inst[-1] == '1':
                follow_instructions_yes.set('1')
            elif follow_inst[-1] == '0.5':
                follow_instructions_partially.set('1')

    e.close()

    with open(my_file) as infile:
        copy = False
        for line in infile:
            my_line = line.strip().split()
            # print(my_line)
            if (len(my_line) > 0) and (my_line[0] == "Feedback:"):
                copy = True
                continue
            elif (len(my_line) > 0) and (my_line[0] == "Total"):
                copy = False
                continue
            elif copy:
                if len(my_line) > 0:
                    personalize_text.insert(END, f"{' '.join(my_line)}\n")

    student_name.insert(END, data_dict['name'])
    assignment_form.insert(END, data_dict['assignment'])
    code_quality_form.insert(END, data_dict['code_qual'])
    scientific_concepts_form.insert(END, data_dict['sci_conc'])
    code_execution_results_form.insert(END, data_dict['execution'])
    assign_completed_form.insert(END, data_dict['completed'])

    # return data_dict
 


def callback():
    read_file = filedialog.askopenfilename()

    if read_file:
    # Read and print the content (in bytes) of the file.
        print(read_file, type(read_file))
        read_saved_file(my_file = read_file)


def clear_form():
    student_name.delete(0, END)
    assignment_form.delete(0, END)
    code_quality_form.delete(0, END)
    scientific_concepts_form.delete(0, END)
    code_execution_results_form.delete(0, END)
    assign_completed_form.delete(0, END)
    personalize_text.delete('1.0', END)
    follow_instructions_yes.set('0')
    follow_instructions_partially.set('0')


my_color = '#FFD1AA'
window = tkinter.Tk()
window.configure(bg=my_color)

window.title("SciPro23WS: Homework Grading")

window.rowconfigure(0, minsize=20)

Label(window, text="Student Name", background=my_color).grid(row=1, column=0)
Label(window, text="Assignment", background=my_color).grid(row=2, column=0)

student_name = tkinter.Entry(window)
assignment_form = tkinter.Entry(window)

student_name.grid(row=1, column=1)
assignment_form.grid(row=2, column=1)

window.rowconfigure(3, minsize=20)

my_row = 4
quality_dict_1 = {"Unacceptable": 0, "Poor": 1, "Sufficient": 2, "Average": 3, "Good": 4, "Excellent": 5}
completion_dict_1 = {"0%": 0, "1-25%": 1, "26-50%": 2, "51-75%": 3, "77-99%": 4, "100%": 5}

Label(window, text="CATAGORY", background=my_color, padx=10, pady=0).grid(row=my_row, column=0)

for column_num, (key, value) in enumerate(quality_dict_1.items()):
    column_num += 1
    Label(window, text=key, background=my_color, padx=10, pady=0).grid(row=my_row, column=column_num)
    Label(window, text=value, background=my_color, padx=10, pady=0).grid(row=my_row+1, column=column_num)

my_row = my_row + column_num

Label(window, text='1. Code Quality', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
code_quality_form = tkinter.Entry(window, textvariable=StringVar())
code_quality_form.grid(row=my_row, column=1)

my_row += 1

Label(window, text='2. Scientific & Scholarly Concepts', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
scientific_concepts_form = tkinter.Entry(window)
scientific_concepts_form.grid(row=my_row, column=1)

my_row += 1
window.rowconfigure(my_row, minsize=20)

my_row += 1

for column_num, (key, value) in enumerate(completion_dict_1.items()):
    column_num += 1
    Label(window, text=key, background=my_color, padx=10, pady=0).grid(row=my_row, column=column_num)
    Label(window, text=value, background=my_color, padx=10, pady=0).grid(row=my_row+1, column=column_num)

my_row = my_row + column_num

Label(window, text='3. Code Execution & Correct Results', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
code_execution_results_form = tkinter.Entry(window)
code_execution_results_form.grid(row=my_row, column=1)

my_row += 1

Label(window, text='4. Assignment Completed', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
assign_completed_form = tkinter.Entry(window)
assign_completed_form.grid(row=my_row, column=1)

my_row += 1
window.rowconfigure(my_row, minsize=20)

my_row += 1

Label(window, text="5. Following Instructions", background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
follow_instructions_yes = IntVar()
follow_instructions_partially = IntVar()
tkinter.Checkbutton(window, text="Yes", background=my_color, variable=follow_instructions_yes, onvalue=1, offvalue=0).grid(row=my_row, column=1)
tkinter.Checkbutton(window, text="Partially", background=my_color, variable=follow_instructions_partially, onvalue=1, offvalue=0).grid(row=my_row, column=2)

my_row += 1
window.rowconfigure(my_row, minsize=20)

my_row += 1

scrollbar = Scrollbar(window, orient='vertical')
scrollbar.grid(row=my_row, column=2, sticky='NSW')

personalize_text = Text(window, height=10, width=60, wrap=WORD, yscrollcommand=scrollbar.set, background='#86DAFE')
personalize_text.grid(row=my_row, column=0, columnspan=2, padx=10, pady=0, sticky=tkinter.E)

scrollbar.config(command=personalize_text.yview)

my_row += 1
window.rowconfigure(my_row, minsize=20)

my_row += 1
Label(window, text="Read File", background=my_color).grid(row=my_row, column=0)
read_file = tkinter.Entry(window)
read_file.grid(row=my_row, column=1)
Button(window, text='Read', command=read_saved_file).grid(row=my_row, column=2, pady=8)
Button(text='Click to Open File', command=callback).grid(row=my_row, column=3, pady=8)

my_row += 1
window.rowconfigure(my_row, minsize=10)

my_row += 1
Button(window, text='Quit', command=window.quit).grid(row=my_row, column=0, pady=8)
Button(window, text='Display', command=show_entry_fields).grid(row=my_row, column=1, pady=8)
Button(window, text='Save', command=save_grade).grid(row=my_row, column=2, pady=8)
Button(window, text='Clear', command=clear_form).grid(row=my_row, column=4, pady=8)


## For quick testing
## assign default values
# for line in range(1, 10): 
#     personalize_text.insert(END, f"Number {str(line)}\n")
# student_name.insert(END, "John")
# assignment.insert(END, "Assignment 1")
# code_quality.insert(END, f"4")
# scientific_concepts.insert(END, f"4")
# code_execution_results.insert(END, f"4")
# assign_completed.insert(END, f"4")
# follow_instructions_yes.set('1')

window.mainloop()