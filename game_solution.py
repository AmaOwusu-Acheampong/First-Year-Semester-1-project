#importing tkinter and other necessary for the game
import tkinter as tk
from tkinter import PhotoImage
import random
import pickle
from tkinter import messagebox
from tkinter import simpledialog
import json

#creating the window
froggy_window = tk.Tk()
froggy_window.geometry("1000x1000")
froggy_window.title("Froggy Froggy Stuck In A Pond")
froggy_window.resizable(width=False,height=False)
button_canvas_image=PhotoImage(file="frameimage.png")
button_canvas=tk.Canvas(width=1000,height=1000,)


#icon for window
icon = PhotoImage(file="froggy.png")
froggy_window.iconphoto(True, icon)
froggy_window.config(background="black")

#canvas background creation  
backgroung_image_froggy=PhotoImage(file="froggy_canvas.backgroung.png")

froggy_canvas = tk.Canvas(froggy_window, width=1000, height=1000, bg="black", highlightthickness=0)
froggy_canvas.create_image(0,0,anchor=tk.NW,image=backgroung_image_froggy)

froggy_canvas.pack()
#game over
image_for_game_over=PhotoImage(file="game_over.png")
game_over_label_1=tk.Label(froggy_window,image=image_for_game_over )

#image for help
image_for_help =PhotoImage(file="help_froggy.png")
help_label=tk.Label(froggy_window,image=image_for_help)


#start labels
start_message_label = tk.Label(froggy_window, text=" Froggy Froggy !", font=("Arial", 32), fg="white", bg="black")
start_message_label.place(x=200,y=10)
bombbys=[]    

#count time and score variables
your_score = 0
countdown_of_time = 30
bomb_initial_speed = 5
score_label = None
countdown_label =None
score_label = None
countdown_label = None

#fruit definitions
fruits = []
fruit_initial_speed = 3

#frog components creation
frog_components = []
frog_x = 100
frog_y = 680

#save button
save_file="saved_game.pkl"
user_data={}
game_paused=False


#previous game 
def go_to_previous_page():
    """
    takes you to the previous page
    """
    froggy_canvas.pack_forget()
    game_over_label_1.place_forget()
    score_label.place_forget()
    pause_game_button.place_forget()
    previous_page_button.place_forget()
    save_buttom.place(relx=0.8, rely=0.2, anchor="center", height=70, width=300)
    load_button.place(relx=0.8, rely=0.35, anchor="center", height=70, width=300)   
    countdown_label.place_forget()
    
    
    start_game_button.place(relx=0.3,rely=0.2,anchor="center", height=70 ,width=300)
    help_button.place(relx=0.8,rely=0.5,anchor="center",height=70, width=300)
    continue_button.place(relx=0.3,rely=0.35,anchor="center",height=70, width=300)
    leaderboard_button.place(relx=0.30,rely=0.5,anchor="center",height=70,width=300)


previous_page_button = tk.Button(froggy_window, text="Back", command=go_to_previous_page)



# Save game
def save_game():
    """
    Used to save the game
    """
    global your_score, countdown_of_time, bombbys, fruits, bomb_initial_speed, user_data

    user_name = simpledialog.askstring("Input", "Enter name:")
    if user_name:
        if user_name in user_data:
            # Update existing user data
            user_data[user_name]["score"] = your_score
            user_data[user_name]["time"] = countdown_of_time
            user_data[user_name]["bombs"] = bombbys[:]
            user_data[user_name]["fruits"] = fruits[:]
            user_data[user_name]["bomb_speed"] = bomb_initial_speed
        else:
            # Create new user data
            user_data[user_name] = {
                "score": your_score,
                "time": countdown_of_time,
                "bombs": bombbys[:],
                "fruits": fruits[:],
                "bomb_speed": bomb_initial_speed,
            }

        with open(save_file, "wb") as f:  
            pickle.dump(user_data, f)

