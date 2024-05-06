import tkinter as tk
from tkinter import messagebox

import numpy as np
from PIL import Image, ImageTk

import requests
from io import BytesIO
import random
import math


class Umamusume:
    def __init__(self, master):
        self.master = master
        self.master.title("别玩赛马娘")
        self.master.geometry("1000x600")

        self.current_balance = 100000 # 起始金额
        self.recharge_count = 5  # 充值次数限制

        self.umas = [
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
        self.selected_uma = tk.StringVar()
        self.selected_uma.set(self.umas[0]["name"])

        self.umaRank = self.geneRank()
        self.startPage()

    def startPage(self):
        self.enterPage()

    def enterPage(self):
        start_frame = tk.Frame(self.master)
        start_frame.pack(pady=20)
        # 这边是进入页面
        img_url = "https://pic.imgdb.cn/item/660683c59f345e8d03eee46b.png"
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img = ImageTk.PhotoImage(img.resize((300, 450)))
        img_label = tk.Label(start_frame, image=img)
        img_label.image = img
        img_label.grid(row=0, column=0, padx=10)

        enter_button = tk.Button(start_frame, text="进  入", command=self.betPage)
        enter_button.grid(row=1, column=0, pady=10)

        # 右侧文本讲解规则
        rules_text = """唉，玩赛马娘玩的\n\n
        需要了解一下规则！\n
        1. 选择您想要投注的马匹。\n
        2. 输入您想要投注的金额。\n
        3. 点击“投注”按钮进行投注。\n
        4. 人气排名越高的马获胜概率越大，但是赔率会相应低！\n
        5. 前五名都能获得奖金！排名越高赔率越高。\n
        6. 若投注的赛马获胜，奖金为投注金额×人气赔率×排名赔率\n
        7. 可以为赛马应援，越贵的应援礼物越能提高赛马胜率！\n
        8. 您的初始金额为100,000元。\n
        9. 如果您的余额不足以进行投注，您将无法进行投注！\n\n
        祝您好运！"""
        rules_label = tk.Label(start_frame, text=rules_text, justify="left", font="幼圆")
        rules_label.grid(row=0, column=1, padx=10)

    def betPage(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.geometry("600x600")

        # 创建滚动条
        scrollbar = tk.Scrollbar(self.master)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建可滚动的Frame
        race_frame_canvas = tk.Canvas(self.master, width=600, height=1050, yscrollcommand=scrollbar.set)
        race_frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=race_frame_canvas.yview)

        race_frame = tk.Frame(race_frame_canvas)  # 放置内容的框架

        race_frame_canvas.create_window((0, 0), window=race_frame, anchor="nw")

        def _on_mousewheel(event):
            race_frame_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        race_frame_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        for i, uma in enumerate(self.umas):
            uma_name = uma["name"]
            uma_image_url = uma["image_url"]
            tk.Label(race_frame, text=uma_name).grid(row=i, column=0, padx=10, pady=5)
            image = self.getImage(uma_image_url)
            label = tk.Label(race_frame, image=image)
            label.image = image
            label.grid(row=i, column=3, padx=10, pady=5)
            tk.Label(race_frame, text=uma_name).grid(row=i, column=0, padx=10, pady=5)
            tk.Label(race_frame, text=f"人气排名: {self.umaRank[uma_name]['rank']}").grid(row=i, column=1,
                                                                                          padx=10, pady=5)
            tk.Label(race_frame, text=f"赔率: {self.umaRank[uma_name]['popularity']:.1f}").grid(row=i,
                                                                                                column=2,
                                                                                                padx=10,
                                                                                                pady=5)
            tk.Radiobutton(race_frame, text="", variable=self.selected_uma, value=uma_name).grid(row=i,
                                                                                                 column=4,
                                                                                                 padx=10,
                                                                                                 pady=5)

        tk.Label(race_frame, text="投注金额:").grid(row=len(self.umas), column=0, padx=10, pady=5)
        tk.Entry(race_frame, textvariable=self.bet_amount).grid(row=len(self.umas), column=1, padx=10,
                                                                pady=5)
        tk.Button(race_frame, text="投注", command=self.betMoney).grid(row=len(self.umas), column=2, padx=10,
                                                                       pady=5)
        tk.Button(race_frame, text="退出游戏", command=self.quitGame).grid(row=len(self.umas), column=3,
                                                                           padx=10, pady=5)
        tk.Button(race_frame, text="充值", command=self.recharge).grid(row=len(self.umas), column=4, padx=10,
                                                                       pady=5)
        tk.Button(race_frame, text="应援", command=self.supportPage).grid(row=len(self.umas), column=5, padx=10, pady=5)
        self.balance_label = tk.Label(race_frame, text=f"当前金额: {self.current_balance}元")
        self.balance_label.grid(row=len(self.umas) + 1, column=0, columnspan=2, padx=10, pady=5)
        self.recharge_label = tk.Label(race_frame, text=f"剩余充值次数: {self.recharge_count}")
        self.recharge_label.grid(row=len(self.umas) + 1, column=2, columnspan=2, padx=10, pady=5)
        # self.balance_label = tk.Label(race_frame, text=f"当前金额: {self.current_balance}元")
        # self.balance_label.grid(row=len(self.umas) + 1, column=0, columnspan=2, padx=10, pady=5)

        # 更新Canvas的scrollregion，以便滚动条能够正常工作
        race_frame.update_idletasks()
        race_frame_canvas.config(scrollregion=race_frame_canvas.bbox("all"))

    def quitGame(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.geometry("400x400")
        # 显示一张图片和用户获得的奖金数量
        img_url = "https://pic.imgdb.cn/item/66091c079f345e8d037b098e.gif"  # 替换为你想要显示的图片的URL
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img = ImageTk.PhotoImage(img.resize((300, 300)))
        img_label = tk.Label(self.master, image=img)
        img_label.image = img
        img_label.pack(pady=20)

        tk.Label(self.master, text=f"游戏结束！您获得的奖金数量为: {self.current_balance - 100000}元").pack(pady=10)

    def betMoney(self):
        uma_name = self.selected_uma.get()
        bet_amount = self.bet_amount.get()

        if bet_amount > self.current_balance:
            messagebox.showerror("错误", "当前金额不足以进行此次投注！\n游戏结束！")
            return

        if uma_name:
            self.current_balance -= bet_amount
            self.balance_label.config(text=f"当前金额: {self.current_balance}元")

            # winners = random.sample([uma["name"] for uma in self.umas], 5)
            # 原来为随机生成，现在为加权生成
            winners = self.generate_winners()

            if uma_name in winners:
                uma_index = winners.index(uma_name) + 1
                payout_multiplier = 2.0 - (0.2 * (uma_index - 1))
                prize_money = bet_amount * self.umaRank[uma_name]['popularity'] * payout_multiplier
                self.current_balance += prize_money
                self.balance_label.config(text=f"当前金额: {self.current_balance}元")
                messagebox.showinfo("恭喜", f"您的马 {uma_name} 获得了第{uma_index}名，获得奖金: {prize_money:.2f}元")
            else:
                messagebox.showinfo("遗憾", f"您的马 {uma_name} 没有获得奖金")

            messagebox.showinfo("比赛结果", f"获胜马匹: {', '.join(winners)}")
        else:
            messagebox.showinfo("提示", "请选择要投注的马匹！")

    def geneRank(self):
        umaRank = {}
        available_ranks = list(range(1, 19))
        for uma in self.umas:
            rank = random.choice(available_ranks)
            available_ranks.remove(rank)
            popularity = 0.8 + (rank - 1) * 0.2
            umaRank[uma["name"]] = {'rank': rank, 'popularity': popularity}
        return umaRank

    def getImage(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((40, 40), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img

    def generate_winners(self):
        # 根据马的人气排名值加权随机生成获胜马匹列表
        winners = []
        uma_probabilities = []
        for uma in self.umas:
            uma_name = uma["name"]
            popularity = self.umaRank[uma_name]['popularity']
            # 将概率值的倒数作为随机抽取的权重
            uma_probabilities.append(1 / popularity)
        total_weight = sum(uma_probabilities)
        count = 0
        # 根据权重随机选择获胜马匹
        while count < 5 :
            winner_index = np.random.choice(len(self.umas),p=[weight / total_weight for weight in uma_probabilities])
            if self.umas[winner_index]["name"] not in winners:
               winners.append(self.umas[winner_index]["name"])
               count += 1
        return winners

    def recharge(self):
        if self.recharge_count > 0:
            self.current_balance += 20000
            self.recharge_count -= 1
            messagebox.showinfo("充值成功", f"充值成功，当前金额增加20000元。\n剩余充值次数: {self.recharge_count}")
            self.balance_label.config(text=f"当前金额: {self.current_balance}元")
            self.recharge_label.config(text=f"剩余充值次数: {self.recharge_count}")
        else:
            messagebox.showinfo("充值失败", "您的充值次数已用完，无法再进行充值。")

    # 新增应援页面
    def supportPage(self):
        support_window = tk.Toplevel(self.master)
        uma_select = self.selected_uma.get()
        support_window.title("选择应援道具")

        support_items = [
            {"name": "赛马嘉年华", "price": 3000, "image_url": "https://pic.imgdb.cn/item/661924d168eb935713ad6f5c.png"},
            {"name": "赛马一号", "price": 1500, "image_url": "https://pic.imgdb.cn/item/661955d968eb935713f19727.png"},
            {"name": "小马玩偶", "price": 1000, "image_url": "https://pic.imgdb.cn/item/6619261468eb935713aff0b1.png"},
            {"name": "应援棒", "price": 500, "image_url": "https://pic.imgdb.cn/item/6619569268eb935713f2c041.png"}
        ]

        selected_item = tk.StringVar()
        selected_item.set(support_items[0]["name"])

        for item in support_items:
            frame = tk.Frame(support_window)
            frame.pack(pady=5)
            tk.Radiobutton(frame, variable=selected_item, value=item['name']).pack(side=tk.LEFT)
            label = tk.Label(frame, text=f"{item['name']} - 价格: {item['price']}元")
            label.pack(side=tk.LEFT, padx=5)
            image = self.getImage(item["image_url"])
            img_label = tk.Label(frame, image=image)
            img_label.image = image
            img_label.pack(side=tk.LEFT)

        def support():
            selected = selected_item.get()
            for item in support_items:
                if item["name"] == selected:
                    if self.current_balance >= item["price"]:
                        self.current_balance -= item["price"]
                        self.balance_label.config(text=f"当前金额: {self.current_balance}元")
                        messagebox.showinfo("应援成功", f"{uma_select}对您表示感谢,会加油的哟！")
                        # Displaying the image
                        img_url = "https://pic.imgdb.cn/item/661951cd68eb935713ece2fd.png"
                        response = requests.get(img_url)
                        img = Image.open(BytesIO(response.content))
                        img = ImageTk.PhotoImage(img.resize((216, 267)))
                        img_label = tk.Label(support_window, image=img)
                        img_label.image = img
                        img_label.pack(pady=10)
                        support_window.update()  # Ensure the window is updated to display the image
                        return
                    else:
                        messagebox.showerror("金额不足", "您的余额不足以购买此道具！")
                        return

        tk.Button(support_window, text="确认支持", command=support).pack(pady=10)

        support_window.mainloop()


def main():
    root = tk.Tk()
    app = Umamusume(root)
    root.mainloop()


if __name__ == "__main__":
    main()
