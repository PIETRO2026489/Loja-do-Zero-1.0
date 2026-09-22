import pygame
import random
import json
import os
import math
import time
from dataclasses import dataclass, field

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
FULLSCREEN = True

BLACK = (15, 17, 22)
WHITE = (245, 245, 245)
LIGHT = (200, 205, 215)
GRAY = (110, 115, 125)
DARK = (34, 38, 46)
GREEN = (55, 195, 95)
RED = (220, 60, 65)
BLUE = (60, 135, 230)
CYAN = (55, 205, 210)
YELLOW = (245, 210, 60)
ORANGE = (245, 135, 50)
PURPLE = (155, 90, 210)
PINK = (235, 100, 170)
BROWN = (150, 95, 55)
CREAM = (245, 228, 188)
WOOD = (145, 95, 50)
FLOOR = (232, 217, 184)
WALL = (238, 235, 224)
SKY = (190, 220, 235)
OUTLINE = (38, 40, 48)
MINT = (115, 220, 175)
GOLD = (247, 190, 65)

FONT = pygame.font.SysFont("arial", 20)
SMALL = pygame.font.SysFont("arial", 16)
TINY = pygame.font.SysFont("arial", 13)
BIG = pygame.font.SysFont("arial", 30, bold=True)
TITLE = pygame.font.SysFont("arial", 48, bold=True)
HUGE = pygame.font.SysFont("arial", 62, bold=True)


# ============================================================
# SAVE
# ============================================================

def safe_save_path():

    base = os.environ.get("APPDATA") or os.path.expanduser("~")

    folder = os.path.join(
        base,
        "LojaDoZero"
    )

    try:

        os.makedirs(
            folder,
            exist_ok=True
        )

    except OSError:

        folder = os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.join(
        folder,
        "loja_do_zero_save.json"
    )


SAVE_FILE = safe_save_path()


# ============================================================
# TELA
# ============================================================

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.FULLSCREEN | pygame.SCALED
)

pygame.display.set_caption(
    "Loja do Zero"
)

clock = pygame.time.Clock()


# ============================================================
# PRODUTOS
# ============================================================

PRODUCTS = {

    "apple": ("Maçã", 2.0, 4.0, 1, RED, "Hortifruti"),
    "banana": ("Banana", 1.8, 3.8, 1, YELLOW, "Hortifruti"),
    "orange": ("Laranja", 2.0, 4.2, 1, ORANGE, "Hortifruti"),
    "tomato": ("Tomate", 2.2, 4.8, 1, RED, "Hortifruti"),
    "potato": ("Batata", 2.4, 5.0, 1, BROWN, "Hortifruti"),

    "rice": ("Arroz", 5.0, 10.5, 1, WHITE, "Mercearia"),
    "beans": ("Feijão", 4.5, 9.5, 1, BROWN, "Mercearia"),
    "pasta": ("Macarrão", 3.8, 8.0, 1, CREAM, "Mercearia"),
    "flour": ("Farinha", 3.2, 7.0, 1, CREAM, "Mercearia"),
    "sugar": ("Açúcar", 3.0, 6.5, 1, WHITE, "Mercearia"),
    "salt": ("Sal", 1.2, 3.0, 1, WHITE, "Mercearia"),

    "bread": ("Pão", 2.5, 5.0, 1, CREAM, "Padaria"),

    "milk": ("Leite", 3.0, 6.0, 1, WHITE, "Frios"),
    "eggs": ("Ovos", 4.0, 8.5, 1, CREAM, "Frios"),
    "cheese": ("Queijo", 8.0, 16.0, 1, YELLOW, "Frios"),
    "yogurt": ("Iogurte", 3.5, 8.0, 1, PINK, "Frios"),

    "juice": ("Suco", 4.0, 8.5, 1, ORANGE, "Bebidas"),
    "water": ("Água", 1.5, 3.5, 1, CYAN, "Bebidas"),
    "soda": ("Refrigerante", 4.0, 9.0, 2, ORANGE, "Bebidas"),
    "coffee": ("Café", 5.5, 12.0, 2, BROWN, "Bebidas"),
    "tea": ("Chá", 4.0, 9.0, 2, GREEN, "Bebidas"),

    "cookies": ("Biscoito", 3.5, 7.5, 1, GOLD, "Doces"),
    "chips": ("Salgadinho", 3.8, 8.0, 1, ORANGE, "Lanches"),
    "chocolate": ("Chocolate", 5.0, 10.0, 2, BROWN, "Doces"),
    "cereal": ("Cereal", 6.0, 13.0, 2, GOLD, "Café da manhã"),

    "icecream": ("Sorvete", 7.0, 15.0, 2, CYAN, "Congelados"),
    "pizza": ("Pizza", 8.0, 17.0, 2, ORANGE, "Congelados"),
    "burger": ("Hambúrguer", 9.0, 19.0, 3, BROWN, "Congelados"),

    "chicken": ("Frango", 11.0, 22.0, 2, CREAM, "Carnes"),
    "meat": ("Carne", 18.0, 36.0, 2, RED, "Carnes"),

    "soap": ("Sabonete", 2.8, 6.5, 2, PINK, "Higiene"),
    "shampoo": ("Shampoo", 6.0, 13.5, 2, PURPLE, "Higiene"),
    "toothpaste": ("Pasta de Dente", 4.0, 8.5, 2, CYAN, "Higiene"),

    "detergent": ("Detergente", 3.0, 7.0, 2, CYAN, "Limpeza"),
    "paper": ("Papel Higiênico", 7.0, 15.0, 2, WHITE, "Limpeza"),

    "petfood": ("Ração", 9.0, 18.0, 2, BROWN, "Pet"),

    "headphones": ("Fone de Ouvido", 25.0, 55.0, 3, PURPLE, "Eletrônicos"),
    "console": ("Videogame", 80.0, 165.0, 3, CYAN, "Eletrônicos"),
    "smartwatch": ("Smartwatch", 70.0, 150.0, 4, CYAN, "Eletrônicos"),
    "phone": ("Celular", 120.0, 250.0, 4, BLUE, "Eletrônicos"),
    "tablet": ("Tablet", 145.0, 300.0, 4, CYAN, "Eletrônicos"),
    "gamingchair": ("Cadeira Gamer", 130.0, 280.0, 4, RED, "Eletrônicos"),
    "computer": ("Computador", 240.0, 490.0, 5, BLUE, "Eletrônicos"),
    "camera": ("Câmera", 190.0, 395.0, 5, PURPLE, "Eletrônicos"),
}

PRODUCT_ORDER = list(PRODUCTS)


# ============================================================
# FUNCIONÁRIOS
# ============================================================

EMPLOYEES = {

    "cashier":
        (
            "Caixa",
            350,
            8,
            BLUE,
            "Atende automaticamente os clientes."
        ),

    "stock":
        (
            "Repositor",
            300,
            7,
            ORANGE,
            "Repõe automaticamente produtos."
        ),

    "cleaner":
        (
            "Faxineiro",
            280,
            6,
            CYAN,
            "Mantém a loja limpa."
        ),

    "security":
        (
            "Segurança",
            650,
            12,
            RED,
            "Reduz a chance de furto."
        ),

    "manager":
        (
            "Gerente",
            900,
            18,
            PURPLE,
            "Melhora satisfação e operação."
        ),
}

EMPLOYEE_ORDER = list(EMPLOYEES)


# ============================================================
# UPGRADES
# ============================================================

UPGRADES = {

    "shelves":
        (
            "Mais prateleiras",
            120,
            8,
            "Aumenta o número de prateleiras."
        ),

    "space":
        (
            "Mais espaço",
            180,
            8,
            "Aumenta o número de clientes."
        ),

    "stock":
        (
            "Estoque maior",
            140,
            8,
            "Aumenta a capacidade de cada produto."
        ),

    "checkout":
        (
            "Caixa melhor",
            260,
            6,
            "Acelera o atendimento."
        ),

    "lights":
        (
            "Iluminação",
            150,
            6,
            "Melhora a satisfação."
        ),

    "cleaning":
        (
            "Limpeza",
            110,
            7,
            "Reduz a sujeira acumulada."
        ),

    "entrance":
        (
            "Entrada maior",
            220,
            6,
            "Atrai clientes mais rapidamente."
        ),

    "decor":
        (
            "Decoração",
            200,
            6,
            "Aumenta reputação."
        ),
}

UPGRADE_ORDER = list(UPGRADES)


# ============================================================
# PROGRESSÃO
# ============================================================

LEVEL_NAMES = {

    1: "Mercadinho",
    2: "Loja de Bairro",
    3: "Supermercado",
    4: "Mega Loja",
    5: "Loja Premium",
}

LEVEL_REVENUE = {

    1: 0,
    2: 500,
    3: 1800,
    4: 5000,
    5: 12000,
}

LEVEL_CUSTOMERS = {

    1: 3,
    2: 5,
    3: 8,
    4: 12,
    5: 18,
}

MAX_LEVEL = 5
MAX_STOCK = 50

THEFT_TIMEOUT = 20.0

PLAYER_SPEED = 190.0
CUSTOMER_SPAWN = 4.0


# ============================================================
# TIPOS DE CLIENTE
# ============================================================

CUSTOMER_TYPES = {

    "normal":
        (BLUE, 1.0, 18),

    "hurry":
        (ORANGE, 1.25, 10),

    "big":
        (GREEN, 0.85, 24),

    "cheap":
        (YELLOW, 0.95, 25),

    "family":
        (PINK, 0.78, 28),
}


# ============================================================
# EVENTOS
# ============================================================

EVENTS = {

    "promo":
        (
            "Promoção do dia",
            "Um produto está vendendo mais hoje!",
            PINK,
            30
        ),

    "rush":
        (
            "Movimento intenso",
            "A loja está cheia de clientes!",
            ORANGE,
            30
        ),

    "supplier":
        (
            "Oferta do fornecedor",
            "As compras de estoque estão mais baratas.",
            CYAN,
            30
        ),

    "happy":
        (
            "Hora feliz",
            "A satisfação aumentou temporariamente.",
            YELLOW,
            30
        ),
}


# ============================================================
# DECORAÇÕES
# ============================================================

DECORATION_ITEMS = [

    ("Planta", GREEN, 80),
    ("Tapete", RED, 140),
    ("Sofá", PURPLE, 220),
    ("Aquário", CYAN, 300),
    ("Neon", PINK, 400),
]


# ============================================================
# CLIENTE
# ============================================================

@dataclass
class Customer:

    cid: int
    kind: str
    x: float
    y: float

    state: str = "entering"

    basket: list = field(
        default_factory=list
    )

    held_items: list = field(
        default_factory=list
    )

    target_product: str = ""

    target_x: float = 120.0
    target_y: float = 200.0

    patience: float = 20.0

    checkout_wait: float = 0.0

    service_time: float = 0.0

    stolen: bool = False


# ============================================================
# LOJA
# ============================================================