#load game
def load_game():
    """
    Used to  load the saved game
    """
    
    global your_score, countdown_of_time, bombbys, fruits, bomb_initial_speed
    try:
        with open(save_file, 'rb') as f:
            loaded_data=pickle.load(f)  
    except FileNotFoundError:
        messagebox.showinfo("Error", "No saved game found.")
        return
    if not loaded_data:
       messagebox.showinfo("Oh Oh .No Saved Game!!")
       return
    user_name=simpledialog.askstring("Input","Enter the name your name here:")
    if user_name in loaded_data:
        data = loaded_data[user_name]
        
        your_score = data["score"]
        countdown_of_time = data["time"]
        bombbys = data["bombs"][:]
        fruits = data["fruits"][:]
        bomb_initial_speed = data["bomb_speed"]
        game_paused=False
        start_game()
        hide_buttons()
    else:
        messagebox.showinfo("Error", "No saved game found for the username inputted.Try again .")
    start_message_label.place_forget()
save_buttom=tk.Button(froggy_window,text="Save Game",command=save_game,font="Roman,16",padx=10,pady=20,bg="white",fg="green",bd=6,relief=tk.GROOVE,highlightbackground="green",highlightcolor="green")
load_button=tk.Button(froggy_window,text="Load Game",command=load_game,font="Roman,16",padx=10,pady=20,bg="white",fg="green",bd=6,relief=tk.GROOVE,highlightbackground="green",highlightcolor="green")
save_buttom.place(relx=0.8, rely=0.2, anchor="center", height=70, width=300)
load_button.place(relx=0.8, rely=0.35, anchor="center", height=70, width=300)   

#functions to pause and resume game
def pause_game():
    """
    Used to pause the game
    """
    
    global game_paused
    game_paused=True

def resume_game():
    """
    Used to resume game
    """
    
    global game_paused,move_frog
    game_paused=False
    move_the_fruit()
    move_the_bomb()
    move_frog()
    update_time()
def pause_resume_game():
    """
    used to pause and resume the game
    """
    global game_paused
    if game_paused:
        resume_game()
        pause_game_button.config(text="Pause Game")
        
    else:
        pause_game()
        pause_game_button.config(text="Resume Game")
         
pause_game_button=tk.Button(froggy_window,text="pause/Resume Game",command=pause_resume_game)

#creating game elements

def create_bomb():
   """
   used to create the bombs
   """
   
   def is_too_close(new_bomb_coords, existing_bombs_coords, min_distance):
    for existing_bomb_coords in existing_bombs_coords:
            distance = ((new_bomb_coords[0] + new_bomb_coords[2]) / 2 - (existing_bomb_coords[0] + existing_bomb_coords[2]) / 2) ** 2 + \
((new_bomb_coords[1] + new_bomb_coords[3]) / 2 - (existing_bomb_coords[1] + existing_bomb_coords[3]) / 2) ** 2
            distance = distance ** 0.5
            if distance < min_distance:
             return True
    return False

   if all(froggy_canvas.coords(bomb)[3] > 90 for bomb, _ in bombbys):
        for _ in range(4):
            while True:
                x = random.randint(3, 900)
                y = 40
                new_bomb_coords = [x, y, x + 50, y + 50]

                if not is_too_close(new_bomb_coords, [froggy_canvas.coords(bomb) for bomb, _ in bombbys], min_distance=100):
                    break

            bomb = froggy_canvas.create_oval(new_bomb_coords, fill="red", outline="yellow")
            bomb_body = froggy_canvas.create_line(x + 25, y, x + 25, y - 20, width=3, fill="green")
            bombbys.append((bomb, bomb_body)) 


def create_fruits():
   """
   used to create the fruits
   """
    
   x = random.randint(3, 900)
   
   y = 40
   radius = 14
   fruit_body = froggy_canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="green", outline="dark red")
   stem_height = 5
   stem_width = 3
   fruit_stem = froggy_canvas.create_rectangle(x - stem_width / 2, y - radius - stem_height, x + stem_width / 2, y - radius, fill="brown")

   return fruit_body, fruit_stem

