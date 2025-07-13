from tkinter import filedialog

def get_group_photo_path(self):
        file_path = filedialog.askopenfilename(title="Select Group Photo", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

def main():
    get_group_photo_path()
if __name__ == "__main__":
    main()