class Store:

    def __init__(self):

        self.money = 100.0

        self.level = 1

        self.total_revenue = 0.0
        self.total_profit = 0.0

        self.total_sales = 0
        self.total_customers = 0

        self.customers_served = 0

        self.stolen_items = 0
        self.thefts = 0

        self.security_alerts = 0

        self.reputation = 50.0
        self.satisfaction = 85.0
        self.cleanliness = 92.0

        self.day = 1
        self.hour = 8.0

        self.inventory = {
            pid: 0
            for pid in PRODUCTS
        }

        self.unlocked = [
            pid
            for pid in PRODUCTS
            if PRODUCTS[pid][3] == 1
        ]

        for pid in self.unlocked:

            self.inventory[pid] = 6

        self.upgrades = {
            key: 0
            for key in UPGRADES
        }

        self.employees = []

        self.decorations = []

        self.active_event = None
        self.event_time = 0.0

        self.missions = {

            "first_sale": False,
            "fifty_customers": False,
            "level_3": False,
            "employee": False,
            "ten_products": False,
            "level_5": False,
        }

        self.achievements = {

            "first_customer": False,
            "100_sales": False,
            "1000_revenue": False,
            "50_customers": False,
            "first_employee": False,
            "all_products": False,
            "mega_store": False,
            "premium": False,
            "security": False,
            "big_profit": False,
        }

        self.history = []

        self.today_revenue = 0.0
        self.today_profit = 0.0
        self.today_expenses = 0.0

        self.last_autosave = 0.0

        self.carts_in_store = 8

        self.tutorial_done = False

        # Estado de cada caixa.
        # Sempre existe pelo menos um caixa manual.
        self.checkout_open = [True]


    def money_text(self):

        return (
            f"R$ {self.money:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


    def product_name(self, pid):

        return PRODUCTS[pid][0]


    def buy_price(self, pid):

        price = PRODUCTS[pid][1]

        if self.active_event == "supplier":

            price *= 0.70

        return price


    def sell_price(self, pid):

        price = PRODUCTS[pid][2]

        if (
            self.active_event == "promo"
            and pid in self.unlocked[:3]
        ):

            price *= 1.15

        return price


    def stock_limit(self):

        return (
            MAX_STOCK
            + self.upgrades["stock"] * 10
        )


    def customer_capacity(self):

        return (
            LEVEL_CUSTOMERS[self.level]
            + self.upgrades["space"]
        )


    def shelf_count(self):

        return (
            8
            + self.upgrades["shelves"] * 2
            + (self.level - 1) * 2
        )


    def spawn_speed(self):

        value = (
            1.0
            + self.upgrades["entrance"] * 0.08
        )

        if self.active_event == "rush":

            value *= 1.9

        return value


    def checkout_speed(self):

        return (
            1.0
            + self.upgrades["checkout"] * 0.08
            + self.employee_count("cashier") * 0.10
        )


    def employee_count(self, kind):

        return sum(
            e == kind
            for e in self.employees
        )


    def active_checkout_count(self):

        return sum(
            bool(v)
            for v in self.checkout_open
        )


    def ensure_checkout_slots(self):

        required = max(
            1,
            1 + self.employee_count("cashier")
        )

        required = min(
            3,
            required
        )

        while len(self.checkout_open) < required:

            self.checkout_open.append(
                True
            )

        if len(self.checkout_open) > required:

            self.checkout_open = (
                self.checkout_open[:required]
            )

        if not self.checkout_open:

            self.checkout_open = [True]


    # ========================================================
    # ESTOQUE
    # ========================================================

    def buy_stock(
        self,
        pid,
        amount
    ):

        if pid not in PRODUCTS:

            return (
                False,
                "Produto inválido."
            )

        if amount <= 0:

            return (
                False,
                "Quantidade inválida."
            )

        if (
            self.inventory[pid]
            + amount
            > self.stock_limit()
        ):

            return (
                False,
                "Limite de estoque atingido."
            )

        cost = (
            self.buy_price(pid)
            * amount
        )

        if self.money < cost:

            return (
                False,
                "Dinheiro insuficiente."
            )

        self.money -= cost

        self.inventory[pid] += amount

        self.today_expenses += cost

        self.total_profit -= cost

        return (
            True,
            f"Comprou {amount}x {self.product_name(pid)}."
        )


    # ========================================================
    # VENDAS
    # ========================================================

    def sell_one(self, pid):

        if (
            self.inventory.get(
                pid,
                0
            )
            <= 0
        ):

            return (
                False,
                0,
                0
            )

        self.inventory[pid] -= 1

        revenue = self.sell_price(pid)

        profit = (
            revenue
            - PRODUCTS[pid][1]
        )

        self.money += revenue

        self.total_revenue += revenue
        self.total_profit += profit

        self.total_sales += 1

        self.today_revenue += revenue
        self.today_profit += profit

        self.history.append(
            (
                time.time(),
                pid,
                revenue,
                profit
            )
        )

        self.history = (
            self.history[-100:]
        )

        self.check_progression()

        return (
            True,
            revenue,
            profit
        )


    # ========================================================
    # PROGRESSÃO
    # ========================================================

    def check_progression(self):

        while (
            self.level < MAX_LEVEL
            and
            self.total_revenue
            >= LEVEL_REVENUE[
                self.level + 1
            ]
        ):

            self.level += 1

            self.reputation = min(
                100,
                self.reputation + 8
            )

            unlock_products()

            self.ensure_checkout_slots()

            notify(
                f"NOVO NÍVEL: {LEVEL_NAMES[self.level]}!",
                GREEN,
                4
            )

        self.check_missions()

        self.check_achievements()


    # ========================================================
    # UPGRADES
    # ========================================================

    def upgrade_cost(self, key):

        return (
            UPGRADES[key][1]
            * (1.35 ** self.upgrades[key])
        )


    def buy_upgrade(self, key):

        if key not in UPGRADES:

            return (
                False,
                "Upgrade inválido."
            )

        if (
            self.upgrades[key]
            >= UPGRADES[key][2]
        ):

            return (
                False,
                "Esse upgrade já está no máximo."
            )

        cost = self.upgrade_cost(key)

        if self.money < cost:

            return (
                False,
                "Dinheiro insuficiente."
            )

        self.money -= cost

        self.total_profit -= cost

        self.today_expenses += cost

        self.upgrades[key] += 1

        self.satisfaction = min(
            100,
            self.satisfaction + 2
        )

        return (
            True,
            f"{UPGRADES[key][0]} melhorado!"
        )


    # ========================================================
    # FUNCIONÁRIOS
    # ========================================================

    def hire(self, kind):

        if kind not in EMPLOYEES:

            return (
                False,
                "Funcionário inválido."
            )

        (
            name,
            price,
            salary,
            color,
            description
        ) = EMPLOYEES[kind]

        max_count = (
            5
            if kind in (
                "cashier",
                "stock"
            )
            else 2
        )

        if (
            self.employee_count(kind)
            >= max_count
        ):

            return (
                False,
                "Limite desse funcionário atingido."
            )

        if self.money < price:

            return (
                False,
                "Dinheiro insuficiente."
            )

        self.money -= price

        self.total_profit -= price

        self.today_expenses += price

        self.employees.append(
            kind
        )

        self.ensure_checkout_slots()

        self.satisfaction = min(
            100,
            self.satisfaction + 3
        )

        if kind == "security":

            self.reputation = min(
                100,
                self.reputation + 2
            )

        self.check_missions()

        return (
            True,
            f"{name} contratado."
        )


    # ========================================================
    # QUALIDADE
    # ========================================================

    def update_quality(self, dt):

        cleaner = self.employee_count(
            "cleaner"
        )

        self.cleanliness += (
            dt
            * (
                0.03
                + cleaner * 0.07
                + self.upgrades["cleaning"] * 0.02
            )
        )

        self.cleanliness -= (
            dt
            * (
                0.018
                + len(customers) * 0.002
            )
        )

        self.cleanliness = max(
            0,
            min(
                100,
                self.cleanliness
            )
        )

        target = (
            62
            + self.cleanliness * 0.20
            + self.upgrades["lights"] * 2.5
            + self.upgrades["decor"] * 2
        )

        target += (
            self.employee_count("manager")
            * 3
        )

        if self.active_event == "happy":

            target += 10

        self.satisfaction += (
            target
            - self.satisfaction
        ) * dt * 0.08

        self.satisfaction = max(
            0,
            min(
                100,
                self.satisfaction
            )
        )


    # ========================================================
    # TEMPO
    # ========================================================

    def update_time(self, dt):

        self.hour += (
            dt / 20.0
        )

        if self.hour >= 23:

            self.hour = 8

            self.day += 1

            self.payroll()

            self.today_revenue = 0
            self.today_profit = 0
            self.today_expenses = 0

        self.last_autosave += dt

        if self.active_event:

            self.event_time -= dt

            if self.event_time <= 0:

                self.active_event = None

        elif random.random() < dt * 0.002:

            start_random_event()


    def payroll(self):

        total = 0

        for kind in self.employees:

            total += EMPLOYEES[kind][2]

        total *= max(
            0.7,
            1
            - self.employee_count("manager")
            * 0.04
        )

        self.money = max(
            0,
            self.money - total
        )

        self.total_profit -= total


    # ========================================================
    # MISSÕES
    # ========================================================

    def check_missions(self):

        targets = {

            "first_sale":
                self.total_sales >= 1,

            "fifty_customers":
                self.total_customers >= 50,

            "level_3":
                self.level >= 3,

            "employee":
                len(self.employees) >= 1,

            "ten_products":
                len(self.unlocked) >= 10,

            "level_5":
                self.level >= 5,
        }

        rewards = {

            "first_sale": 50,
            "fifty_customers": 150,
            "level_3": 400,
            "employee": 180,
            "ten_products": 500,
            "level_5": 1500,
        }

        for key, done in targets.items():

            if (
                done
                and
                not self.missions[key]
            ):

                self.missions[key] = True

                self.money += rewards[key]

                notify(
                    f"Missão concluída! +R$ {rewards[key]}",
                    GOLD,
                    3.5
                )


    # ========================================================
    # CONQUISTAS
    # ========================================================

    def check_achievements(self):

        conditions = {

            "first_customer":
                self.total_customers >= 1,

            "100_sales":
                self.total_sales >= 100,

            "1000_revenue":
                self.total_revenue >= 1000,

            "50_customers":
                self.total_customers >= 50,

            "first_employee":
                len(self.employees) >= 1,

            "all_products":
                len(self.unlocked)
                == len(PRODUCTS),

            "mega_store":
                self.level >= 4,

            "premium":
                self.level >= 5,

            "security":
                self.employee_count("security") >= 1,

            "big_profit":
                self.total_profit >= 5000,
        }

        for key, value in conditions.items():

            if (
                value
                and
                not self.achievements[key]
            ):

                self.achievements[key] = True

                notify(
                    f"CONQUISTA: {key.replace('_', ' ').title()}!",
                    PURPLE,
                    4
                )


    # ========================================================
    # SAVE
    # ========================================================

    def to_dict(self):

        return {

            "money":
                self.money,

            "level":
                self.level,

            "total_revenue":
                self.total_revenue,

            "total_profit":
                self.total_profit,

            "total_sales":
                self.total_sales,

            "total_customers":
                self.total_customers,

            "customers_served":
                self.customers_served,

            "stolen_items":
                self.stolen_items,

            "thefts":
                self.thefts,

            "security_alerts":
                self.security_alerts,

            "reputation":
                self.reputation,

            "satisfaction":
                self.satisfaction,

            "cleanliness":
                self.cleanliness,

            "day":
                self.day,

            "hour":
                self.hour,

            "inventory":
                self.inventory,

            "unlocked":
                self.unlocked,

            "upgrades":
                self.upgrades,

            "employees":
                self.employees,

            "decorations":
                self.decorations,

            "missions":
                self.missions,

            "achievements":
                self.achievements,

            "carts_in_store":
                self.carts_in_store,

            "tutorial_done":
                self.tutorial_done,

            "checkout_open":
                self.checkout_open,
        }


    def load(self, data):

        current = self.to_dict()

        for key in current:

            if key in data:

                setattr(
                    self,
                    key,
                    data[key]
                )

        self.level = max(
            1,
            min(
                MAX_LEVEL,
                int(self.level)
            )
        )

        self.inventory = {

            pid:
                max(
                    0,
                    int(
                        self.inventory.get(
                            pid,
                            0
                        )
                    )
                )

            for pid in PRODUCTS
        }

        self.unlocked = [

            pid
            for pid in self.unlocked

            if pid in PRODUCTS
        ]

        if not self.unlocked:

            self.unlocked = [

                pid

                for pid in PRODUCTS

                if PRODUCTS[pid][3] == 1
            ]

        unlock_products()

        self.upgrades = {

            key:
                max(
                    0,
                    min(
                        UPGRADES[key][2],
                        int(
                            self.upgrades.get(
                                key,
                                0
                            )
                        )
                    )
                )

            for key in UPGRADES
        }

        self.employees = [

            employee

            for employee in self.employees

            if employee in EMPLOYEES
        ]

        self.carts_in_store = max(
            0,
            int(
                self.carts_in_store
            )
        )

        self.reputation = max(
            0,
            min(
                100,
                float(
                    self.reputation
                )
            )
        )

        self.satisfaction = max(
            0,
            min(
                100,
                float(
                    self.satisfaction
                )
            )
        )

        self.cleanliness = max(
            0,
            min(
                100,
                float(
                    self.cleanliness
                )
            )
        )

        self.ensure_checkout_slots()


store = Store()


# ============================================================
# ESTADO GLOBAL
# ============================================================

state = "menu"

running = True

customers = []

customer_id = 0

player_x = 170.0
player_y = 485.0

carrying_cart = False

selected_product = store.unlocked[0]

last_spawn = time.monotonic()

message_queue = []

message_timer = 0


# ============================================================
# UTILIDADES
# ============================================================

def money(value):

    return (
        f"R$ {value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def text(
    surface,
    value,
    x,
    y,
    color=WHITE,
    font=FONT
):

    surface.blit(
        font.render(
            str(value),
            True,
            color
        ),
        (
            int(x),
            int(y)
        )
    )


def center_text(
    surface,
    value,
    y,
    color=WHITE,
    font=FONT
):

    rendered = font.render(
        str(value),
        True,
        color
    )

    surface.blit(
        rendered,
        (
            (
                WIDTH
                - rendered.get_width()
            ) // 2,
            int(y)
        )
    )


def panel(
    rect,
    fill=DARK,
    border=OUTLINE,
    width=2,
    radius=10
):

    pygame.draw.rect(
        screen,
        fill,
        rect,
        border_radius=radius
    )

    if width:

        pygame.draw.rect(
            screen,
            border,
            rect,
            width,
            border_radius=radius
        )


def button(
    rect,
    label,
    fill=(55, 70, 90),
    disabled=False,
    font=SMALL
):

    color = (
        (70, 72, 80)
        if disabled
        else fill
    )

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=9
    )

    pygame.draw.rect(
        screen,
        OUTLINE,
        rect,
        2,
        border_radius=9
    )

    rendered = font.render(
        label,
        True,
        LIGHT
        if disabled
        else WHITE
    )

    screen.blit(
        rendered,
        (
            rect[0]
            + (
                rect[2]
                - rendered.get_width()
            ) / 2,

            rect[1]
            + (
                rect[3]
                - rendered.get_height()
            ) / 2
        )
    )


