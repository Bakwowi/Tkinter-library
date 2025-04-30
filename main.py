#team_Bakwowi_Ramez_Eneh
#Bakwowi: junior.bakwowi@stud.th-deg.de
#Ramez: ramez.ayad@stud.th-deg.de
#Eneh: frank.eneh@stud.th-deg.de


import ttkbootstrap as tb
from view import ViewClass
from controller import LibController
# import time



def main():
    root = tb.Window(themename="darkly")
    view = ViewClass(root)
    LibController(view)
    
    root.mainloop()


#Entry point of the script
if __name__ == "__main__":
    #If the script is run directly, execute the main function
    main()
else:
    #If the script is imported as a module, print an error message
    print("Sorry. An error has occurred. Unable to launch the library")