#checking fruit collision
def check_fruit_collision():
    """
    Used to ckeck the collision with fruits
    """
    global your_score
    frog_coords = froggy_canvas.coords(frog_components[0])

    for fruit in fruits:
        fruit_coords = froggy_canvas.coords(fruit[0])
        if (fruit_coords[0] < frog_coords[2] and fruit_coords[2] > frog_coords[0] ):
            froggy_canvas.delete(fruit[0])
            
            fruits.remove(fruit)
            update_score()

#moving the fruit function
def move_the_fruit():
    """
    move the fruits
    """
    global countdown_of_time
    if not game_paused and countdown_of_time>0:
     global fruit_initial_speed
     fruits_to_be_removed = []

     for fruit in fruits:
        froggy_canvas.move(fruit[0], 0, fruit_initial_speed)
        froggy_canvas.move(fruit[1], 0, fruit_initial_speed)

        fruit_coords = froggy_canvas.coords(fruit[0])
        frog_coords = froggy_canvas.coords(frog_components[0])

        if (
            fruit_coords[0] < frog_coords[2] and fruit_coords[2] > frog_coords[0] and
            fruit_coords[1] < frog_coords[3] and fruit_coords[3] > frog_coords[1]
        ):
            fruits_to_be_removed.append(fruit)
            update_score()

        if fruit_coords[3] > 1000:
            fruits_to_be_removed.append(fruit)

     for fruit in fruits_to_be_removed:
        froggy_canvas.delete(fruit[0])
        froggy_canvas.delete(fruit[1])
        fruits.remove(fruit)

     if len(fruits) < 2:
        for man in range(2 - len(fruits)):
            new_fruit = create_fruits()
            fruits.append(new_fruit)     

    froggy_window.after(100, move_the_fruit)
    
#creating the frog
def whole_froggy_body(x, y):
    """
    The frog body parts canvas creation
    """
    
    
    froggy_body = froggy_canvas.create_oval(x, y, x + 100, y + 100, fill="green", outline="")
    froggy_leg_left = froggy_canvas.create_line(x + 20, y + 80, x + 20, y + 100, width=6, fill="yellow")
    froggy_leg_right = froggy_canvas.create_line(x + 80, y + 80, x + 80, y + 100, width=5, fill="yellow")
    froggy_eye1 = froggy_canvas.create_oval(x + 30, y + 30, x + 50, y + 50, fill="white")
    froggy_eye2 = froggy_canvas.create_oval(x + 70, y + 30, x + 90, y + 50, fill="white")
    pupil1 = froggy_canvas.create_oval(x + 40, y + 40, x + 45, y + 45, fill="black")
    pupil2 = froggy_canvas.create_oval(x + 80, y + 40, x + 85, y + 45, fill="black")
    froggy_smile = froggy_canvas.create_arc(x + 40, y + 60, x + 90, y + 80, start=-30, extent=60, style=tk.ARC)

    return [froggy_body, froggy_leg_left, froggy_leg_right, froggy_eye1, froggy_eye2, pupil1, pupil2, froggy_smile]

#function for frog
def update_score():
    """
    updating the score
    """
    
    global your_score,score_label
    your_score+=3
    score_label.config(text="Your current score: {}".format(your_score))
    
#checking collision between the bomb
def check_collision():
    """
    checks collision
    """
   
    global countdown_of_time
    if countdown_of_time==0:
     frog_coords = froggy_canvas.coords(frog_components[0])

     for bomb, todd in bombbys:
        bomb_coords = froggy_canvas.coords(bomb)
        if (bomb_coords[0] < frog_coords[2] and bomb_coords[2] > frog_coords[0] and bomb_coords[1] < frog_coords[3] and bomb_coords[3] > frog_coords[1]):
            if not game_over_label_1.winfo_ismapped():
             game_over_label_1.place(x=700, y=700)  
             
             

             score_saver()
            
           