def bar(
    x,
    y,
    width,
    height,
    value,
    maximum,
    color
):

    pygame.draw.rect(
        screen,
        (45, 48, 56),
        (x, y, width, height),
        border_radius=5
    )

    ratio = (
        0
        if maximum <= 0
        else max(
            0,
            min(
                1,
                value / maximum
            )
        )
    )

    pygame.draw.rect(
        screen,
        color,
        (
            x,
            y,
            int(width * ratio),
            height
        ),
        border_radius=5
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (
            x,
            y,
            width,
            height
        ),
        1,
        border_radius=5
    )


def notify(
    msg,
    color=YELLOW,
    seconds=3
):

    global message_timer

    message_queue.append(
        (
            msg,
            color,
            seconds
        )
    )

    del message_queue[:-5]

    message_timer = max(
        message_timer,
        seconds
    )


def draw_notifications():

    for i, (
        msg,
        color,
        seconds
    ) in enumerate(
        reversed(
            message_queue[-4:]
        )
    ):

        panel(
            (
                WIDTH - 430,
                100 + i * 52,
                400,
                42
            ),
            (25, 28, 35),
            color,
            2,
            8
        )

        text(
            screen,
            msg[:55],
            WIDTH - 415,
            112 + i * 52,
            WHITE,
            SMALL
        )


def update_notifications(dt):

    global message_queue
    global message_timer

    message_timer -= dt

    new_queue = []

    for (
        msg,
        color,
        seconds
    ) in message_queue:

        seconds -= dt

        if seconds > 0:

            new_queue.append(
                (
                    msg,
                    color,
                    seconds
                )
            )

    message_queue = new_queue


# ============================================================
# MAPA / HITBOX
# ============================================================

def store_rect():

    widths = {
        1: 900,
        2: 1010,
        3: 1100,
        4: 1170,
        5: 1210,
    }

    heights = {
        1: 440,
        2: 470,
        3: 500,
        4: 530,
        5: 555,
    }

    return pygame.Rect(
        35,
        105,
        widths[store.level],
        heights[store.level]
    )


def shelf_rects():

    """
    As prateleiras ficam somente na esquerda.
    A área direita é reservada aos caixas.
    """

    r = store_rect()

    if store.level == 1:

        cols = 4
        rows = 2

    elif store.level == 2:

        cols = 5
        rows = 2

    elif store.level == 3:

        cols = 5
        rows = 3

    elif store.level == 4:

        cols = 6
        rows = 3

    else:

        cols = 6
        rows = 4

    count = min(
        store.shelf_count(),
        cols * rows
    )

    rects = []

    start_x = (
        r.left
        + 90
    )

    start_y = (
        r.top
        + 115
    )

    spacing_x = 145
    spacing_y = 90

    checkout_zone_left = (
        r.right
        - 235
    )

    for i in range(count):

        col = i % cols
        row = i // cols

        x = start_x + col * spacing_x
        y = start_y + row * spacing_y

        rect = pygame.Rect(
            x,
            y,
            126,
            58
        )

        # Não deixa a prateleira entrar
        # no corredor dos caixas.
        if rect.right <= checkout_zone_left:

            rects.append(
                rect
            )

    return rects


def cashier_rects():

    store.ensure_checkout_slots()

    r = store_rect()

    count = min(
        3,
        len(
            store.checkout_open
        )
    )

    checkout_x = (
        r.right
        - 165
    )

    checkout_y = (
        r.top
        + 110
    )

    return [

        pygame.Rect(
            checkout_x,
            checkout_y + i * 105,
            125,
            72
        )

        for i in range(count)
    ]


def cart_area():

    r = store_rect()

    return pygame.Rect(
        r.x + 20,
        r.bottom - 85,
        115,
        52
    )


def player_rect(
    x=None,
    y=None
):

    px = (
        player_x
        if x is None
        else x
    )

    py = (
        player_y
        if y is None
        else y
    )

    return pygame.Rect(
        int(px - 14),
        int(py - 14),
        28,
        28
    )


def can_walk(
    x,
    y
):

    r = store_rect()

    player = player_rect(
        x,
        y
    )

    # --------------------------------------------------------
    # LIMITES EXTERNOS
    # --------------------------------------------------------

    if player.left < r.left + 18:

        return False

    if player.right > r.right - 18:

        return False

    if player.top < r.top + 88:

        return False

    if player.bottom > r.bottom - 18:

        return False

    # --------------------------------------------------------
    # PRATELEIRAS
    # --------------------------------------------------------

    for obstacle in shelf_rects():

        if player.colliderect(
            obstacle.inflate(
                5,
                5
            )
        ):

            return False

    # --------------------------------------------------------
    # CAIXAS
    # --------------------------------------------------------

    for obstacle in cashier_rects():

        if player.colliderect(
            obstacle.inflate(
                5,
                5
            )
        ):

            return False

    return True


def find_free_player_position():

    r = store_rect()

    positions = [

        (
            r.left + 140,
            r.bottom - 55
        ),

        (
            r.left + 180,
            r.bottom - 55
        ),

        (
            r.left + 250,
            r.bottom - 55
        ),

        (
            r.left + 360,
            r.bottom - 55
        ),

        (
            r.right - 300,
            r.bottom - 70
        ),

        (
            r.right - 250,
            r.top + 400
        ),

        (
            r.right - 250,
            r.top + 300
        ),
    ]

    for x, y in positions:

        if can_walk(
            x,
            y
        ):

            return (
                float(x),
                float(y)
            )

    return (
        float(
            r.left + 140
        ),
        float(
            r.bottom - 55
        )
    )


def reset_player_position():

    global player_x
    global player_y

    (
        player_x,
        player_y
    ) = find_free_player_position()


def move_player(
    dx,
    dy,
    dt
):

    global player_x
    global player_y

    if (
        dx == 0
        and
        dy == 0
    ):

        return

    length = math.hypot(
        dx,
        dy
    )

    if length:

        dx /= length
        dy /= length

    amount = (
        PLAYER_SPEED
        * dt
    )

    # Eixo X
    new_x = (
        player_x
        + dx
        * amount
    )

    if can_walk(
        new_x,
        player_y
    ):

        player_x = new_x

    # Eixo Y
    new_y = (
        player_y
        + dy
        * amount
    )

    if can_walk(
        player_x,
        new_y
    ):

        player_y = new_y


# ============================================================
# PRODUTOS / PRATELEIRAS
# ============================================================

