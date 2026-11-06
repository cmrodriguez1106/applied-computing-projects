'''
Name: Chris Rodriguez
Date: 11/15/2021
Description: A Basic Calculator App
'''
from tkinter import *

# Create the frame for the calculator
def calculate(source, side):
    storeObj = Frame(source, borderwidth=5, bd=5, bg='light blue')
    storeObj.pack(side=side, expand =YES, fill =BOTH)
    return storeObj

# Create a button
def push_button(source, side, text, command=None):
    storeObj = Button(source, text=text, command=command)
    storeObj.pack(side=side, expand = YES, fill=BOTH)
    return storeObj

class app(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.option_add('*Font', 'calibri 20 bold')
        self.pack(expand = YES, fill =BOTH)
        self.master.title('My Calculator App')

        # Create the Display Widget
        display = StringVar()
        Entry(self, relief=RIDGE, textvariable=display,
        justify='right'
        , bd=30, bg='light blue').pack(side=TOP,
                                        expand=YES, fill=BOTH)
        
        # Create the Clear Button Widget
        for clearButton in (['C']):
            erase = calculate(self, TOP)
            for ichar in clearButton:
                push_button(erase, LEFT, ichar, lambda
                storeObj=display, q=ichar: storeObj.set(''))
        
        # Create Numbers and Symbols Widget
        for numButton in ('789/', '456*', '123-', '0.+'):
            FunctionNum =calculate(self, TOP)
            for iEquals in numButton:
                push_button(FunctionNum, LEFT, iEquals, lambda
                    storeObj=display, q=iEquals: storeObj
                        .set(storeObj.get() + q))

        # Create the Equal Button
        EqualButton = calculate(self, TOP)
        for iEquals in '=':
            if iEquals == '=':
                btniEquals = push_button(EqualButton, LEFT, iEquals)
                btniEquals.bind('<ButtonRelease-1>', lambda e,s=self,
                                storeObj=display: s.compute(storeObj), '+')
            else:
                btniEquals = push_button(EqualButton, LEFT, iEquals,
                                    lambda storeObj=display, s=' %s ' % iEquals: storeObj.set
                                    (storeObj.get() + s))
    # Apply Event Trigger on Widgets
    def compute(self, display):
        try:
            display.set(eval(display.get()))
        except:
            display.set('ERROR')
    
# Start the GUI
if __name__=='__main__':
    app().mainloop()