#moving the bomb            
bomb_horizontal_direction = 5

# Update move_the_bomb function
def move_the_bomb():
    """
    moves the frog
    """
    global your_score
    global countdown_of_time
    global bomb_initial_speed
    global bomb_horizontal_direction

    if not game_paused and countdown_of_time>0:
       

        bombs_to_be_removed = []
        for bomb, bomb_body in bombbys:
            froggy_canvas.move(bomb, bomb_horizontal_direction / bomb_initial_speed, bomb_initial_speed)
            froggy_canvas.move(bomb_body, bomb_horizontal_direction / bomb_initial_speed, bomb_initial_speed)

            bomb_coords = froggy_canvas.coords(bomb)
            frog_coords = froggy_canvas.coords(frog_components[0])

            if (
                bomb_coords[0] < frog_coords[2] and bomb_coords[2] > frog_coords[0] and bomb_coords[1] < frog_coords[3] and
                bomb_coords[3] > frog_coords[1]
            ):
                countdown_of_time -= 10
                bombs_to_be_removed.append((bomb, bomb_body))
                check_collision()

            if bomb_coords[3] > 1000:
                bombs_to_be_removed.append((bomb, bomb_body))

            # Check if bomb hits left or right edge, then change direction
            if bomb_coords[0] <= 0 or bomb_coords[2] >= 1000:
                bomb_horizontal_direction *= -1

        for bomb, bomb_body in bombs_to_be_removed:
            bombbys.remove((bomb, bomb_body))
            froggy_canvas.delete(bomb)
            froggy_canvas.delete(bomb_body)
            create_bomb()

        if your_score >= 5 and your_score % 10 == 0:
            bomb_initial_speed += 1
            

        

             

    froggy_window.after(100, move_the_bomb)
#moving the frog 
def move_frog(event=None):
    """
    key binding
    """
    
    global frog_x, frog_y
    if event is not None:
     if event.keysym == 'Right' and frog_x < 900:
        frog_x += 10
     elif event.keysym == 'Left' and frog_x > 0:
        frog_x -= 10
     elif event.keysym == 'Up' and frog_y > 40:
        frog_y -= 10
     elif event.keysym == 'Down' and frog_y < 650:
        frog_y += 10

     update_frog_position()
    
     check_collision()

#updating the time
def update_time():
    """
    updating the time
    """
   
    if not game_paused:
     global countdown_of_time
     countdown_label.config(text=" Your Remaining Time left: {} seconds".format(countdown_of_time))
     if countdown_of_time > 0:
        froggy_window.after(50, update_time)
     else:
        game_over_label_1.place(x=0, y=0)

#updating frog position
def update_frog_position():
    """
    updating frog position
    """
    
    global frog_components
    for component in frog_components:
        froggy_canvas.delete(component)

    frog_components = whole_froggy_body(frog_x, frog_y)

#starting the game
def start_game():
    """
    starting the game
    """
   
    global frog_x, frog_y, frog_components, your_score, countdown_of_time, bombbys, fruits, bomb_initial_speed,score_label,countdown_label
    for bomb ,bomb_body in bombbys:
       froggy_canvas.delete(bomb)
       froggy_canvas.delete(bomb_body)

    for component in frog_components:
        froggy_canvas.delete(component)
    for fruit in fruits:
        froggy_canvas.delete(fruit[0])
        froggy_canvas.delete(fruit[1])
    frog_x = 100
    frog_y = 680
    frog_components = whole_froggy_body(frog_x, frog_y)

    your_score = 0
    countdown_of_time = 30
    bombbys = []
    fruits = []
    bomb_initial_speed = 2

    score_label=tk.Label(froggy_window,text="Your current score: {}".format(your_score),font="Arial",fg="black")
    score_label.place(x=10,y=10)
    countdown_label=tk.Label(froggy_window,text=" Your Remaining Time left: {} seconds".format(countdown_of_time),font="Arial",fg="black")
    countdown_label.place(x=200,y=10)
    create_bomb()
    start_message_label.place_forget()
    for man in range(2):
        fruit_eaten = create_fruits()
        fruits.append(fruit_eaten)

    froggy_window.bind('<Up>', move_frog)
    froggy_window.bind('<Down>', move_frog)
    froggy_window.bind('<Left>', move_frog)
    froggy_window.bind('<Right>', move_frog)
    froggy_canvas.pack()
    froggy_window.after(100, check_fruit_collision)
    froggy_window.after(100, move_the_fruit)
    froggy_window.after(100, move_the_bomb)
    froggy_window.after(50, update_time)
    pause_game_button.place(x=500,y=10) 
    start_game_button.place_forget()
    previous_page_button.place(x=700, y=10)
    
    