def unlock_products():

    for pid in PRODUCT_ORDER:

        if (
            PRODUCTS[pid][3]
            <= store.level
            and
            pid not in store.unlocked
        ):

            store.unlocked.append(
                pid
            )

            store.inventory.setdefault(
                pid,
                0
            )

            notify(
                "Novo produto: "
                + PRODUCTS[pid][0],
                CYAN,
                2
            )


def shelf_product(
    index
):

    if not store.unlocked:

        return "apple"

    return store.unlocked[
        index
        % len(store.unlocked)
    ]


def shelf_for_product(
    pid
):

    shelves = shelf_rects()

    for index, product in enumerate(
        store.unlocked
    ):

        if (
            index < len(shelves)
            and
            product == pid
        ):

            return shelves[index]

    if shelves:

        return shelves[0]

    return pygame.Rect(
        200,
        250,
        100,
        60
    )


def draw_product_icon(
    pid,
    cx,
    cy,
    scale=1.0
):

    color = PRODUCTS[pid][4]
    category = PRODUCTS[pid][5]

    size = max(
        7,
        int(
            13 * scale
        )
    )

    if category == "Hortifruti":

        pygame.draw.circle(
            screen,
            color,
            (
                cx,
                cy
            ),
            size
        )

        pygame.draw.ellipse(
            screen,
            GREEN,
            (
                cx - 4,
                cy - size - 8,
                10,
                8
            )
        )

    elif category in (
        "Bebidas",
        "Higiene",
        "Limpeza"
    ):

        pygame.draw.rect(
            screen,
            color,
            (
                cx - size // 2,
                cy - size,
                size,
                size * 2
            ),
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                cx - 3,
                cy - size // 2,
                6,
                10
            ),
            border_radius=2
        )

    elif category == "Eletrônicos":

        pygame.draw.rect(
            screen,
            color,
            (
                cx - size,
                cy - size,
                size * 2,
                size * 2
            ),
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (
                cx - size // 2,
                cy - size // 2,
                size,
                size
            ),
            border_radius=2
        )

    else:

        pygame.draw.rect(
            screen,
            color,
            (
                cx - size,
                cy - size // 2,
                size * 2,
                size
            ),
            border_radius=4
        )


def draw_shelf(
    rect,
    pid
):

    pygame.draw.rect(
        screen,
        WOOD,
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        OUTLINE,
        rect,
        2,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        (210, 172, 110),
        (
            rect.x + 5,
            rect.y + 8,
            rect.w - 10,
            12
        ),
        border_radius=3
    )

    pygame.draw.rect(
        screen,
        (210, 172, 110),
        (
            rect.x + 5,
            rect.y + 34,
            rect.w - 10,
            12
        ),
        border_radius=3
    )

    quantity = store.inventory.get(
        pid,
        0
    )

    for j in range(
        min(
            5,
            quantity
        )
    ):

        draw_product_icon(
            pid,
            rect.x + 20 + j * 20,
            rect.y + 26,
            0.55
        )

    text(
        screen,
        PRODUCTS[pid][0][:16],
        rect.x + 4,
        rect.bottom + 3,
        BLACK,
        TINY
    )

    if quantity == 0:

        text(
            screen,
            "VAZIA",
            rect.x + 43,
            rect.y + 20,
            RED,
            TINY
        )


# ============================================================
# CLIENTES
# ============================================================

def available_products():

    return [

        pid

        for pid in store.unlocked

        if store.inventory.get(
            pid,
            0
        ) > 0
    ]


def customer_kind():

    value = random.random()

    if value < 0.55:
        return "normal"

    if value < 0.70:
        return "hurry"

    if value < 0.84:
        return "big"

    if value < 0.93:
        return "cheap"

    return "family"


def make_basket(
    kind
):

    options = available_products()

    if not options:

        return []

    limits = {

        "normal":
            (2, 3),

        "hurry":
            (1, 2),

        "big":
            (3, 6),

        "cheap":
            (2, 4),

        "family":
            (4, 6),
    }

    low, high = limits[kind]

    number = random.randint(
        low,
        min(
            high,
            max(
                1,
                len(options)
            )
        )
    )

    return [

        random.choice(options)

        for _ in range(
            number
        )
    ]


def spawn_customer():

    global customer_id
    global last_spawn

    if (
        len(customers)
        >= store.customer_capacity()
    ):

        return

    kind = customer_kind()

    basket = make_basket(
        kind
    )

    if not basket:

        return

    customer_id += 1

    customer = Customer(
        customer_id,
        kind,
        store_rect().x + 55,
        store_rect().bottom - 55
    )

    customer.basket = basket

    customer.target_product = basket[0]

    customer.patience = CUSTOMER_TYPES[
        kind
    ][2]

    customers.append(
        customer
    )

    store.total_customers += 1

    last_spawn = time.monotonic()

    if store.total_customers == 1:

        notify(
            "Seu primeiro cliente entrou!",
            GREEN,
            3
        )


def move_to(
    customer,
    x,
    y,
    dt,
    speed_mult=1.0
):

    dx = (
        x
        - customer.x
    )

    dy = (
        y
        - customer.y
    )

    distance = math.hypot(
        dx,
        dy
    )

    if distance <= 5:

        return True

    speed = (
        CUSTOMER_TYPES[
            customer.kind
        ][1]
        * 65
        * speed_mult
    )

    customer.x += (
        dx / distance
        * speed
        * dt
    )

    customer.y += (
        dy / distance
        * speed
        * dt
    )

    return False


def choose_open_checkout_for_customer():

    cashiers = cashier_rects()

    open_indices = [

        i

        for i in range(
            len(cashiers)
        )

        if store.checkout_open[i]
    ]

    if not open_indices:

        return None

    return random.choice(
        open_indices
    )


def checkout_position(
    index=0
):

    cashiers = cashier_rects()

    open_indices = [

        i

        for i in range(
            len(cashiers)
        )

        if store.checkout_open[i]
    ]

    if open_indices:

        index = open_indices[
            min(
                index,
                len(open_indices) - 1
            )
        ]

        rect = cashiers[index]

        return (
            rect.centerx,
            rect.bottom + 35
        )

    r = store_rect()

    return (
        r.right - 255,
        r.bottom - 75
    )


def customer_take_item(
    customer
):

    pid = customer.target_product

    if (
        not pid
        or
        store.inventory.get(
            pid,
            0
        ) <= 0
    ):

        choices = [

            p

            for p in available_products()

            if p not in customer.held_items
        ]

        if choices:

            customer.target_product = random.choice(
                choices
            )

            customer.state = "shopping"

        else:

            customer.state = "leaving"

        return

    store.inventory[pid] -= 1

    customer.held_items.append(
        pid
    )

    if (
        len(customer.held_items)
        >= len(customer.basket)
    ):

        customer.state = "to_checkout"

    else:

        remaining = [

            p

            for p in customer.basket[
                len(
                    customer.held_items
                ):
            ]

            if store.inventory.get(
                p,
                0
            ) > 0
        ]

        if remaining:

            customer.target_product = remaining[0]

            customer.state = "shopping"

        else:

            customer.state = "to_checkout"


def checkout_has_cashier():

    return (
        store.employee_count(
            "cashier"
        ) > 0
    )


def service_customer(
    customer
):

    if not customer.held_items:

        customer.state = "leaving"

        return

    total = 0

    for pid in list(
        customer.held_items
    ):

        ok, revenue, profit = (
            store.sell_one(pid)
        )

        if ok:

            total += revenue

    customer.held_items = []

    if total > 0:

        store.customers_served += 1

        notify(
            f"Venda de {money(total)} realizada!",
            GREEN,
            1.7
        )

    customer.state = "leaving"


def steal_customer(
    customer
):

    if not customer.held_items:

        customer.state = "leaving"

        return

    items = list(
        customer.held_items
    )

    stolen = len(items)

    guards = store.employee_count(
        "security"
    )

    if (
        guards
        and
        random.random()
        < min(
            0.95,
            0.65
            + guards * 0.12
        )
    ):

        for pid in items:

            store.inventory[pid] = min(
                store.stock_limit(),
                store.inventory.get(
                    pid,
                    0
                ) + 1
            )

        store.security_alerts += 1

        customer.held_items = []

        customer.state = "leaving"

        notify(
            "Segurança conteve uma tentativa de furto!",
            GREEN,
            3
        )

        return

    store.thefts += 1

    store.stolen_items += stolen

    store.reputation = max(
        0,
        store.reputation - 1.2
    )

    store.satisfaction = max(
        0,
        store.satisfaction - 2
    )

    customer.held_items = []

    customer.state = "leaving"

    notify(
        f"Um cliente furtou {stolen} item(ns)!",
        RED,
        3.5
    )


def update_customers(
    dt
):

    remove_ids = []

    for customer in customers:

        if customer.state == "entering":

            customer.state = "shopping"

        elif customer.state == "shopping":

            shelf = shelf_for_product(
                customer.target_product
            )

            if move_to(
                customer,
                shelf.centerx,
                shelf.centery - 24,
                dt
            ):

                customer_take_item(
                    customer
                )

        elif customer.state == "to_checkout":

            open_index = (
                choose_open_checkout_for_customer()
            )

            if open_index is None:

                # Sem caixa aberto.
                # O cliente espera dentro da loja.
                customer.checkout_wait += (
                    dt * 0.25
                )

            else:

                tx, ty = checkout_position(
                    open_index
                )

                if move_to(
                    customer,
                    tx,
                    ty,
                    dt,
                    store.checkout_speed()
                ):

                    customer.state = "checkout"

                    customer.checkout_wait = 0

        elif customer.state == "checkout":

            customer.checkout_wait += dt

            if (
                checkout_has_cashier()
                and
                store.active_checkout_count() > 0
            ):

                customer.service_time -= (
                    dt
                    * store.checkout_speed()
                )

                if customer.service_time <= 0:

                    customer.service_time = 2.2

                    service_customer(
                        customer
                    )

            elif (
                customer.checkout_wait
                >= THEFT_TIMEOUT
            ):

                steal_customer(
                    customer
                )

        elif customer.state == "leaving":

            customer.x += (
                80 * dt
            )

            if (
                customer.x
                > store_rect().right + 80
            ):

                remove_ids.append(
                    customer.cid
                )

    if remove_ids:

        customers[:] = [

            c

            for c in customers

            if c.cid
            not in remove_ids
        ]


