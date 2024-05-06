import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import requests
from io import BytesIO
import random


class Umamusume:
    def __init__(self, master):
        self.master = master
        self.master.title("玩赛马娘玩的")
        self.master.geometry("500x500")  # 调整窗口大小

        self.canvas = tk.Canvas(master)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.on_frame_configure)

        # 用户初始金额，100000！
        self.initial_balance = 100000
        self.current_balance = self.initial_balance

        # 马匹名称和图片文件路径
        self.horses = [
            {"name": "特别周", "image_url": "https://pic.imgdb.cn/item/66067b9c9f345e8d03c5ee66.png"},
            {"name": "草上飞", "image_url": "https://pic.imgdb.cn/item/66067da19f345e8d03cfcb9f.png"},
            {"name": "东海帝王", "image_url": "https://pic.imgdb.cn/item/66067bc39f345e8d03c6aa16.png"},
            {"name": "神鹰", "image_url": "https://pic.imgdb.cn/item/66067d099f345e8d03ccdc9c.png"},
            {"name": "好歌剧", "image_url": "https://pic.imgdb.cn/item/66067be89f345e8d03c744bc.png"},
            {"name": "圣王光环", "image_url": "https://pic.imgdb.cn/item/66067d519f345e8d03ce34eb.png"},
            {"name": "目白麦昆", "image_url": "https://pic.imgdb.cn/item/66067d2f9f345e8d03cd98d8.png"},
            {"name": "米浴", "image_url": "https://pic.imgdb.cn/item/66067c589f345e8d03c94c35.png"},
            {"name": "美浦波旁", "image_url": "https://pic.imgdb.cn/item/66067c3c9f345e8d03c8ba42.png"},
            {"name": "名将怒涛", "image_url": "https://pic.imgdb.cn/item/66067c139f345e8d03c7ec2b.png"},
            {"name": "爱丽数码", "image_url": "https://pic.imgdb.cn/item/66067d7e9f345e8d03cf1501.png"},
            {"name": "超级小海湾", "image_url": "https://pic.imgdb.cn/item/66067cf09f345e8d03cc6653.png"},
            {"name": "鲁道夫象征", "image_url": "https://pic.imgdb.cn/item/66067ca49f345e8d03cae244.png"},
            {"name": "黄金船", "image_url": "https://pic.imgdb.cn/item/66067cce9f345e8d03cbc49c.png"},
            {"name": "成田路", "image_url": "https://pic.imgdb.cn/item/66067e019f345e8d03d1a032.png"},
            {"name": "丸善斯基", "image_url": "https://pic.imgdb.cn/item/66067c7f9f345e8d03ca1b06.png"},
            {"name": "青云天空", "image_url": "https://pic.imgdb.cn/item/66067b769f345e8d03c53589.png"},
            {"name": "小栗帽", "image_url": "https://pic.imgdb.cn/item/66067b439f345e8d03c43525.png"},
        ]
        self.bet_amount = tk.DoubleVar()
        self.selected_horse = tk.StringVar()
        self.selected_horse.set(self.horses[0]["name"])  # 默认选中第一匹马

        self.horse_ranking = self.geneRanking()  # 生成初始的马匹排名
        self.infoAndBet()

    def infoAndBet(self):
        # 显示马匹信息和投注控件
        for i, horse in enumerate(self.horses):
            horse_name = horse["name"]
            horse_image_url = horse["image_url"]
            tk.Label(self.frame, text=horse_name).grid(row=i, column=0, padx=10, pady=5)
            # 获取图片并显示
            image = self.getImage(horse_image_url)
            label = tk.Label(self.frame, image=image)
            label.image = image
            label.grid(row=i, column=3, padx=10, pady=5)
            tk.Label(self.frame, text=f"人气排名: {self.horse_ranking[horse_name]['rank']}").grid(row=i, column=1, padx=10, pady=5)
            tk.Label(self.frame, text=f"人气倍率: {self.horse_ranking[horse_name]['popularity']:.1f}").grid(row=i, column=2, padx=10, pady=5)
            # 按钮用于选择投注的马匹
            tk.Radiobutton(self.frame, text="", variable=self.selected_horse, value=horse_name).grid(row=i, column=4, padx=10, pady=5)

        # 显示当前金额
        self.balance_label = tk.Label(self.frame, text=f"当前金额: {self.current_balance}元")
        self.balance_label.grid(row=len(self.horses) + 1, column=0, columnspan=5, padx=10, pady=5)

        # 投注输入框和按钮
        tk.Label(self.frame, text="投注金额:").grid(row=len(self.horses) + 2, column=0, padx=10, pady=5)
        tk.Entry(self.frame, textvariable=self.bet_amount).grid(row=len(self.horses) + 2, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="投注", command=self.betNum).grid(row=len(self.horses) + 2, column=2, padx=10, pady=5)

    def betNum(self):
        # 获取用户投注的马匹和金额
        horse_name = self.selected_horse.get()
        bet_amount = self.bet_amount.get()

        # 检查用户的当前金额是否足够进行投注
        if bet_amount > self.current_balance:
            messagebox.showerror("错误", "您的当前金额不足以进行此次投注！")
            return

        if horse_name:
            # 更新当前金额
            self.current_balance -= bet_amount
            self.balance_label.config(text=f"当前金额: {self.current_balance}元")

            # 生成比赛结果
            winners = random.sample([horse["name"] for horse in self.horses], 5)

            # 判断用户是否投注的马匹获胜
            if horse_name in winners:
                # 计算奖金
                horse_index = winners.index(horse_name) + 1
                payout_multiplier = 2.0 - (0.2 * (horse_index - 1))
                prize_money = bet_amount * self.horse_ranking[horse_name]['popularity'] * payout_multiplier
                # 更新当前金额
                self.current_balance += prize_money
                self.balance_label.config(text=f"当前金额: {self.current_balance}元")
                messagebox.showinfo("恭喜！",f"您的马 {horse_name} 获得了第{horse_index}名，获得奖金: {prize_money:.2f}元")
            else:
                messagebox.showinfo("遗憾！", f"您的马 {horse_name} 没有获得奖金,下次加油哦~")

            # 显示比赛结果
            messagebox.showinfo("比赛结果", f"获胜马匹: {', '.join(winners)}")
        else:
            messagebox.showinfo("提示", "请选择要投注的马匹！")

    def geneRanking(self):
        horse_ranking = {}
        available_ranks = list(range(1, 19))
        for horse in self.horses:
            rank = random.choice(available_ranks)
            available_ranks.remove(rank)
            popularity = 0.8 + (rank - 1) * 0.2
            horse_ranking[horse["name"]] = {'rank': rank, 'popularity': popularity}
        return horse_ranking

    def getImage(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((40, 40), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def main():
    root = tk.Tk()
    app = Umamusume(root)
    root.mainloop()


if __name__ == "__main__":
    main()
