import tkinter as tk
import winsound


class DuckPiano:
    def __init__(self, master):
        self.master = master
        self.master.title("鸭鸭のpiano")

        self.key_button_map = {
            'Q': 'C3', 'W': 'D3', 'E': 'E3', 'R': 'F3', 'T': 'G3', 'Y': 'A3', 'U': 'B3',
            'A': 'C4', 'S': 'D4', 'D': 'E4', 'F': 'F4', 'G': 'G4', 'H': 'A4', 'J': 'B4',
            'Z': 'C5', 'X': 'D5', 'C': 'E5', 'V': 'F5', 'B': 'G5', 'N': 'A5', 'M': 'B5'
        }

        self.key_buttons = []
        self.pianoKeys()
        self.entry()
        self.playMusic()
        self.frequencyButton()
        self.addInstructions()

        # 绑定键盘事件
        self.master.bind('<KeyPress>', self.playSoundFromKeyboard)

    def playSoundFromKeyboard(self, event):
        # 检查按下的按键是否在映射表中
        if event.char.upper() in self.key_button_map:
            # 获取相应的音符
            note = self.key_button_map[event.char.upper()]
            # 播放声音
            self.playSound(note)

    def pianoKeys(self):
        for key, note in self.key_button_map.items():
            button = tk.Button(self.master, text=note, width=5, height=10, command=lambda k=note: self.playSound(k), bg="#f0f0f0")
            button.grid(row=0, column=list(self.key_button_map.keys()).index(key))
            self.key_buttons.append(button)

    def entry(self):
        self.entry_var = tk.StringVar()
        entry = tk.Entry(self.master, textvariable=self.entry_var, width=50)
        entry.grid(row=1, column=0, columnspan=len(self.key_buttons), pady=10)

    def playMusic(self):
        play_button = tk.Button(self.master, text="播放您输入的音符串", command=self.playInputMusic, bg="#39C5BB",fg="#002fa7") # 初音色+克莱因蓝
        play_button.grid(row=2, column=0, columnspan=len(self.key_buttons), pady=10)

    def playSound(self, key):
        frequency = self.calFrequency(key)
        winsound.Beep(int(frequency), 500)

    def calFrequency(self, key):
        base_frequency = 261.63  # C4的频率
        notes = {'C3': -21, 'D3': -19, 'E3': -17, 'F3': -16, 'G3': -14, 'A3': -12, 'B3': -10,
                 'C4': 0, 'D4': 2, 'E4': 4, 'F4': 5, 'G4': 7, 'A4': 9, 'B4': 11,
                 'C5': 12, 'D5': 14, 'E5': 16, 'F5': 17, 'G5': 19, 'A5': 21, 'B5': 23}
        return base_frequency * (2 ** (notes[key] / 12))

    def playInputMusic(self):
        music_notes = self.entry_var.get().split('/')
        for note in music_notes:
            if note:
                duration, key = note[:-2], note[-2:]  # 从后往前分割，最后两位为音符
                frequency = self.calFrequency(key)
                winsound.Beep(int(frequency), int(float(duration) * 1000))

    def frequencyButton(self):
        frequency_button = tk.Button(self.master, text="播放0-2000hz的声音", command=self.playFrequency, bg="#39C5BB",fg="#002fa7")
        frequency_button.grid(row=3, column=0, columnspan=len(self.key_buttons), pady=10)

    def playFrequency(self):
        for frequency in range(100, 2000, 100):  # 播放频率，步长100，从100到2000，第三个是步长
            winsound.Beep(frequency, 500)  # 每个声音播放0.5秒
            # time.sleep(0.5)  # 每0.5秒播放，感觉会不会加上这个变成一秒了（

    def addInstructions(self):
        instructions = "鸭鸭提醒您记得开大写锁定~\nC3到B3对应QWERTYU\nC4到B4对应ASDFGHJ\nC5到B5对应ZXCVBNM"
        label = tk.Label(self.master, text=instructions,fg="#ffa500")
        label.grid(row=4, column=0, columnspan=len(self.key_buttons), pady=10)



def main():
    root = tk.Tk()
    app = DuckPiano(root)
    root.mainloop()


if __name__ == "__main__":
    main()