def draw_customer(
    customer
):

    color = CUSTOMER_TYPES[
        customer.kind
    ][0]

    pygame.draw.circle(
        screen,
        color,
        (
            int(customer.x),
            int(customer.y)
        ),
        17
    )

    pygame.draw.circle(
        screen,
        OUTLINE,
        (
            int(customer.x),
            int(customer.y)
        ),
        17,
        2
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            int(customer.x - 6),
            int(customer.y - 4)
        ),
        2
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            int(customer.x + 6),
            int(customer.y - 4)
        ),
        2
    )

    if customer.held_items:

        if customer.kind in (
            "big",
            "family"
        ):

            draw_cart(
                int(customer.x + 22),
                int(customer.y + 13)
            )

        else:

            pygame.draw.circle(
                screen,
                GOLD,
                (
                    int(customer.x),
                    int(customer.y + 22)
                ),
                6
            )

    if (
        customer.state == "checkout"
        and
        not checkout_has_cashier()
    ):

        remaining = max(
            0,
            THEFT_TIMEOUT
            - customer.checkout_wait
        )

        bar(
            int(customer.x - 25),
            int(customer.y - 40),
            50,
            7,
            remaining,
            THEFT_TIMEOUT,
            RED
        )

        text(
            screen,
            f"{remaining:0.0f}s",
            customer.x - 17,
            customer.y - 56,
            RED,
            TINY
        )


# ============================================================
# DESENHO
# ============================================================

def draw_cart(
    cx,
    cy
):

    pygame.draw.rect(
        screen,
        (170, 175, 185),
        (
            cx - 14,
            cy - 8,
            28,
            16
        ),
        2,
        border_radius=3
    )

    pygame.draw.line(
        screen,
        (170, 175, 185),
        (
            cx - 14,
            cy - 8
        ),
        (
            cx - 20,
            cy - 18
        ),
        3
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            cx - 9,
            cy + 10
        ),
        4
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            cx + 9,
            cy + 10
        ),
        4
    )


def draw_store_background():

    screen.fill(
        SKY
    )

    r = store_rect()

    pygame.draw.rect(
        screen,
        WALL,
        r,
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        OUTLINE,
        r,
        3,
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        FLOOR,
        (
            r.x,
            r.y + 85,
            r.w,
            r.h - 85
        ),
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        (75, 68, 80),
        (
            r.x,
            r.y,
            r.w,
            78
        ),
        border_radius=18
    )

    pygame.draw.rect(
        screen,
        (55, 50, 60),
        (
            r.x + 15,
            r.y + 13,
            r.w - 30,
            45
        ),
        border_radius=10
    )

    text(
        screen,
        "LOJA DO ZERO",
        r.x + 35,
        r.y + 20,
        YELLOW,
        BIG
    )

    text(
        screen,
        LEVEL_NAMES[store.level],
        r.x + 300,
        r.y + 27,
        WHITE,
        BIG
    )

    for i in range(5):

        wx = (
            r.right
            - 390
            + i * 67
        )

        pygame.draw.rect(
            screen,
            (160, 210, 225),
            (
                wx,
                r.y + 17,
                52,
                35
            ),
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                wx,
                r.y + 17,
                52,
                35
            ),
            2,
            border_radius=5
        )

    for floor_y in range(
        r.y + 100,
        r.bottom,
        45
    ):

        pygame.draw.line(
            screen,
            (214, 199, 165),
            (
                r.x + 2,
                floor_y
            ),
            (
                r.right - 2,
                floor_y
            ),
            1
        )


def draw_shelves():

    for index, shelf in enumerate(
        shelf_rects()
    ):

        draw_shelf(
            shelf,
            shelf_product(index)
        )


def draw_checkout(
    index,
    rect
):

    is_open = (
        store.checkout_open[index]
        if index < len(
            store.checkout_open
        )
        else True
    )

    pygame.draw.rect(
        screen,
        WOOD
        if is_open
        else
        (90, 88, 88),
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        OUTLINE,
        rect,
        2,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        DARK,
        (
            rect.x + 20,
            rect.y + 12,
            rect.w - 40,
            25
        ),
        border_radius=4
    )

    pygame.draw.rect(
        screen,
        GREEN
        if is_open
        else
        RED,
        (
            rect.x + 25,
            rect.y + 42,
            rect.w - 50,
            20
        ),
        border_radius=4
    )

    text(
        screen,
        f"CAIXA {index + 1}",
        rect.x + 25,
        rect.y + 82,
        WHITE,
        SMALL
    )

    text(
        screen,
        "ABERTO"
        if is_open
        else
        "FECHADO",
        rect.x + 30,
        rect.y - 24,
        GREEN
        if is_open
        else
        RED,
        SMALL
    )

    if (
        index == 0
        and
        store.employee_count(
            "cashier"
        ) == 0
    ):

        text(
            screen,
            "MANUAL",
            rect.x + 80,
            rect.y + 82,
            CYAN,
            TINY
        )


def draw_entrance():

    r = store_rect()

    entrance = pygame.Rect(
        r.x + 15,
        r.bottom - 75,
        95,
        54
    )

    pygame.draw.rect(
        screen,
        (145, 185, 205),
        entrance,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        WHITE,
        entrance,
        3,
        border_radius=8
    )

    pygame.draw.line(
        screen,
        WHITE,
        (
            entrance.centerx,
            entrance.y + 4
        ),
        (
            entrance.centerx,
            entrance.bottom - 4
        ),
        2
    )

    text(
        screen,
        "ENTRADA",
        entrance.x + 5,
        entrance.bottom + 2,
        BLACK,
        TINY
    )

    bay = cart_area()

    pygame.draw.rect(
        screen,
        (120, 125, 135),
        bay,
        border_radius=6
    )

    pygame.draw.rect(
        screen,
        OUTLINE,
        bay,
        2,
        border_radius=6
    )

    text(
        screen,
        f"CARRINHOS {store.carts_in_store}",
        bay.x + 6,
        bay.y + 18,
        WHITE,
        TINY
    )


def draw_player():

    pygame.draw.circle(
        screen,
        BLUE,
        (
            int(player_x),
            int(player_y)
        ),
        15
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            int(player_x),
            int(player_y)
        ),
        15,
        2
    )

    pygame.draw.rect(
        screen,
        CYAN,
        (
            int(player_x - 9),
            int(player_y - 27),
            18,
            5
        ),
        border_radius=2
    )

    if carrying_cart:

        draw_cart(
            int(player_x + 28),
            int(player_y + 15)
        )

    text(
        screen,
        "VOCÊ",
        player_x - 18,
        player_y - 43,
        WHITE,
        TINY
    )


def draw_store_hud():

    pygame.draw.rect(
        screen,
        (20, 23, 29),
        (
            0,
            0,
            WIDTH,
            88
        )
    )

    text(
        screen,
        store.money_text(),
        20,
        15,
        YELLOW,
        BIG
    )

    text(
        screen,
        f"Dia {store.day}",
        230,
        12,
        WHITE,
        SMALL
    )

    text(
        screen,
        f"{int(store.hour):02d}:{int((store.hour % 1) * 60):02d}",
        230,
        35,
        CYAN,
        BIG
    )

    text(
        screen,
        LEVEL_NAMES[store.level],
        330,
        24,
        WHITE,
        FONT
    )

    text(
        screen,
        f"Clientes {len(customers)}/{store.customer_capacity()}",
        505,
        15,
        WHITE,
        SMALL
    )

    text(
        screen,
        f"Vendas {store.total_sales}",
        505,
        40,
        WHITE,
        SMALL
    )

    text(
        screen,
        f"Furtos {store.thefts}",
        635,
        15,
        RED
        if store.thefts
        else WHITE,
        SMALL
    )

    text(
        screen,
        f"Reputação {store.reputation:.0f}",
        635,
        40,
        PURPLE,
        SMALL
    )

    text(
        screen,
        "Satisfação",
        785,
        10,
        WHITE,
        TINY
    )

    bar(
        785,
        28,
        110,
        12,
        store.satisfaction,
        100,
        GREEN
    )

    text(
        screen,
        f"{store.satisfaction:.0f}%",
        905,
        25,
        WHITE,
        TINY
    )

    text(
        screen,
        "Limpeza",
        785,
        47,
        WHITE,
        TINY
    )

    bar(
        785,
        65,
        110,
        12,
        store.cleanliness,
        100,
        CYAN
    )

    text(
        screen,
        f"{store.cleanliness:.0f}%",
        905,
        62,
        WHITE,
        TINY
    )

    text(
        screen,
        "F5 SALVAR",
        1020,
        15,
        GREEN,
        SMALL
    )

    text(
        screen,
        "F9 CARREGAR",
        1115,
        40,
        CYAN,
        SMALL
    )

    text(
        screen,
        "F11 TELA CHEIA",
        1010,
        62,
        YELLOW,
        TINY
    )


def draw_bottom_menu():

    options = [

        ("1 Loja", 10, 100),

        ("2 Estoque", 115, 105),

        ("3 Upgrades", 225, 120),

        ("4 Equipe", 350, 105),

        ("5 Missões", 460, 110),

        ("6 Conquistas", 575, 125),

        ("7 Decoração", 705, 125),

        ("8 Estatísticas", 835, 125),

        ("ESC Pausa", 965, 110),
    ]

    for label, x, width in options:

        button(
            (
                x,
                HEIGHT - 42,
                width,
                32
            ),
            label,
            (
                50,
                65,
                85
            ),
            False,
            TINY
        )


def draw_store():

    draw_store_background()

    draw_shelves()

    for index, rect in enumerate(
        cashier_rects()
    ):

        draw_checkout(
            index,
            rect
        )

    draw_entrance()

    for customer in customers:

        draw_customer(
            customer
        )

    draw_player()

    draw_store_hud()

    draw_bottom_menu()

    text(
        screen,
        "E = atender   F = abrir/fechar caixa   C = carrinho",
        45,
        675,
        WHITE,
        TINY
    )

    if store.employee_count(
        "cashier"
    ) == 0:

        panel(
            (
                45,
                95,
                370,
                72
            ),
            (
                45,
                35,
                30
            ),
            ORANGE,
            2
        )

        text(
            screen,
            "SEM CAIXA CONTRATADO",
            60,
            107,
            ORANGE,
            FONT
        )

        text(
            screen,
            "E atende • F abre/fecha o caixa",
            60,
            134,
            WHITE,
            SMALL
        )

        text(
            screen,
            "Feche um caixa para controlar o atendimento",
            60,
            153,
            WHITE,
            TINY
        )

    else:

        text(
            screen,
            f"CAIXAS ATIVOS: {store.employee_count('cashier')}",
            45,
            177,
            GREEN,
            SMALL
        )

    waiting = sum(
        c.state == "checkout"
        for c in customers
    )

    if waiting:

        text(
            screen,
            f"Fila: {waiting} cliente(s)",
            45,
            200,
            ORANGE,
            FONT
        )


# ============================================================
# INTERAÇÃO COM CAIXA
# ============================================================

def nearest_cashier():

    cashiers = cashier_rects()

    if not cashiers:

        return None

    return min(
        cashiers,
        key=lambda rect:
        math.hypot(
            player_x - rect.centerx,
            player_y - rect.bottom
        )
    )


def cashier_index_from_rect(
    target
):

    cashiers = cashier_rects()

    for i, rect in enumerate(
        cashiers
    ):

        if rect == target:

            return i

    return None