#help,continue and leadership functions
def help():
    """
    help function
    """
   
    help_label.place(x=0,y=30)
    froggy_canvas.place_forget()
    hide_buttons()
    help_button_2.place(x=0,y=0)
def go_back():
    
    froggy_canvas.place_forget()
    start_game_button.place(relx=0.3,rely=0.2,anchor="center", height=70 ,width=300)
    help_button.place(relx=0.8,rely=0.5,anchor="center",height=70, width=300)
    continue_button.place(relx=0.3,rely=0.35,anchor="center",height=70, width=300)
    leaderboard_button.place(relx=0.30,rely=0.5,anchor="center",height=70,width=300)  
    save_buttom.place(relx=0.8, rely=0.2, anchor="center", height=70, width=300)
    load_button.place(relx=0.8, rely=0.35, anchor="center", height=70, width=300) 
    help_label.place_forget()
    help_button_2.place_forget()
    

help_button_2=tk.Button(froggy_window,text="Back",command=go_back,font="Roman,36",bg="white",fg="green",highlightbackground="green",highlightcolor="green")    
# contine
def continue_game():
   """
   used to continue the game
   """
   froggy_window.quit()
#leadership board
# Add a canvas for the leaderboard in froggy_window

def go_back_from_leader():
    """
    go back from leader board
    """
    global start_game_button,help_button,leaderboard_button,save_buttom,load_button,continue_button
    leaderboard_canvas.place_forget()
    start_game_button.place(relx=0.3,rely=0.2,anchor="center", height=70 ,width=300)
    help_button.place(relx=0.8,rely=0.5,anchor="center",height=70, width=300)
    continue_button.place(relx=0.3,rely=0.35,anchor="center",height=70, width=300)
    leaderboard_button.place(relx=0.30,rely=0.5,anchor="center",height=70,width=300)
    froggy_canvas.place_forget()
    back_button.place_forget()
    save_buttom.place(relx=0.8, rely=0.2, anchor="center", height=70, width=300)
    load_button.place(relx=0.8, rely=0.35, anchor="center", height=70, width=300) 
back_button=tk.Button(text="back",command=go_back_from_leader)


def score_saver():
  """
  saves scores
  """
  user_name=simpledialog.askstring("input your name","whats your name")
  with open("myleader.json","r") as f:
         
      leader=json.load(f)
  
  leader.append([user_name,your_score])
  sortedlist=sorted(leader,key=lambda x:x[1],reverse=True)
      
  with open("myleader.json", "w") as f:
        json.dump(sortedlist, f)    

def update_leaderboard_canvas():
    """
    updates leader canvas
    """
    global leaderboard_text
    # Load leaderboard data from the file
    try:
        with open("myleader.json", "r") as f:
            leaderboard_data = json.load(f)
    except FileNotFoundError:
        leaderboard_data = []

    # Create a formatted string to display on the canvas
    leaderboard_text = "Leaderboard\n\n"
    for i, (name, score) in enumerate(leaderboard_data[:10], start=1):
        leaderboard_text += f"{i}. {name}: {score}\n"

    
