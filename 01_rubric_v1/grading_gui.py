import bisect
import csv
import tkinter

from tkinter import (Button, Checkbutton, END, Entry, filedialog, HORIZONTAL,
                     IntVar, Label, Scrollbar, StringVar, Text, WORD)


def show_entry_fields():
    ''' Print to screen the values of the filled in fields and
            the computed final score and mark.
    '''

    data = grab_form_data()

    final_score = compute_final_score()
    final_mark = score2mark(score=final_score)

    print(f"Student Name:                         {data['name']}\n"
          f"Assignment:                           {data['assignment']}\n"
          f"Code Quality (x6):                    {data['code_qual']}\n"
          f"Scientific & Scholarly Concepts (x6): {data['sci_conc']}\n"
          f"Code Execution & Results (x4):        {data['execution']}\n"
          f"Assignment Completed (x2):            {data['completed']}\n"
          f"Followed Instructions (x10):          {data['follow_inst']}\n\n"
          f"Feedback:\n{data['Feedback']}\n"
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

    # if data['Feedback'] != '':
    #     feedback = f"{data['Feedback']}\n\n"
    # else:
    #     feedback = ''

    show_entry_fields()

    feedback = repr(data['Feedback'])

    with open(f"{data['name']}.csv", "w") as text_file:
        text_file.write(f"Student,{data['name']}\n")
        text_file.write(f"Assignment,{data['assignment']}\n")
        text_file.write(f"Code Quality (x6),{data['code_qual']}\n")
        text_file.write(f"Scientific & Scholarly Concepts Score (x6),{data['sci_conc']}\n")
        text_file.write(f"Code Execution & Results Score (x4),{data['execution']}\n")
        text_file.write(f"Assignment Completed Score (x2),{data['completed']}\n")
        text_file.write(f"Followed Instructions Score (x10),{data['follow_inst']}\n\n")
        text_file.write(f"Feedback,{feedback}\n")
        text_file.write(f"Total Points,{final_score}\n")
        text_file.write(f"Final Mark,{final_mark}")


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

    data_dict['Feedback'] = personalize_text.get("1.0", tkinter.END)

    return data_dict


# def read_saved_file(my_file):

#     clear_form()

#     data_dict = {}
#     import re
#     # print('KNK', read_file.get())
#     # my_file = read_file.get()

#     # my_file = read_file.get()
#     # print('KNK', type(my_file), my_file)
#     e = open(my_file, 'r')

#     for line in e:
#         if "Student:" in line:
#             name = line.split()
#             data_dict['name'] = name[-1]

#         elif "Assignment:" in line:
#             assignment = line.split()
#             assignment = assignment[1:]
#             data_dict['assignment'] = ' '.join(assignment)

#         elif "Code Quality (x6):" in line:
#             code_quality = re.findall(r"[-+]?\d*\.\d+|\d+", line)
#             data_dict['code_qual'] = code_quality[-1]

#         elif "Scientific & Scholarly Concepts Score (x6):" in line:
#             scientific_concepts = re.findall(r"[-+]?\d*\.\d+|\d+", line)
#             data_dict['sci_conc'] = scientific_concepts[-1]

#         elif "Code Execution & Results Score (x4):" in line:
#             code_execution_results = re.findall(r"[-+]?\d*\.\d+|\d+", line)
#             data_dict['execution'] = code_execution_results[-1]

#         elif "Assignment Completed Score(x2):" in line:
#             assign_completed = re.findall(r"[-+]?\d*\.\d+|\d+", line)
#             data_dict['completed'] = assign_completed[-1]

#         elif "Followed Instructions Score (x10):" in line:
#             follow_inst = re.findall(r"[-+]?\d*\.\d+|\d+", line)
#             if follow_inst[-1] == '1':
#                 follow_instructions_yes.set('1')
#             elif follow_inst[-1] == '0.5':
#                 follow_instructions_partially.set('1')

#     e.close()

#     with open(my_file) as infile:
#         copy = False
#         for line in infile:
#             my_line = line.strip().split()
#             # print(my_line)
#             if (len(my_line) > 0) and (my_line[0] == "Feedback:"):
#                 copy = True
#                 continue
#             elif (len(my_line) > 0) and (my_line[0] == "Total"):
#                 copy = False
#                 continue
#             elif copy:
#                 if len(my_line) > 0:
#                     personalize_text.insert(END, f"{' '.join(my_line)}\n")

#     student_name.insert(END, data_dict['name'])
#     assignment_form.insert(END, data_dict['assignment'])
#     code_quality_form.insert(END, data_dict['code_qual'])
#     scientific_concepts_form.insert(END, data_dict['sci_conc'])
#     code_execution_results_form.insert(END, data_dict['execution'])
#     assign_completed_form.insert(END, data_dict['completed'])

#     # return data_dict
 

def read_csv(my_file):

    clear_form()

    data_dict = {}

    with open(my_file) as infile:
        data_dict = dict(filter(None, csv.reader(infile, quotechar="'")))

    student_name.insert(END, data_dict['Student'])
    assignment_form.insert(END, data_dict['Assignment'])
    code_quality_form.insert(END, data_dict['Code Quality (x6)'])
    scientific_concepts_form.insert(END, data_dict['Scientific & Scholarly Concepts Score (x6)'])
    code_execution_results_form.insert(END, data_dict['Code Execution & Results Score (x4)'])
    assign_completed_form.insert(END, data_dict['Assignment Completed Score (x2)'])

    if data_dict['Followed Instructions Score (x10)'] == '1':
        follow_instructions_yes.set('1')
    elif data_dict['Followed Instructions Score (x10)'] == '0.5':
        follow_instructions_partially.set('1')

    feedback_txt = bytes(str(data_dict['Feedback']), 'utf-8').decode("unicode_escape")
    personalize_text.insert(END, f"{feedback_txt}")


def open_file_browser():
    ''' Open browser box for reading in data.
    '''

    read_file = filedialog.askopenfilename()

    if read_file:
        # read_saved_file(my_file=read_file)
        read_csv(my_file=read_file)


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


## Grading values
quality_dict_1 = {"Unacceptable": 0, "Poor": 1, "Sufficient": 2, "Average": 3, "Good": 4, "Excellent": 5}
completion_dict_1 = {"0%": 0, "1-25%": 1, "26-50%": 2, "51-75%": 3, "77-99%": 4, "100%": 5}

my_color = '#FFD1AA'

window = tkinter.Tk()
window.configure(bg=my_color)
window.title("Grading Scheme: 5 Catagories")

grading_frame = tkinter.Frame(window, bg=my_color)
grading_frame.grid(row=0, column=0, pady=8)

buttonframe = tkinter.Frame(window, bg=my_color)

## Fill in grading frame
my_row = 0
grading_frame.rowconfigure(my_row, minsize=20)

my_row += 1
Label(grading_frame, text="Instructions: Fill in form, or ", background=my_color).grid(row=my_row, column=0)
# Button(grading_frame, text='Open File', command=read_saved_data).grid(row=my_row, column=1, pady=8)
Button(grading_frame, text='Open File', command=open_file_browser).grid(row=my_row, column=1, pady=8)

my_row += 1
Label(grading_frame, text="Student Name", background=my_color).grid(row=my_row, column=0)
student_name = tkinter.Entry(grading_frame)
student_name.grid(row=my_row, column=1)

my_row += 1
Label(grading_frame, text="Assignment", background=my_color).grid(row=my_row, column=0)
assignment_form = tkinter.Entry(grading_frame)
assignment_form.grid(row=my_row, column=1)

my_row += 1
grading_frame.rowconfigure(my_row, minsize=20)

my_row += 1
Label(grading_frame, text="GRADING CATAGORY", background=my_color, padx=10, pady=0).grid(row=my_row, column=0)

for column_num, (key, value) in enumerate(quality_dict_1.items()):
    column_num += 2
    Label(grading_frame, text=key, background=my_color, padx=10, pady=0).grid(row=my_row, column=column_num)
    Label(grading_frame, text=value, background=my_color, padx=10, pady=0).grid(row=my_row+1, column=column_num)

my_row = my_row + column_num

Label(grading_frame, text='1. Code Quality', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
code_quality_form = tkinter.Entry(grading_frame, textvariable=StringVar())
code_quality_form.grid(row=my_row, column=1)

my_row += 1
Label(grading_frame, text='2. Scientific & Scholarly Concepts', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
scientific_concepts_form = tkinter.Entry(grading_frame)
scientific_concepts_form.grid(row=my_row, column=1)

my_row += 1
grading_frame.rowconfigure(my_row, minsize=20)

my_row += 1
for column_num, (key, value) in enumerate(completion_dict_1.items()):
    column_num += 2
    Label(grading_frame, text=key, background=my_color, padx=10, pady=0).grid(row=my_row, column=column_num)
    Label(grading_frame, text=value, background=my_color, padx=10, pady=0).grid(row=my_row+1, column=column_num)

my_row = my_row + column_num

Label(grading_frame, text='3. Code Execution & Correct Results', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
code_execution_results_form = tkinter.Entry(grading_frame)
code_execution_results_form.grid(row=my_row, column=1)

my_row += 1
Label(grading_frame, text='4. Assignment Completed', background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
assign_completed_form = tkinter.Entry(grading_frame)
assign_completed_form.grid(row=my_row, column=1)

my_row += 1
grading_frame.rowconfigure(my_row, minsize=20)

my_row += 1
Label(grading_frame, text="5. Following Instructions", background=my_color, padx=10, pady=0).grid(row=my_row, column=0)
follow_instructions_yes = IntVar()
follow_instructions_partially = IntVar()
tkinter.Checkbutton(grading_frame, text="Yes", background=my_color, variable=follow_instructions_yes, onvalue=1, offvalue=0).grid(row=my_row, column=1)
tkinter.Checkbutton(grading_frame, text="Partially", background=my_color, variable=follow_instructions_partially, onvalue=1, offvalue=0).grid(row=my_row, column=2)

my_row += 1
grading_frame.rowconfigure(my_row, minsize=20)

my_row += 1
Label(grading_frame, text="Personalized Feedback", background=my_color, padx=10, pady=0).grid(row=my_row, column=0, columnspan=2)

my_row += 1
scrollbar = Scrollbar(grading_frame, orient='vertical')
scrollbar.grid(row=my_row, column=2, sticky='NSW')

personalize_text = Text(grading_frame, height=10, width=79, wrap=WORD, yscrollcommand=scrollbar.set, background='#86DAFE')
personalize_text.grid(row=my_row, column=0, columnspan=2, padx=10, pady=0, sticky=tkinter.E)

scrollbar.config(command=personalize_text.yview)

## Fill in button frame
my_row += 1
buttonframe.grid(row=my_row, column=0, pady=0)

my_row += 1
Button(buttonframe, text='Display', command=show_entry_fields).grid(row=my_row, column=0, padx=8, pady=8)
Button(buttonframe, text='Save', command=save_grade).grid(row=my_row, column=1, padx=8, pady=8)
Button(buttonframe, text='Clear', command=clear_form).grid(row=my_row, column=2, padx=8, pady=8)

my_row += 1
Button(buttonframe, text='Quit', command=grading_frame.quit).grid(row=my_row, column=1, pady=8)

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

grading_frame.mainloop()