def toggle_cashier():

    rect = nearest_cashier()

    if rect is None:

        notify(
            "Nenhum caixa disponível.",
            RED,
            2
        )

        return

    distance = math.hypot(
        player_x - rect.centerx,
        player_y - rect.bottom
    )

    if distance > 125:

        notify(
            "Chegue mais perto do caixa.",
            GRAY,
            1.5
        )

        return

    index = cashier_index_from_rect(
        rect
    )

    if index is None:

        return

    store.ensure_checkout_slots()

    store.checkout_open[index] = not (
        store.checkout_open[index]
    )

    status = (
        "ABERTO"
        if store.checkout_open[index]
        else
        "FECHADO"
    )

    notify(
        f"Caixa {index + 1}: {status}.",
        GREEN
        if status == "ABERTO"
        else RED,
        2
    )


def manual_service():

    rect = nearest_cashier()

    if rect is None:

        notify(
            "Nenhum caixa disponível.",
            RED,
            2
        )

        return

    distance = math.hypot(
        player_x - rect.centerx,
        player_y - rect.bottom
    )

    if distance > 125:

        notify(
            "Chegue mais perto do caixa.",
            GRAY,
            1.5
        )

        return

    index = cashier_index_from_rect(
        rect
    )

    if index is None:

        return

    if not store.checkout_open[index]:

        notify(
            "Este caixa está fechado. Use F para abrir.",
            RED,
            2
        )

        return

    candidates = [

        c

        for c in customers

        if c.state == "checkout"
    ]

    if not candidates:

        notify(
            "Não há clientes esperando.",
            GRAY,
            1.5
        )

        return

    customer = max(
        candidates,
        key=lambda c:
        c.checkout_wait
    )

    service_customer(
        customer
    )


def interact():

    global carrying_cart

    area = cart_area()

    distance = math.hypot(
        player_x - area.centerx,
        player_y - area.centery
    )

    if distance < 100:

        if (
            store.carts_in_store > 0
            or
            carrying_cart
        ):

            if not carrying_cart:

                store.carts_in_store -= 1

            else:

                store.carts_in_store += 1

            carrying_cart = not carrying_cart

            notify(
                "Carrinho pego."
                if carrying_cart
                else
                "Carrinho devolvido.",
                CYAN,
                1.5
            )

            return

    manual_service()


# ============================================================
# SAVE
# ============================================================

def save_game():

    try:

        data = store.to_dict()

        data.update({

            "player_x":
                player_x,

            "player_y":
                player_y,

            "carrying_cart":
                carrying_cart,
        })

        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )

        store.last_autosave = 0

        notify(
            "Jogo salvo!",
            GREEN,
            2
        )

        return True

    except Exception as error:

        print(
            "Erro ao salvar:",
            error
        )

        notify(
            "Erro ao salvar o jogo.",
            RED,
            3
        )

        return False


# ============================================================
# LOAD
# ============================================================

def load_game():

    global store
    global player_x
    global player_y
    global carrying_cart
    global selected_product
    global customer_id
    global last_spawn

    if not os.path.exists(
        SAVE_FILE
    ):

        notify(
            "Nenhum jogo salvo.",
            RED,
            3
        )

        return False

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        store.load(
            data
        )

        player_x = float(
            data.get(
                "player_x",
                170
            )
        )

        player_y = float(
            data.get(
                "player_y",
                485
            )
        )

        carrying_cart = bool(
            data.get(
                "carrying_cart",
                False
            )
        )

        if not can_walk(
            player_x,
            player_y
        ):

            reset_player_position()

        selected_product = (
            store.unlocked[0]
            if store.unlocked
            else
            "apple"
        )

        customers.clear()

        customer_id = 0

        last_spawn = time.monotonic()

        notify(
            "Jogo carregado!",
            GREEN,
            3
        )

        return True

    except Exception as error:

        print(
            "Erro ao carregar:",
            error
        )

        notify(
            "Save inválido.",
            RED,
            3
        )

        return False


# ============================================================
# TELA CHEIA
# ============================================================

def toggle_fullscreen():

    global FULLSCREEN
    global screen

    FULLSCREEN = not FULLSCREEN

    flags = (
        pygame.FULLSCREEN
        | pygame.SCALED
        if FULLSCREEN
        else
        pygame.SCALED
    )

    screen = pygame.display.set_mode(
        (
            WIDTH,
            HEIGHT
        ),
        flags
    )

    notify(
        "Tela cheia ativada."
        if FULLSCREEN
        else
        "Modo janela ativado.",
        CYAN,
        2
    )


# ============================================================
# MENU
# ============================================================

def draw_menu():

    screen.fill(
        (
            22,
            27,
            38
        )
    )

    center_text(
        screen,
        "LOJA DO ZERO",
        80,
        YELLOW,
        HUGE
    )

    center_text(
        screen,
        "Simulador de supermercado",
        150,
        WHITE,
        BIG
    )

    panel(
        (
            300,
            220,
            680,
            300
        ),
        (
            35,
            41,
            53
        ),
        OUTLINE,
        3,
        20
    )

    button(
        (
            445,
            270,
            390,
            55
        ),
        "1 - NOVO JOGO",
        (
            55,
            100,
            75
        ),
        False,
        FONT
    )

    button(
        (
            445,
            345,
            390,
            55
        ),
        "2 - CARREGAR JOGO",
        (
            60,
            85,
            120
        ),
        False,
        FONT
    )

    button(
        (
            445,
            420,
            390,
            55
        ),
        "3 - SAIR",
        (
            100,
            65,
            75
        ),
        False,
        FONT
    )

    center_text(
        screen,
        "F5 salva • F9 carrega • F11 tela cheia",
        585,
        LIGHT,
        SMALL
    )


def draw_tutorial():

    screen.fill(
        (
            227,
            235,
            240
        )
    )

    panel(
        (
            120,
            55,
            1040,
            600
        ),
        (
            35,
            41,
            51
        ),
        OUTLINE,
        3,
        20
    )

    center_text(
        screen,
        "PRIMEIROS PASSOS",
        80,
        YELLOW,
        TITLE
    )

    steps = [

        (
            "1",
            "Ande pela loja",
            "Use WASD ou as setas."
        ),

        (
            "2",
            "Abasteça",
            "Abra Estoque e compre produtos."
        ),

        (
            "3",
            "Atenda",
            "E atende o cliente perto do caixa."
        ),

        (
            "4",
            "Abra e feche caixas",
            "F alterna entre ABERTO e FECHADO."
        ),

        (
            "5",
            "Contrate equipe",
            "Caixas e outros funcionários automatizam a loja."
        ),
    ]

    for index, (
        number,
        title,
        description
    ) in enumerate(
        steps
    ):

        y = 155 + index * 82

        pygame.draw.circle(
            screen,
            BLUE,
            (
                190,
                y + 10
            ),
            23
        )

        text(
            screen,
            number,
            184,
            y - 1,
            WHITE,
            SMALL
        )

        text(
            screen,
            title,
            235,
            y - 5,
            YELLOW,
            FONT
        )

        text(
            screen,
            description,
            235,
            y + 25,
            WHITE,
            SMALL
        )

    button(
        (
            440,
            590,
            400,
            45
        ),
        "ENTER - COMEÇAR",
        (
            55,
            105,
            80
        ),
        False,
        FONT
    )


# ============================================================
# ESTOQUE
# ============================================================

def draw_inventory():

    screen.fill(
        (
            226,
            233,
            239
        )
    )

    center_text(
        screen,
        "ESTOQUE",
        20,
        YELLOW,
        TITLE
    )

    text(
        screen,
        f"Dinheiro: {store.money_text()}",
        35,
        82,
        YELLOW,
        BIG
    )

    text(
        screen,
        f"Limite: {store.stock_limit()}",
        980,
        87,
        WHITE,
        SMALL
    )

    items = store.unlocked

    if not hasattr(
        draw_inventory,
        "page"
    ):

        draw_inventory.page = 0

    per_page = 10

    max_page = max(
        0,
        (
            len(items) - 1
        )
        // per_page
    )

    draw_inventory.page = max(
        0,
        min(
            draw_inventory.page,
            max_page
        )
    )

    visible = items[
        draw_inventory.page * per_page:
        (
            draw_inventory.page + 1
        ) * per_page
    ]

    for index, pid in enumerate(
        visible
    ):

        col = index % 2
        row = index // 2

        x = 35 + col * 610
        y = 125 + row * 100

        name, buy, sell, level, color, category = (
            PRODUCTS[pid]
        )

        panel(
            (
                x,
                y,
                585,
                85
            ),
            (
                41,
                48,
                59
            ),
            OUTLINE,
            2
        )

        draw_product_icon(
            pid,
            x + 40,
            y + 40,
            0.9
        )

        text(
            screen,
            name,
            x + 75,
            y + 11,
            WHITE,
            FONT
        )

        text(
            screen,
            category,
            x + 75,
            y + 38,
            LIGHT,
            TINY
        )

        text(
            screen,
            f"Estoque: {store.inventory[pid]}",
            x + 260,
            y + 12,
            WHITE,
            SMALL
        )

        text(
            screen,
            f"Compra: {money(store.buy_price(pid))}",
            x + 260,
            y + 39,
            WHITE,
            TINY
        )

        text(
            screen,
            f"Venda: {money(store.sell_price(pid))}",
            x + 390,
            y + 12,
            GREEN,
            TINY
        )

        if pid == selected_product:

            pygame.draw.rect(
                screen,
                CYAN,
                (
                    x + 3,
                    y + 3,
                    579,
                    79
                ),
                2,
                border_radius=8
            )

    text(
        screen,
        "A/D seleciona • Q compra 5 • W compra 10 • Z/X páginas • ESC volta",
        35,
        665,
        LIGHT,
        SMALL
    )


# ============================================================
# UPGRADES
# ============================================================

def draw_upgrades():

    screen.fill(
        (
            226,
            235,
            229
        )
    )

    center_text(
        screen,
        "MELHORIAS",
        20,
        YELLOW,
        TITLE
    )

    y = 100

    for key in UPGRADE_ORDER:

        name, base, max_level, description = (
            UPGRADES[key]
        )

        level = store.upgrades[key]

        cost = store.upgrade_cost(
            key
        )

        panel(
            (
                35,
                y,
                1210,
                62
            ),
            (
                38,
                48,
                45
            ),
            OUTLINE,
            2
        )

        text(
            screen,
            name,
            55,
            y + 10,
            WHITE,
            FONT
        )

        text(
            screen,
            f"Lv. {level}/{max_level}",
            55,
            y + 36,
            CYAN,
            TINY
        )

        text(
            screen,
            description,
            275,
            y + 19,
            LIGHT,
            SMALL
        )

        label = (
            "MÁXIMO"
            if level >= max_level
            else
            f"Comprar {money(cost)}"
        )

        button(
            (
                1010,
                y + 12,
                205,
                38
            ),
            label,
            (
                65,
                100,
                80
            ),
            level >= max_level,
            SMALL
        )

        y += 70

    text(
        screen,
        "1-8 comprar upgrade • ESC voltar",
        35,
        680,
        LIGHT,
        SMALL
    )


