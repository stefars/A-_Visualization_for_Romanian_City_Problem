import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Cartesian System with Origin at Center")

# Set the size of the canvas
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()


# Function to draw a point based on Cartesian coordinates (center as (0, 0))
def draw_cartesian_point(x, y):
    # Shift the origin to the center of the canvas
    center_x = canvas_width // 2
    center_y = canvas_height // 2

    # Translate the Cartesian coordinates to canvas coordinates
    canvas_x = center_x + x  # Positive X moves to the right
    canvas_y = center_y - y  # Negative Y moves down, positive Y moves up

    # Draw the point at (canvas_x, canvas_y)
    canvas.create_oval(canvas_x+2, canvas_y+2, canvas_x-2, canvas_y-2, fill="blue")
    canvas.create_text(canvas_x-10, canvas_y-10, text="Cartesian System")



# Example: Draw a point at (100, 100) in Cartesian coordinates
draw_cartesian_point(100, 100)

# Example: Draw a point at (-100, -50) in Cartesian coordinates
draw_cartesian_point(-100, -50)

# Example: Draw a point at (50, -150) in Cartesian coordinates
draw_cartesian_point(50, -150)

# Start the Tkinter event loop
root.mainloop()