leaderboard_canvas = tk.Canvas(froggy_window, width=1000, height=800, bg="black", highlightthickness=0)

def leadership_thingy():
    """
    leadeship board fuction
    """
    
    global user_data,froggy_canvas
    
    back_button.place(x=0,y=0)
    leaderboard_button.place_forget()
    start_game_button.place_forget()
    load_button.place_forget()
    help_button.place_forget()
    save_buttom.place_forget()   
    continue_button.place_forget()     
    
    update_leaderboard_canvas()
    leaderboard_canvas.create_text(10, 10, anchor="nw", text=leaderboard_text, font=("Arial", 16), fill="white")
    leaderboard_canvas.place(x=0,y=20)




#fuction to hide the buttons
def hide_buttons():
    """
    hide buttons for boss key
    """
    
    help_button.place_forget()
    continue_button.place_forget()
    leaderboard_button.place_forget()
    save_buttom.place_forget()
    load_button.place_forget()
    leaderboard_button.place_forget()
    start_game_button.place_forget()
    start_message_label.place_forget()
def hide_buttons2():
    """
    hide buttons
    """
    help_button.place_forget()
    continue_button.place_forget()
    leaderboard_button.place_forget()
    save_buttom.place_forget()
    load_button.place_forget()
    leaderboard_button.place_forget()

help_button=tk.Button(froggy_window,text="Help",command=help,font="Roman,36",padx=20,pady=50,bg="white",fg="green",bd=6,relief=tk.GROOVE,highlightbackground="green",highlightcolor="green")

start_game_button = tk.Button(froggy_window, text="Start Game", command=start_game,font="Roman,36",padx=20,pady=50,bg="white",fg="green",bd=6,relief=tk.GROOVE,highlightbackground="green",highlightcolor="green")

continue_button=tk.Button(froggy_window,text="Quit Game",command=continue_game,font="Roman,36",padx=20,pady=50,bg="white",fg="green",bd=6,relief=tk.GROOVE,highlightbackground="green",highlightcolor="green")

start_game_button.bind("<Button-1>",lambda event: hide_buttons2())
leaderboard_button=tk.Button(froggy_window,text="Leader Board",command=leadership_thingy,font="Roman,36",padx=20,pady=50,bg="white",fg="green",bd=6,relief=tk.GROOVE,highlightbackground="green",highlightcolor="green")

start_game_button.place(relx=0.3,rely=0.2,anchor="center", height=70 ,width=300)
help_button.place(relx=0.8,rely=0.5,anchor="center",height=70, width=300)
continue_button.place(relx=0.3,rely=0.35,anchor="center",height=70, width=300)
leaderboard_button.place(relx=0.30,rely=0.5,anchor="center",height=70,width=300)


#boss key
boss_key_image=PhotoImage(file="boss_key_google.png")
boss_key_canvas=tk.Canvas(froggy_window,width=1000,height=1000,background="black",highlightthickness=0)
boss_key_canvas.create_image(0,0,anchor=tk.NW,image=boss_key_image)
boss_key_canvas.pack_forget()
boss_key_active=False

#boss key fuction 
     
def boss_key(event):
  """
  boss key fuction
  """
   
  global boss_key_active
  boss_key_active=not boss_key_active
  
  if boss_key_active :
     if game_paused is False:
        pause_game()
     froggy_canvas.pack_forget()
     boss_key_canvas.place(x=0,y=0)
     
  else:
     froggy_canvas.pack()
     boss_key_canvas.place_forget()

froggy_window.bind("<Escape>", boss_key)

#the cheat function
def cheat():
    """
    cheat function
    """
   
    global your_score,score_label
    
    your_score += 100  
    score_label.config(text="Your current score: {}".format(your_score))


froggy_window.bind("<space>", lambda event: cheat())
 



   

 

    





 
froggy_window.mainloop()