# ============================================================
# EQUIPE
# ============================================================

def draw_employees():

    screen.fill(
        (
            233,
            226,
            240
        )
    )

    center_text(
        screen,
        "EQUIPE",
        20,
        YELLOW,
        TITLE
    )

    y = 105

    for key in EMPLOYEE_ORDER:

        (
            name,
            price,
            salary,
            color,
            description
        ) = EMPLOYEES[key]

        count = store.employee_count(
            key
        )

        max_count = (
            5
            if key in (
                "cashier",
                "stock"
            )
            else 2
        )

        panel(
            (
                35,
                y,
                1210,
                82
            ),
            (
                48,
                43,
                58
            ),
            OUTLINE,
            2
        )

        pygame.draw.circle(
            screen,
            color,
            (
                75,
                y + 41
            ),
            24
        )

        text(
            screen,
            name,
            115,
            y + 11,
            WHITE,
            FONT
        )

        text(
            screen,
            description,
            115,
            y + 40,
            LIGHT,
            SMALL
        )

        text(
            screen,
            f"{count}/{max_count}",
            670,
            y + 12,
            CYAN,
            BIG
        )

        text(
            screen,
            f"Salário: {money(salary)}",
            670,
            y + 45,
            LIGHT,
            SMALL
        )

        label = (
            "MÁXIMO"
            if count >= max_count
            else
            f"Contratar {money(price)}"
        )

        button(
            (
                1000,
                y + 20,
                210,
                42
            ),
            label,
            (
                65,
                100,
                80
            ),
            count >= max_count,
            SMALL
        )

        y += 93

    text(
        screen,
        "1-5 contratar • ESC voltar",
        35,
        675,
        LIGHT,
        SMALL
    )


# ============================================================
# ESTATÍSTICAS
# ============================================================

def draw_stats():

    screen.fill(
        (
            224,
            231,
            239
        )
    )

    center_text(
        screen,
        "ESTATÍSTICAS",
        18,
        YELLOW,
        TITLE
    )

    data = [

        (
            "Dinheiro",
            store.money_text(),
            YELLOW
        ),

        (
            "Receita",
            money(
                store.total_revenue
            ),
            GREEN
        ),

        (
            "Lucro",
            money(
                store.total_profit
            ),
            MINT
        ),

        (
            "Vendas",
            store.total_sales,
            CYAN
        ),

        (
            "Clientes",
            store.total_customers,
            BLUE
        ),

        (
            "Atendidos",
            store.customers_served,
            GREEN
        ),

        (
            "Furtos",
            store.thefts,
            RED
        ),

        (
            "Itens furtados",
            store.stolen_items,
            RED
        ),

        (
            "Reputação",
            f"{store.reputation:.1f}",
            PURPLE
        ),

        (
            "Satisfação",
            f"{store.satisfaction:.1f}%",
            GREEN
        ),

        (
            "Limpeza",
            f"{store.cleanliness:.1f}%",
            CYAN
        ),

        (
            "Caixas",
            store.employee_count(
                "cashier"
            ),
            BLUE
        ),
    ]

    for index, (
        name,
        value,
        color
    ) in enumerate(data):

        col = index % 3
        row = index // 3

        x = (
            35
            + col * 410
        )

        y = (
            95
            + row * 88
        )

        panel(
            (
                x,
                y,
                385,
                72
            ),
            (
                38,
                43,
                53
            ),
            OUTLINE,
            2
        )

        text(
            screen,
            name,
            x + 15,
            y + 8,
            LIGHT,
            SMALL
        )

        text(
            screen,
            value,
            x + 15,
            y + 31,
            color,
            BIG
        )

    text(
        screen,
        "ESC voltar",
        35,
        650,
        LIGHT,
        SMALL
    )


# ============================================================
# MISSÕES
# ============================================================

def draw_missions():

    screen.fill(
        (
            239,
            235,
            216
        )
    )

    center_text(
        screen,
        "MISSÕES",
        20,
        YELLOW,
        TITLE
    )

    missions = [

        (
            "Primeira venda",
            store.total_sales >= 1,
            50
        ),

        (
            "50 clientes",
            store.total_customers >= 50,
            150
        ),

        (
            "Nível 3",
            store.level >= 3,
            400
        ),

        (
            "Primeiro funcionário",
            len(store.employees) >= 1,
            180
        ),

        (
            "10 produtos",
            len(store.unlocked) >= 10,
            500
        ),

        (
            "Nível 5",
            store.level >= 5,
            1500
        ),
    ]

    y = 110

    for name, done, reward in missions:

        panel(
            (
                50,
                y,
                1180,
                64
            ),
            (
                56,
                52,
                44
            ),
            OUTLINE,
            2
        )

        text(
            screen,
            "OK"
            if done
            else
            "--",
            70,
            y + 17,
            GREEN
            if done
            else
            YELLOW,
            BIG
        )

        text(
            screen,
            name,
            120,
            y + 17,
            WHITE,
            FONT
        )

        text(
            screen,
            f"Recompensa: {money(reward)}",
            880,
            y + 20,
            GOLD,
            SMALL
        )

        y += 76

    text(
        screen,
        "ESC voltar",
        50,
        620,
        LIGHT,
        SMALL
    )


# ============================================================
# CONQUISTAS
# ============================================================

def draw_achievements():

    screen.fill(
        (
            232,
            225,
            242
        )
    )

    center_text(
        screen,
        "CONQUISTAS",
        20,
        YELLOW,
        TITLE
    )

    names = {

        "first_customer":
            "Primeiro cliente",

        "100_sales":
            "100 vendas",

        "1000_revenue":
            "R$ 1.000 faturados",

        "50_customers":
            "50 clientes",

        "first_employee":
            "Primeiro funcionário",

        "all_products":
            "Todos os produtos",

        "mega_store":
            "Mega Loja",

        "premium":
            "Loja Premium",

        "security":
            "Segurança contratada",

        "big_profit":
            "R$ 5.000 de lucro",
    }

    y = 105

    for key, name in names.items():

        done = store.achievements[key]

        panel(
            (
                50,
                y,
                1180,
                52
            ),
            (
                61,
                55,
                70
            )
            if done
            else
            (
                42,
                42,
                48
            ),
            GOLD
            if done
            else OUTLINE,
            2
        )

        text(
            screen,
            "[OK]"
            if done
            else
            "[ ]",
            70,
            y + 14,
            GOLD
            if done
            else
            GRAY,
            SMALL
        )

        text(
            screen,
            name,
            120,
            y + 14,
            GOLD
            if done
            else
            WHITE,
            FONT
        )

        y += 58

    text(
        screen,
        "ESC voltar",
        50,
        690,
        LIGHT,
        SMALL
    )


# ============================================================
# DECORAÇÃO
# ============================================================

def buy_decoration(
    index
):

    if (
        index < 0
        or
        index >= len(
            DECORATION_ITEMS
        )
    ):

        return

    name, color, price = (
        DECORATION_ITEMS[index]
    )

    if store.money < price:

        notify(
            "Dinheiro insuficiente.",
            RED,
            2
        )

        return

    store.money -= price

    store.total_profit -= price

    store.today_expenses += price

    store.decorations.append(
        name
    )

    store.reputation = min(
        100,
        store.reputation + 2
    )

    store.upgrades["decor"] = min(
        UPGRADES["decor"][2],
        store.upgrades["decor"] + 1
    )

    notify(
        f"{name} adicionada à loja!",
        GREEN,
        2
    )


def draw_decor():

    screen.fill(
        (
            225,
            237,
            234
        )
    )

    center_text(
        screen,
        "DECORAÇÃO",
        20,
        YELLOW,
        TITLE
    )

    for index, (
        name,
        color,
        price
    ) in enumerate(
        DECORATION_ITEMS
    ):

        y = (
            120
            + index * 88
        )

        panel(
            (
                50,
                y,
                1180,
                68
            ),
            (
                39,
                49,
                51
            ),
            OUTLINE,
            2
        )

        pygame.draw.rect(
            screen,
            color,
            (
                70,
                y + 15,
                50,
                36
            ),
            border_radius=6
        )

        text(
            screen,
            name,
            145,
            y + 22,
            WHITE,
            FONT
        )

        text(
            screen,
            f"Possui: {store.decorations.count(name)}",
            400,
            y + 23,
            LIGHT,
            SMALL
        )

        button(
            (
                1010,
                y + 15,
                190,
                38
            ),
            f"Adicionar {money(price)}",
            (
                65,
                100,
                85
            ),
            store.money < price,
            SMALL
        )

    text(
        screen,
        "1-5 adicionar decoração • ESC voltar",
        50,
        650,
        LIGHT,
        SMALL
    )


# ============================================================
# PAUSA
# ============================================================

def draw_pause():

    screen.fill(
        (
            18,
            20,
            27
        )
    )

    center_text(
        screen,
        "PAUSADO",
        105,
        YELLOW,
        HUGE
    )

    button(
        (
            430,
            240,
            420,
            55
        ),
        "ENTER - CONTINUAR",
        (
            55,
            85,
            110
        ),
        False,
        FONT
    )

    button(
        (
            430,
            315,
            420,
            55
        ),
        "F5 - SALVAR",
        (
            60,
            100,
            75
        ),
        False,
        FONT
    )

    button(
        (
            430,
            390,
            420,
            55
        ),
        "ESC - MENU",
        (
            100,
            65,
            75
        ),
        False,
        FONT
    )

    center_text(
        screen,
        "O tempo da loja para enquanto você está pausado.",
        500,
        LIGHT,
        SMALL
    )


# ============================================================
# SUCESSO
# ============================================================

def draw_success():

    screen.fill(
        (
            10,
            42,
            28
        )
    )

    center_text(
        screen,
        "LOJA PREMIUM!",
        95,
        GOLD,
        HUGE
    )

    center_text(
        screen,
        "Você transformou o mercadinho em um grande negócio.",
        195,
        WHITE,
        BIG
    )

    center_text(
        screen,
        f"Receita: {money(store.total_revenue)}",
        285,
        GREEN,
        BIG
    )

    center_text(
        screen,
        f"Lucro: {money(store.total_profit)}",
        335,
        MINT,
        BIG
    )

    center_text(
        screen,
        "ESC - voltar ao menu",
        535,
        WHITE,
        FONT
    )


# ============================================================
# EVENTOS
# ============================================================

def start_random_event():

    key = random.choice(
        list(EVENTS)
    )

    store.active_event = key

    store.event_time = EVENTS[key][3]

    notify(
        (
            f"EVENTO: "
            f"{EVENTS[key][0]} - "
            f"{EVENTS[key][1]}"
        ),
        EVENTS[key][2],
        4
    )


# ============================================================
# ESTOQUE
# ============================================================

def buy_selected_stock(
    amount
):

    if not store.unlocked:

        return

    ok, msg = store.buy_stock(
        selected_product,
        amount
    )

    notify(
        msg,
        GREEN
        if ok
        else RED,
        2
    )


# ============================================================
# NOVO JOGO
# ============================================================

def start_new_game():

    global store
    global customer_id
    global player_x
    global player_y
    global carrying_cart
    global selected_product
    global last_spawn
    global message_queue
    global message_timer

    store = Store()

    customers.clear()

    customer_id = 0

    player_x = 170.0
    player_y = 485.0

    carrying_cart = False

    selected_product = (
        store.unlocked[0]
    )

    last_spawn = time.monotonic()

    message_queue.clear()

    message_timer = 0

    reset_player_position()


# ============================================================
# VOLTAR AO MENU
# ============================================================

def return_to_menu():

    global state

    customers.clear()

    state = "menu"


# ============================================================
# TECLADO
# ============================================================

def handle_key(
    event
):

    global state
    global running
    global selected_product
    global carrying_cart

    key = event.key

    # --------------------------------------------------------
    # F5
    # --------------------------------------------------------

    if key == pygame.K_F5:

        save_game()

        return

    # --------------------------------------------------------
    # F9
    # --------------------------------------------------------

    if key == pygame.K_F9:

        if load_game():

            state = "store"

        return

    # --------------------------------------------------------
    # F11
    # --------------------------------------------------------

    if key == pygame.K_F11:

        toggle_fullscreen()

        return

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    if state == "menu":

        if key == pygame.K_1:

            start_new_game()

            state = "tutorial"

        elif key == pygame.K_2:

            if load_game():

                state = "store"

        elif key in (
            pygame.K_3,
            pygame.K_ESCAPE
        ):

            running = False

    # --------------------------------------------------------
    # TUTORIAL
    # --------------------------------------------------------

    elif state == "tutorial":

        if key == pygame.K_RETURN:

            store.tutorial_done = True

            state = "store"

            reset_player_position()

        elif key in (
            pygame.K_w,
            pygame.K_a,
            pygame.K_s,
            pygame.K_d,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT
        ):

            store.tutorial_done = True

            state = "store"

    # --------------------------------------------------------
    # LOJA
    # --------------------------------------------------------

    elif state == "store":

        if key == pygame.K_1:

            state = "store"

        elif key == pygame.K_2:

            state = "inventory"

        elif key == pygame.K_3:

            state = "upgrades"

        elif key == pygame.K_4:

            state = "employees"

        elif key == pygame.K_5:

            state = "missions"

        elif key == pygame.K_6:

            state = "achievements"

        elif key == pygame.K_7:

            state = "decor"

        elif key == pygame.K_8:

            state = "stats"

        elif key == pygame.K_ESCAPE:

            state = "pause"

        elif key == pygame.K_e:

            interact()

        elif key == pygame.K_f:

            toggle_cashier()

        elif key == pygame.K_c:

            if (
                not carrying_cart
                and
                store.carts_in_store > 0
            ):

                store.carts_in_store -= 1

                carrying_cart = True

                notify(
                    "Você pegou um carrinho.",
                    CYAN,
                    1.5
                )

            elif carrying_cart:

                store.carts_in_store += 1

                carrying_cart = False

                notify(
                    "Carrinho devolvido.",
                    CYAN,
                    1.5
                )

        elif (
            key == pygame.K_g
            and
            store.level == 5
            and
            store.total_profit >= 8000
        ):

            state = "success"

    # --------------------------------------------------------
    # ESTOQUE
    # --------------------------------------------------------

    elif state == "inventory":

        if key == pygame.K_ESCAPE:

            state = "store"

        elif key == pygame.K_a:

            if store.unlocked:

                index = store.unlocked.index(
                    selected_product
                )

                selected_product = store.unlocked[
                    (
                        index - 1
                    )
                    % len(
                        store.unlocked
                    )
                ]

        elif key == pygame.K_d:

            if store.unlocked:

                index = store.unlocked.index(
                    selected_product
                )

                selected_product = store.unlocked[
                    (
                        index + 1
                    )
                    % len(
                        store.unlocked
                    )
                ]

        elif key == pygame.K_q:

            buy_selected_stock(
                5
            )

        elif key == pygame.K_w:

            buy_selected_stock(
                10
            )

        elif key == pygame.K_z:

            draw_inventory.page = max(
                0,
                getattr(
                    draw_inventory,
                    "page",
                    0
                )
                - 1
            )

        elif key == pygame.K_x:

            draw_inventory.page = (
                getattr(
                    draw_inventory,
                    "page",
                    0
                )
                + 1
            )

    # --------------------------------------------------------
    # UPGRADES
    # --------------------------------------------------------

    elif state == "upgrades":

        if key == pygame.K_ESCAPE:

            state = "store"

        elif pygame.K_1 <= key <= pygame.K_8:

            index = key - pygame.K_1

            if index < len(
                UPGRADE_ORDER
            ):

                ok, msg = (
                    store.buy_upgrade(
                        UPGRADE_ORDER[index]
                    )
                )

                notify(
                    msg,
                    GREEN
                    if ok
                    else RED,
                    2
                )

    # --------------------------------------------------------
    # EQUIPE
    # --------------------------------------------------------

    elif state == "employees":

        if key == pygame.K_ESCAPE:

            state = "store"

        elif pygame.K_1 <= key <= pygame.K_5:

            index = key - pygame.K_1

            ok, msg = store.hire(
                EMPLOYEE_ORDER[index]
            )

            notify(
                msg,
                GREEN
                if ok
                else RED,
                2.5
            )

    # --------------------------------------------------------
    # MISSÕES
    # --------------------------------------------------------

    elif state == "missions":

        if key == pygame.K_ESCAPE:

            state = "store"

    # --------------------------------------------------------
    # CONQUISTAS
    # --------------------------------------------------------

    elif state == "achievements":

        if key == pygame.K_ESCAPE:

            state = "store"

    # --------------------------------------------------------
    # DECORAÇÃO
    # --------------------------------------------------------

    elif state == "decor":

        if key == pygame.K_ESCAPE:

            state = "store"

        elif pygame.K_1 <= key <= pygame.K_5:

            buy_decoration(
                key - pygame.K_1
            )

    # --------------------------------------------------------
    # ESTATÍSTICAS
    # --------------------------------------------------------

    elif state == "stats":

        if key == pygame.K_ESCAPE:

            state = "store"

    # --------------------------------------------------------
    # PAUSA
    # --------------------------------------------------------

    elif state == "pause":

        if key == pygame.K_RETURN:

            state = "store"

        elif key == pygame.K_ESCAPE:

            return_to_menu()

    # --------------------------------------------------------
    # SUCESSO
    # --------------------------------------------------------

    elif state == "success":

        if key == pygame.K_ESCAPE:

            return_to_menu()


# ============================================================
# MOUSE
# ============================================================

def handle_mouse(
    pos
):

    global state

    if state != "store":

        return

    x, y = pos

    if y > HEIGHT - 55:

        choices = [

            (
                10,
                110,
                "store"
            ),

            (
                115,
                220,
                "inventory"
            ),

            (
                225,
                345,
                "upgrades"
            ),

            (
                350,
                455,
                "employees"
            ),

            (
                460,
                570,
                "missions"
            ),

            (
                575,
                700,
                "achievements"
            ),

            (
                705,
                830,
                "decor"
            ),

            (
                835,
                960,
                "stats"
            ),
        ]

        for left, right, target in choices:

            if (
                left
                <= x
                <= right
            ):

                state = target

                return


# ============================================================
# ATUALIZAÇÃO DO JOGO
# ============================================================

def update_game(
    dt
):

    global last_spawn

    if state != "store":

        return

    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if (
        keys[pygame.K_a]
        or
        keys[pygame.K_LEFT]
    ):

        dx -= 1

    if (
        keys[pygame.K_d]
        or
        keys[pygame.K_RIGHT]
    ):

        dx += 1

    if (
        keys[pygame.K_w]
        or
        keys[pygame.K_UP]
    ):

        dy -= 1

    if (
        keys[pygame.K_s]
        or
        keys[pygame.K_DOWN]
    ):

        dy += 1

    move_player(
        dx,
        dy,
        dt
    )

    store.update_quality(
        dt
    )

    store.update_time(
        dt
    )

    store.ensure_checkout_slots()

    update_customers(
        dt
    )

    # --------------------------------------------------------
    # REPOSITOR
    # --------------------------------------------------------

    for _ in range(
        store.employee_count(
            "stock"
        )
    ):

        for pid in store.unlocked:

            if (
                store.inventory[pid]
                < 3
                and
                store.money
                >= store.buy_price(pid)
            ):

                cost = store.buy_price(
                    pid
                )

                store.money -= cost

                store.inventory[pid] += 1

                store.total_profit -= cost

                store.today_expenses += cost

                break

    # --------------------------------------------------------
    # FAXINEIRO
    # --------------------------------------------------------

    cleaners = store.employee_count(
        "cleaner"
    )

    if cleaners:

        store.cleanliness = min(
            100,
            store.cleanliness
            + dt
            * cleaners
            * 0.08
        )

    # --------------------------------------------------------
    # SEGURANÇA
    # --------------------------------------------------------

    if (
        store.employee_count(
            "security"
        )
        and
        random.random()
        < dt * 0.02
    ):

        store.security_alerts += 1

    # --------------------------------------------------------
    # CLIENTES
    # --------------------------------------------------------

    interval = (
        CUSTOMER_SPAWN
        /
        max(
            0.45,
            store.spawn_speed()
        )
    )

    if (
        time.monotonic()
        - last_spawn
        >= interval
    ):

        spawn_customer()

    # --------------------------------------------------------
    # AUTO SAVE
    # --------------------------------------------------------

    if store.last_autosave >= 30:

        save_game()


# ============================================================
# DESENHO
# ============================================================

def draw_current():

    if state == "menu":

        draw_menu()

    elif state == "tutorial":

        draw_tutorial()

    elif state == "store":

        draw_store()

    elif state == "inventory":

        draw_inventory()

    elif state == "upgrades":

        draw_upgrades()

    elif state == "employees":

        draw_employees()

    elif state == "missions":

        draw_missions()

    elif state == "achievements":

        draw_achievements()

    elif state == "decor":

        draw_decor()

    elif state == "stats":

        draw_stats()

    elif state == "pause":

        draw_pause()

    elif state == "success":

        draw_success()

    draw_notifications()


# ============================================================
# LOOP PRINCIPAL
# ============================================================

last_time = time.monotonic()

while running:

    now = time.monotonic()

    dt = min(
        0.05,
        now - last_time
    )

    last_time = now

    clock.tick(
        FPS
    )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.KEYDOWN:

            handle_key(
                event
            )

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and
            event.button == 1
        ):

            handle_mouse(
                event.pos
            )

    update_game(
        dt
    )

    update_notifications(
        dt
    )

    draw_current()

    pygame.display.flip()


pygame.quit()
